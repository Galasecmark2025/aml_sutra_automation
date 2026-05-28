# validate_processed_data.py

def validate_processed_data(post_process_table_data, config_process_ids_list, logger):
    if not post_process_table_data:
        logger.info("No post process data found")
        return False
    process_success = True
    for row in post_process_table_data:
        proc_id = row.get("Proc ID", "")
        status_raw = row.get("Status")
        status = ("" if status_raw is None else str(status_raw).strip().lower())
        if (proc_id in config_process_ids_list) and (status != "finished"):
            logger.error(f"Process ID: {proc_id}, Status: {status}")
            process_success = False
    return process_success