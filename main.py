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

# Logging
from log_to_csv import log_call

model_name = 'gemini-2.5-flash'

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client     = genai.Client(api_key=api_key)


    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    if len(sys.argv) > 2:
        verbose = sys.argv[2] == "--verbose"
    else:
        verbose = False

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
           ),
        ]


      # Start of the for loop
    got_final_response = False

    for _ in range(10):
            # The config=type.generate.config points to the list of available functins. The list is in
            # available_function. The list then takes it to
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],system_instruction=system_prompt)
             )

          # Add all candidates to conversation history so the model sees them in future iterations
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

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

                    # Orignal Bootdev required Printout.
                if verbose:
                    print(f"\n Bootdev req printout -> {function_call_result.parts[0].function_response.response}")

                      # Log to CSV for my stuff
                log_call(user_prompt, func_call.name, func_call.args, function_call_result.parts[0].function_response.response)
                print(f"-Calling Function: {func_call.name}")

        else:
            print("\nFinal Reponse:\n", response.text)
            got_final_response = True
            break

          # Append collected function results so the model sees them in the next iteration
        if func_results:
            messages.append(types.Content(role="user", parts=func_results))

      # Only exit with error if all 10 iterations were exhausted without a final text response
    if not got_final_response:
        sys.exit(1)


if __name__ == "__main__":
    main()
