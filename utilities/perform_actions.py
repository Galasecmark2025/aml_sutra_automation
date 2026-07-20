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
from utilities.db_operations import get_execution_dates
from utilities.dump_controls import dump_controls


def _resolve_global_execution_dates(config, actions_json, database_name, logger):
    """
    Resolve execution dates ONCE, globally, ONLY when both from_date and
    to_date are provided at the top level of actions_json.

    Returns:
      - list of dates, if global from_date + to_date are present.
      - None, if either global from_date or to_date is missing -> caller
        must fall back to per-action date resolution.
    """
    from_date = str(actions_json.get("from_date", "")).strip()
    to_date = str(actions_json.get("to_date", "")).strip()

    if from_date and to_date:
        bkmcode = actions_json.get("bkmcode")
        execution_dates = get_execution_dates(
            config=config,
            bkmcode=bkmcode,
            database_name=database_name,
            range_required=True,
            from_date=from_date,
            to_date=to_date,
            logger=logger
        )
        logger.info(f"Global date range resolved: {execution_dates}")
        return execution_dates

    logger.info("Global from_date/to_date not fully provided. Falling back to per-action date resolution.")
    return None


def _resolve_single_action_date(action, config, database_name, logger):
    """
    Per-action date resolution, used when global from_date/to_date is not
    (fully) provided.

    Priority:
      1. Action's own "date" field.
      2. Fetch date from query using the action's bkmcode.
    """
    date = str(action.get("date", "")).strip()
    bkmcode = action.get("bkmcode")

    if date:
        logger.info(f"Using action-level date: '{date}'")
        return [date]

    logger.info("Date not provided for action. Fetching from PTRADE.")
    if not bkmcode:
        logger.warning("bkmcode configuration required if not using date explicitly")
        return []

    fetched_date = get_execution_dates(config=config, bkmcode=bkmcode, database_name=database_name, logger=logger)
    logger.info(f"Date from query: '{fetched_date}'")
    if not fetched_date:
        logger.warning("Failed to read date from database.")
        return []

    return [fetched_date]


def _run_single_action(window, app, action, actions_json, date, read_path, write_path, logger, error_screenshots_only):
    """
    Runs a single action (one main_menu/sub_menu/company/proc_type combination)
    for a single, already-resolved execution date.
    """
    start_time = time.perf_counter()
    window = app.top_window()
    window.click_input(coords=(200, 10))
    time.sleep(0.5)

    main_menu = action.get("main_menu", "")
    sub_menu = action.get("sub_menu", "")
    company = action.get("company", "")
    proc_type = action.get("proc_type", "")
    proc_ids = action.get("proc_ids")

    if not all((main_menu, sub_menu, company, proc_type)):
        logger.warning("Required fields are missing: One of the 'main_menu', 'sub_menu', 'company', 'proc_type'")
        return

    type_selection = actions_json.get("selection_type", {}).get(sub_menu, "")
    logger.info(f"sub_menu = '{sub_menu}'")
    logger.info(f"type_selection = '{type_selection}'")
    logger.info(f"Processing execution date: {date}")

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
    # dump_controls(window, "controls_for_closing.txt")

    dialog_window = app.top_window()
    dialog_window.wait("ready", timeout=10)

    company_list = fetch_company_list(dialog_window, logger)
    logger.info(f"Found companies: {company_list}")
    fetch_dropdown_value(dialog_window, "popCBECode", "ComboBox", company, logger)
    if proc_type:
        fetch_dropdown_value(dialog_window, type_selection, "ComboBox", proc_type, logger)

    if date:
        fetch_dropdown_value(dialog_window, "boxDate", "Group", date, logger)

    process_ids = fetch_table_data(dialog_window, column_list=["Proc ID"], logger=logger)
    table_process_ids_list = [p_data["Proc ID"] for p_data in process_ids if p_data.get("Proc ID")]
    logger.info(f"Table Process IDs: {table_process_ids_list}")

    process_all = proc_ids is None
    config_process_ids_list = []
    if proc_ids:
        config_process_ids_list = [
            str(pid)
            for pid in proc_ids
            if str(pid) in table_process_ids_list
        ]

    if process_all:
        mark_rows_by_process_ids(dialog_window, process_all=True, logger=logger)
    elif config_process_ids_list:
        logger.info(f"IDs to process: {config_process_ids_list}")
        mark_rows_by_process_ids(dialog_window, process_ids=config_process_ids_list, logger=logger)

    post_process_table_data = trade_summary_processing(dialog_window, read_path, logger)
    logger.info(f"Post process table data: {post_process_table_data}")

    if config_process_ids_list:
        is_processed = validate_processed_data(post_process_table_data, config_process_ids_list, logger)
    else:
        is_processed = validate_processed_data(post_process_table_data, table_process_ids_list, logger)

    if not is_processed:
        logger.warning("Process failure")
    else:
        logger.info("Action performed successfully")
        if not error_screenshots_only:
            capture_screenshot(write_path, logger)

    try:
        close_opened_window(dialog_window, logger)
    except Exception as e:
        logger.warning(f"Close failed: {e}")
        send_keys("{ESC}")
    finally:
        elapsed_time = time.perf_counter() - start_time
        logger.info(f"Action '{sub_menu}' '{proc_type}' completed in {elapsed_time:.2f} seconds")


def perform_actions(window, config, actions_json, actions, read_path, write_path, database_name, logger, error_screenshots_only=True):
    if not database_name:
        logger.error("Database name required for fetching date, user is requested to update configurations")
        return

    app = window.app

    # Try to resolve a GLOBAL date range first (only when both from_date and
    # to_date are provided at the top level). If either is missing, this
    # returns None and we fall back to per-action date resolution below.
    global_execution_dates = _resolve_global_execution_dates(config, actions_json, database_name, logger)

    if global_execution_dates is not None:
        # Global range drives everything: date is the OUTER loop,
        # actions run in order (inner loop) for each date.
        if not global_execution_dates:
            logger.warning("No execution dates found from global range. Skipping all actions.")
            return

        logger.info(f"Global execution dates: {global_execution_dates}")
        for date in global_execution_dates:
            for action in actions:
                _run_single_action(
                    window, app, action, actions_json, date,
                    read_path, write_path, logger, error_screenshots_only
                )
    else:
        # Global from_date/to_date not (fully) provided:
        # for EACH action, check if it has its own "date" field;
        # if not, fetch the date from the query using that action's bkmcode.
        for action in actions:
            action_dates = _resolve_single_action_date(action, config, database_name, logger)
            if not action_dates:
                logger.warning("No execution dates found for action. Skipping action.")
                continue
            for date in action_dates:
                _run_single_action(
                    window, app, action, actions_json, date,
                    read_path, write_path, logger, error_screenshots_only
                )