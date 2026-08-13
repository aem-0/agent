# I Built My Own AI Agent
This repo is my implementation of the ["Build your own Claude Code"](https://app.codecrafters.io/courses/claude-code/overview) challenge on CodeCrafters.

## Why I Built It
In this era of AI, there is a lot going on, so I was curious about how AI agents work.
The best way to understand how something works is to build it yourself, so I found this course and implemented my own solution.
This agent is CLI based and has tools (function calls) that allow it to execute tasks autonomously. It can also answer your prompts, but you need to provide an API key.

## Features
* Read tool for reading files that the LLM wants to read.
* Write tool for writing content that the LLM wants to write to files.
* Bash tool for executing commands requested by the LLM.

## How It works
1. When you run the application, you pass a prompt using the -p argument.
2. The agent sends the prompt and the tools defined in `tools.py` to the model through the OpenRouter api.
3. If the model returns `tool_calls`, the `ToolRegistry` class executes the functions, read_file, write_file and run_bash.
4. The agent stores each step of the conversation until the model sends a final answer. 
Then the result is printed in the terminal.

## Tech Stack
* Python 3.14
* OpenAI SDK 
* python-dotenv
* subprocess
* pathlib

## How To Run
- You need an API key to communicate with the LLM. Make sure to add it to the `.env` file. See `.env.example` for the configuration.
- The `requirements.txt` file contains all the required dependencies.
1. Clone the repository
```bash
git clone https://github.com/aem-0/agent.git
cd agent
```
2. Install packages from requirements.txt
```bash
pip install -r requirements.txt
```

## Usage
1. Example 1: The LLM reads the current directory
```bash
python3 app/main.py -p "What files are in the current directory?"
```

2. Example 2: The LLM creates a file and modifies it
```bash
python3 app/main.py -p "Create a python script called hello.py that prints 'Hello World' and execute it."
```
