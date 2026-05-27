# wait_for_window.py

import re, time

def wait_for_window(app, logger, timeout=30):
    """
    Wait for AML main window after login
    """
    pattern = r"^AMLSutra\s*\(([\d\.]+)\)\s*:\s*([^\[]+)\[([^\]]+)\]$"
    start = time.time()

    while time.time() - start < timeout:
        try:
            windows = app.windows()

            for w in windows:
                title = w.window_text()

                logger.info(f"Detected Window: {title}")

                # 1. STRICT PATTERN MATCH
                if re.match(pattern, title, re.IGNORECASE):
                    logger.info(f"Pattern matched window: {title}")
                    return app.window(title=title)

                # 2. FALLBACK: NOT LOGIN WINDOW
                if title and "login" not in title.lower():
                    logger.info(f"Fallback matched window: {title}")
                    return app.window(title=title)

        except Exception as e:
            logger.warning(f"Waiting for window: {e}")

        time.sleep(1)

    return None