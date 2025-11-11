import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    
    abs_working_dir = os.path.abspath(working_directory)
    directory_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if not directory_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'
    
    meta_data = ""
    for dir_item in os.listdir(directory_path):
        item_size = 0
        is_dir = True
        item_path = os.path.join(directory_path, dir_item)
        if os.path.isfile(item_path):
            is_dir = False
        item_size = os.path.getsize(item_path)
        meta_data += f"- {dir_item}: file_size={item_size} bytes, is_dir={is_dir}\n"
    
    return meta_data


from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files and directories in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)