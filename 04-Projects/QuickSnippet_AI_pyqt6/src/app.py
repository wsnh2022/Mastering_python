import asyncio
import sys

from PyQt6.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import (
    QApplication,
    QMenu,
    QStyle,
    QSystemTrayIcon,
    QWidgetAction,
)

from src.core.ai_engine import execute_chain
from src.core.config_manager import load_config
from src.core.paste_engine import (
    capture_selection,
    get_active_window_handle,
    paste_text,
)
from src.listeners.keyboard_listener import start_keyboard_listener
from src.ui.hud_gui import MicroHUD
from src.ui.menu_overlay import HoverOverlaySnippetRow
from src.ui.settings_gui import SettingsWindow

app_config = load_config()


class AITaskThread(QThread):
    step_start_signal = pyqtSignal(str, str)  # step_id, name
    step_complete_signal = pyqtSignal(
        str, object, int, int
    )  # step_id, output, prompt_tokens, completion_tokens
    step_error_signal = pyqtSignal(str, str)  # step_id, error_msg
    chain_complete_signal = pyqtSignal(str)  # final_text

    def __init__(self, chain_data, input_text, api_key, default_model):
        super().__init__()
        self.chain_data = chain_data
        self.input_text = input_text
        self.api_key = api_key
        self.default_model = default_model
        self.loop = None
        self.task = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        callbacks = {
            "on_step_start": lambda sid, name: self.step_start_signal.emit(sid, name),
            "on_step_complete": lambda sid, out, toks: self.step_complete_signal.emit(
                sid, out, toks[0], toks[1]
            ),
            "on_step_error": lambda sid, err: self.step_error_signal.emit(sid, err),
            "on_chain_complete": lambda txt: self.chain_complete_signal.emit(txt),
        }

        # create_task() before the loop runs is unsafe on Python < 3.10.
        # Store the coroutine and schedule it once the loop is live.
        coro = execute_chain(
            self.chain_data,
            self.input_text,
            self.api_key,
            self.default_model,
            callbacks,
        )

        async def _run():
            self.task = asyncio.current_task()  # grab live task so cancel() works
            await coro

        try:
            self.loop.run_until_complete(_run())
        except asyncio.CancelledError:
            pass
        finally:
            self.loop.close()

    def cancel(self):
        if self.loop and self.task and not self.task.done():
            self.loop.call_soon_threadsafe(self.task.cancel)


class SnippetApp(QObject):
    trigger_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings_window = None
        self.hud = None
        self.ai_thread = None

        self.captured_text = ""
        self.captured_hwnd = None

        # System Tray Setup
        self.tray_icon = QSystemTrayIcon(self)
        style = QApplication.style()
        if style:
            self.tray_icon.setIcon(
                style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
            )

        tray_menu = QMenu()
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(self.open_settings)
        
        reload_action = QAction("🔄 Reload Config", self)
        reload_action.triggered.connect(self.reload_config)
        
        quit_action = QAction("❌ Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        tray_menu.addAction(settings_action)
        tray_menu.addAction(reload_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.trigger_signal.connect(self.handle_trigger)

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
            self.settings_window.config_saved.connect(self.reload_config)
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def reload_config(self):
        global app_config
        app_config = load_config()

    def handle_trigger(self):
        # Guard: ignore if a chain is already running
        if self.ai_thread and self.ai_thread.isRunning():
            return

        self.captured_hwnd = get_active_window_handle()
        self.captured_text = capture_selection()

        self.reload_config()
        self.show_menu()

    def show_menu(self):
        menu = QMenu()
        menu.setWindowFlags(menu.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        settings = app_config.get("settings", {})
        menu_width = settings.get("menu_width_px", 230)

        menu.setFixedWidth(menu_width)
        menu.setStyleSheet("""
            QMenu {
                background-color: #111111;
                border: 1px solid #222222;
                border-radius: 12px;
                padding: 4px;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }
            QMenu::separator {
                height: 1px;
                background: #444444;
                margin: 4px 10px;
            }
        """)

        chains = app_config.get("chains", {})
        for title, chain_data in chains.items():
            action = QWidgetAction(menu)
            row = HoverOverlaySnippetRow(
                title=title,
                on_select_callback=lambda t, c=chain_data: self.on_chain_selected(t, c),
                parent_menu=menu,
                row_width=menu_width,
            )
            action.setDefaultWidget(row)
            menu.addAction(action)

        menu.exec(QCursor.pos())

    def on_chain_selected(self, title, chain_data):
        self.hud = MicroHUD(chain_data.get("steps", []))
        self.hud.move_to_cursor()
        self.hud.show()

        self.hud.cancel_requested.connect(self.cancel_ai_task)
        self.hud.fallback_input_submitted.connect(
            lambda txt: self.start_ai_task(chain_data, txt)
        )

        if not self.captured_text:
            self.hud.show_empty_text_fallback()
        else:
            self.start_ai_task(chain_data, self.captured_text)

    def start_ai_task(self, chain_data, text_input):
        api_key = app_config.get("openrouter_api_key", "")
        if not api_key:
            if self.hud:
                self.hud.update_step(
                    next(iter(self.hud.nodes), ""), "error", "No API key — set it in Settings"
                )
            return

        default_model = app_config.get("default_model", "anthropic/claude-3.5-sonnet")

        self.ai_thread = AITaskThread(chain_data, text_input, api_key, default_model)

        self.ai_thread.step_start_signal.connect(
            lambda sid, name: self.hud.update_step(sid, "active") if self.hud else None
        )
        self.ai_thread.step_complete_signal.connect(
            lambda sid, out, p, c: (
                [
                    self.hud.update_step(sid, "done", out),
                    self.hud.update_tokens(p, c),
                ]
                if self.hud
                else None
            )
        )
        self.ai_thread.step_error_signal.connect(
            lambda sid, err: (
                self.hud.update_step(sid, "error", err) if self.hud else None
            )
        )
        self.ai_thread.chain_complete_signal.connect(self.on_chain_complete)

        self.ai_thread.start()

    def cancel_ai_task(self):
        if self.ai_thread:
            self.ai_thread.cancel()
        if self.hud:
            self.hud.close()

    def on_chain_complete(self, final_text: str):
        auto_paste = app_config.get("settings", {}).get("auto_paste_enabled", True)

        success = paste_text(final_text, auto_paste, self.captured_hwnd)

        if self.hud:
            if not success or not auto_paste:
                self.hud.show_paste_fallback(final_text)
            else:
                # If successfully pasted, close the HUD automatically after a short delay
                QTimer.singleShot(1500, self.hud.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    main_app = SnippetApp()

    # Listeners
    # The global right-click listener is disabled because it intercepts ALL OS right-clicks 
    # (including the tray icon). We rely exclusively on the Ctrl+Shift+C hotkey hook.
    # mouse_listener = start_mouse_listener(lambda: main_app.trigger_signal.emit())
    
    kb_listener = start_keyboard_listener(lambda: main_app.trigger_signal.emit())

    sys.exit(app.exec())
