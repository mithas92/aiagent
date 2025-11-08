# Testing out Gemini Connection
import os
import sys
from dotenv import load_dotenv
from google import genai

from google.genai import types

from prompts import system_prompt
from functions.get_files_info import available_functions

model_name = 'gemini-2.0-flash-001'

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