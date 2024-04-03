import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(
    logger_name: str = "root",
    log_root: str = os.getcwd(),
    log_file: Optional[str] = None,
    log_level: int = logging.INFO,
    stream: bool = True,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """
    Set up a logger with the given parameters.

    Args:
        logger_name (str): The name of the logger.
        log_root (str): The root directory for the log files.
        log_file (Optional[str]): The name of the log file. If None, no file logging is done.
        log_level (int): The logging level.
        stream (bool): If True, logs will also be output to stdout.
        log_format (Optional[str]): The format of the log messages.

    Returns:
        logging.Logger: The set up logger.
    """
    logger = logging.getLogger(logger_name)

    # Check if the logger already has handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if stream:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if log_file:
        log_file = os.path.join(log_root, "logs", log_file)
        os.makedirs(os.path.join(log_root, "logs"), exist_ok=True)

        if os.path.exists(log_file):
            # If the log file already exists, rotate it
            file_handler = RotatingFileHandler(
                log_file, mode="a", maxBytes=10 * 1024 * 1024, backupCount=5
            )
        else:
            file_handler = logging.FileHandler(log_file, mode="a")

        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":

    def main() -> None:
        """
        Main function to set up a custom logger and log some messages.
        """
        setup_logging(
            logger_name="custom_logger",
            log_root=os.getcwd(),
            log_file="custom_log_file.log",
            log_level=logging.DEBUG,
        )

        # Get the custom logger
        custom_logger = logging.getLogger("custom_logger")

        # Log some messages
        custom_logger.debug("Debug message")
        custom_logger.info("Info message")
        custom_logger.warning("Warning message")
        custom_logger.error("Error message")
        custom_logger.critical("Critical message")

    main()
