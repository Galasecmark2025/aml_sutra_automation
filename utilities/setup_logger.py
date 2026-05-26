import logging
import os
from datetime import datetime
from PIL import ImageGrab


class ScreenshotOnErrorHandler(logging.Handler):
    """
    Automatically captures screenshot
    whenever ERROR or CRITICAL log occurs
    """

    def __init__(self, screenshot_dir):
        super().__init__()
        self.screenshot_dir = screenshot_dir

    def emit(self, record):
        try:
            # Only capture for ERROR+
            if record.levelno >= logging.ERROR:

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                screenshot_path = os.path.join(self.screenshot_dir,f"error_{timestamp}.png")

                screenshot = ImageGrab.grab()
                screenshot.save(screenshot_path)

        except Exception:
            # Prevent logger crash
            pass


def setup_logger(write_path):
    logger = logging.getLogger("trade_processor")

    try:
        # Create logs folder
        log_dir = os.path.join(write_path,"logs")

        os.makedirs(log_dir,exist_ok=True)

        # Create screenshots folder
        screenshot_dir = os.path.join(log_dir,"screenshots")

        os.makedirs(screenshot_dir,exist_ok=True)

        # Timestamp for log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        log_file = os.path.join(log_dir,f"app_{timestamp}.log")

        # Avoid duplicate logs
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        # File logger
        file_handler = logging.FileHandler(log_file,encoding="utf-8")

        file_handler.setFormatter(formatter)

        # Console logger
        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        # Screenshot handler
        screenshot_handler = (ScreenshotOnErrorHandler(screenshot_dir))

        screenshot_handler.setLevel(logging.ERROR)

        # Add handlers
        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        logger.addHandler(screenshot_handler)

        logger.info(f"Logger started: {log_file}")

        return logger

    except Exception as e:
        print(f"Logger setup failed: {e}")
        return logger