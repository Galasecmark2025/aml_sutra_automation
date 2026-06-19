# from pywinauto.keyboard import send_keys
# import time

# def fetch_dropdown_value(window, dropdown_auto_id, control_type, value, logger):
#     try:
#         combobox = window.child_window(
#             auto_id=dropdown_auto_id,
#             control_type=control_type
#         )
#         dropdown_btn = combobox.child_window(
#             auto_id="[Editor] dropdown button",
#             control_type="Button"
#         )
        
#         dropdown_btn.click_input()
#         time.sleep(1)
        
#         send_keys(value)
#         time.sleep(0.5)

#         # PRESS ENTER
#         send_keys("{ENTER}")
#         time.sleep(0.5)
#     except Exception as e:
#         logger.error(f"Error occurred while fetching dropdown: {e}")

from pywinauto.keyboard import send_keys
import time

def fetch_dropdown_value(window, dropdown_auto_id, control_type, value, logger):
    try:
        # logger.info(
        #     f"Searching control: auto_id='{dropdown_auto_id}', "
        #     f"control_type='{control_type}'"
        # )

        combobox = window.child_window(
            auto_id=dropdown_auto_id,
            control_type=control_type
        )

        # combobox.wait("exists ready visible", timeout=10)

        # logger.info(
        #     f"Found control: "
        #     f"title='{combobox.window_text()}', "
        #     f"auto_id='{combobox.element_info.automation_id}', "
        #     f"type='{combobox.element_info.control_type}'"
        # )

        dropdown_btn = combobox.child_window(
            auto_id="[Editor] dropdown button",
            control_type="Button"
        )

        # logger.info(
        #     f"Found dropdown button: "
        #     f"auto_id='{dropdown_btn.element_info.automation_id}'"
        # )

        dropdown_btn.click_input()
        time.sleep(1)

        send_keys(value)
        time.sleep(0.5)

        send_keys("{ENTER}")
        time.sleep(0.5)

    except Exception as e:
        logger.exception(
            f"Error locating dropdown "
            f"(auto_id={dropdown_auto_id}, control_type={control_type})"
        )