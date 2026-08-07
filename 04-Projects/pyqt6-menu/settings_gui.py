import sys

from config_manager import load_config, save_config
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QColorDialog,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


# --- Tab 1: Snippet & Category Editor ---
class SnippetEditorTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.current_category = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Column: Category List & Controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(QLabel("<b>Snippet Categories</b>"))
        self.category_list = QListWidget()
        self.category_list.itemSelectionChanged.connect(self.on_category_selected)
        left_layout.addWidget(self.category_list)

        cat_btn_layout = QHBoxLayout()
        add_cat_btn = QPushButton("+ Category")
        add_cat_btn.clicked.connect(self.add_category)
        del_cat_btn = QPushButton("- Category")
        del_cat_btn.clicked.connect(self.delete_category)
        cat_btn_layout.addWidget(add_cat_btn)
        cat_btn_layout.addWidget(del_cat_btn)
        left_layout.addLayout(cat_btn_layout)

        splitter.addWidget(left_widget)

        # Right Column: Detail Editor for selected category
        self.right_widget = QWidget()
        right_layout = QVBoxLayout(self.right_widget)
        right_layout.setContentsMargins(10, 0, 0, 0)

        form_layout = QFormLayout()
        self.cat_name_input = QLineEdit()
        self.cat_name_input.editingFinished.connect(self.rename_category)
        form_layout.addRow("Category Name:", self.cat_name_input)

        # Color Picker Row
        color_row = QHBoxLayout()
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(24, 24)
        self.color_preview.setStyleSheet("border: 1px solid #555; border-radius: 4px;")
        self.color_btn = QPushButton("Choose Color")
        self.color_btn.clicked.connect(self.pick_color)
        color_row.addWidget(self.color_preview)
        color_row.addWidget(self.color_btn)
        color_row.addStretch()
        form_layout.addRow("Highlight Color:", color_row)

        right_layout.addLayout(form_layout)

        # Versions Table ($v_1 \dots v_9$)
        right_layout.addWidget(QLabel("<b>Versions (Up to 9)</b>"))
        self.versions_table = QTableWidget(0, 2)
        self.versions_table.setHorizontalHeaderLabels(["Version Tag", "Snippet Text"])

        header = self.versions_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        right_layout.addWidget(self.versions_table)

        ver_btn_layout = QHBoxLayout()
        add_ver_btn = QPushButton("+ Add Version")
        add_ver_btn.clicked.connect(self.add_version)
        del_ver_btn = QPushButton("- Delete Version")
        del_ver_btn.clicked.connect(self.delete_version)
        ver_btn_layout.addWidget(add_ver_btn)
        ver_btn_layout.addWidget(del_ver_btn)
        right_layout.addLayout(ver_btn_layout)

        splitter.addWidget(self.right_widget)
        splitter.setSizes([180, 420])
        main_layout.addWidget(splitter)

        self.populate_categories()

    def populate_categories(self):
        self.category_list.clear()
        for cat in self.config["snippets"]:
            self.category_list.addItem(cat)
        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)

    def on_category_selected(self):
        # Save previous category table edits before switching selection
        self.save_current_table_to_config()

        selected = self.category_list.selectedItems()
        if not selected:
            self.right_widget.setEnabled(False)
            self.current_category = None
            return

        self.right_widget.setEnabled(True)
        self.current_category = selected[0].text()
        cat_data = self.config["snippets"][self.current_category]

        self.cat_name_input.setText(self.current_category)
        color = cat_data.get("color", "#10b981")
        self.color_preview.setStyleSheet(
            f"background-color: {color}; border: 1px solid #555; border-radius: 4px;"
        )

        # Populate Versions Table
        versions = cat_data.get("versions", {})
        self.versions_table.setRowCount(0)
        for tag, text in versions.items():
            row = self.versions_table.rowCount()
            self.versions_table.insertRow(row)
            self.versions_table.setItem(row, 0, QTableWidgetItem(tag))
            self.versions_table.setItem(row, 1, QTableWidgetItem(text))

    def add_category(self):
        self.save_current_table_to_config()

        new_name = f"New Category {self.category_list.count() + 1}"
        self.config["snippets"][new_name] = {
            "color": "#10b981",
            "hover_border": "#34d399",
            "versions": {"v1": "Sample Text"},
        }
        self.populate_categories()

        items = self.category_list.findItems(new_name, Qt.MatchFlag.MatchExactly)
        if items:
            self.category_list.setCurrentItem(items[0])

    def delete_category(self):
        if not self.current_category:
            return
        del self.config["snippets"][self.current_category]
        self.current_category = None
        self.populate_categories()

    def rename_category(self):
        if not self.current_category:
            return
        new_name = self.cat_name_input.text().strip()
        if not new_name or new_name == self.current_category:
            return
        if new_name in self.config["snippets"]:
            QMessageBox.warning(self, "Warning", "Category name already exists!")
            self.cat_name_input.setText(self.current_category)
            return

        self.config["snippets"][new_name] = self.config["snippets"].pop(
            self.current_category
        )
        self.current_category = new_name
        self.populate_categories()

    def pick_color(self):
        if not self.current_category:
            return
        current_hex = self.config["snippets"][self.current_category].get(
            "color", "#10b981"
        )
        color = QColorDialog.getColor(QColor(current_hex), self, "Select Accent Color")
        if color.isValid():
            hex_val = color.name()
            self.config["snippets"][self.current_category]["color"] = hex_val
            self.color_preview.setStyleSheet(
                f"background-color: {hex_val}; border: 1px solid #555; border-radius: 4px;"
            )

    def add_version(self):
        if not self.current_category:
            return
        row_count = self.versions_table.rowCount()
        if row_count >= 9:
            QMessageBox.information(
                self, "Limit Reached", "Maximum of 9 versions allowed per category."
            )
            return

        tag = f"v{row_count + 1}"
        self.versions_table.insertRow(row_count)
        self.versions_table.setItem(row_count, 0, QTableWidgetItem(tag))
        self.versions_table.setItem(row_count, 1, QTableWidgetItem("New Snippet"))

    def delete_version(self):
        current_row = self.versions_table.currentRow()
        if current_row >= 0:
            self.versions_table.removeRow(current_row)

    def save_current_table_to_config(self):
        """Flushes active QTableWidget versions back into dictionary."""
        if (
            not self.current_category
            or self.current_category not in self.config["snippets"]
        ):
            return

        versions_dict = {}
        for row in range(self.versions_table.rowCount()):
            tag_item = self.versions_table.item(row, 0)
            text_item = self.versions_table.item(row, 1)
            if tag_item and text_item:
                versions_dict[tag_item.text()] = text_item.text()

        self.config["snippets"][self.current_category]["versions"] = versions_dict


# --- Tab 2: Timing & Preferences ---
class PreferencesTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        settings = self.config["settings"]

        self.reveal_slider = QSlider(Qt.Orientation.Horizontal)
        self.reveal_slider.setRange(100, 1500)
        self.reveal_slider.setValue(settings.get("auto_reveal_delay_ms", 500))
        self.reveal_label = QLabel(f"{self.reveal_slider.value()} ms")
        self.reveal_slider.valueChanged.connect(
            lambda v: self.reveal_label.setText(f"{v} ms")
        )

        reveal_row = QHBoxLayout()
        reveal_row.addWidget(self.reveal_slider)
        reveal_row.addWidget(self.reveal_label)
        layout.addRow("Auto-Reveal Delay (Hover):", reveal_row)

        self.arrow_spin = QSpinBox()
        self.arrow_spin.setRange(100, 1000)
        self.arrow_spin.setSingleStep(50)
        self.arrow_spin.setSuffix(" ms")
        self.arrow_spin.setValue(settings.get("arrow_scroll_delay_ms", 300))
        layout.addRow("Arrow Scroll Repeat Delay:", self.arrow_spin)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(180, 400)
        self.width_spin.setSingleStep(10)
        self.width_spin.setSuffix(" px")
        self.width_spin.setValue(settings.get("menu_width_px", 230))
        layout.addRow("Popup Menu Width:", self.width_spin)

    def save_preferences_to_config(self):
        self.config["settings"]["auto_reveal_delay_ms"] = self.reveal_slider.value()
        self.config["settings"]["arrow_scroll_delay_ms"] = self.arrow_spin.value()
        self.config["settings"]["menu_width_px"] = self.width_spin.value()


# --- Main Settings Window ---
class SettingsWindow(QDialog):
    config_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setWindowTitle("Snippet Manager - Settings")
        self.resize(650, 450)

        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.snippet_tab = SnippetEditorTab(self.config)
        self.pref_tab = PreferencesTab(self.config)

        self.tabs.addTab(self.snippet_tab, "Snippets & Categories")
        self.tabs.addTab(self.pref_tab, "Timing & Dimensions")
        main_layout.addWidget(self.tabs)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save & Apply")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.save_all)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        main_layout.addLayout(btn_layout)

    def save_all(self):
        self.snippet_tab.save_current_table_to_config()
        self.pref_tab.save_preferences_to_config()
        save_config(self.config)
        self.config_saved.emit()
        self.accept()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #2d2d2d;
                background-color: #181818;
            }
            QTabBar::tab {
                background-color: #252526;
                color: #cccccc;
                padding: 8px 16px;
                border: 1px solid #1e1e1e;
            }
            QTabBar::tab:selected {
                background-color: #181818;
                color: #ffffff;
                border-bottom: 2px solid #0078d4;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLineEdit, QTextEdit, QSpinBox, QListWidget, QTableWidget {
                background-color: #252526;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 4px;
                border: 1px solid #3c3c3c;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #0078d4;
                border-color: #0078d4;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
