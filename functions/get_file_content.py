import os
from config import MAX_CHARS 

def get_file_content(working_directory: str, file_path: str) -> str:

    try: 
        working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory, file_path))
        
        valid_target_file_path = os.path.commonpath([working_directory, target_file]) 
        if valid_target_file_path != working_directory:
            return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        
        return file_content_string
        
        
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
    
    
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file. If the file exceeds the maximum allowed length, the returned content is truncated and includes a truncation notice.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The directory the file must be inside. Files outside this directory cannot be accessed.",
                },
                "file_path": {
                    "type": "string",
                    "description": "path to the file which contents will be retrieved"
                }
            },
        "required": ["working_directory", "file_path"]
        },
    },
}