import json
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import helper modules
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function
from Support.logger import log_conversation, log_data
from Support.config import SYSTEM_PROMPT


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MAX_RECALLS: int = 20

def main(userPrompt: str, verbose: bool):
    
    # Log the start of the session and the initial prompt
    log_data("\n\n\n")
    log_data("--- Agent Session Started ---")
    log_conversation("User", userPrompt)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=userPrompt)])
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    )
    
    for recall in range(MAX_RECALLS):
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
        )
        
        if not (response or response.usage_metadata):
            log_conversation("System Error", "Response is malformed or empty.", level='ERROR')
            return
        
        # Log token usage for tracking
        if verbose:
            log_data(
                f"--- Turn {recall+1} Token Usage ---",
                {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "response_tokens": response.usage_metadata.candidates_token_count
                }
            )
        
        # --- 1. Process and Log Model's Response ---
        if response.candidates:
            for candidate in response.candidates:
                if not (candidate and candidate.content):
                    continue
                
                # Append the model's message to the conversation history
                messages.append(candidate.content)

                # Check if the model is calling functions or providing text
                if response.function_calls:
                    function_names = [c.name for c in response.function_calls]
                    log_conversation("Model Action", f"Calling functions: {', '.join(function_names)}")
                else:
                    # Final text response
                    log_conversation("Model Final Response", response.text)
                    log_data("--- Agent Session Ended ---")
                    return
        
        # --- 2. Execute Functions and Prepare Tool Response ---
        if response.function_calls:
            # List to hold all function response Parts (Crucial for multi-call fix)
            function_response_parts = []
            
            for function_call_part in response.function_calls:
                # Execute the function and get the result Part
                _output_part = call_function(function_call_part, verbose)
                
                if _output_part:
                    function_response_parts.append(_output_part)
            
            # --- Append the unified Tool message (ONE tool message with ALL parts) ---
            if function_response_parts:
                tool_content = types.Content(role="tool", parts=function_response_parts)
                messages.append(tool_content)
                log_conversation("Tool Action", f"Sent {len(function_response_parts)} function results back to the Model.")

        # Safety break for max recalls
        if recall == MAX_RECALLS - 1:
            log_conversation("System Warning", f"Reached maximum {MAX_RECALLS} recalls. Exiting loop.", level='WARNING')
            break
            
    # Final cleanup output if the loop completes without a text response
    log_data("--- Agent Session Ended (Max Recalls) ---")
    if messages[-1].parts and messages[-1].parts[0].text:
        log_conversation("Model Final Response", messages[-1].parts[0].text)


if __name__ == "__main__":
    scriptArgs = sys.argv
    totalArgs = len(scriptArgs)
    userPrompt = None
    verbose = False
    if totalArgs == 1:
        log_conversation("System Error", "I Need a Prompt !", level='ERROR')
        sys.exit(1)
    elif totalArgs == 2:
        userPrompt = scriptArgs[1]
    elif totalArgs == 3 and scriptArgs[2].lower() == "--verbose":
        verbose = True
        userPrompt = scriptArgs[1]
    else:
        log_conversation("System Error", "Too many arguments !!", level='ERROR')
        sys.exit(1)
    
    main(userPrompt, verbose)