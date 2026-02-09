import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        result = "Result for current directory:\n"
        workdir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir_path, directory))
        valid_target_dir = os.path.commonpath([workdir_path, target_dir]) == workdir_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        content = os.listdir(target_dir)
        for i in content:
            result += f"- {i}: file_size={os.path.getsize(os.path.join(target_dir, i))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, i))}\n"
        return result
    except Exception as e:
        return str(f"Error: {e}")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
