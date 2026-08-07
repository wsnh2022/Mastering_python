from ahk import AHK

ahk = AHK(executable_path=r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe")

# ================
# for win in ahk.list_windows():
#     print(win.title)

# ================
# ahk.win_activate("Untitled - Notepad4")
# time.sleep(1)
# ahk.win_activate("*testcases.txt - Notepad")

# ================
# ahk.mouse_move(
#     x=100, y=100, blocking=True
# )  # Blocks until mouse finishes moving (the default)

# ahk.mouse_move(
#     x=150, y=150, speed=10, blocking=True
# )  # Moves the mouse to x, y taking 'speed' seconds to move


# print(ahk.mouse_position)  #  (150, 150)


# # ===== Launch Notepad
# ahk.run_script("notepad.exe")
# time.sleep(1)
# # Type into the active window
# ahk.send("This is Python running AutoHotkey version 2.")

# ===== create menu
# ahk.run_script("""
# myMenu := Menu()

# myMenu.Add("Hello", (*) => MsgBox("Hello from AHK"))
# myMenu.Add("Exit", (*) => ExitApp())

# myMenu.Show()
# """)

# ==============
# ==============
# import keyboard

# keyboard.wait("ctrl+space")

# print("Pressed!")

# ==============
import keyboard
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QMenu


class MenuController(QObject):
    show_menu = Signal()

    def __init__(self):
        super().__init__()

        self.menu = QMenu()
        self.menu.addAction("Open")
        self.menu.addAction("Settings")
        self.menu.addSeparator()
        self.menu.addAction("Exit")

        self.show_menu.connect(self.popup)

    def popup(self):
        self.menu.popup(QCursor.pos())


app = QApplication([])

controller = MenuController()

keyboard.add_hotkey("Rclick", controller.show_menu.emit)

app.exec()
