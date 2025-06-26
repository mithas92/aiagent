from functions.get_files_info import get_files_info

if __name__ == "__main__":
    # List contents of the current directory within "calculator"
    print(get_files_info("calculator", "."))

    # List contents of the "pkg" subdirectory within "calculator"
    print(get_files_info("calculator", "pkg"))

    # Attempt to list "/bin" (outside permitted directory)
    print(get_files_info("calculator", "/bin"))

    # Attempt to list parent directory (outside permitted directory)
    print(get_files_info("calculator", "../"))