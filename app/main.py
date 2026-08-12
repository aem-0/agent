import argparse
import os
import sys
import json

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

from tools import (
    READ_TOOL,
    WRITE_TOOL,
    BASH_TOOL,
    read_file,
    write_file,
    run_bash,
    Tool,
    ToolRegistry,
)

from agent import Agent


def main():
    load_dotenv()

    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    t = ToolRegistry()
    t.register(Tool(READ_TOOL, read_file))
    t.register(Tool(WRITE_TOOL, write_file))
    t.register(Tool(BASH_TOOL, run_bash))

    # I chose this model for my tests.
    # Take a look at OpenRouter for other models to replace it.
    agent = Agent(client=client, model="openrouter/free", registry=t)
    result = agent.run(args.p)

    print(result)


if __name__ == "__main__":
    main()
