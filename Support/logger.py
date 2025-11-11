
import logging
import sys
import json

LOG_FILE = "Agent.log"

def setup_logger(log_file: str = LOG_FILE):
    """
    Sets up a logger that outputs to both a file and the terminal (stdout).
    """
    # Create the logger
    logger = logging.getLogger('AgentLogger')
    logger.setLevel(logging.INFO)

    # Prevent logs from propagating to the root logger (which might duplicate output)
    logger.propagate = False 

    # Define the format for the log entries
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # --- 1. File Handler ---
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # --- 2. Stream Handler (Terminal) ---
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(message)s')) # Cleaner output for the terminal
    logger.addHandler(stream_handler)
    
    return logger

# Initialize the logger globally
agent_logger = setup_logger()

def log_conversation(role: str, content: str, level: str = 'INFO'):
    """
    Logs a conversation turn to the file (with full details) and terminal (clean output).
    """
    # The file log needs the full format (timestamp, level, etc.)
    file_log_message = f"{role}: {content}"
    
    # The terminal log needs to be cleaner, so we just write the message part
    terminal_log_message = f"{role}: {content}"
    
    # Send to the file handler with full formatting
    if level == 'INFO':
        agent_logger.info(file_log_message)
    elif level == 'WARNING':
        agent_logger.warning(file_log_message)
    elif level == 'ERROR':
        agent_logger.error(file_log_message)

def log_data(message: str, data: dict = None, level: str = 'INFO'):
    """Logs important data/parameters like token counts, errors, etc."""
    log_message = message
    if data:
        # Use simple string concatenation for the console to keep it readable, but full JSON for the file
        log_message = f"{message}:\n{json.dumps(data, indent=4)}"
    
    if level == 'INFO':
        agent_logger.info(log_message)
    elif level == 'ERROR':
        agent_logger.error(log_message)
