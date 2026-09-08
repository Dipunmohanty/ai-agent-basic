import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import Client, OpenAI, base_url

from call_function import call_function
from prompt import available_functions, system_prompt

def main():
    
    load_dotenv()
    api_key = os.environ.get("model-api-key")
    if api_key is None:
        raise RuntimeError("No api key found.")
    client = OpenAI(
        base_url = "model-url",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":args.user_prompt},
    ]
    # Now we can access `args.user_prompt`
    for i in range(20):
        response = client.chat.completions.create(
            model = "model-name",
            messages = messages,
            tools=available_functions,
        )
    
        if response.usage.prompt_tokens is None: raise RuntimeError("No api call")
        if args.verbose:
            print("User prompt:",args.user_prompt)
            print("Prompt tokens:",response.usage.prompt_tokens)
            print("Response tokens:",response.usage.completion_tokens)

        message = response.choices[0].message
        messages.append(message)
        
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                result_message = call_function(tool_call,args.verbose)
                if "content" not in result_message:
                    raise Exception ("No function output")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            if response.choices[0].message.content:
                print("Response: \n",response.choices[0].message.content)
                break

            print("System returned with no tool call or content.")
            sys.exit(1)
            
    else:
        print("Ran out of session window.")    
        sys.exit(1)
    
    sys.exit(0)
    

if __name__ == "__main__":
    main()
