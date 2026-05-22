import time 
from pywinauto.mouse import click

def mark_rows_by_process_ids(window_obj, process_all=False, process_ids=None, logger=None):
    try:
        process_ids = process_ids or []

        if process_all:
            mark_all_option = window_obj.child_window(
                title="Mark",
                auto_id="[Column Header] MyMark",
                control_type="HeaderItem"
            )

            rect = mark_all_option.rectangle()

            x = rect.right - 12
            y = rect.top + (rect.height() // 2)

            click(coords=(x, y))
            time.sleep(2)
            return

        elif process_ids:

            data_rows = window_obj.descendants(control_type="DataItem")

            logger.info(f"Total rows found: {len(data_rows)}")

            marked_count = 0

            for row_index, row in enumerate(data_rows):

                try:
                    proc_id = None

                    # FIND PROC ID IN ROW
                    edit_controls = row.descendants(control_type="Edit")

                    for edit in edit_controls:
                        try:
                            value = ""

                            try:
                                value = (edit.iface_value.CurrentValue)
                            except:
                                value = edit.window_text()

                            value = str(value).strip()

                            if value in process_ids:
                                proc_id = value
                                break

                        except:
                            pass

                    # MARK MATCHED ROW
                    if proc_id:

                        try:
                            checkboxes = row.descendants(control_type="CheckBox")

                            if not checkboxes:
                                logger.info(f"No checkbox found for {proc_id}")
                                continue

                            checkbox = checkboxes[0]

                            try:
                                toggle_state = (checkbox.get_toggle_state())
                            except:
                                toggle_state = 0

                            if toggle_state == 0:
                                checkbox.click_input()
                                time.sleep(0.3)

                            marked_count += 1

                            logger.info(f"Marked Proc ID: {proc_id}")

                        except Exception as e:
                            logger.warning(f"Checkbox failed for {proc_id}: {e}")

                except Exception as e:
                    logger.warning(f"Row {row_index} failed: {e}")

            logger.info(f"Total marked rows: {marked_count}")   
    except Exception as e:
        logger.warning(f"Error occurred while row marking: {e}")