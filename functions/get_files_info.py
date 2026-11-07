import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
     try:
          working_dir_abs=os.path.abspath(working_directory)
          target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
          # Will be True or False
          valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
          if not valid_target_dir:
               print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
          if not os.path.isdir(target_dir):
               print(f'Error: "{directory}" is not a directory')
               
          else:
               print(f'Success: "{directory}" is within the working directory')

          contents = os.listdir(target_dir)
          print(f"result for '{working_directory}' directory:")
          for file in contents:
               file=target_dir+"/"+file
               name = os.path.basename(file)
               size = os.path.getsize(file)
               isdir = os.path.isdir(file)
               print(f"\t- {name}: file_size={size}, is_dir={isdir}")
          
     except Exception as e:
          print(f"Error: {e}")

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
        },
    },
}


