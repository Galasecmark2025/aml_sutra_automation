def fetch_proc_type_list(window, logger):
    try:
        # FETCH COMBOBOX
        company_combo = window.child_window(
            auto_id="popProcType",
            control_type="ComboBox"
        )
        # FETCH ALL LIST ITEMS INSIDE COMBOBOX
        list_items = company_combo.descendants(
            control_type="ListItem"
        )

        logger.info(f"Total List Items: {len(list_items)}")
        
        company_list = []

        # ITERATE OVER ITEMS
        for index, item in enumerate(list_items):
            data = {}
            try:
                title = item.window_text()

                data["index"] = index
                data["title"] = title
                
                company_list.append(data)

            except Exception as e:
                logger.warning(f"Error reading item {index}: {e}")
        return company_list
    except Exception as e:
        logger.warning(f"Error occurred while fetching process list: {e}")