from pynput import mouse


def start_mouse_listener(on_right_click_callback):
    """
    Starts a background thread listening for right clicks globally.
    Calls `on_right_click_callback` when a right click occurs.
    """

    def on_click(x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            on_right_click_callback()

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    return listener
