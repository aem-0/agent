import argparse
import os
import sys
import json

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path


def main():
    load_dotenv()

    API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
        # I chose this model for my tests.
        # Take a look at OpenRouter for other models to replace it.
        model="openrouter/free",
        messages=[{"role": "user", "content": args.p}],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["file_path"],
                    },
                },
            }
        ],
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    message = chat.choices[0].message
    print("Logs from your program will appear here!", file=sys.stderr)

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        if tool_call.function.name == "Read":
            args_dict = json.loads(tool_call.function.arguments)
            file_path = args_dict.get("file_path")

            if file_path:
                content = Path(file_path).read_text()
                print(content, end="")
    else:
        if message.content:
            print(message.content)


if __name__ == "__main__":
    main()
