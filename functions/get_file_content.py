import os
MAX_CHARS = 10000
def get_file_content(working_directory: str, file_path: str) -> str:
     try:
          working_dir_abs=os.path.abspath(working_directory)
          abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
          relative_file_path = os.path.normpath(os.path.join(working_directory,file_path))
          valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
          if not valid_target_dir:
               print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
          if not os.path.isfile(relative_file_path):
               print(f'Error: File not found or is not a regular file: "{abs_file_path}"')

          with open(relative_file_path, "r") as f:
               file_content_string = f.read(MAX_CHARS)
               # After reading the first MAX_CHARS...
               if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
               print(file_content_string)
               return file_content_string

     except Exception as e:
          print(f"Error: {e}")

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file relative to the working directory, truncated to the first 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}