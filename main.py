# Testing out Gemini Connection
import os
import sys
from dotenv import load_dotenv
from google import genai

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) > 1:
        prompt_string = sys.argv[1]
    else: 
        print("Usage: python main prompt_string")
        sys.exit(1)

    client  = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=prompt_string
    )

    print(response.text)

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")      


if __name__ == "__main__":
    main()