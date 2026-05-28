# perform_actions.py

from pywinauto.keyboard import send_keys
import time

from utilities.trade_summary_processing import trade_summary_processing
from utilities.mark_rows_by_process_ids import mark_rows_by_process_ids
from utilities.validate_processed_data import validate_processed_data
from utilities.fetch_dropdown_value import fetch_dropdown_value
from utilities.close_opened_window import close_opened_window
from utilities.fetch_company_list import fetch_company_list
from utilities.capture_screenshot import capture_screenshot
from utilities.fetch_table_data import fetch_table_data

def perform_actions(window, actions, read_path, write_path, logger, error_screenshots_only=True):
    for action in actions:
        window.click_input(coords=(200, 10))
        time.sleep(0.5)
        main_menu = action.get("main_menu", "")
        sub_menu = action.get("sub_menu", "")
        company = action.get("company", "")
        proc_type = action.get("proc_type", "")
        proc_ids = action.get("proc_ids")
        date = action.get("date")
        
        if not all((main_menu, sub_menu, company, proc_type)):
            logger.warning(f"Required fields are missing: One of the 'main_menu', 'sub_menu', 'company', 'proc_type'")
            # return
            continue
        
        main_menu_btn = window.child_window(
            title=main_menu,
            control_type="MenuItem"
        )
        time.sleep(0.5)
        main_menu_btn.click_input()
        time.sleep(1)
        sub_menu_btn = window.child_window(
            title=sub_menu,
            control_type="MenuItem"
        )
        time.sleep(0.5)
        sub_menu_btn.click_input()
        time.sleep(1)
            
        company_list = fetch_company_list(window, logger)
        logger.info(f"Found companies: {company_list}")
        fetch_dropdown_value(window, "popCBECode", "ComboBox", company, logger)
        if proc_type:
            fetch_dropdown_value(window, "popProcType", "ComboBox", proc_type, logger)
        if date:
            fetch_dropdown_value(window, "boxDate", "Group", date, logger)
        process_ids = fetch_table_data(window, column_list=["Proc ID"], logger=logger)
        table_process_ids_list = [p_data["Proc ID"] for p_data in process_ids if p_data.get("Proc ID")] 
        logger.info(f"Table Process IDs: {table_process_ids_list}")
        process_all = False
        if proc_ids is None:
            process_all = True
        config_process_ids_list = []
        if proc_ids:
            config_process_ids_list = [
                str(pid)
                for pid in proc_ids
                if str(pid)
                in table_process_ids_list
            ]
        if process_all:
            mark_rows_by_process_ids(window, process_all=True, logger=logger)
        elif config_process_ids_list:    
            logger.info(f"IDs to process: {config_process_ids_list}")
            mark_rows_by_process_ids(window, process_ids=config_process_ids_list, logger=logger)
        post_process_table_data = trade_summary_processing(window, read_path, logger)
        logger.info(f"Post process table data: {post_process_table_data}")
        if config_process_ids_list:
            is_processed = validate_processed_data(post_process_table_data, config_process_ids_list, logger)
        else:
            is_processed = validate_processed_data(post_process_table_data, table_process_ids_list, logger)
            
        if not is_processed:
            logger.warning(f"Process failure")
        else: 
            logger.info("Action performed successfully")
            if not error_screenshots_only:
                capture_screenshot(write_path, logger)
            
        try:
            close_opened_window(window, logger)
        except:
            send_keys("{ESC}")