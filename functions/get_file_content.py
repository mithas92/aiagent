import os
from google import genai
from google.genai import types

from functions.config import MAX_CHARACTERS

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Return the contents of file_path (absolute or relative to working_directory)
    as a string, up to MAX_CHARACTERS. If the file is longer, the returned
    string is truncated and a notice is appended. Errors are returned as strings
    prefixed with 'Error:'.

    :param working_directory: base directory under which files are permitted
    :param file_path: absolute path or path relative to working_directory
    :return: file contents or error message
    """
    # Resolve absolute paths
    wd_abs = os.path.abspath(working_directory)
    if os.path.isabs(file_path):
        target = os.path.abspath(file_path)
    else:
        target = os.path.abspath(os.path.join(wd_abs, file_path))

    # Ensure target is within working_directory
    try:
        if os.path.commonpath([wd_abs, target]) != wd_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'

    # Check that target is a regular file
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read up to MAX_CHARACTERS + 1 to detect truncation
    try:
        with open(target, 'r') as f:
            data = f.read(MAX_CHARACTERS + 1)
    except Exception as e:
        return f'Error: {e}'

    # Truncate if needed
    if len(data) > MAX_CHARACTERS:
        truncated = data[:MAX_CHARACTERS]
        return (
            truncated
            + f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        )

    return data


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file as as string. The file path is provided and is limited to the sub-tree within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path is relative to the working directory and inlcudes the name. If not provided, function returns an error messaage",
            ),
        },
    ),
)

