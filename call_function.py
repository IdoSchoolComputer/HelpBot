from functions.get_files_info import schema_get_files_info,get_files_info
from functions.get_file_content import schema_get_file_content,get_file_content
from functions.write_file import schema_write_file,write_file
from functions.run_python_file import schema_run_python_file,run_python_file
import json
from collections.abc import Callable
import io
from contextlib import redirect_stdout


available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]

function_map: dict[str, Callable[..., str]] = {
          "get_file_content": get_file_content, 
          "get_files_info" : get_files_info,
          "write_file" : write_file,
          "run_python_file" : run_python_file,
          }

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_args["working_directory"] = "./calculator"

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        returned = function_map[function_name](**function_args)

    printed = buffer.getvalue()

    # Use stdout, plus the return value if there is one
    parts = [printed.strip()]
    if returned:
        parts.append(str(returned))
    content = "\n".join(p for p in parts if p) or "(no output)"

    if verbose:
        print(content)  # now you still see it in your terminal

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": content,
    }

     

