import os
from google.genai import types

def write_file(working_directory, file_path, content):
    """
    Write `content` to `file_path`, ensuring it lives within `working_directory`.
    If `file_path` doesn’t exist, its parent directories will be created.
    Returns a success message or an error string.
    """
    try:
        # Resolve absolute paths
        wd_abs = os.path.abspath(working_directory)
        if os.path.isabs(file_path):
            file_abs = os.path.abspath(file_path)
        else:
            file_abs = os.path.abspath(os.path.join(wd_abs, file_path))

        # Verify that file_abs is inside wd_abs
        if not (file_abs == wd_abs or file_abs.startswith(wd_abs + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directory exists
        parent_dir = os.path.dirname(file_abs)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # Write (or overwrite) the file
        with open(file_abs, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to the file_path, The file path is provided and is limited to the sub-tree within the working directory..",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path is relative to the working directory and inlcudes the name. If not provided, function returns an error messaage.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="This is the content that needs to be written to the file",
            )
        },
    ),
)
