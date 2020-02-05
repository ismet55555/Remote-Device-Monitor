#!/usr/bin/env python3

import logging
import sys
from logging.handlers import RotatingFileHandler

# Import all modules for app
import coloredlogs

# class NoParsingFilter(logging.Filter):
#     def filter(self, record):
#         return not record.getMessage().startswith('NOTE')

# Setting up log file handler
file_handler = logging.handlers.RotatingFileHandler(
    filename="tc-monitor.log", mode="w", maxBytes=10000000, backupCount=0
)
# Also include any sys.stdout in logs
stdout_handler = logging.StreamHandler(sys.stdout)
# Defining the logger
logger = logging.basicConfig(
    level=logging.INFO,
    format="[TC-Monitor] - [%(asctime)s] - %(levelname)-10s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[file_handler, stdout_handler],
)
# logger.addFilter(NoParsingFilter())

# Applying color to the output logs
colored_logger = coloredlogs.install(
    fmt="[TC-Monitor] - [%(asctime)s] - %(levelname)-10s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    logger=logger,
)
