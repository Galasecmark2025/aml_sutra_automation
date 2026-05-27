# app.py

from pywinauto.application import Application
import time, sys, os

from utilities.connect_or_start_app import connect_or_start_app
from utilities.wait_for_window import wait_for_window
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
    
    use_fresh_instance = config.get("use_fresh_instance",False)
    
    logger.info("Checking AMLSutra instance...")

    try:
        app, window, already_running = (
            connect_or_start_app(exe_path,logger,max_trials=3,force_new=use_fresh_instance))

    except Exception as e:
        logger.error(f"Failed to start/connect AMLSutra: {str(e)}")
        return
    
    credentials = config.get("credential", {})
    username = credentials.get("username", "")
    password_encrypted = credentials.get("password", "")
    password_decrypted = CryptoUtil.decrypt(password_encrypted)

    if already_running:
        logger.info("Existing AMLSutra instance detected")

        # Re-fetch as WindowSpecification
        new_window = app.window(title=window.window_text())

    else:
        logger.info("Fresh AMLSutra instance started")

        login_window = app.window(title_re=r".*AMLSutra.*Login.*")

        login_window.wait("ready",timeout=30)

        logger.info(f"Current Window: {login_window.window_text()}")

        login(login_window,username,password_decrypted,logger)

        new_window = wait_for_window(app,logger)

        if not new_window:
            logger.error("AMLSutra window not found after login")
            return

    try:
        new_window.wait("ready", timeout=30)
        time.sleep(2)
        new_window.maximize()
        new_window.set_focus()

    except Exception as e:
        logger.error(f"Window preparation failed: {str(e)}")

    logger.info(f"Final Window: {new_window.window_text()}")
    
    actions_json = get_config(read_path, "actions.json", logger=logger)
    actions = actions_json.get("actions", [])
    print(f"Fetched action details: {actions}")
    error_screenshots_only = config.get("error_screenshots_only", True)
    if actions:
        perform_actions(new_window, actions, read_path, write_path, logger, error_screenshots_only)
    
    time.sleep(2)
    # try:
    #     if app and not already_running:
    #         logger.info("Closing AMLSutra instance")
    #         app.kill()            
    try:
        if app:
            logger.info("Closing AMLSutra instance")
            app.kill()

    except Exception as e:
        logger.error(f"Failed to close app: {str(e)}")


if __name__ == '__main__':
    run()