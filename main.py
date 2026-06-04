# Main file for the aiagent bootdev course
import os
import sys
from dotenv import load_dotenv
from google import genai

from google.genai import types

from prompts import system_prompt

#Defines which functions are available for the LLM to use. 
from call_function import available_functions

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

    # print (f"User prompt: {user_prompt}")
    # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    

    
    
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