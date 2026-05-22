import ujson as json
import time, os, sys

from utilities.connect_or_start_app import connect_or_start_app
from utilities.perform_actions import perform_actions
from utilities.setup_logger import setup_logger
from utilities.login import login

logger = setup_logger()
def get_config():
    with open("config.json", "r", encoding="utf-8") as fp:
        config = json.load(fp)
    return config if config else None

def get_actions_from_command():
    """
    Usage:
    python app.py actions.json
    """
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as fp:
                    data = json.load(fp)

                return data.get("actions", [])

            except Exception as e:
                logger.error(f"Failed to read action file: {e}")

        else:
            logger.error(f"File not found: {file_path}")

    return []

def run():
    config = get_config()
    if not config:
        logger.warning("Configuration reading failure")
        return
    exe_path = config.get("exe_path", "")
    if not exe_path:
        logger.warning("exe_path missing in config")
        return
    app, window = connect_or_start_app(exe_path)
    
    window_title = window.window_text()
    logger.info(f"Current Window: {window_title}")
    
    credentials = config.get("credential", "")
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    if "Login" in window_title:
        login(window, username, password, logger)

    new_window = app.window(title="AMLSutra (1.0.0) : PMLA [TRAMLSutra]")
    new_window.wait("exists enabled visible ready", timeout=30)
    # return

    new_window = app.top_window()
    logger.info(new_window.window_text())
    
    actions = get_actions_from_command()
    print(f"Fetched action details: {actions}")
    if actions:
        perform_actions(new_window, actions, logger)
        
    # return
    
    time.sleep(2)
    # close_exe(new_window)
    app.kill()

if __name__ == '__main__':
    run()