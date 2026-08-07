from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QCursor, QGuiApplication
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PipNode(QFrame):
    clicked_signal = pyqtSignal(str)  # emits step_id

    def __init__(self, step_id: str):
        super().__init__()
        self.step_id = step_id
        self.output_data = None
        self.state = "pending"  # pending, active, done, error

        self.setFixedSize(120, 32)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)

        self.icon_label = QLabel("⚪")
        self.text_label = QLabel(f"{step_id}")
        self.text_label.setStyleSheet(
            "color: #FFFFFF; font-weight: bold; font-size: 11px;"
        )

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()

        self.update_style()

    def update_style(self):
        colors = {
            "pending": ("#4E586E", "⚪"),
            "active": ("#F78361", "🟡"),
            "done": ("#10b981", "🟢"),
            "error": ("#F54B64", "🔴"),
        }
        border_color, icon = colors.get(self.state, ("#4E586E", "⚪"))
        self.icon_label.setText(icon)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #242933;
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
            QFrame:hover {{
                background-color: #3B4353;
            }}
        """)

    def set_state(self, state: str, output_data=None):
        self.state = state
        self.output_data = output_data
        if state == "done":
            self.setToolTip("Click to copy output")
        elif state == "error":
            self.setToolTip(str(output_data) if output_data else "Error occurred")
        self.update_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked_signal.emit(self.step_id)
        super().mousePressEvent(event)


class MicroHUD(QWidget):
    cancel_requested = pyqtSignal()
    fallback_input_submitted = pyqtSignal(str)

    def __init__(self, steps: list):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.nodes = {}
        self.init_ui(steps)

    def init_ui(self, steps):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_frame = QFrame()
        self.bg_frame.setStyleSheet("""
            QFrame {
                background-color: #1E222A;
                border: 1px solid #4E586E;
                border-radius: 8px;
            }
        """)
        bg_layout = QVBoxLayout(self.bg_frame)
        bg_layout.setContentsMargins(10, 10, 10, 10)

        # Pips row
        self.pips_layout = QHBoxLayout()
        for step in steps:
            step_id = step.get("step_id", "L?")
            node = PipNode(step_id)
            node.clicked_signal.connect(self.handle_node_click)
            self.pips_layout.addWidget(node)
            self.nodes[step_id] = node

        bg_layout.addLayout(self.pips_layout)

        # Controls row (Tokens + Cancel)
        controls_layout = QHBoxLayout()

        self.token_label = QLabel("⚡ 0 tokens")
        self.token_label.setStyleSheet("color: #888888; font-size: 10px; border: none;")

        self.cancel_btn = QPushButton("✕")
        self.cancel_btn.setFixedSize(24, 24)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #ef4444;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)

        controls_layout.addWidget(self.token_label)
        controls_layout.addStretch()
        controls_layout.addWidget(self.cancel_btn)

        bg_layout.addLayout(controls_layout)

        # Fallback Input row (Hidden by default)
        self.fallback_widget = QWidget()
        fallback_layout = QHBoxLayout(self.fallback_widget)
        fallback_layout.setContentsMargins(0, 5, 0, 0)
        self.fallback_input = QLineEdit()
        self.fallback_input.setPlaceholderText("No text selected. Type prompt here...")
        self.fallback_input.setStyleSheet("""
            QLineEdit {
                background-color: #242933;
                color: #FFFFFF;
                border: 1px solid #4E586E;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #F54B64;
            }
        """)
        self.fallback_input.returnPressed.connect(self.submit_fallback)
        fallback_layout.addWidget(self.fallback_input)
        self.fallback_widget.hide()

        bg_layout.addWidget(self.fallback_widget)

        # Paste Error Fallback button
        self.paste_fallback_btn = QPushButton("📋 Click to Copy Result")
        self.paste_fallback_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F54B64, stop:1 #F78361);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F78361, stop:1 #F54B64);
            }
        """)
        self.paste_fallback_btn.hide()
        self.paste_fallback_btn.clicked.connect(self.handle_paste_fallback)
        bg_layout.addWidget(self.paste_fallback_btn)

        self.main_layout.addWidget(self.bg_frame)
        self.final_output_cache = ""

    def handle_node_click(self, step_id):
        node = self.nodes.get(step_id)
        if node and node.state == "done" and node.output_data:
            cb = QApplication.clipboard()
            if cb:
                text_to_copy = (
                    node.output_data
                    if isinstance(node.output_data, str)
                    else str(node.output_data)
                )
                cb.setText(text_to_copy)

                # Visual feedback flash
                orig_text = node.text_label.text()
                node.text_label.setText("Copied ✓")
                node.text_label.setStyleSheet(
                    "color: #10b981; font-weight: bold; font-size: 11px;"
                )

                QTimer.singleShot(1500, lambda: self.reset_node_text(node, orig_text))

    def reset_node_text(self, node, orig_text):
        node.text_label.setText(orig_text)
        node.text_label.setStyleSheet(
            "color: #FFFFFF; font-weight: bold; font-size: 11px;"
        )

    def submit_fallback(self):
        text = self.fallback_input.text().strip()
        if text:
            self.fallback_input.setEnabled(False)
            self.fallback_input_submitted.emit(text)

    def show_empty_text_fallback(self):
        self.fallback_widget.show()
        self.adjustSize()
        self.fallback_input.setFocus()

    def show_paste_fallback(self, final_output: str):
        self.final_output_cache = final_output
        self.paste_fallback_btn.show()
        self.adjustSize()

    def handle_paste_fallback(self):
        cb = QApplication.clipboard()
        if cb and self.final_output_cache:
            cb.setText(self.final_output_cache)
            self.paste_fallback_btn.setText("✓ Copied!")
            QTimer.singleShot(1500, self.close)

    def update_step(self, step_id: str, state: str, output_data=None):
        if step_id in self.nodes:
            self.nodes[step_id].set_state(state, output_data)

    def update_tokens(self, total_prompt, total_completion):
        self.token_label.setText(
            f"⚡ {total_prompt + total_completion} tokens (P:{total_prompt} C:{total_completion})"
        )

    def move_to_cursor(self, offset_x=10, offset_y=10):
        """Smart positioning to keep HUD on screen."""
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos)
        if not screen:
            screen = QGuiApplication.primaryScreen()

        if screen:
            screen_geom = screen.availableGeometry()
            x = cursor_pos.x() + offset_x
            y = cursor_pos.y() + offset_y

            # Ensure it fits width
            if x + self.width() > screen_geom.right():
                x = cursor_pos.x() - self.width() - offset_x

            # Ensure it fits height
            if y + self.height() > screen_geom.bottom():
                y = cursor_pos.y() - self.height() - offset_y

            self.move(x, y)
        else:
            # Fallback if no screen detected at all
            self.move(cursor_pos.x() + offset_x, cursor_pos.y() + offset_y)
