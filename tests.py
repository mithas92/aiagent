from functions.write_file import write_file

if __name__ == "__main__":
    
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


    # print(get_file_content("calculator", "main.py"))
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print(get_file_content("calculator", "/bin/cat"))
    
    
    
    
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