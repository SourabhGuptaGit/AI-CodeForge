import os
import subprocess as sp


def run_command(cmd, path, timeout=30):
    
    try:
        response = sp.run(cmd, cwd=path, stdout=sp.PIPE, stderr=sp.PIPE, timeout=timeout)
        output = f"""
                STDOUT: {response.stdout.decode()}
                STDERR: {response.stderr.decode()}
                """
        output = output if response.stdout or response.stderr else "No output produced."
        return output if response.returncode == 0 else f"{output} Process exited with code {response.returncode}"
    
    except Exception as cmd_error:
        return f"Error: executing Python file: {cmd_error}"


def run_python_file(working_directory, file_name, args=[]):
    
    abs_working_dir = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(abs_working_dir, file_name))
    
    if not file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_name}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        return f'Error: File "{file_name}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_name}" is not a Python file.'
    
    cmd = ["python", file_path]
    if args:
        cmd.extend(args)
    
    return run_command(cmd, abs_working_dir)



from google.genai import types
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python script/file with python3.12 interpreter also accepts CLI args as optional list, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="the file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of strings to be used as CLI args with python file.",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
    ),
)