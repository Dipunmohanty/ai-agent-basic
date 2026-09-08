import os

schema_write_file = {
    "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes to the text file, using the content, present at the pointed path, relative to working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path, pointing python file, for read, relative to the working directory(default is the working directory itself)",
                    },
                    "content": {
                        "type": "string",
                        "description": "Contains the string, which is write to file pointed by the file path."
                    }
                },
                "required":[
                    "file_path","content"
                ],
            },
        },
    }


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_dir = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), target_dir]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_dir),exist_ok= True)

        with open(target_dir,"w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)' 

    except Exception as e:
        return f"Error: {e}"


#if __name__ == "__main__":
#    write_file("./calculator","try.txt","this is a test")