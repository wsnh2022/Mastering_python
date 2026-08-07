import sys

from PyQt6.QtCore import QRegularExpression, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QSplitter,
    QTabWidget,
    QTextBrowser,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import load_config, load_prompts, save_config, save_prompts


class VariableHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setForeground(QColor("#F54B64"))
        self.highlight_format.setFontWeight(QFont.Weight.Bold)
        self.pattern = QRegularExpression(r"\{[^\}]+\}")

    def highlightBlock(self, text):
        match_iterator = self.pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(
                match.capturedStart(0), match.capturedLength(0), self.highlight_format
            )


class NodeEditorWidget(QFrame):
    def __init__(
        self, step_data=None, saved_models=None, prompts_data=None, parent=None
    ):
        super().__init__(parent)
        self.saved_models = saved_models or []
        self.prompts_data = prompts_data or {"prompts": []}
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(
            "NodeEditorWidget { border: 1px solid #444; border-radius: 5px; margin-bottom: 5px; }"
        )

        self.init_ui()
        if step_data:
            self.load_data(step_data)

    def init_ui(self):
        layout = QFormLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.step_id_input = QLineEdit()
        self.step_id_input.setPlaceholderText("ID (e.g. L1)")
        layout.addRow("Step ID:", self.step_id_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Draft Email (for your reference)")
        layout.addRow("Name:", self.name_input)

        self.model_input = QComboBox()
        self.model_input.setEditable(True)
        self.model_input.addItems(self.saved_models)
        layout.addRow("Model:", self.model_input)

        self.template_btn = QPushButton("Load Prompt Template...")
        self.template_btn.setStyleSheet("text-align: left; padding: 4px;")
        self.template_btn.setMinimumWidth(200)
        self.template_menu = QMenu(self)

        categories = {}
        for p in self.prompts_data.get("prompts", []):
            cat = p.get("category", "General")
            if not cat:
                cat = "General"
            categories.setdefault(cat, []).append(p)

        for cat in sorted(categories.keys()):
            cat_menu = self.template_menu.addMenu(cat)
            for p in categories[cat]:
                name = p.get("name", "Unnamed")
                action = cat_menu.addAction(name)
                action.triggered.connect(
                    lambda checked, prompt_data=p: self.on_menu_template_selected(
                        prompt_data
                    )
                )

        self.template_btn.setMenu(self.template_menu)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.template_btn)

        btn_input = QPushButton("{input_text}")
        btn_input.setToolTip("Insert the user's highlighted text")
        btn_input.clicked.connect(
            lambda: self.prompt_input.insertPlainText("{input_text}")
        )

        btn_prev = QPushButton("{previous_step_result}")
        btn_prev.setToolTip("Insert the JSON output from the previous step")
        btn_prev.clicked.connect(
            lambda: self.prompt_input.insertPlainText("{previous_step_result}")
        )

        for btn in [btn_input, btn_prev]:
            btn_layout.addWidget(btn)

        btn_layout.addStretch()
        layout.addRow("Template:", btn_layout)

        self.prompt_input = QPlainTextEdit()
        self.prompt_input.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 5px;"
        )
        self.highlighter = VariableHighlighter(self.prompt_input.document())
        self.prompt_input.setPlaceholderText("Write your prompt here...")
        self.prompt_input.setFixedHeight(90)
        layout.addRow("Prompt:", self.prompt_input)

        self.output_key_input = QLineEdit()
        self.output_key_input.setPlaceholderText(
            "Extract Final Key (Optional, e.g. clean_code)"
        )
        layout.addRow("Output Key:", self.output_key_input)

        self.remove_btn = QPushButton("Remove Node")
        layout.addRow("", self.remove_btn)

    def on_menu_template_selected(self, p):
        if p:
            self.prompt_input.setPlainText(p.get("system_prompt", ""))
            self.output_key_input.setText(p.get("output_key", ""))

    def load_data(self, data):
        self.step_id_input.setText(data.get("step_id", ""))
        self.name_input.setText(data.get("name", ""))
        self.model_input.setCurrentText(data.get("model", ""))
        self.prompt_input.setPlainText(data.get("system_prompt", ""))
        self.output_key_input.setText(data.get("output_key", ""))

    def get_data(self):
        return {
            "step_id": self.step_id_input.text().strip(),
            "name": self.name_input.text().strip(),
            "model": self.model_input.currentText().strip(),
            "system_prompt": self.prompt_input.toPlainText().strip(),
            "output_key": self.output_key_input.text().strip(),
        }


class ChainEditorTab(QWidget):
    def __init__(self, config, prompts_data, parent=None):
        super().__init__(parent)
        self.config = config
        self.prompts_data = prompts_data
        self.current_chain = None
        self.nodes = []
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Column: Chains List
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(QLabel("<b>AI Chains</b>"))
        self.chain_list = QListWidget()
        self.chain_list.itemSelectionChanged.connect(self.on_chain_selected)
        left_layout.addWidget(self.chain_list)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Chain")
        add_btn.clicked.connect(self.add_chain)
        del_btn = QPushButton("- Chain")
        del_btn.clicked.connect(self.delete_chain)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        left_layout.addLayout(btn_layout)
        splitter.addWidget(left_widget)

        # Right Column: Chain Detail Editor
        self.right_widget = QWidget()
        right_layout = QVBoxLayout(self.right_widget)
        right_layout.setContentsMargins(10, 0, 0, 0)

        form_layout = QFormLayout()
        self.chain_name_input = QLineEdit()
        self.chain_name_input.editingFinished.connect(self.rename_chain)
        form_layout.addRow("Chain Name:", self.chain_name_input)

        color_row = QHBoxLayout()
        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(lambda: self.pick_color("color"))
        self.color_preview = QLabel(" ")
        self.color_preview.setFixedSize(20, 20)

        self.border_btn = QPushButton("Hover Border")
        self.border_btn.clicked.connect(lambda: self.pick_color("hover_border"))
        self.border_preview = QLabel(" ")
        self.border_preview.setFixedSize(20, 20)

        color_row.addWidget(self.color_preview)
        color_row.addWidget(self.color_btn)
        color_row.addWidget(self.border_preview)
        color_row.addWidget(self.border_btn)
        color_row.addStretch()
        form_layout.addRow("Colors:", color_row)
        right_layout.addLayout(form_layout)

        right_layout.addWidget(QLabel("<b>Nodes (Steps)</b>"))

        # Scroll area for nodes
        self.nodes_scroll = QScrollArea()
        self.nodes_scroll.setWidgetResizable(True)
        self.nodes_container = QWidget()
        self.nodes_layout = QVBoxLayout(self.nodes_container)
        self.nodes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.nodes_scroll.setWidget(self.nodes_container)
        right_layout.addWidget(self.nodes_scroll)

        add_node_btn = QPushButton("+ Add Node")
        add_node_btn.clicked.connect(self.add_node)
        right_layout.addWidget(add_node_btn)

        splitter.addWidget(self.right_widget)
        splitter.setSizes([200, 600])
        main_layout.addWidget(splitter)

        self.populate_chains()
        self.right_widget.setEnabled(False)

    def populate_chains(self):
        self.chain_list.clear()
        if "chains" not in self.config:
            self.config["chains"] = {}

        for chain_name in self.config["chains"]:
            self.chain_list.addItem(chain_name)

    def on_chain_selected(self):
        self.save_current_chain()

        items = self.chain_list.selectedItems()
        if not items:
            self.right_widget.setEnabled(False)
            self.current_chain = None
            return

        self.current_chain = items[0].text()
        self.right_widget.setEnabled(True)
        self.chain_name_input.setText(self.current_chain)

        chain_data = self.config["chains"][self.current_chain]

        # Colors
        c1 = chain_data.get("color", "#ffffff")
        c2 = chain_data.get("hover_border", "#ffffff")
        self.color_preview.setStyleSheet(f"background-color: {c1};")
        self.border_preview.setStyleSheet(f"background-color: {c2};")

        # Clear existing nodes
        for n in self.nodes:
            self.nodes_layout.removeWidget(n)
            n.deleteLater()
        self.nodes.clear()

        # Populate nodes
        for step in chain_data.get("steps", []):
            self._create_node_widget(step)

    def _create_node_widget(self, step_data=None):
        saved_models = self.config.get(
            "saved_models",
            [
                "anthropic/claude-3.5-sonnet",
                "deepseek/deepseek-v4-flash",
                "meta-llama/llama-3.1-8b-instruct",
            ],
        )
        node = NodeEditorWidget(
            step_data, saved_models=saved_models, prompts_data=self.prompts_data
        )
        node.remove_btn.clicked.connect(lambda _, n=node: self.remove_node(n))
        self.nodes_layout.addWidget(node)
        self.nodes.append(node)

    def add_node(self):
        self._create_node_widget()

    def remove_node(self, node):
        self.nodes_layout.removeWidget(node)
        self.nodes.remove(node)
        node.deleteLater()

    def add_chain(self):
        name, ok = QInputDialog.getText(self, "New Chain", "Enter chain name:")
        if ok and name:
            if name not in self.config["chains"]:
                self.config["chains"][name] = {
                    "color": "#ffffff",
                    "hover_border": "#ffffff",
                    "steps": [],
                }
                self.populate_chains()
                items = self.chain_list.findItems(name, Qt.MatchFlag.MatchExactly)
                if items:
                    self.chain_list.setCurrentItem(items[0])
            else:
                QMessageBox.warning(self, "Error", "Chain already exists.")

    def delete_chain(self):
        items = self.chain_list.selectedItems()
        if items:
            name = items[0].text()
            res = QMessageBox.question(self, "Confirm", f"Delete chain '{name}'?")
            if res == QMessageBox.StandardButton.Yes:
                self.current_chain = None
                del self.config["chains"][name]
                self.populate_chains()

    def rename_chain(self):
        if not self.current_chain:
            return
        new_name = self.chain_name_input.text().strip()
        if new_name and new_name != self.current_chain:
            if new_name in self.config["chains"]:
                QMessageBox.warning(self, "Error", "Name already exists.")
                self.chain_name_input.setText(self.current_chain)
                return

            self.save_current_chain()
            self.config["chains"][new_name] = self.config["chains"].pop(
                self.current_chain
            )
            self.current_chain = new_name
            self.populate_chains()
            items = self.chain_list.findItems(new_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.chain_list.setCurrentItem(items[0])

    def pick_color(self, key):
        if not self.current_chain:
            return
        c = QColorDialog.getColor()
        if c.isValid():
            hex_color = c.name()
            if key == "color":
                self.color_preview.setStyleSheet(f"background-color: {hex_color};")
            else:
                self.border_preview.setStyleSheet(f"background-color: {hex_color};")
            self.config["chains"][self.current_chain][key] = hex_color

    def save_current_chain(self):
        if self.current_chain and self.current_chain in self.config["chains"]:
            steps = []
            for n in self.nodes:
                data = n.get_data()
                if data["step_id"] and data["model"]:
                    # Clean up empty output_key so it doesn't pollute
                    if not data["output_key"]:
                        del data["output_key"]
                    steps.append(data)
            self.config["chains"][self.current_chain]["steps"] = steps


class GlobalSettingsTab(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # API Keys
        api_group = QGroupBox("API Configuration")
        api_layout = QFormLayout()
        self.api_key_input = QLineEdit(self.config.get("openrouter_api_key", ""))
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        api_layout.addRow("OpenRouter API Key:", self.api_key_input)
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # Default & Saved Models
        models_group = QGroupBox("Saved AI Models")
        models_layout = QVBoxLayout()

        form_l = QVBoxLayout()
        self.model_input = QLineEdit(
            self.config.get("default_model", "anthropic/claude-3.5-sonnet")
        )
        form_l.addWidget(QLabel("Default Model:"))
        form_l.addWidget(self.model_input)
        models_layout.addLayout(form_l)

        models_layout.addWidget(QLabel("Model List:"))
        self.models_list = QListWidget()
        self.models_list.setFixedHeight(100)
        saved_models = self.config.get(
            "saved_models",
            [
                "anthropic/claude-3.5-sonnet",
                "deepseek/deepseek-v4-flash",
                "meta-llama/llama-3.1-8b-instruct",
            ],
        )
        self.models_list.addItems(saved_models)
        models_layout.addWidget(self.models_list)

        model_btns = QHBoxLayout()
        self.model_add_input = QLineEdit()
        self.model_add_input.setPlaceholderText("e.g. openai/gpt-4o")

        add_m_btn = QPushButton("Add")
        add_m_btn.clicked.connect(self.add_saved_model)

        del_m_btn = QPushButton("Remove Selected")
        del_m_btn.clicked.connect(self.remove_saved_model)

        model_btns.addWidget(self.model_add_input)
        model_btns.addWidget(add_m_btn)
        model_btns.addWidget(del_m_btn)
        models_layout.addLayout(model_btns)

        models_group.setLayout(models_layout)

        # Behavior
        behavior_group = QGroupBox("Behavior and UI Settings")
        b_layout = QFormLayout()

        self.auto_paste = QCheckBox("Auto-Paste final result back into active window")
        settings_dict = self.config.get("settings", {})
        self.auto_paste.setChecked(settings_dict.get("auto_paste_enabled", True))
        b_layout.addRow(self.auto_paste)

        self.reveal_delay = QSpinBox()
        self.reveal_delay.setRange(0, 5000)
        self.reveal_delay.setFixedWidth(120)
        self.reveal_delay.setValue(settings_dict.get("auto_reveal_delay_ms", 500))
        b_layout.addRow("Menu Reveal Delay (ms):", self.reveal_delay)

        self.scroll_delay = QSpinBox()
        self.scroll_delay.setRange(0, 5000)
        self.scroll_delay.setFixedWidth(120)
        self.scroll_delay.setValue(settings_dict.get("arrow_scroll_delay_ms", 300))
        b_layout.addRow("Menu Scroll Delay (ms):", self.scroll_delay)

        self.menu_width = QSpinBox()
        self.menu_width.setRange(100, 800)
        self.menu_width.setFixedWidth(120)
        self.menu_width.setValue(settings_dict.get("menu_width_px", 230))
        b_layout.addRow("Menu Width (px):", self.menu_width)

        behavior_group.setLayout(b_layout)

        # Create two columns for the bottom section
        columns_layout = QHBoxLayout()
        columns_layout.addWidget(models_group)
        columns_layout.addWidget(behavior_group)

        layout.addLayout(columns_layout)

        layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def add_saved_model(self):
        new_model = self.model_add_input.text().strip()
        if new_model:
            items = self.models_list.findItems(new_model, Qt.MatchFlag.MatchExactly)
            if not items:
                self.models_list.addItem(new_model)
                self.model_add_input.clear()

    def remove_saved_model(self):
        for item in self.models_list.selectedItems():
            self.models_list.takeItem(self.models_list.row(item))

    def apply_settings(self):
        self.config["openrouter_api_key"] = self.api_key_input.text().strip()
        self.config["default_model"] = self.model_input.text().strip()

        models = []
        for i in range(self.models_list.count()):
            item = self.models_list.item(i)
            if item is not None:
                models.append(item.text())
        self.config["saved_models"] = models

        if "settings" not in self.config:
            self.config["settings"] = {}
        self.config["settings"]["auto_paste_enabled"] = self.auto_paste.isChecked()
        self.config["settings"]["auto_reveal_delay_ms"] = self.reveal_delay.value()
        self.config["settings"]["arrow_scroll_delay_ms"] = self.scroll_delay.value()
        self.config["settings"]["menu_width_px"] = self.menu_width.value()


class HelpTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        help_text = """
        <div style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; color: #FFFFFF; padding: 10px;">
            <h2 style="color: #F78361; border-bottom: 1px solid #4E586E; padding-bottom: 6px; margin-top: 0;">QuickSnippet AI - Prompt Guide</h2>
            <p style="margin-bottom: 16px;">The AI Engine uses simple template variables to pass data between steps. Always instruct the AI to output JSON.</p>

            <h3 style="color: #F54B64; margin-top: 24px; margin-bottom: 8px;">Sample 1: Basic Single Step <span style="color:#CCCCCC; font-weight:normal;">(Using <code style="color: #F78361; font-family: Consolas, monospace;">{input_text}</code>)</span></h3>
            <p style="margin-bottom: 8px; color: #E0E0E0;">A simple step that takes highlighted text and translates it.</p>
            <div style="background-color: #242933; padding: 12px; border: 1px solid #4E586E; border-radius: 6px;">
<div style="margin: 0; color: #E0E0E0; font-family: Consolas, monospace; font-size: 14px; line-height: 1.5;">Task: Translate the following text into French.<br>
Input: <span style="color: #F54B64; font-weight: bold;">{input_text}</span><br>
<br>
Return strictly in this JSON format:<br>
{<br>
&nbsp;&nbsp;"translation": "the translated text"<br>
}</div>
            </div>
            <p style="margin-top: 8px; color: #CCCCCC; font-style: italic;">Set <b style="color:#FFFFFF;">Output Key</b> to: <code style="color: #F78361; font-family: Consolas, monospace; font-weight: bold;">translation</code></p>

            <h3 style="color: #F54B64; margin-top: 28px; margin-bottom: 8px;">Sample 2: Multi-Step Chaining <span style="color:#CCCCCC; font-weight:normal;">(Using <code style="color: #F78361; font-family: Consolas, monospace;">{previous_step_result}</code>)</span></h3>
            <p style="margin-bottom: 8px; color: #E0E0E0;">Imagine Step 1 generated a JSON with a <code style="color: #F78361; font-family: Consolas, monospace; font-weight: bold;">"draft"</code> key. Step 2 can read that draft using <code style="color: #F78361; font-family: Consolas, monospace;">{previous_step_result}</code>.</p>
            <div style="background-color: #242933; padding: 12px; border: 1px solid #4E586E; border-radius: 6px;">
<div style="margin: 0; color: #E0E0E0; font-family: Consolas, monospace; font-size: 14px; line-height: 1.5;">Task: Proofread the provided draft. Fix any grammar and spelling mistakes.<br>
Draft to proofread: <span style="color: #F54B64; font-weight: bold;">{previous_step_result}</span><br>
<br>
Return strictly in this JSON format:<br>
{<br>
&nbsp;&nbsp;"corrected_text": "the proofread text goes here",<br>
&nbsp;&nbsp;"changes_made": "summary of what you fixed"<br>
}</div>
            </div>
            <p style="margin-top: 8px; color: #CCCCCC; font-style: italic;">Set <b style="color:#FFFFFF;">Output Key</b> to: <code style="color: #F78361; font-family: Consolas, monospace; font-weight: bold;">corrected_text</code></p>

            <h3 style="color: #F54B64; margin-top: 28px; margin-bottom: 8px;">Sample 3: Extracting Specific Keys</h3>
            <p style="margin-bottom: 8px; color: #E0E0E0;">If Step 1 returned multiple things, you can target a specific key like this: <code style="color: #F78361; font-family: Consolas, monospace;">{previous_step_result.vulnerabilities}</code></p>
            <div style="background-color: #242933; padding: 12px; border: 1px solid #4E586E; border-radius: 6px;">
<div style="margin: 0; color: #E0E0E0; font-family: Consolas, monospace; font-size: 14px; line-height: 1.5;">Task: Write a python script to fix these security vulnerabilities:<br>
Vulnerabilities: <span style="color: #F54B64; font-weight: bold;">{previous_step_result.vulnerabilities}</span><br>
<br>
Return strictly in this JSON format:<br>
{<br>
&nbsp;&nbsp;"clean_code": "the new secure code"<br>
}</div>
            </div>
            <p style="margin-top: 8px; color: #CCCCCC; font-style: italic;">Set <b style="color:#FFFFFF;">Output Key</b> to: <code style="color: #F78361; font-family: Consolas, monospace; font-weight: bold;">clean_code</code></p>
        </div>
        """

        browser = QTextBrowser()
        browser.setHtml(help_text)
        browser.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(browser)


class PromptManagerTab(QWidget):
    def __init__(self, prompts_data, parent=None):
        super().__init__(parent)
        self.prompts_data = prompts_data
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(QLabel("<b>Saved Prompts</b>"))

        self.prompt_tree = QTreeWidget()
        self.prompt_tree.setHeaderHidden(True)
        self.prompt_tree.setIndentation(15)
        self.prompt_tree.itemSelectionChanged.connect(self.on_select)
        left_layout.addWidget(self.prompt_tree)

        self.current_selected_idx = -1

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Add")
        add_btn.clicked.connect(self.add_prompt)
        del_btn = QPushButton("- Delete")
        del_btn.clicked.connect(self.delete_prompt)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        left_layout.addLayout(btn_layout)

        right_widget = QWidget()
        self.right_layout = QVBoxLayout(right_widget)
        self.right_layout.setContentsMargins(10, 0, 0, 0)

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.output_key_input = QLineEdit()

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Output Key:", self.output_key_input)
        self.right_layout.addLayout(form_layout)

        self.right_layout.addWidget(QLabel("System Prompt:"))
        self.system_prompt_input = QPlainTextEdit()
        self.system_prompt_input.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 5px;"
        )
        self.system_highlighter = VariableHighlighter(
            self.system_prompt_input.document()
        )
        self.right_layout.addWidget(self.system_prompt_input)

        self.save_btn = QPushButton("Save Selected")
        self.save_btn.clicked.connect(self.save_current)
        self.right_layout.addWidget(self.save_btn)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 600])
        layout.addWidget(splitter)

        self.refresh_list()
        right_widget.setEnabled(False)
        self.right_widget = right_widget

    def refresh_list(self):
        self.prompt_tree.clear()

        categories = {}
        for idx, p in enumerate(self.prompts_data.get("prompts", [])):
            cat = p.get("category", "General")
            if not cat:
                cat = "General"
            categories.setdefault(cat, []).append((idx, p))

        for cat in sorted(categories.keys()):
            cat_item = QTreeWidgetItem(self.prompt_tree, [cat])

            for idx, p in categories[cat]:
                name = p.get("name", "Unnamed")
                prompt_item = QTreeWidgetItem(cat_item, [name])
                prompt_item.setData(0, Qt.ItemDataRole.UserRole, idx)

            cat_item.setExpanded(True)

        self.category_input.clear()
        self.category_input.addItems(sorted(categories.keys()))

    def on_select(self):
        items = self.prompt_tree.selectedItems()
        if not items:
            self.right_widget.setEnabled(False)
            self.current_selected_idx = -1
            return

        item = items[0]
        idx = item.data(0, Qt.ItemDataRole.UserRole)

        if idx is None or idx < 0 or idx >= len(self.prompts_data.get("prompts", [])):
            self.right_widget.setEnabled(False)
            self.current_selected_idx = -1
            return

        self.current_selected_idx = idx

        p = self.prompts_data["prompts"][idx]
        self.name_input.setText(p.get("name", ""))
        self.category_input.setCurrentText(p.get("category", "General"))
        self.output_key_input.setText(p.get("output_key", ""))
        self.system_prompt_input.setPlainText(p.get("system_prompt", ""))
        self.right_widget.setEnabled(True)

    def add_prompt(self):
        self.prompts_data.setdefault("prompts", []).append(
            {
                "name": "New Prompt",
                "category": "General",
                "system_prompt": "",
                "output_key": "",
            }
        )
        self.refresh_list()

        # Select the newly added item
        new_idx = len(self.prompts_data["prompts"]) - 1
        self._select_by_index(new_idx)

    def delete_prompt(self):
        if self.current_selected_idx >= 0:
            del self.prompts_data["prompts"][self.current_selected_idx]
            self.current_selected_idx = -1
            self.refresh_list()
            self.right_widget.setEnabled(False)

    def save_current(self):
        if self.current_selected_idx >= 0:
            idx = self.current_selected_idx
            self.prompts_data["prompts"][idx].update(
                {
                    "name": self.name_input.text().strip(),
                    "category": self.category_input.currentText().strip(),
                    "output_key": self.output_key_input.text().strip(),
                    "system_prompt": self.system_prompt_input.toPlainText().strip(),
                }
            )
            self.refresh_list()
            self._select_by_index(idx)

    def _select_by_index(self, target_idx):
        for i in range(self.prompt_tree.topLevelItemCount()):
            cat_item = self.prompt_tree.topLevelItem(i)
            if not cat_item:
                continue
            for j in range(cat_item.childCount()):
                prompt_item = cat_item.child(j)
                if (
                    prompt_item
                    and prompt_item.data(0, Qt.ItemDataRole.UserRole) == target_idx
                ):
                    self.prompt_tree.setCurrentItem(prompt_item)
                    return

    def apply_settings(self):
        self.save_current()


class SettingsWindow(QDialog):
    config_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QuickSnippet AI Settings")
        self.resize(900, 600)

        self.config = load_config()
        self.prompts_data = load_prompts()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #1E222A;
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #4E586E;
                background-color: #1E222A;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #242933;
                color: #FFFFFF;
                padding: 8px 16px;
                border: 1px solid #4E586E;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1E222A;
                border-top: 3px solid #F54B64;
            }
            QLineEdit, QPlainTextEdit, QSpinBox, QComboBox, QTreeWidget, QListWidget {
                background-color: #242933;
                color: #FFFFFF;
                border: 1px solid #4E586E;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #F54B64;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #242933;
                border: 1px solid #4E586E;
                selection-background-color: #F54B64;
            }
            QCheckBox {
                spacing: 8px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                background-color: #242933;
                border: 2px solid #4E586E;
            }
            QCheckBox::indicator:hover {
                border-color: #F78361;
            }
            QCheckBox::indicator:checked {
                background-color: #F54B64;
                border: 2px solid #F54B64;
                image: url(src/ui/assets/check.svg);
            }
            QPushButton {
                background-color: #4E586E;
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5C677D;
            }
            QPushButton:pressed {
                background-color: #3B4353;
            }
            QPushButton[primary="true"] {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F54B64, stop:1 #F78361);
            }
            QPushButton[primary="true"]:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F78361, stop:1 #F54B64);
            }
            QPushButton[primary="true"]:pressed {
                background-color: #F54B64;
            }
            QGroupBox {
                border: 1px solid #4E586E;
                border-radius: 4px;
                margin-top: 15px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #F78361;
            }
            QScrollBar:vertical {
                border: none;
                background: #1E222A;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4E586E;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #1E222A;
                height: 10px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #4E586E;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QHeaderView::section {
                background-color: #242933;
                color: white;
                border: none;
                border-bottom: 1px solid #4E586E;
            }
        """)

        self.tabs = QTabWidget()
        self.global_tab = GlobalSettingsTab(self.config)
        self.chain_tab = ChainEditorTab(self.config, self.prompts_data)
        self.help_tab = HelpTab()

        self.prompt_tab = PromptManagerTab(self.prompts_data)

        self.tabs.addTab(self.global_tab, "Global Settings")
        self.tabs.addTab(self.chain_tab, "AI Chains")
        self.tabs.addTab(self.prompt_tab, "Prompt Manager")
        self.tabs.addTab(self.help_tab, "Help & Examples")

        main_layout.addWidget(self.tabs)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("Save Settings")
        save_btn.setProperty("primary", True)
        save_btn.clicked.connect(self.save_settings)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(close_btn)
        btn_layout.addWidget(save_btn)

        main_layout.addLayout(btn_layout)

    def save_settings(self):
        self.global_tab.apply_settings()
        self.chain_tab.save_current_chain()
        self.prompt_tab.apply_settings()

        save_config(self.config)
        save_prompts(self.prompts_data)
        self.config_saved.emit()
        QMessageBox.information(
            self, "Settings Saved", "Your settings have been saved successfully."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    sys.exit(app.exec())
