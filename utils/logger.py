import logging
import sys
import os
from logging import handlers

logger = None

os.makedirs("logs/", exist_ok=True)

if "runserver" in sys.argv[1] or "gunicorn" in sys.argv[0]:
    logfile = "logs/app.log"
    logger_name = "app"
    log_handler = handlers.TimedRotatingFileHandler(
        filename=logfile, when="midnight"
    )
    log_handler.suffix = "%Y-%m-%d"
else:
    logfile = "logs/generic-platform.log"
    logger_name = "generic_log"
    log_handler = logging.FileHandler(filename=logfile)

log_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="[%(levelname)s] - %(asctime)s - %(filename)s - %(funcName)s - %(message)s"
)
log_handler.setFormatter(formatter)
logger = logging.getLogger(logger_name)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)
