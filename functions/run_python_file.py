import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
     try:
          working_dir_abs=os.path.abspath(working_directory)
          print(working_dir_abs)
          abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
          print(abs_file_path)
          relative_file_path = os.path.normpath(os.path.join(working_directory,file_path))
          print(relative_file_path)
          valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
          if not valid_target_dir:
               print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
          if not os.path.isfile(relative_file_path):
               print(f'Error: "{file_path}" does not exist or is not a regular file')
          if not os.path.basename(abs_file_path).endswith('.py'):
                    print(f'Error: "{file_path}" is not a Python file')
          
          command = ["python", abs_file_path]
          if args != None:
               command.extend(args)

          print(command)
          try:
               CommandRun = subprocess.run(command,capture_output=True,text=True,timeout=30)

               if CommandRun.returncode != 0:
                    print(f"Process exited with code {CommandRun.returncode}")

               if CommandRun.stderr == "" and CommandRun.stdout == "":
                    print("No output produced")
               else:
                    if CommandRun.stderr != "":
                         print("STDERR: "+CommandRun.stderr)
                    
                    if CommandRun.stdout != "":
                         print("STDOUT: "+CommandRun.stdout)
          except Exception as e:
               print(f"Error: executing Python file: {e}")
          
     except Exception as e:
          print(f'Error: {e}')

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory (30 second timeout) and returns its stdout and stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the .py file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}