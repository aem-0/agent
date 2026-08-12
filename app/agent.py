import tools
import json
import sys
from openai import OpenAI
from tools import ToolRegistry


class Agent:
    def __init__(self, client, model: str, registry: tools.ToolRegistry):
        self.client = client
        self.model = model
        self.registry = registry
        self.messages = []

    def run(self, user_prompt: str):
        self.messages.append({"role": "user", "content": user_prompt})

        while True:
            chat = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.registry.get_schemas(),
            )

            if not chat.choices or len(chat.choices) == 0:
                raise RuntimeError("no choices in chat")

            message = chat.choices[0].message
            self.messages.append(message.model_dump())

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    result = self.registry.execute_tool(tool_call.function.name, args)

                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )
            else:
                print("Logs from your program will appear here!", file=sys.stderr)
                return message.content
