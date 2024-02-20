#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

"""
Setup operations.
"""

import coloredlogs
import logging
import sys
import os

LOG_LEVELS = ("NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
LOGGER = logging.getLogger(__name__)


def setup_logger(
        name: str,
        log_filepath: str = None,
        mode: str = "a",
        primary_level: str = "DEBUG",
        secondary_level: str = "CRITICAL",
        secondary_modules: [str] = ("google", "azure", "urllib3", "msal")
) -> logging.Logger:
    """
    Define default logger.

    Parameters
    ----------
    name: str
        Module name.
    log_filepath: str
        Log filepath.
    mode: str
        Log file open mode.
    primary_level: str
        Primary log level.
    secondary_level: str
        Secondary log level.
    secondary_modules: [str]
        Secondary modules to filter.

    Returns
    -------
    logging.Logger
        Logger.
    """
    assert primary_level in LOG_LEVELS, f"log level '{primary_level}' not recognized."
    assert secondary_level in LOG_LEVELS, f"log level '{secondary_level}' not recognized."

    # Setting-up the application logging:
    logging_handlers = [logging.StreamHandler(sys.stdout)]

    if log_filepath:
        logging_handlers.append(logging.FileHandler(log_filepath, mode=mode))

    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=primary_level,
        handlers=logging_handlers
    )

    logger = logging.getLogger(name=name)
    coloredlogs.install(level=primary_level, logger=logger, isatty=True)

    # Suppressing warnings not sent by `logging` module:
    if secondary_level in ("ERROR", "CRITICAL"):
        os.environ["PYTHONWARNINGS"] = "ignore"

    # Filtering secondary logs:
    for module in secondary_modules:
        secondary_logger = logging.getLogger(module)
        secondary_logger.setLevel(secondary_level)

    return logger
