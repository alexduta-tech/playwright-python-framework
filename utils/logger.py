"""
Docstring for utils.logger module.
Provides a logger setup function for consistent logging across the framework.
"""
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from utils.config import DEFAULT_LOG_DIR, DEFAULT_LOG_LEVEL

# Use log settings directly from config
os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)

def get_logger(name=__name__):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace("/", "_").replace("\\", "_")
    log_file = os.path.join(DEFAULT_LOG_DIR, f"{safe_name}_{timestamp}.log")
    
    # Convert string level to logging constant
    try:
        level = logging._nameToLevel.get(DEFAULT_LOG_LEVEL.upper(), logging.DEBUG)
    except (AttributeError, TypeError):
        level = logging.DEBUG

    logger = logging.getLogger(name)
  
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler with same level
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # File handler with rotation
        fh = RotatingFileHandler(
            log_file,
            mode='a',
            encoding='utf-8'
        )
        fh.setLevel(level)

        # Use same formatter for both handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        # Log initial configuration
        logger.debug(f"Logger configured: dir='{DEFAULT_LOG_DIR}', level={logging.getLevelName(level)}")

    return logger
