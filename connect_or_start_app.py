from pywinauto.application import Application
import time

def connect_or_start_app(exe_path, window_title="AMLSutra"):
    try:
        # Try connecting to already running app
        app = Application(backend="uia").connect(
            title_re=f".*{window_title}.*",
            timeout=5
        )

        window = app.top_window()

        # Restore if minimized
        try:
            if not window.is_maximized():
                window.restore()
                window.maximize()
        except Exception:
            pass

        # Bring window to front
        window.set_focus()

        print("Connected to already running application")
        return app, window

    except Exception:
        print("Application not running. Starting new instance...")

        app = Application(backend="uia").start(exe_path)

        time.sleep(3)

        window = app.top_window()
        window.maximize()
        window.set_focus()

        return app, window