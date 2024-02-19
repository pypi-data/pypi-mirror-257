# logger_config.py
import os
import logging
from az_auto.utils.custom_formatter import CustomFormatter

def setup_logger(name=__name__, log_directory='logs'):
    """Configure and return a logger with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if handlers already exist, return the logger to prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    # Create log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Define log file path
    log_file = os.path.join(log_directory, 'app.log')

    # Create a file handler and set its formatter
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(CustomFormatter())
    logger.addHandler(file_handler)

    # Create a stream handler with custom formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter())
    logger.addHandler(stream_handler)

    return logger
