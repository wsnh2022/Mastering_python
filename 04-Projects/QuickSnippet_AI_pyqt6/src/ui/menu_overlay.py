from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMenu,
    QWidget,
)


class HoverOverlaySnippetRow(QWidget):
    def __init__(
        self,
        title: str,
        on_select_callback,
        parent_menu: QMenu,
        row_width: int = 230,
    ):
        super().__init__()
        self.title = title
        self.on_select_callback = on_select_callback
        self.parent_menu = parent_menu
        self.ROW_WIDTH = row_width

        self.setFixedSize(self.ROW_WIDTH - 8, 28)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("SnippetRow")

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            "color: #E0E0E0; font-size: 13px; font-weight: 500;"
        )
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.setStyleSheet("""
            #SnippetRow {
                background-color: transparent;
                border-radius: 14px;
                border: 1px solid transparent;
            }
            #SnippetRow:hover {
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_menu.close()
            self.on_select_callback(self.title)
        super().mousePressEvent(event)
