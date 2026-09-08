import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
        "function": {
            "name": "get_file_content",
            "description": "Read the text file present at the pointed path, returns a output to be printed onto to the console, relative to working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path, pointing python file, for read, relative to the working directory(default is the working directory itself)",
                    },
                },
                "required":[
                    "file_path"
                ],
            },
        },
    }


def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        target_dir = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), target_dir]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"
