from pywinauto.mouse import click
from pywinauto.application import Application
import time
from pywinauto.keyboard import send_keys

def fetch_company_list(window):
    # FETCH COMBOBOX
    company_combo = window.child_window(
        auto_id="popCBECode",
        control_type="ComboBox"
    )
    # FETCH ALL LIST ITEMS INSIDE COMBOBOX
    list_items = company_combo.descendants(
        control_type="ListItem"
    )

    print(f"Total List Items: {len(list_items)}")
    
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
            print(f"Error reading item {index}: {e}")
    return company_list
    

def close_exe(window_obj):
    title_bar = window_obj.child_window(
        control_type="TitleBar"
    )

    close_btn = title_bar.child_window(
        title="Close",
        control_type="Button"
    )

    close_btn.click_input()

def fetch_table_data(window_obj, control_type):
    data_rows = window_obj.descendants(control_type=control_type)

    print(f"Total rows found: {len(data_rows)}")
    
    table_data = []

    for row_index, row in enumerate(data_rows):
        data = {}
        try:
            data["row"] = row_index
            status_value = None
            proc_id_value = None

            controls = row.descendants()

            for control in controls:

                try:

                    # auto_id = control.element_info.automation_id
                    control_type = control.element_info.control_type
                    title = control.window_text()

                    # STATUS
                    if title == "Status" and control_type == "Edit":

                        try:
                            status_value = control.iface_value.CurrentValue
                        except:
                            status_value = control.window_text()
                        data["status"] = status_value

                    # PROC ID
                    elif title == "Proc ID" and control_type == "Edit":

                        try:
                            proc_id_value = control.iface_value.CurrentValue
                        except:
                            proc_id_value = control.window_text()
                        data["proc_id"] = proc_id_value

                except:
                    pass
            table_data.append(data)
            

        except Exception as e:
            print(f"Error in row {row_index}: {e}")
    return table_data

def process_all(window):
    mark_all_option = window.child_window(
        title="Mark",
        auto_id="[Column Header] MyMark",
        control_type="HeaderItem"
    )

    rect = mark_all_option.rectangle()

    x = rect.right - 12
    y = rect.top + (rect.height() // 2)

    click(coords=(x, y))
    time.sleep(5)
    
    process_doc_option = window.child_window(
        title="Process",
        auto_id="[Toolbar : Process Tools] Tool : PR01 - Index : 0 ",
        control_type="Button"
    )
    process_doc_option.click_input()
    time.sleep(5)
    
    # new_window = app.top_window()
    # new_window.print_control_identifiers(filename="controls_new.txt")
    
    table_data = fetch_table_data(window, "DataItem")
    print(table_data)

def run():
    app = Application(backend="uia").start(r"D:\DB&Exc\TRAMLSUTRA_15052026\AMLSutra.exe")

    time.sleep(3)

    window = app.top_window()

    # Click Login
    login_btn = window.child_window(
        title="Login",
        auto_id="cmdOK",
        control_type="Button"
    )

    login_btn.click_input()

    # wait for next screen
    time.sleep(5)

    # IMPORTANT: re-fetch window
    new_window = app.top_window()

    print(new_window.window_text())

    process_menu = new_window.child_window(
        title="Process",
        auto_id="[MainMenu : MainMenu Tools] Tool : 3904000000 - Index : 3 ",
        control_type="MenuItem"
    )
    process_menu.click_input()
    time.sleep(3)
    
    alert_option = new_window.child_window(
        title="Alert Generation",
        auto_id="[Process Items] Menu Item :  - Index : 0 ",
        control_type="MenuItem"
    )
    alert_option.click_input()
    time.sleep(3)
    
    company_list = fetch_company_list(new_window)
    print(company_list)
    
    company_combo = new_window.child_window(
        auto_id="popCBECode",
        control_type="ComboBox"
    )
    dropdown_btn = company_combo.child_window(
        auto_id="[Editor] dropdown button",
        control_type="Button"
    )
    
    for company_row in company_list:
        title = company_row.get("title", "")
        
        dropdown_btn.click_input()

        time.sleep(1)
        
        send_keys(title)
        
        time.sleep(1)

        # PRESS ENTER
        send_keys("{ENTER}")
        
        time.sleep(2)
        
        selected = company_combo.window_text()

        print(f"Selected UI Value: {selected}")
        # SEARCH FROM WINDOW, NOT COMBOBOX
        # company_option = new_window.child_window(
        #     title=title,
        #     control_type="ListItem"
        # )

        # company_option.wait("ready", timeout=5)

        # print(f"Selecting: {title}")

        # company_option.click_input()
        
        print(f'Processing: {title}')
        process_all(new_window)
    
    time.sleep(10)
    # close_exe(new_window)
    app.kill()

if __name__ == '__main__':
    run()