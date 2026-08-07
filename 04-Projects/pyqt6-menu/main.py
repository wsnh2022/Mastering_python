# horizotal row icons slide in right to left version 1

import sys
import time

# Import local configuration and settings GUI
from config_manager import load_config
from pynput import mouse
from pynput.keyboard import Controller, Key
from PyQt6.QtCore import (
    QEasingCurve,
    QObject,
    QPoint,
    QPropertyAnimation,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QStyle,
    QSystemTrayIcon,
    QWidget,
    QWidgetAction,
)
from settings_gui import SettingsWindow

print("use right click to see snippet insertion menu")

# Global keyboard controller for auto-pasting
kb = Controller()

# Global runtime configuration container
app_config = load_config()


# --- Interactive Edge Arrow Button Component ---
class EdgeArrowButton(QLabel):
    hovered_signal = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(14, 26)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                font-weight: bold;
                background: transparent;
                border-radius: 3px;
            }
            QLabel:hover {
                color: #ffffff;
                background-color: #333333;
            }
        """)

    def enterEvent(self, event):
        self.hovered_signal.emit()
        super().enterEvent(event)


# --- Sliding Snippet Row Component ---
class HoverOverlaySnippetRow(QWidget):
    ICONS_PER_PAGE = 5

    def __init__(
        self,
        title: str,
        snippet_data: dict,
        on_select_callback,
        parent_menu: QMenu,
        row_width: int = 230,
        reveal_delay_ms: int = 500,
        scroll_delay_ms: int = 300,
    ):
        super().__init__()
        self.on_select_callback = on_select_callback
        self.parent_menu = parent_menu
        self.ROW_WIDTH = row_width

        self.setFixedSize(self.ROW_WIDTH, 30)

        highlight_color = snippet_data.get("color", "#0078d4")
        hover_border = snippet_data.get("hover_border", "#2b88d8")
        versions = list(snippet_data.get("versions", {}).values())

        # Sliding Container: Page 0 (Text) | Page 1 (Icons 1-5) | Page 2 (Icons 6-10)
        self.slider_container = QWidget(self)
        self.slider_container.setGeometry(0, 0, self.ROW_WIDTH * 3, 30)

        slider_layout = QHBoxLayout(self.slider_container)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(0)

        # PAGE 0: Readable Text Title Page
        page_text = QWidget()
        page_text.setFixedSize(self.ROW_WIDTH, 30)
        text_layout = QHBoxLayout(page_text)
        text_layout.setContentsMargins(8, 0, 8, 0)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: 500;")
        text_layout.addWidget(title_label)
        text_layout.addStretch()
        slider_layout.addWidget(page_text)

        # PAGES 1 & 2: Icon Buttons (5 Per Page)
        all_icons = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")

        for page_idx in range(2):
            page_widget = QWidget()
            page_widget.setFixedSize(self.ROW_WIDTH, 30)
            page_layout = QHBoxLayout(page_widget)
            page_layout.setContentsMargins(16, 2, 16, 2)
            page_layout.setSpacing(2)

            for slot_idx in range(self.ICONS_PER_PAGE):
                item_idx = (page_idx * self.ICONS_PER_PAGE) + slot_idx
                has_snippet = item_idx < len(versions)
                icon_symbol = all_icons[item_idx] if item_idx < len(all_icons) else "•"

                btn = QPushButton(icon_symbol)
                btn.setProperty("class", "SnippetBtn")
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                btn.setFixedHeight(26)

                if has_snippet:
                    snippet_text = versions[item_idx]
                    btn.setToolTip(snippet_text[:50] + "...")
                    btn.setStyleSheet(f"""
                        QPushButton:hover {{
                            background-color: {highlight_color};
                            border: 1px solid {hover_border};
                        }}
                    """)
                    btn.clicked.connect(lambda _, t=snippet_text: self.handle_click(t))
                else:
                    btn.setEnabled(False)

                page_layout.addWidget(btn)

            slider_layout.addWidget(page_widget)

        # Floating Interactive Edge Arrows
        self.left_arrow = EdgeArrowButton("◀", self)
        self.left_arrow.move(1, 2)
        self.left_arrow.hide()

        self.right_arrow = EdgeArrowButton("▶", self)
        self.right_arrow.move(self.ROW_WIDTH - 15, 2)
        self.right_arrow.hide()

        # Arrow Repeat Timer
        self.arrow_scroll_timer = QTimer(self)
        self.arrow_scroll_timer.setInterval(scroll_delay_ms)
        self.scroll_direction = 0
        self.arrow_scroll_timer.timeout.connect(self.process_arrow_scroll)

        # Connect Arrow Hover Signals
        self.left_arrow.hovered_signal.connect(lambda: self.start_arrow_scroll(-1))
        self.right_arrow.hovered_signal.connect(lambda: self.start_arrow_scroll(1))

        # Smooth Horizontal Slide Animation Engine
        self.anim = QPropertyAnimation(self.slider_container, b"pos", self)
        self.anim.setDuration(220)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.current_page = 0

        # Auto-reveal Timer
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.setInterval(reveal_delay_ms)
        self.hover_timer.timeout.connect(lambda: self.slide_to_page(1))

    def start_arrow_scroll(self, direction: int):
        self.scroll_direction = direction
        self.process_arrow_scroll()
        self.arrow_scroll_timer.start()

    def process_arrow_scroll(self):
        new_page = self.current_page + self.scroll_direction
        if 1 <= new_page <= 2:
            self.slide_to_page(new_page)
        else:
            self.arrow_scroll_timer.stop()

    def update_arrow_visibility(self):
        if self.current_page == 0:
            self.left_arrow.hide()
            self.right_arrow.hide()
        elif self.current_page == 1:
            self.left_arrow.hide()
            self.right_arrow.show()
        elif self.current_page == 2:
            self.left_arrow.show()
            self.right_arrow.hide()

    def slide_to_page(self, page_index: int):
        page_index = max(0, min(page_index, 2))
        if self.current_page == page_index:
            return

        self.current_page = page_index
        target_x = -self.ROW_WIDTH * page_index

        self.anim.stop()
        self.anim.setStartValue(self.slider_container.pos())
        self.anim.setEndValue(QPoint(target_x, 0))
        self.anim.start()

        self.update_arrow_visibility()

    def enterEvent(self, event):
        self.hover_timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover_timer.stop()
        self.arrow_scroll_timer.stop()
        self.current_page = 0
        self.anim.stop()
        self.slider_container.move(0, 0)
        self.update_arrow_visibility()
        super().leaveEvent(event)

    def wheelEvent(self, event):
        self.hover_timer.stop()
        delta = event.angleDelta().y()
        if delta < 0:
            self.slide_to_page(self.current_page + 1)
        elif delta > 0:
            self.slide_to_page(self.current_page - 1)
        event.accept()

    def handle_click(self, text: str):
        self.parent_menu.close()
        self.on_select_callback(text)


# --- System Tray & Popup Application Core ---
class SnippetApp(QObject):
    show_menu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings_window = None

        # System Tray Icon Setup
        self.tray_icon = QSystemTrayIcon(self)
        # ✅ Fixed (Safe check for style instance)
        style = QApplication.style()
        if style is not None:
            self.tray_icon.setIcon(
                style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
            )

        # System Tray Context Menu
        tray_menu = QMenu()
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(self.open_settings)
        quit_action = QAction("❌ Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        tray_menu.addAction(settings_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Connect thread-safe signal for showing menu from pynput thread
        self.show_menu_signal.connect(self.show_menu)

    def open_settings(self):
        """Opens or brings the PyQt6 Settings Panel to the front."""
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
            self.settings_window.config_saved.connect(self.reload_config)

        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def reload_config(self):
        """Reloads config.json data when saved from the Settings GUI."""
        global app_config
        app_config = load_config()

    def show_menu(self):
        """Builds and opens the popup snippet menu dynamically from config.json."""
        # Always reload configuration to guarantee fresh data
        self.reload_config()

        menu = QMenu()
        settings = app_config.get("settings", {})

        menu_width = settings.get("menu_width_px", 230)
        reveal_delay = settings.get("auto_reveal_delay_ms", 500)
        scroll_delay = settings.get("arrow_scroll_delay_ms", 300)

        menu.setFixedWidth(menu_width)
        menu.setStyleSheet("""
            QMenu {
                background-color: #141414;
                border: 1px solid #2e2e2e;
                border-radius: 8px;
                padding: 4px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton.SnippetBtn {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                font-size: 16px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton.SnippetBtn:pressed {
                opacity: 0.8;
            }
            QPushButton.SnippetBtn:disabled {
                background-color: #1a1a1a;
                border: 1px solid #252525;
                opacity: 0.15;
            }
        """)

        snippets = app_config.get("snippets", {})
        for title, snippet_data in snippets.items():
            action = QWidgetAction(menu)
            row = HoverOverlaySnippetRow(
                title=title,
                snippet_data=snippet_data,
                on_select_callback=self.insert_snippet,
                parent_menu=menu,
                row_width=menu_width,
                reveal_delay_ms=reveal_delay,
                scroll_delay_ms=scroll_delay,
            )
            action.setDefaultWidget(row)
            menu.addAction(action)

        menu.exec(QCursor.pos())

    def insert_snippet(self, text: str):
        """Copies selected text to clipboard and simulates Ctrl+V if enabled."""
        cb = QApplication.clipboard()
        if cb is not None:
            cb.setText(text)

        time.sleep(0.1)

        auto_paste = app_config.get("settings", {}).get("auto_paste_enabled", True)
        if auto_paste:
            with kb.pressed(Key.ctrl):
                kb.press("v")
                kb.release("v")


# --- Main Application Startup ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(
        False
    )  # Keeps system tray app alive when windows close

    main_app = SnippetApp()

    # System-wide right-click listener
    def on_click(x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            main_app.show_menu_signal.emit()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    sys.exit(app.exec())
