from pywinauto.keyboard import send_keys
import ujson as json
import time

from trade_summary_processing import trade_summary_processing
from mark_rows_by_process_ids import mark_rows_by_process_ids
from validate_processed_data import validate_processed_data
from connect_or_start_app import connect_or_start_app
from close_opened_window import close_opened_window
from fetch_company_list import fetch_company_list
from fetch_table_data import fetch_table_data
from setup_logger import setup_logger
from login import login

logger = setup_logger()
def get_config():
    with open("config.json", "r", encoding="utf-8") as fp:
        config = json.load(fp)
    return config if config else None

def perform_actions(window, actions, logger):
    for action in actions:
        window.click_input(coords=(200, 10))
        time.sleep(0.5)
        main_menu = action.get("main_menu")
        sub_menu = action.get("sub_menu")
        company = action.get("company")
        proc_type = action.get("proc_type")
        proc_ids = action.get("proc_ids", None)
        date = action.get("date")
        
        main_menu_btn = window.child_window(
            title=main_menu,
            # auto_id="[MainMenu : MainMenu Tools] Tool : 3904000000 - Index : 3 ",
            control_type="MenuItem"
        )
        time.sleep(0.5)
        main_menu_btn.click_input()
        time.sleep(1)
        sub_menu_btn = window.child_window(
            title=sub_menu,
            # auto_id="[MainMenu : MainMenu Tools] Tool : 3904000000 - Index : 3 ",
            control_type="MenuItem"
        )
        time.sleep(0.5)
        sub_menu_btn.click_input()
        time.sleep(3)
            
        company_list = fetch_company_list(window, logger)
        logger.info(f"Found companies: {company_list}")
        
        company_combo = window.child_window(
            auto_id="popCBECode",
            control_type="ComboBox"
        )
        dropdown_btn = company_combo.child_window(
            auto_id="[Editor] dropdown button",
            control_type="Button"
        )
        time.sleep(1)

        title = company
        
        dropdown_btn.click_input()
        time.sleep(1)
        
        send_keys(title)
        time.sleep(1)

        # PRESS ENTER
        send_keys("{ENTER}")
        time.sleep(2)
        
        selected = company_combo.window_text()
        logger.info(f"Selected UI Value: {selected}")
        proc_type_combo = window.child_window(
            auto_id="popProcType",
            control_type="ComboBox"
        )
        proc_type_dropdown_btn = proc_type_combo.child_window(
            auto_id="[Editor] dropdown button",
            control_type="Button"
        )
        time.sleep(1)
        
        proc_type_dropdown_btn.click_input()
        time.sleep(1)
        
        send_keys(proc_type)
        time.sleep(1)

        # PRESS ENTER
        send_keys("{ENTER}")
        time.sleep(2)
        process_ids = fetch_table_data(window, column_list=["Proc ID"], logger=logger)
        table_process_ids_list = [p_data["Proc ID"] for p_data in process_ids if p_data.get("Proc ID")] 
        logger.info(f"Table Process IDs: {table_process_ids_list}")
        process_all = False
        if proc_ids is None:
            process_all = True
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
        post_process_table_data = trade_summary_processing(window, logger)
        logger.info(f"Post process table data: {post_process_table_data}")
        is_processed = validate_processed_data(post_process_table_data, config_process_ids_list, logger)
        if not is_processed:
            logger.warning(f"Process failure")
        try:
            close_opened_window(window)
        except:
            send_keys("{ESC}")
        
        

def run():
    config = get_config()
    if not config:
        logger.warning("Configuration reading failure")
        return
    exe_path = config.get("exe_path", "")
    if not exe_path:
        logger.warning("exe_path missing in config")
        return
    app, window = connect_or_start_app(exe_path)
    
    window_title = window.window_text()
    logger.info(f"Current Window: {window_title}")
    
    credentials = config.get("credential", "")
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    if "Login" in window_title:
        login(window, username, password, logger)

    time.sleep(5)
    # return

    new_window = app.top_window()
    logger.info(new_window.window_text())
    
    actions = config.get("actions", [])
    if actions:
        perform_actions(new_window, actions, logger)
        
    # return
    
    time.sleep(2)
    # close_exe(new_window)
    app.kill()

if __name__ == '__main__':
    run()