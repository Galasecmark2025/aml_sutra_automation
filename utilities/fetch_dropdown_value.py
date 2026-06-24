from pywinauto.keyboard import send_keys
import time


def fetch_dropdown_value(window, dropdown_auto_id, control_type, value, logger):
    try:
        target = str(value).strip()

        logger.info(
            f"Searching control: auto_id='{dropdown_auto_id}', "
            f"control_type='{control_type}', "
            f"value='{target}'"
        )

        combobox = window.child_window(
            auto_id=dropdown_auto_id,
            control_type=control_type
        )

        combobox.wait("exists ready visible", timeout=10)

        try:
            combobox.click_input()
        except Exception:
            pass

        time.sleep(0.2)

        try:
            editor = combobox.child_window(
                auto_id="[Editor]",
                control_type="Edit"
            )

            editor.click_input()
            time.sleep(0.3)

            send_keys("^a")
            time.sleep(0.3)

            send_keys("{BACKSPACE}")
            time.sleep(0.3)

            send_keys(target, with_spaces=True)
            time.sleep(0.3)

            send_keys("{ENTER}")
            # time.sleep(0.2)

            logger.info(f"Selected value: {target}")
            return True

        except Exception as e:
            logger.warning(f"Editor selection failed: {e}")

        try:
            dropdown_btn = combobox.child_window(
                auto_id="[Editor] dropdown button",
                control_type="Button"
            )

            dropdown_btn.click_input()
            time.sleep(0.3)

            send_keys(target, with_spaces=True)
            time.sleep(0.3)

            send_keys("{ENTER}")
            time.sleep(0.3)

            logger.info(f"Selected value via dropdown: {target}")
            return True

        except Exception as e:
            logger.warning(f"Dropdown selection failed: {e}")

        logger.error(f"Failed selecting value: {target}")
        return False

    except Exception:
        logger.exception(
            f"Error locating control "
            f"(auto_id={dropdown_auto_id}, control_type={control_type})"
        )
        return False