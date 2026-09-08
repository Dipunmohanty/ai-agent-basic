import os
import subprocess

schema_run_python_file = {
    "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Executes a python file, based on the file name in a specified directory relative to working directory, using subprocess.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path, pointing python file, for execution, relative to the working directory(default is the working directory itself)",
                    },
                    "args": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Optional list of command-line arguments to pass to the script."
                    }
                },
                "required":[
                    "file_path"
                ]
            },
        },
    }


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        target_dir = os.path.normpath(os.path.join(os.path.abspath(working_directory),file_path))
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory),target_dir]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        print(target_dir)
        command = ['python3',target_dir]
        if args:
            command.extend(args)
        comp = subprocess.run(command,capture_output=True,text=True,timeout=30,check=False)
        output = ""
        if comp.returncode:
            output += f"Process exited with code {comp.returncode}"
        if comp.stdout is None and comp.stderr is None:
            output += "No output produced."
        if comp.stdout: output += f"STDOUT: {comp.stdout}"
        elif comp.stderr: output += f"STDERR: {comp.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

if __name__ == "__main__":
    res = run_python_file("functions","test.py")
    print(res)
