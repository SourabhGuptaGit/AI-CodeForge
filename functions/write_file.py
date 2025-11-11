import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
    try:
        file_dir_path = os.path.dirname(file_path)
        if not os.path.exists(file_dir_path):
            os.makedirs(file_dir_path)
        with open(file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'


from google.genai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites Existing file or create a new file if doesn't exists already (and creates non existing required parent directories safely), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write/Overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String Content to write in the file, relative to the working directory.",
            ),
        },
    ),
)