"""Setup custom logging"""
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from pathlib import Path


def configure_logging(log_file: Path) -> None:
    """Configure custom logging.

    :param log_file: path to the log file
    """
    msg_format = "%(asctime)s | %(levelname)s | %(message)s"
    formatter = Formatter(msg_format)

    handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        backupCount=31
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

