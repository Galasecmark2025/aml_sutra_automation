# connect_or_start_app.py

from pywinauto.application import Application
import time
import re


def connect_or_start_app(exe_path,window_pattern=r"^AMLSutra\s*\(([\d\.]+)\)\s*:\s*([^\[]+)\[([^\]]+)\]$", logger=None,max_trials=3, force_new=False):
    """
    Connect to running AMLSutra instance.
    If not running, start new instance.

    Returns:
        app
        window
        already_running (bool)
    """

    pattern = window_pattern

    # ==================================
    # CONNECT TO EXISTING APP
    # ==================================
    if not force_new:
        try:
            app = Application(backend="uia").connect(title_re=r".*AMLSutra.*",timeout=5)

            windows = app.windows()

            for w in windows:
                title = w.window_text()

                logger and logger.info(f"Detected running window: {title}")

                # AML MAIN WINDOW
                if re.match(pattern,title,re.IGNORECASE):
                    logger and logger.info(f"Connected to AML window: {title}")

                    return (app,w,True)

                # LOGIN WINDOW
                if (title and "login" in title.lower()):
                    logger and logger.info(f"AML login window already open: {title}")

                    return (app,w,False)

        except Exception as e:
            logger and logger.info(f"No running AML instance found: {e}")

    # ==================================
    # START NEW INSTANCE
    # ==================================
    logger and logger.info("Starting new AMLSutra instance...")

    for trial in range(1,max_trials + 1):

        try:
            logger and logger.info(f"Launching application (Attempt {trial}/{max_trials})")

            app = Application(backend="uia").start(exe_path)

            time.sleep(5)

            start = time.time()

            while (time.time() - start < 20):

                windows = app.windows()

                for w in windows:
                    title = w.window_text()

                    logger and logger.info(f"Detected Window: {title}")

                    # LOGIN WINDOW
                    if (title and "login" in title.lower()):
                        logger and logger.info(f"Login window detected: {title}")

                        return (app,w,False)

                    # AML MAIN WINDOW
                    if re.match(pattern,title,re.IGNORECASE):
                        logger and logger.info(f"AML main window detected: {title}")

                        return (app,w,False)

                time.sleep(1)

            raise RuntimeError("No AML window detected")

        except Exception as e:
            logger and logger.warning(f"Attempt {trial} failed: {str(e)}")

            try:
                if app: app.kill()
            except Exception:
                pass

            time.sleep(3)

    raise RuntimeError(f"Failed to launch AMLSutra after {max_trials} attempts")