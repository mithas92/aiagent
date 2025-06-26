import os

def get_files_info(working_directory, directory=None):
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