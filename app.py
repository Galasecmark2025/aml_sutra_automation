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
    app = Application(backend="uia").start(exe_path)
    window = app.top_window()
    window.maximize()
    window.set_focus()
    
    window_title = window.window_text()
    logger.info(f"Current Window: {window_title}")
    
    credentials = config.get("credential", {})
    username = credentials.get("username", "")
    password_encrypted = credentials.get("password", "")
    password_decrypted = CryptoUtil.decrypt(password_encrypted)
    if "Login" in window_title:
        login(window, username, password_decrypted, logger)

    new_window = app.window(title="AMLSutra (1.0.0) : PMLA [TRAMLSutra]")
    new_window.wait("exists enabled visible ready", timeout=30)
    # return

    new_window = app.top_window()
    logger.info(new_window.window_text())
    
    # actions = get_actions_from_command()
    actions_json = get_config(read_path, "actions.json", logger=logger)
    actions = actions_json.get("actions", [])
    print(f"Fetched action details: {actions}")
    if actions:
        perform_actions(new_window, actions, read_path, logger)
        
    # return
    
    time.sleep(2)
    # close_exe(new_window)
    app.kill()

if __name__ == '__main__':
    run()