import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try: 
        working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory, file_path))

        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, mode=0o777, exist_ok=True)

        valid_target_file_path = os.path.commonpath([working_directory, target_file]) 
        if valid_target_file_path != working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        

        
        with open(target_file, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except ValueError as e:
        return f"Error: {e}"
    except OSError as e:
        return f"Error: {e}"
    except FileNotFoundError:
        return f'Error: "{file_path}" does not exist'
    except IsADirectoryError:
        return f'Error: "{file_path}" is a directory'
    except PermissionError:
        return f'Error: Permission denied for "{file_path}"'
    
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Adds content to the target file",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The directory the file must be inside. Files outside this directory cannot be accessed.",
                },
                "file_path": {
                    "type": "string",
                    "description": "path to the file which contents will be added to"
                },
                "content": {
                    "type": "string",
                    "description": "content that will be added to the target file"
                }
            },
        "required": ["working_directory", "file_path", "content"]
        },
    },
}