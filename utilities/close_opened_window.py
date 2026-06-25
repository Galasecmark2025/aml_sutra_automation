# close_opened_window.py

def close_opened_window(dialog_window, logger):
    try:
        process_btn = dialog_window.child_window(
            title="Process",
            control_type="Button"
        ).wrapper_object()

        siblings = process_btn.parent().children()

        for ctrl in siblings:
            if (
                ctrl.element_info.control_type == "Button"
                and ctrl.window_text() == "Close"
                and ctrl.is_visible()
                and ctrl.is_enabled()
            ):
                logger.info("Clicking Close button")
                ctrl.click_input()
                return

        logger.warning("Close button not found")

    except Exception as e:
        logger.warning(f"Error occurred while closing window: {e}")