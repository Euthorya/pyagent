import os
from google.genai import types

MAX_SIZE = 10000

def get_file_content(working_directory, file_path):
    try:
        workdir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir_path, file_path))
        valid_target_dir = os.path.commonpath([workdir_path, target_dir]) == workdir_path
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir) as f:
            content = f.read(MAX_SIZE)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_SIZE} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Opens a file located in file_path under working directory and returns its contents, truncated to {MAX_SIZE} symbols",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path, relative to the working directory",
            ),
        },
    ),
)


