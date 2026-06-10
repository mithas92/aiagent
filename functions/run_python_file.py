import os
import subprocess
import sys

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    """
    Run an external Python script, capturing stdout/stderr.

    Parameters:
        working_directory (str): permitted base directory
        file_path (str): path to the .py file (absolute or relative to working_directory)
        args (list of str, optional): additional command-line args to pass

    Returns:
        str: formatted output or error message
    """
    if args is None:
        args = []

    # Resolve absolute paths
    wd_abs = os.path.abspath(working_directory)
    fp_abs = os.path.abspath(os.path.join(working_directory, file_path)
                             if not os.path.isabs(file_path) else file_path)

    # 2. Prevent escape from working_directory
    if os.path.commonpath([wd_abs, fp_abs]) != wd_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # 3. Must be a file (not a directory)
    if not os.path.isfile(fp_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    # 4. Must be a .py file
    if not fp_abs.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # 5. Run via subprocess.run. Note sys.executable provides the exact python interpreter
        completed_process = subprocess.run(
            [sys.executable, fp_abs] + args,
            cwd=wd_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 6a–c. Format stdout/stderr and exit code
        parts = []
        if completed_process.stdout:
            parts.append(f'STDOUT:\n{completed_process.stdout}')
        if completed_process.stderr:
            parts.append(f'STDERR:\n{completed_process.stderr}')
        if completed_process.returncode != 0:
            parts.append(f'Process exited with code {completed_process.returncode}')

        return "\n".join(parts) if parts else "No output produced."

    except Exception as e:
        # 7. Catch any execution errors
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with or without arguments. The file path is provided and is limited to the sub-tree within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path is relative to the working directory and inlcudes the name. Errors are produced are returned in the output",
            ),
        },
    ),
)

