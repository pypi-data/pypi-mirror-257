from enum import Enum
import json
import re
from typing import List, TypedDict, Optional, cast
from promptflow import tool
from promptflow.contracts.types import PromptTemplate

from promptflow.connections import OpenAIConnection
from promptflow import tool
from promptflow.connections import OpenAIConnection
from promptflow.tools.common import render_jinja_template, to_content_str_or_list, \
    to_bool, validate_functions, process_function_call, try_parse_name_and_content, validate_role, \
    post_process_chat_api_response, normalize_connection_config, handle_openai_error
from promptflow.contracts.types import PromptTemplate
from promptflow.tools.exception import ChatAPIInvalidFunctions, ChatAPIFunctionRoleInvalidFormat
from ast import literal_eval

try:
    from openai import OpenAI as OpenAIClient
except Exception:
    raise Exception(
        "Please upgrade your OpenAI package to version 1.0.0 or later using the command: pip install --upgrade openai.")


class ModelEnum(str, Enum):
    GPT_35_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_35_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT_35_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_35_TURBO_0125 = "gpt-3.5-turbo-0125"
    GPT_35_TURBO_16K_0613 = "gpt-3.5-turbo-16k-0613"
    GPT_35_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"
    GPT_35_TURBO_INSTRUCT_0914 = "gpt-3.5-turbo-instruct-0914"
    GPT_4_0125_PREVIEW = "gpt-4-0125-preview"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_4_VISION_PREVIEW = "gpt-4-vision-preview"
    GPT_4_0613 = "gpt-4-0613"


class ToolFunctionDict(TypedDict):
    parameters: object
    description: str
    name: str


class ToolDict(TypedDict):
    type: str
    function: ToolFunctionDict


class ToolChoiceFunctionDict(TypedDict):
    name: str


class ToolChoiceDict(TypedDict):
    type: str
    function: ToolChoiceFunctionDict


def _try_parse_tool_message(role_prompt):
    # customer can add ## in front of name/content for markdown highlight.
    # and we still support name/content without ## prefix for backward compatibility.
    pattern = r"\n*#{0,2}\s*tool_call_id:\n+\s*(\S+)\s*\n*#{0,2}\s*content:\n?(.*)"
    match = re.search(pattern, role_prompt, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None

def _try_parse_tool_calls(role_prompt):
    # customer can add ## in front of name/content for markdown highlight.
    # and we still support name/content without ## prefix for backward compatibility.
    pattern = r"\n*#{0,2}\s*tool_calls:\n?(.*)"
    match = re.search(pattern, role_prompt, re.DOTALL)
    if match:
        rendered = literal_eval(match.group(1))
        for v in rendered:
            v["function"]["arguments"] = str(v["function"]["arguments"])
        return rendered
    return None


def _parse_chat(chat_str, images: Optional[List] = None, valid_roles: Optional[List[str]] = None):
    valid_roles = ["system", "user", "assistant", "function", "tool"]

    # openai chat api only supports below roles.
    # customer can add single # in front of role name for markdown highlight.
    # and we still support role name without # prefix for backward compatibility.
    separator = r"(?i)^\s*#?\s*(" + "|".join(valid_roles) + r")\s*:\s*\n"

    images = images or []
    hash2images = {str(x): x for x in images}

    chunks = re.split(separator, chat_str, flags=re.MULTILINE)
    chat_list = []

    for chunk in chunks:
        last_message = chat_list[-1] if len(chat_list) > 0 else None
        if last_message and "role" in last_message and "content" not in last_message:
            parsed_result = None
            if last_message["role"] == "assistant":
                parsed_result = _try_parse_tool_calls(chunk)
            if last_message["role"] == "tool":
                parsed_result = _try_parse_tool_message(chunk)
                if parsed_result is None:
                    raise ChatAPIFunctionRoleInvalidFormat(message="tool message should include tool_call_id, content")
            if parsed_result is None:
                parsed_result = try_parse_name_and_content(chunk)
            if parsed_result is None:
                # "name" is required if the role is "function"
                if last_message["role"] == "function" or last_message["role"] == "tool":
                    raise ChatAPIFunctionRoleInvalidFormat(
                        message="Failed to parse function role prompt. Please make sure the prompt follows the "
                                "format: 'name:\\nfunction_name\\ncontent:\\nfunction_content'. "
                                "'name' is required if role is function, and it should be the name of the function "
                                "whose response is in the content. May contain a-z, A-Z, 0-9, and underscores, "
                                "with a maximum length of 64 characters. See more details in "
                                "https://platform.openai.com/docs/api-reference/chat/create#chat/create-name "
                                "or view sample 'How to use functions with chat models' in our gallery.")
                # "name" is optional for other role types.
                else:
                    last_message["content"] = to_content_str_or_list(chunk, hash2images)
            else:
                if last_message["role"] == "assistant":
                    if isinstance(parsed_result, list):
                        last_message["tool_calls"] = parsed_result
                        last_message["content"] = None
                        continue
                if last_message["role"] == "tool":
                    assert len(parsed_result) == 2
                    last_message["tool_call_id"] = parsed_result[0]
                    last_message["content"] = to_content_str_or_list(parsed_result[1], hash2images)
                    continue
                last_message["name"] = parsed_result[0]
                last_message["content"] = to_content_str_or_list(parsed_result[1], hash2images)
        else:
            if chunk.strip() == "":
                continue
            # Check if prompt follows chat api message format and has valid role.
            # References: https://platform.openai.com/docs/api-reference/chat/create.
            role = chunk.strip().lower()
            validate_role(role, valid_roles=valid_roles)
            new_message = {"role": role}
            chat_list.append(new_message)
    return chat_list



@tool
@handle_openai_error()
def openai_tool_use(
    connection: OpenAIConnection,
    prompt: PromptTemplate,
    model: ModelEnum,
    temperature: float = 1,
    top_p: float = 1,
    n: int = 1,
    stream: bool = False,
    stop: Optional[list] = None,  # type: ignore
    max_tokens: Optional[int] = None,  # type: ignore
    presence_penalty: float = 0,
    frequency_penalty: float = 0,
    logit_bias: dict = {},
    user: Optional[str] = "",
    function_call: Optional[object] = None,
    functions: Optional[list] = None, # type: ignore
    response_format: object = dict(type="text"),
    tools: Optional[list[ToolDict]] = None, # type: ignore
    tool_choice: Optional[str] = None, # type: ignore
    rendered_prompt_text: Optional[str] = None,
    **kwargs
) -> [str, dict]:  # type: ignore
    chat_str = render_jinja_template(
        prompt  if rendered_prompt_text is None else rendered_prompt_text, trim_blocks=True, keep_trailing_newline=True, **kwargs)
    messages = _parse_chat(chat_str)
    # TODO: remove below type conversion after client can pass json rather than string.
    stream = to_bool(stream)
    params = {
        "model": model,
        "messages": messages,
        "temperature": float(temperature),
        "top_p": float(top_p),
        "n": int(n),
        "stream": stream,
        "stop": stop if stop else None,
        "max_tokens": int(max_tokens) if max_tokens is not None and str(max_tokens).lower() != "inf" else None,
        "presence_penalty": float(presence_penalty),
        "frequency_penalty": float(frequency_penalty),
        "logit_bias": logit_bias,
        "user": user,
        "response_format": response_format
    }

    if functions is not None:
        validate_functions(functions)
        params["functions"] = functions
        params["function_call"] = process_function_call(function_call)

    if tools is not None:
        functions = []
        for tool in tools:
            tool = cast(ToolDict, tool)
            if "type" in tool and "function" in tool:
                functions.append(tool["function"])
            else:
                raise ChatAPIInvalidFunctions(
                    message=f"tools parameter is invalid: {tools}")
        validate_functions(functions)
        params["tools"] = tools
    
    if tool_choice is not None:
        if tool_choice in ["none", "auto"]:
            params["tool_choice"] = tool_choice
        else:
            try:
                tool_choice_dict = json.loads(tool_choice)
            except:
                raise ChatAPIInvalidFunctions(
                    message=f"tool_choice parameter is invalid: {tool_choice}")
            tool_choice_dict = cast(ToolChoiceDict, tool_choice_dict)
            if "type" not in tool_choice_dict or "function" not in tool_choice_dict:
                raise ChatAPIInvalidFunctions(
                    message=f"tool_choice parameter is invalid: {tool_choice_dict}")
            else:
                if "name" not in tool_choice_dict["function"]:
                    raise ChatAPIInvalidFunctions(
                        message=f"tool_choice parameter is invalid: {tool_choice_dict}")
                
            params["tool_choice"] = tool_choice_dict["function"]

    _connection_dict = normalize_connection_config(connection)
    _client = OpenAIClient(**_connection_dict)
    completion = _client.chat.completions.create(**params)
    return post_process_chat_api_response(completion, stream, functions)
