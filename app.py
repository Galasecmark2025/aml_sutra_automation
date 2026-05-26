# app.py

from pywinauto.application import Application
import time, sys, os

from utilities.perform_actions import perform_actions
from utilities.setup_logger import setup_logger
from utilities.crypto_util import CryptoUtil
from utilities.get_config import get_config
from utilities.login import login

def get_base_path():
    """
    Returns:
      - read_path: where config/actions are read from
      - write_path: where logs/output are written
    """
    if getattr(sys, 'frozen', False):
        # EXE folder
        base_path = os.path.dirname(sys.executable)
    else:
        # SCRIPT folder
        base_path = os.path.dirname(os.path.abspath(__file__))

    return base_path, base_path

def wait_for_window(app, logger, timeout=30):
    """
    Wait for AML main window after login
    """
    start = time.time()

    while time.time() - start < timeout:
        try:
            windows = app.windows()

            for w in windows:
                title = w.window_text()

                logger.info(f"Detected Window: {title}")

                # Match AML main window
                if (
                    "AMLSutra" in title
                    and "TRAMLSutra" in title
                ):
                    logger.info(f"Matched Window: {title}")

                    return app.window(title_re=r".*AMLSutra.*TRAMLSutra.*")

        except Exception as e:
            logger.warning(f"Waiting for window: {e}")

        time.sleep(1)

    return None

def run():
    read_path, write_path = get_base_path()
    logger = setup_logger(write_path)
    config = get_config(read_path, logger=logger)
    if not config:
        logger.warning("Configuration reading failure")
        return
    exe_path = config.get("exe_path", "")
    if not exe_path:
        logger.warning("exe_path missing in config")
        return
    # app, window = connect_or_start_app(exe_path)
    logger.info("Opening new AMLSutra instance...")
    app = None
    window = None
    max_trials = 3

    for trial in range(1, max_trials + 1):
        window = None
        try:
            logger.info(f"Launching application (Attempt {trial}/{max_trials})")

            app = Application(backend="uia").start(exe_path)

            # Wait for app to initialize
            time.sleep(5)

            # Retry getting top window
            start = time.time()

            while time.time() - start < 20:
                try:
                    window = app.top_window()

                    if window.exists():
                        logger.info("Application window found")
                        break

                except Exception:
                    pass

                time.sleep(1)

            if window:
                break

            raise RuntimeError("No window detected")

        except Exception as e:
            logger.warning(f"Attempt {trial} failed: {str(e)}")

            # Kill broken process before retry
            try:
                if app:
                    app.kill()
            except Exception:
                pass

            time.sleep(3)

    # Final validation
    if not window:
        logger.error(f"Failed to launch application after {max_trials} attempts")
        return
    
    credentials = config.get("credential", {})
    username = credentials.get("username", "")
    password_encrypted = credentials.get("password", "")
    password_decrypted = CryptoUtil.decrypt(password_encrypted)

    window = app.window(title_re=r".*AMLSutra.*Login.*")
    window.wait("exists", timeout=30)
    logger.info(f"Current Window: {window.window_text()}")
    login(window, username, password_decrypted, logger)
    
    new_window = wait_for_window(app, logger)

    if not new_window:
        logger.error("AMLSutra window not found after login")
        return

    try:
        new_window.wait("exists", timeout=30)
        time.sleep(2)
        new_window.maximize()
        new_window.set_focus()

    except Exception as e:
        logger.error(f"Window preparation failed: {str(e)}")

    logger.info(f"Final Window: {new_window.window_text()}")
    
    actions_json = get_config(read_path, "actions.json", logger=logger)
    actions = actions_json.get("actions", [])
    print(f"Fetched action details: {actions}")
    if actions:
        perform_actions(new_window, actions, read_path, logger)
    
    time.sleep(2)
    try:
        if app:
            app.kill()
    except Exception as e:
        logger.error(f"Failed to close app: {str(e)}")

if __name__ == '__main__':
    run()