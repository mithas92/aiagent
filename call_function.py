from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

from collections.abc import Callable

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
# This dictionary matches the function name string with the function names itself
# Note: This only works since wer have imported all the functions from their
# respective files. 
function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

# The function calling 
def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
# def call_function(function_call: types.FunctionCall, verbose: bool = False):
    
    # Convert function_name to a empty string if function name does not exist. 
    function_name = function_call.name or ""
       
    # if function_name is not in the list as per the dict, then return this error
    # as a type that is understood by Gemini
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                   name=function_name,
                   response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Makes a 'shallow copy' of of the arguments list. 
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator" #Add the working directory. 

    # print(f"\n +++ INSIDE CALL_FUNCTION.PY +++ ")
    # print(f" --> function name: {function_name}")
    # print(f" --> arg dictionary: {args}")
    
    # Run the function. Using Keyword Arguments using a dictionary. 
    function_result = function_map[function_name](**args)
    
    # Another old test printout 
    # print(f" --> result from function: {function_result} <---")

    # MAIN RETURN FUNCTION
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
                )
            ],
        )
    # THIS IS THE ORIGINAL PRINTOUT FOR THE COURSE 
    # if verbose:
    #     print(f"** Calling function: {function_name}({function_call.args})")
    # else:
    #     print(f" ** - Calling function: {function_name}")

    