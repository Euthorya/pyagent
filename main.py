import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function

MAX_CALLS = 10

def main():
    print("Hello from pyagent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("The api key was not set")
    client = genai.Client(api_key=api_key)
    args = get_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for i in range(MAX_CALLS):
        response = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)


        if not response.usage_metadata:
            raise RuntimeError(f"Empty response from Google API: {response}")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for function_call in response.function_calls:
                call_results = []
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Empty parts in the function result")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Parts response contains None as a response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Response is None")
                call_results.append(function_call_result.parts[0])
                messages.append(types.Content(role="user", parts=call_results))
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            break
    else:
        print(f"Agent was not able to find a solution in {MAX_CALLS} iterations")
        exit(1)

def get_args():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()




if __name__ == "__main__":
    main()
