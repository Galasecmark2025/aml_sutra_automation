# trade_summary_processing.py

import time
from utilities.fetch_table_data import fetch_table_data
from utilities.get_config import get_config

def trade_summary_processing(window, logger):
    error_bypass = get_config("actions.json", value="error_bypass")
    process_doc_option = window.child_window(
        title="Process",
        auto_id="[Toolbar : Process Tools] Tool : PR01 - Index : 0 ",
        control_type="Button"
    )
    process_doc_option.click_input()
    time.sleep(5)
    try:
        dialogs = (window.descendants(control_type="Window"))
        for dialog in dialogs:
            try:
                title = dialog.window_text().strip().lower()
                if "save" in title:
                    logger.info(f"Error window opened: {title}")
                    if error_bypass:
                        ok_btns = dialog.descendants(
                            title="OK", 
                            control_type="Button"
                        )
                        if ok_btns:
                            ok_btns[0].click_input()
                            logger.info("Bypassing error window.")
                    else:
                        close_btns = dialog.descendants(
                            title="Close", 
                            control_type="Button"
                        )
                        if close_btns:
                            close_btns[0].click_input()
                            logger.info("Closing error window.")
                        
            except:
                pass
    except Exception as e:
        logger.warning(f"Login validation handling error: {e}")
    # window.print_control_identifiers(filename="error_msg_controls.txt")
    trial = 1
    for i in range(1, 4):
        processed = True
        table_data = fetch_table_data(window, "DataItem", ["Proc ID", "Status"], logger=logger)
        
        for row in table_data:
            status_raw = row.get("Status")
            status = ("" if status_raw is None else str(status_raw).strip().lower())
            if status != "" and status != "finished":
                logger.warning(f'Trial {i}/3 Current status: {status} for {row.get("Proc ID", "")}, waiting for status update...')
                processed = False
                time.sleep(2)
            
        trial += 1
        if processed:
            return table_data
        elif (not processed) and trial == 4:
            logger.warning(f"Process took longer time than usual")
            return table_data