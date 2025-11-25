# This file is specifically for chapter 3, lesson of bootdev aiagent course. 
# The purpose of this is to setup the file to test the exact logic flow and and ask an LLM to help understand the logic. 
# As of now (Nov 23, 2025) will just update the later since LLM not calling the function yet.  

import os
import sys
from dotenv import load_dotenv
from google import genai

from google.genai import types

# from prompts import system_prompt
#Defines which functions are available for the LLM to use. 
from functions.get_files_info import available_functions

model_name = 'gemini-2.0-flash-001'

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


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

# This helps file LLM to understand what the function does.  
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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)



# This function is the main program it self. 
def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else: 
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    client  = genai.Client(api_key=api_key)

    # The config=type.generate.config points to the list of available functins. The list is in 
    # available_function. The list then takes it to 
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt)
    )


    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print (f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    

    if response.function_calls:
        for i in response.function_calls:
           print(f"Calling function: {i.name}({i.args})")
    else:
        print("Response", response.text)    
  

if __name__ == "__main__":
    main()