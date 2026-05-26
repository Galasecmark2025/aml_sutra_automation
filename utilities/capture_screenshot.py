import os
from datetime import datetime
from PIL import ImageGrab


def capture_screenshot(write_path, logger=None, prefix="screenshot"):
    """
    Capture full screen screenshot and save in:
    logs/screenshots/

    Args:
        write_path (str): Base project path
        logger: Logger object (optional)
        prefix (str): Filename prefix

    Returns:
        str: Saved screenshot path
    """

    try:
        # Create logs/screenshots folder
        screenshots_folder = os.path.join(
            write_path,
            "logs",
            "screenshots"
        )

        os.makedirs(
            screenshots_folder,
            exist_ok=True
        )

        # Timestamp
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # File name
        file_name = (
            f"{prefix}_{timestamp}.png"
        )

        screenshot_path = os.path.join(
            screenshots_folder,
            file_name
        )

        # Capture screen
        screenshot = ImageGrab.grab()

        # Save image
        screenshot.save(screenshot_path)

        if logger:
            logger.info(
                f"Screenshot saved: "
                f"{screenshot_path}"
            )

        return screenshot_path

    except Exception as e:
        if logger:
            logger.error(
                f"Screenshot capture failed: "
                f"{str(e)}"
            )

        return None