import os

def write_file(working_directory, file_path, content):
    try:
        workdir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir_path, file_path))
        valid_target_dir = os.path.commonpath([workdir_path, target_dir]) == workdir_path
        #breakpoint()
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return str(f"Error: {e}")