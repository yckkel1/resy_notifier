import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(
        info_log_file="logs/resy_notifier.log",
        error_log_file="logs/error.log",
        max_bytes=5 * 1024 * 1024,
        backup_count=5
):
    """
    Set up the logging configuration.

    Args:
        info_log_file (str): Path to the info-level log file.
        error_log_file (str): Path to the error-level log file.
        max_bytes (int): Maximum size of a log file before rotating (in bytes).
        backup_count (int): Number of backup log files to keep.
    """

    # Create the logger
    logger = logging.getLogger("ResyNotifier")
    logger.setLevel(logging.DEBUG)  # The logger captures all log levels

    # Formatter for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # INFO-level file handler
    info_handler = RotatingFileHandler(
        info_log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    info_handler.setLevel(logging.INFO)  # Capture only INFO and above
    info_handler.setFormatter(formatter)
    info_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    # ERROR-level file handler
    error_handler = RotatingFileHandler(
        error_log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    error_handler.setLevel(logging.ERROR)  # Capture only ERROR and above
    error_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    # Prevent log propagation to root logger
    logger.propagate = False

    return logger
