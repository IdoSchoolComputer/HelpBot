import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
import json
from call_function import call_function
import sys


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
print("got key")
if api_key == None:
    raise(RuntimeError)

parser = argparse.ArgumentParser(description="HelpBot")
parser.add_argument("user_prompt",type=str,help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
print("sending query...")
messages = [
    {"role" : "system", "content" : system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for i in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message

    assistant_message = {
        "role": "assistant",
        "content": message.content or "",
    }
    if message.tool_calls:
        assistant_message["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments or "{}",
                },
            }
            for tc in message.tool_calls
        ]
    messages.append(assistant_message)

    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result = call_function(tool_call=tool_call,verbose=args.verbose)
            messages.append(result)
            

    else:
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens:{response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Response:\n{response.choices[0].message.content}")
        break
else:
    print(f"\nError: Maximum number of iterations (10) reached.")
    print("The model failed to produce a final response.")
    sys.exit(1) 
