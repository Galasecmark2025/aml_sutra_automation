import time

def login(window, username, password, logger):
    try:
        # FETCH ALL EDIT FIELDS
        edit_controls = (window.descendants(control_type="Edit"))

        username_input = None
        password_input = None

        # FIND USERNAME & PASSWORD
        for edit in edit_controls:
            auto_id = (edit.element_info.automation_id)

            if (auto_id == "txtUserName"):
                username_input = edit

            elif (auto_id == "txtUserPassword"):
                password_input = edit

        # VALIDATE CONTROLS
        if not username_input:
            logger.warning("Username input not found")
            return False

        if not password_input:
            logger.warning("Password input not found")
            return False

        # ENTER USERNAME
        username_input.click_input()
        username_input.type_keys("^a{BACKSPACE}")
        time.sleep(0.5)
        username_input.type_keys(username,with_spaces=True, set_foreground=True)

        time.sleep(0.5)

        # ENTER PASSWORD
        password_input.click_input()
        password_input.type_keys("^a{BACKSPACE}")
        time.sleep(0.5)
        password_input.type_keys(password,with_spaces=True, set_foreground=True)

        time.sleep(0.5)

        # FIND LOGIN BUTTON
        login_button = None

        buttons = (window.descendants(control_type="Button"))

        for btn in buttons:
            try:
                if (btn.window_text().strip().lower() == "login"):
                    login_button = btn
                    break
            except:
                pass

        if not login_button:
            logger.warning("Login button not found")
            return False

        # CLICK LOGIN
        login_button.click_input()
        logger.info("Login button clicked")
        
        try:
            dialogs = (window.descendants(control_type="Window"))
            login_validation_window = None
            for dialog in dialogs:
                try:
                    title = dialog.window_text().strip().lower()
                    if title == "isac":
                        login_validation_window = dialog
                except:
                    pass
            if login_validation_window:
                yes_btns = login_validation_window.descendants(
                    title="Yes", 
                    control_type="Button"
                )
                yes_btns[0].click_input()
                logger.info("Trying to login even after logged in another device")
        except Exception as e:
            logger.warning(f"Login validation handling error: {e}")
        
        window.print_control_identifiers(filename="login_validation_controls.txt")

        return True

    except Exception as e:
        logger.warning(f"Login failed: {e}")
        return False