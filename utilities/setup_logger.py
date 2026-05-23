import logging
import os
from datetime import datetime


def setup_logger(write_path):
    try:
        log_dir = os.path.join(write_path, "logs")
        os.makedirs(log_dir, exist_ok=True)

        # TIMESTAMP FILE NAME
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        log_file = os.path.join(log_dir,f"app_{timestamp}.log")

        logger = logging.getLogger("trade_processor")

        # AVOID DUPLICATE LOGS
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        # FILE LOGGER
        file_handler = logging.FileHandler(log_file,encoding="utf-8")
        file_handler.setFormatter(formatter)

        # CONSOLE LOGGER
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info(f"Logger started: {log_file}")

        return logger
    except Exception as e:
        logger.warning(f"Error occurred while setting up logger: {e}")