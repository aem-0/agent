import argparse
import os
import sys
import json

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path

READ_TOOL = {
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

WRITE_TOOL = {
    "type": "function",
    "function": {
        "name": "Write",
        "description": "Write content to a file",
        "parameters": {
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write to",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
        },
    },
}


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
    messages = [{"role": "user", "content": args.p}]
    while True:
        chat = client.chat.completions.create(
            # I chose this model for my tests.
            # Take a look at OpenRouter for other models to replace it.
            model="openrouter/free",
            messages=messages,
            tools=[READ_TOOL, WRITE_TOOL],
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        message = chat.choices[0].message
        messages.append(message.model_dump())

        if message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.function.name == "Read":
                    args_dict = json.loads(tool_call.function.arguments)
                    file_path = args_dict.get("file_path")
                    file_content = ""
                    if file_path and Path(file_path).exists():
                        file_content = Path(file_path).read_text()
                    else:
                        file_content = f"Error: File '{file_path}' not found."

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": file_content,
                        }
                    )
                elif tool_call.function.name == "Write":
                    args_dict = json.loads(tool_call.function.arguments)
                    file_path = args_dict.get("file_path")
                    content = args_dict.get("content", "")

                    result_message = ""
                    if file_path:
                        try:
                            path = Path(file_path)
                            path.parent.mkdir(parents=True, exist_ok=True)
                            path.write_text(content)
                            result_message = f"Successfully wrote to {file_path}"
                        except Exception as e:
                            result_message = f"Error writing file: {str(e)}"
                    else:
                        result_message = "Error: 'file_path' argument is missing."

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result_message,
                        }
                    )
        else:
            print("Logs from your program will appear here!", file=sys.stderr)
            if message.content:
                print(message.content)
            break


if __name__ == "__main__":
    main()
