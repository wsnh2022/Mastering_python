# QuickSnippet AI

A lightweight, system-wide productivity overlay and AI prompt chaining engine built with Python and PyQt6. **QuickSnippet AI** bridges the gap between your daily workflow and powerful LLMs by allowing you to highlight text anywhere on your computer and instantly run it through customizable AI prompt chains via a low-latency overlay menu.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## ✨ Features

- **System-Wide Overlay Menu:** Trigger a highly responsive PyQt6 overlay menu via global mouse or keyboard hooks. The menu appears directly at your cursor, eliminating context switching.
- **Visual AI Prompt Chaining:** Build complex pipelines where the output of one AI prompt feeds directly into the next. Manage this seamlessly in the built-in Node Editor GUI.
- **Dynamic Variable Interpolation:** Prompts support variables like `{input_text}` (the text you highlighted) and `{previous_step_result}` (the output from the previous node in the chain).
- **Auto-Paste Integration:** Once the AI finishes processing, the output is automatically pasted back into your active application (e.g., your code editor, email client, or web browser).
- **OpenRouter Integration:** Built-in support for OpenRouter, allowing you to use state-of-the-art models like Claude 3.5 Sonnet, GPT-4o, and DeepSeek, all configured via the Settings UI.
- **Live Settings Panel:** Fully dark-themed PyQt6 GUI window for managing AI Chains, Prompt Templates, OpenRouter API keys, AI models, and UI behavior.

---

## 🏗️ Architecture & Project Structure

The project is modularized into distinct domains to ensure scalability and maintainability:

```text
QuickSnippet_AI_pyqt6/
│
├── config.json                 # Core settings, API keys, and AI chain definitions
├── prompts.json                # Pre-configured and user-defined prompt templates
├── main.py                     # Entry point for the application
│
└── src/
    ├── app.py                  # PyQt6 Application and Tray Icon orchestration
    ├── core/                   # Core business logic
    │   ├── ai_engine.py        # LLM integration (OpenRouter API calls)
    │   ├── config_manager.py   # Thread-safe JSON state management
    │   └── paste_engine.py     # Keyboard simulation & clipboard injection
    ├── listeners/              # System-wide input hooks
    │   ├── keyboard_listener.py# Listens for global hotkeys
    │   └── mouse_listener.py   # Listens for specific mouse triggers
    └── ui/                     # PyQt6 User Interfaces
        ├── hud_gui.py          # On-screen HUD for processing status
        ├── menu_overlay.py     # The main right-click/hotkey overlay popup
        └── settings_gui.py     # The comprehensive AI Node Editor & settings panel
```

---

## 🚀 Quick Start

### 1. Prerequisites & Installation

Ensure you have Python 3.10+ installed. Clone this repository and install the required dependencies:

```bash
pip install PyQt6 pynput requests
```

### 2. Running the Application

Start the background service and system tray icon:

```bash
python main.py
```

### 3. Setup Your API Key

1. Right-click the QuickSnippet AI icon in your system tray and select **⚙️ Settings**.
2. Navigate to the **Global Settings** tab.
3. Under **API Configuration**, paste your OpenRouter API Key.
4. (Optional) Adjust your default AI model or add new ones.

### 4. Usage Flow

1. **Highlight Text:** Select some text in your browser, IDE, or document.
2. **Trigger Menu:** Use the designated global mouse/keyboard shortcut to summon the overlay menu at your cursor.
3. **Select Chain:** Click on the AI Chain you want to run (e.g., "Refactor Code", "Draft Email Reply").
4. **Processing:** A small HUD will appear showing the AI processing your request.
5. **Auto-Paste:** The final result is seamlessly typed/pasted back into your active window, replacing your highlighted text!

---

## 🛠️ Configuration (`config.json` & `prompts.json`)

Settings and chains are saved to `config.json` and `prompts.json` automatically when you use the Settings GUI.

- **`config.json`**: Manages UI settings (menu widths, scroll delays) and user-defined AI Chains (nodes, models, output keys).
- **`prompts.json`**: Manages the library of prompt templates, categorized for quick access in the Node Editor via the hierarchical dropdown menu.

---

## 📄 License

MIT License — Free for personal and commercial modification.
