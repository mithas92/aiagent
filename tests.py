from functions.run_python import run_python_file

if __name__ == "__main__":
    
    print(run_python_file("calculator", "main.py")) # (should print the calculator's usage instructions)
    print(run_python_file("calculator", "main.py", ["3 + 5"])) # (should run the calculator... which gives a kinda nasty rendered result)
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py")) # (this should return an error)
    print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)

    
    
    
    # print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    # print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    # print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


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