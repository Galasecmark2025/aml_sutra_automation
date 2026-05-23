import time
from utilities.fetch_table_data import fetch_table_data
from utilities.get_config import get_config


def handle_error_window(window, error_bypass, logger):
    """
    Continuously checks and handles error/save dialog.
    Returns True if dialog was found.
    """
    try:
        dialogs = window.descendants(control_type="Window")

        for dialog in dialogs:
            try:
                title = dialog.window_text().strip().lower()

                if "save" in title:
                    logger.warning(f"Error window opened: {title}")

                    button_title = ("OK" if error_bypass else "Close")

                    buttons = dialog.descendants(title=button_title, control_type="Button")

                    if buttons:
                        buttons[0].click_input()

                        action = ("Bypassing" if error_bypass else "Closing")

                        logger.warning(f"{action} error window.")

                    return True

            except Exception:
                continue

    except Exception as e:
        logger.warning(f"Error dialog handling failed: {e}")

    return False


def trade_summary_processing(window, read_path, logger):
    error_bypass = get_config(read_path,"actions.json",value="error_bypass",logger=logger)

    max_trials = get_config(read_path,value="number_of_trials",logger=logger) or 10

    waittime = get_config(read_path,value="waittime(seconds)",logger=logger) or 5

    process_doc_option = window.child_window(
        title="Process",
        auto_id="[Toolbar : Process Tools] Tool : PR01 - Index : 0 ",
        control_type="Button"
    )

    process_doc_option.click_input()

    logger.info("Process button clicked.")

    last_table_data = []

    for trial in range(max_trials):

        # CHECK ERROR WINDOW EVERY LOOP
        handle_error_window(window,error_bypass,logger)

        try:
            table_data = fetch_table_data(window,"DataItem",["Proc ID", "Status"],logger=logger)

            last_table_data = table_data

            processing_found = False

            for row in table_data:
                proc_id = row.get("Proc ID","")

                status_raw = row.get("Status")

                status = (
                    ""
                    if status_raw is None
                    else str(status_raw)
                    .strip()
                    .lower()
                )

                if (status and "processing" in status):
                    processing_found = True

                    logger.info(f"Trial {trial + 1}/{max_trials} | Proc ID: {proc_id} | Status: {status}")

            # ALL FINISHED
            if not processing_found:
                logger.info("Processing completed.")
                return table_data

        except Exception as e:
            logger.warning(f"Status fetch error: {e}")

        # WAIT BEFORE NEXT CHECK
        time.sleep(waittime)

    logger.warning("Process took longer than expected.")

    return last_table_data