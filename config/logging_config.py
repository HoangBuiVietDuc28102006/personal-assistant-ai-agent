import logging
import logging.config
import os
from config.config import Config


# === Ensure log directory exists ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "assistant.log")


# === Base formatters ===
FORMATTERS = {
    "standard": {
        "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    },
    "detailed": {
        "format": "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(name)s: %(message)s"
    },
}


# === Handlers ===
# In production, file-only. In dev, file + console.
HANDLERS = {
    "console": {
        "class": "logging.StreamHandler",
        "level": "DEBUG" if Config.DEBUG else "INFO",
        "formatter": "standard",
    },
    "file": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOG_FILE,
        "maxBytes": 5_000_000,   # 5 MB
        "backupCount": 5,
        "formatter": "detailed",
        "level": "DEBUG",
    },
}


# === Dynamic root handler selection ===
root_handlers = ["file"]
if Config.DEBUG:
    root_handlers.append("console")


# === Final configuration ===
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS,
    "handlers": HANDLERS,
    "root": {
        "handlers": root_handlers,
        "level": "DEBUG" if Config.DEBUG else "INFO",
    },
}


def setup_logging():
    """Initialize project-wide logging."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info(f"🪵 Logging initialized (ENV={Config.ENV}, DEBUG={Config.DEBUG})")
