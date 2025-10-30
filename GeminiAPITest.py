# A test program created using ChatGPT to check if Gemini API key exists in .env 
# and if the is valid. 

import os
from dotenv import load_dotenv
from google import genai

# Load .env file if present
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No API key found. Please set GOOGLE_API_KEY in your .env or environment.")
    exit(1)

# Initialize the client
client = genai.Client(api_key=api_key)

# Try a very simple request to verify the key works
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Test message: reply with a single word 'OK'"
    )
    print("✅ API key is valid!")
    print("Model replied:", response.text.strip())

except Exception as e:
    print("❌ API key is invalid or request failed.")
    print("Error details:", str(e))