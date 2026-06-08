import os
from google.genai import types

def get_files_info(working_directory, directory=None) -> str:
    """
    List contents of `directory` inside `working_directory`.

    Returns:
      - Formatted listing string on success
      - Error if `directory` is None, outside working_directory, not a directory, or on other exceptions
    """
    try:
        # If no directory provided, treat as error
        if directory is None:
            return f'Error: "{directory}" is not a directory'

        # Resolve absolute paths
        wd_abs = os.path.abspath(working_directory)
        dir_abs = os.path.abspath(os.path.join(working_directory, directory))

        # Ensure target is inside working_directory
        if not dir_abs.startswith(wd_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure it’s a directory
        if not os.path.isdir(dir_abs):
            return f'Error: "{directory}" is not a directory'

        # Build listing
        entries = []
        for name in os.listdir(dir_abs):
            path = os.path.join(dir_abs, name)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            entries.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')

        return "\n".join(entries)

    except Exception as e:
        return f'Error: {e}'

# This helps file LLM to understand what the function does.  
# The working directory is NOT passed by the LLM. So it is not mentioned in the schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)




