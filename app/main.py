import argparse
import os
import sys

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv



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
        model="inclusionai/ling-3.0-tiny:free",
        messages=[{"role": "user", "content": args.p}],
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    print("Logs from your program will appear here!", file=sys.stderr)
    print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()
