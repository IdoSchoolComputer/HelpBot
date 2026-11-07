import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
     try:
          working_dir_abs=os.path.abspath(working_directory)
          abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
          relative_file_path = os.path.normpath(os.path.join(working_directory,file_path))
          valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
          if not valid_target_dir:
               print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
          if os.path.isdir(relative_file_path):
               print(f'Error: Cannot write to "{file_path}" as it is a directory')

          parent_dir = os.path.dirname(abs_file_path)
          os.makedirs(parent_dir, exist_ok=True)

          with open(relative_file_path, "w") as f:
               f.write(content)
               print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
     
     except Exception as e:
          print(f'Error: {e}')
          

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory, creating parent directories and overwriting the file if it already exists",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The full text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}