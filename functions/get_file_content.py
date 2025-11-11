import os
from Support.config import MAX_FILE_CHAR


def get_file_content(working_directory, file_path):
    
    try:
        abs_working_dir = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        
        if not file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        file_data = ""
        with open(file_path, "r") as file_content:
            file_data = file_content.read()
        
        if len(file_data) > MAX_FILE_CHAR:
            file_data = f'{file_data[:MAX_FILE_CHAR]}[...File "{file_path}" truncated at {MAX_FILE_CHAR} characters]'
        return file_data
    except Exception as e:
        return f"Error: {e}"


from google.genai import types
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file as string in the specified directory with specific file name (and ensure's read upto Maximum charactor length defined by variable 'MAX_FILE_CHAR'), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of file to read, relative to the working directory. ",
            ),
        },
    ),
)