
import os, json
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key")

    from openai import OpenAI   
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

    import argparse
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
)
        message = response.choices[0].message
        messages.append(message)
        content = args.user_prompt


        if response.usage == None:
          raise RuntimeError("failed API request - usage == None")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        if not message.tool_calls:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if result_message["content"]:  
                pass
            else:
                raise Exception("call_function function result is empty")
            if args.verbose:
                print(f"-> {result_message['content']}")
        
if __name__ == "__main__":
    main()
    