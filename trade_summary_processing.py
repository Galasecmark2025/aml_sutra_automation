import time
from fetch_table_data import fetch_table_data

def trade_summary_processing(window_obj, logger):
    process_doc_option = window_obj.child_window(
        title="Process",
        auto_id="[Toolbar : Process Tools] Tool : PR01 - Index : 0 ",
        control_type="Button"
    )
    process_doc_option.click_input()
    time.sleep(5)
    trial = 1
    for i in range(1, 4):
        processed = True
        table_data = fetch_table_data(window_obj, "DataItem", ["Proc ID", "Status"], logger=logger)
        
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
        elif (not processed) and trial == 3:
            logger.warning(f"Process took longer time than usual")
            return table_data