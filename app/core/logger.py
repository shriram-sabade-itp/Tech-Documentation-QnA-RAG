from loguru import logger
import os
from datetime import datetime


# -----------------------------------
# CREATE LOG DIRECTORY
# -----------------------------------

os.makedirs("logs", exist_ok=True)

timestamp = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

log_file = f"logs/{timestamp}.log"


# -----------------------------------
# REMOVE DEFAULT CONSOLE LOGGER
# -----------------------------------

logger.remove()


# -----------------------------------
# FILE LOGGER ONLY
# -----------------------------------

logger.add(
    log_file,

    level="INFO",

    format=(
        "{time} | "
        "{level} | "
        "{message}"
    ),

    rotation="10 MB",

    encoding="utf-8"
)