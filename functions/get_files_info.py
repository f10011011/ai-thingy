import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try: 
        working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory, directory))
        
        valid_target_dir = os.path.commonpath([working_directory, target_dir]) 
        if valid_target_dir != working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_list = os.listdir(target_dir)
        directory_content = []
        
        for file in files_list:
            file_dir = os.path.join(target_dir, file)
            file_name = os.path.basename(file_dir)
            file_size = os.path.getsize(file_dir)
            is_dir = os.path.isdir(file_dir)
            path_line=f"- {file}: file_size={file_size} bytes, is_dir={is_dir}" 
            directory_content.append(path_line)

        text_to_return="\n".join(directory_content)

        return text_to_return


    
    except ValueError as e:
        return f"Error: {e}"
    except OSError as e:
        return f"Error: {e}"
    except FileNotFoundError:
        return f'Error: "{directory}" does not exist'
    except NotADirectoryError:
        return f'Error: "{directory}" is not a directory'
    except PermissionError:
        return f'Error: Permission denied for "{directory}"'
    
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
         "required": ["working_directory", "directory"]
        },
    },
}
    
    
