from pywinauto.keyboard import send_keys
import time

def fetch_dropdown_value(window, dropdown_auto_id, control_type, value, logger):
    try:
        combobox = window.child_window(
            auto_id=dropdown_auto_id,
            control_type=control_type
        )
        dropdown_btn = combobox.child_window(
            auto_id="[Editor] dropdown button",
            control_type="Button"
        )
        time.sleep(1)
        
        dropdown_btn.click_input()
        time.sleep(1)
        
        send_keys(value)
        time.sleep(1)

        # PRESS ENTER
        send_keys("{ENTER}")
        time.sleep(2)
    except Exception as e:
        logger.warning(f"Error occurred while fetching dropdown: {e}")