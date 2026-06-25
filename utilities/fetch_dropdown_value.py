# from pywinauto.keyboard import send_keys
# import time


# def fetch_dropdown_value(window, dropdown_auto_id, control_type, value, logger):
#     try:
#         target = str(value).strip()

#         logger.info(
#             f"Searching control: auto_id='{dropdown_auto_id}', "
#             f"control_type='{control_type}', "
#             f"value='{target}'"
#         )

#         combobox = window.child_window(
#             auto_id=dropdown_auto_id,
#             control_type=control_type
#         )

#         combobox.wait("exists ready visible", timeout=10)

#         try:
#             combobox.click_input()
#         except Exception:
#             pass

#         time.sleep(0.2)

#         try:
#             editor = combobox.child_window(
#                 auto_id="[Editor]",
#                 control_type="Edit"
#             )

#             editor.click_input()
#             time.sleep(0.3)

#             send_keys("^a")
#             time.sleep(0.3)

#             send_keys("{BACKSPACE}")
#             time.sleep(0.3)

#             send_keys(target, with_spaces=True)
#             time.sleep(0.3)

#             send_keys("{ENTER}")
#             # time.sleep(0.2)

#             logger.info(f"Selected value: {target}")
#             return True

#         except Exception as e:
#             logger.warning(f"Editor selection failed: {e}")

#         try:
#             dropdown_btn = combobox.child_window(
#                 auto_id="[Editor] dropdown button",
#                 control_type="Button"
#             )

#             dropdown_btn.click_input()
#             time.sleep(0.3)

#             send_keys(target, with_spaces=True)
#             time.sleep(0.3)

#             send_keys("{ENTER}")
#             time.sleep(0.3)

#             logger.info(f"Selected value via dropdown: {target}")
#             return True

#         except Exception as e:
#             logger.warning(f"Dropdown selection failed: {e}")

#         logger.error(f"Failed selecting value: {target}")
#         return False

#     except Exception:
#         logger.exception(
#             f"Error locating control "
#             f"(auto_id={dropdown_auto_id}, control_type={control_type})"
#         )
#         return False

# fetch_dropdown_value.py

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

        # Special handling for date field
        if dropdown_auto_id == "boxDate":
            try:
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

                    logger.info(f"Selected date: {target}")
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

                    logger.info(f"Selected date via dropdown: {target}")
                    return True

                except Exception as e:
                    logger.warning(f"Dropdown selection failed: {e}")

                logger.error(f"Failed selecting date: {target}")
                return False

            except Exception as e:
                logger.warning(f"Date selection failed: {e}")
                return False

        # Handle dropdowns using list items
        list_items = combobox.descendants(control_type="ListItem")

        if not list_items:
            logger.error(
                f"No list items found for '{dropdown_auto_id}'"
            )
            return False

        target_index = None

        for index, item in enumerate(list_items):
            if item.window_text().strip() == target:
                target_index = index
                break

        if target_index is None:
            logger.error(
                f"Value '{target}' not found in '{dropdown_auto_id}'"
            )
            return False

        combobox.click_input()
        time.sleep(0.1)

        send_keys("{HOME}")

        if target_index > 0:
            send_keys(f"{{DOWN {target_index}}}")

        send_keys("{ENTER}")

        logger.info(
            f"Selected value '{target}' "
            f"(index={target_index})"
        )

        return True

    except Exception:
        logger.exception(
            f"Error locating control "
            f"(auto_id={dropdown_auto_id}, control_type={control_type})"
        )
        return False