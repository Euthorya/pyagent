import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        workdir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir_path, file_path))
        valid_target_dir = os.path.commonpath([workdir_path, target_dir]) == workdir_path
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args:
            command.extend(args)
        p = subprocess.run(command, capture_output=True, text=True, timeout=30) 
        result = ""
        if p.returncode != 0:
            result += f"Process exited with code {p.returncode}\n"
        if not p.stderr and not p.stdout:
            result += f"No output produced\n"
        else:
            result += f"STDOUT: {p.stdout}\nSTDERR: {p.stderr}\n"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
        
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Runs the .py file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file",
            ),
        },
    ),
)