from pynput import keyboard


def start_keyboard_listener(on_hotkey_callback):
    """
    Starts a background thread listening for Ctrl+Shift+C.
    """

    def on_activate():
        on_hotkey_callback()

    hotkey = keyboard.GlobalHotKeys({"<ctrl>+<shift>+c": on_activate})
    hotkey.start()
    return hotkey
