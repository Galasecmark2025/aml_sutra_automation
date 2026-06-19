def dump_controls(window, filename="controls_dump.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, c in enumerate(window.descendants()):
            try:
                f.write(
                    f"Index: {i}\n"
                    f"Text: {repr(c.window_text())}\n"
                    f"AutoID: {repr(c.element_info.automation_id)}\n"
                    f"ControlType: {repr(c.element_info.control_type)}\n"
                    f"{'-'*80}\n"
                )
            except Exception as e:
                f.write(f"Error reading control {i}: {e}\n")