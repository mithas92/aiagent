from functions.get_file_content import get_file_content

if __name__ == "__main__":
    
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    
    
    
    
    # List out the the lorem ipsum 
    # print(get_file_content("calculator", "lorem.txt"))

    # List contents of the current directory within "calculator"
    # print(get_files_info("calculator", "."))

    # List contents of the "pkg" subdirectory within "calculator"
    # print(get_files_info("calculator", "pkg"))

    # Attempt to list "/bin" (outside permitted directory)
    # print(get_files_info("calculator", "/bin"))

    # Attempt to list parent directory (outside permitted directory)
    # print(get_files_info("calculator", "../"))