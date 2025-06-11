# Testing out Gemini Connection
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else: 
        print("Usage: python main 'Prompt'")
        sys.exit(1)



    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    client  = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print (f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    

    print("Response:")
    print(response.text)

      


if __name__ == "__main__":
    main()