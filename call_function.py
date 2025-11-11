from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from Support.logger import log_conversation # Import the logger
from Support.config import WORKING_DIRECTORY


# Modified to return types.Part instead of types.Content
def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Part:

    func_name = function_call_part.name
    
    log_conversation("Tool Action", f"Executing function: {func_name}({function_call_part.args})")
    
    func_to_run = [
        get_files_info, get_file_content, run_python_file, write_file
    ]
    
    response_result = {"error": f"Unknown function: {func_name}"}
    
    for func in func_to_run:
        if func_name == func.__name__:
            try:
                result = func(WORKING_DIRECTORY, **function_call_part.args)
                response_result = {"result": result}
                log_conversation("Tool Result", f"Successfully ran {func_name}. Result length: {len(str(result))} chars.")
            except Exception as e:
                response_result = {"error": f"Function execution failed: {type(e).__name__}: {str(e)}"}
                log_conversation("Tool Result", f"ERROR running {func_name}. Error: {e}", level='ERROR')
            break
            
    return types.Part.from_function_response(
        name=func_name,
        response=response_result,
    )
