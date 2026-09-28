import os, subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try: 
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        target_file_commonpath = os.path.commonpath([abs_working_directory, target_file]) 
        
        if target_file_commonpath != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args: 
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )
        messages = []
        if result.returncode != 0:
            messages.append(f"Process exited with code {result.returncode}")
        if len(result.stdout)!=0:
             messages.append("STDOUT:" + result.stdout)
        if len(result.stderr)!=0:
            messages.append("STDERR:" + result.stderr)
        if len(result.stderr)==0 and len(result.stdout)==0:
            messages.append("No output produced")
           
            
        final_output="\n".join(messages)

        return final_output

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the target python file, can accept args. Will log STDOUT and STDERR. ",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The directory the file must be inside. Files outside this directory cannot be accessed.",
                },
                "file_path": {
                    "type": "string",
                    "description": "path to the file which contents will be executed"
                },
                "args": {
                    "type": "list[str]",
                    "description": "additional information on how to run file"                }
            },
        "required": ["working_directory", "file_path"]
        },
    },
}