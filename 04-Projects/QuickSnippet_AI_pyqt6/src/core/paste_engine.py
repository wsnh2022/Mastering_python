import ctypes
import logging
import time

import pyperclip
from pynput.keyboard import Controller, Key

kb = Controller()
logger = logging.getLogger(__name__)

# Global snapshot memory for clipboard restoration
_clipboard_snapshot = ""


def safe_get_clipboard(retries=5, delay=0.1) -> str:
    for _ in range(retries):
        try:
            return pyperclip.paste()
        except (pyperclip.PyperclipException, OSError) as e:
            logger.warning(f"Clipboard paste failed: {e}")
            time.sleep(delay)
    return ""


def safe_set_clipboard(text: str, retries=5, delay=0.1):
    for _ in range(retries):
        try:
            pyperclip.copy(text)
            return
        except (pyperclip.PyperclipException, OSError) as e:
            logger.warning(f"Clipboard copy failed: {e}")
            time.sleep(delay)


def get_active_window_handle():
    """Returns the HWND of the currently focused window."""
    try:
        return ctypes.windll.user32.GetForegroundWindow()
    except (OSError, AttributeError) as e:
        logger.warning(f"Failed to get active window handle: {e}")
        return None


def set_active_window_handle(hwnd):
    """Brings the specified HWND back to the foreground."""
    if hwnd:
        try:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        except (OSError, AttributeError) as e:
            logger.warning(f"Failed to set active window handle: {e}")


def capture_selection() -> str:
    """
    Captures the currently selected text by simulating Ctrl+C
    and reading the clipboard. Returns the selected text or empty string.
    """
    global _clipboard_snapshot
    _clipboard_snapshot = safe_get_clipboard(retries=3, delay=0.05)

    safe_set_clipboard("", retries=3, delay=0.05)
    time.sleep(0.05)

    # Release potentially held keys from the hotkey combination
    kb.release(Key.shift)
    kb.release(Key.shift_l)
    kb.release(Key.shift_r)
    kb.release('c')
    kb.release('C')
    time.sleep(0.05)

    # Simulate Ctrl+C
    with kb.pressed(Key.ctrl):
        kb.press("c")
        kb.release("c")

    time.sleep(0.2)  # Wait for OS to populate clipboard

    selected_text = safe_get_clipboard(retries=5, delay=0.1)

    if not selected_text:
        if _clipboard_snapshot:
            safe_set_clipboard(_clipboard_snapshot, retries=3, delay=0.05)
        return ""

    # Restore original clipboard so the user doesn't lose what they had copied
    if _clipboard_snapshot:
        safe_set_clipboard(_clipboard_snapshot, retries=3, delay=0.05)

    return selected_text


def paste_text(text: str, auto_paste: bool, target_hwnd=None):
    """
    Copies text to clipboard and simulates Ctrl+V if auto_paste is True.
    Returns True if successful, False if focus restoration failed.
    """
    safe_set_clipboard(text, retries=5, delay=0.1)

    time.sleep(0.1)

    if auto_paste:
        if target_hwnd:
            current_hwnd = get_active_window_handle()
            if current_hwnd != target_hwnd:
                set_active_window_handle(target_hwnd)
                time.sleep(0.1)
                if get_active_window_handle() != target_hwnd:
                    return False  # Focus failed, caller should show fallback

        with kb.pressed(Key.ctrl):
            kb.press("v")
            kb.release("v")

        time.sleep(0.3)  # 150ms was too tight; give OS time to paste before restoring
        if _clipboard_snapshot:
            safe_set_clipboard(_clipboard_snapshot, retries=5, delay=0.1)

    return True
