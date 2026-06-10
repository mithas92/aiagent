# Main file for the aiagent bootdev course
import os
import sys
from dotenv import load_dotenv
from google import genai

from google.genai import types

# The System Prompt
from prompts import system_prompt

# CALLING functions. Defines which are vailable are available for the LLM to use. 
from call_function import available_functions, call_function

model_name = 'gemini-2.5-flash'

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

    # Old Test
    # user_prompt = "What is the capital of Pakistan"

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

    # Old Tests
    # print (f"User prompt: {user_prompt}")
    # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    
    
    # if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    #     print (f"User prompt: {user_prompt}")
    #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    

    # if response.function_calls:
    #     for i in response.function_calls:
    #        print(f"Old Test calling function:  {i.name}({i.args})")
    # else:
    #     print("Old Test Response:  ", response.text)    
  
    if len(sys.argv) > 2: 
        verbose = sys.argv[2] == "--verbose"
    else:
        verbose = False

    func_results = []
  
    # response.function_calls is a LIST of objects type.FunctionCall
    if response.function_calls:
        for func_call in response.function_calls:
            function_call_result = call_function(func_call, verbose)
            if not function_call_result.parts:
               raise ValueError(f"Function '{func_call.name}' returned a result with no parts.")
            if not function_call_result.parts[0].function_response:
               raise ValueError(f"Function '{func_call.name}' returned with response")
            if not function_call_result.parts[0].function_response.response:
               raise ValueError(f"Function '{func_call.name}' returned with response text")
           
            func_results.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print("New no Test Response:  ", response.text)    


if __name__ == "__main__":
    main()