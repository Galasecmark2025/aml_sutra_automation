def close_opened_window(window):
    close_btn = window.child_window(
        title="Close",
        auto_id="[Toolbar : Process Tools] Tool : PR99 - Index : 3 ",
        control_type="Button"
    )

    close_btn.click_input()