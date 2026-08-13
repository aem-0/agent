import subprocess
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

BASH_TOOL = {
    "type": "function",
    "function": {
        "name": "Bash",
        "description": "Execute a shell command",
        "parameters": {
            "type": "object",
            "required": ["command"],
            "properties": {
                "command": {"type": "string", "description": "The command to execute"}
            },
        },
    },
}


def read_file(file_path: str) -> str:
    path = Path(file_path)
    if path.exists():
        return path.read_text()
    return f"Error: File '{file_path}' not found."


def write_file(file_path: str, content: str) -> str:
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def run_bash(command: str) -> str:
    try:
        res = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        return res.stdout + res.stderr
    except subprocess.TimeoutExpired:
        return "Error: Command "


class Tool:
    def __init__(self, tool: dict, func):
        self.tool = tool
        self.name = tool["function"]["name"]
        self.func = func

    def execute(self, **kwargs):
        return self.func(**kwargs)


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get_schemas(self):
        return [t.tool for t in self._tools.values()]

    def execute_tool(self, name: str, args: dict) -> str:
        if name in self._tools:
            return self._tools[name].execute(**args)
        return f"Error: Tool '{name}' not found."
