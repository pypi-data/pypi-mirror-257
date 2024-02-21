from setuptools import find_packages, setup

PACKAGE_NAME = "tool_use"

setup(
    name=PACKAGE_NAME,
    version="0.0.2",
    description="This is my tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["openai_tool_use = tool_use.tools.utils:list_package_tools"],
    },
    # This line tells setuptools to include files from MANIFEST.in
    include_package_data=True,
)
