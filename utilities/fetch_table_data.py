def fetch_table_data(window_obj, control_type="DataItem", column_list=[], logger=None):
    try:
        data_rows = window_obj.descendants(control_type=control_type)

        logger.info(f"Total rows found: {len(data_rows)}")
        
        table_data = []

        for row_index, row in enumerate(data_rows):
            data = {}
            try:
                data["row"] = row_index

                controls = row.descendants()

                for control in controls:
                    try:
                        control_type = control.element_info.control_type
                        title = control.window_text()
                        
                        for col_title in column_list:
                            if title == col_title and control_type == "Edit":
                                try:
                                    fetched_value = control.iface_value.CurrentValue
                                except:
                                    fetched_value = control.window_text()
                                data[f"{col_title}"] = fetched_value if fetched_value else None

                    except:
                        pass
                if len(data) > 1:
                    table_data.append(data)
                

            except Exception as e:
                logger.error(f"Error in row {row_index}: {e}")
        return table_data
    except Exception as e:
        logger.error(f"Error occurred while fetching table data: {e}")