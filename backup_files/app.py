from pywinauto.mouse import click
from pywinauto.application import Application
import time


def run():
    app = Application(backend="uia").start(
        r"D:\DB&Exc\TRAMLSUTRA_15052026\AMLSutra.exe"
    )

    time.sleep(5)

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

    # print new controls
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
    time.sleep(5)
    new_window.print_control_identifiers(filename="controls.txt")
    # new_window.print_control_identifiers()
    # controls = new_window.descendants()

    # for i, c in enumerate(controls):
    #     try:
    #         print(
    #             f"Index: {i}\n"
    #             f"Title: {c.window_text()}\n"
    #             f"Auto ID: {c.element_info.automation_id}\n"
    #             f"Control Type: {c.friendly_class_name()}\n"
    #             f"{'-' * 50}"
    #         )
    #     except Exception as e:
    #         print(f"Error reading control {i}: {e}")
    mark_all_option = new_window.child_window(
        title="Mark",
        auto_id="[Column Header] MyMark",
        control_type="HeaderItem"
    )

    rect = mark_all_option.rectangle()

    x = rect.right - 12
    y = rect.top + (rect.height() // 2)

    click(coords=(x, y))
    # mark_all_option.click_input()
    time.sleep(5)
    process_doc_option = new_window.child_window(
        title="Process",
        auto_id="[Toolbar : Process Tools] Tool : PR01 - Index : 0 ",
        control_type="Button"
    )
    process_doc_option.click_input()
    time.sleep(5)


if __name__ == '__main__':
    run()