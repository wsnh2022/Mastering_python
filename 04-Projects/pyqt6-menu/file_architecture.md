Here is the project file architecture connecting your PyQt6 Snippet Popup Menu with the Settings GUI Panel and local configuration storage.

---

## Complete Project File Architecture

To keep the application clean, modular, and easy to maintain, the project is structured into **4 key files** inside a single project directory:

```text
snippet_manager/
│
├── config.json           # Stores your snippet database (v1–v9) & menu preferences
├── config_manager.py     # JSON load/save helper functions with error handling
├── settings_gui.py       # Full PyQt6 Settings Panel GUI window
└── main.py               # Background runner + Right-click listener + Popup Menu

```

---

## File Breakdown & Responsibilities

### 1. `config.json` *(Auto-generated data store)*

* **Purpose:** Stores your settings and snippet database as structured data.
* **Contains:**
* **`settings`:** Timings (`auto_reveal_delay_ms`, `arrow_scroll_delay_ms`) and dimensions (`menu_width_px`).
* **`snippets`:** Categories, custom highlight colors, and text versions (`v1` through `v9`).



```json
{
  "settings": {
    "auto_reveal_delay_ms": 500,
    "arrow_scroll_delay_ms": 300,
    "menu_width_px": 230
  },
  "snippets": {
    "Email Signature": {
      "color": "#10b981",
      "hover_border": "#34d399",
      "versions": {
        "v1": "Best regards,\nAlex Developer",
        "v2": "Thanks,\nAlex"
      }
    }
  }
}

```

---

### 2. `config_manager.py` *(Configuration I/O Module)*

* **Purpose:** Provides thread-safe loading and saving of `config.json`.
* **Contains:**
* `load_config()`: Reads `config.json` with fallback defaults and specific exception handling (`FileNotFoundError`, `json.JSONDecodeError`, `OSError`).
* `save_config(data)`: Writes python dictionaries back into formatted JSON.



---

### 3. `settings_gui.py` *(Customization GUI Window)*

* **Purpose:** The standalone PyQt6 configuration panel with dark styling.
* **Contains:**
* `SnippetEditorTab`: Left-side category list + right-side details panel with color picker and $v_1 \dots v_9$ versions table.
* `PreferencesTab`: Sliders and spin boxes for timing delays and width.
* `SettingsWindow`: Main modal dialog emitting `config_saved` signal when saved.



---

### 4. `main.py` *(Application Entry Point)*

* **Purpose:** Runs in the background, listens for right-clicks, renders the popup menu, and handles clipboard paste.
* **Contains:**
* `EdgeArrowButton`: Interactive left/right arrow hotspots (`◀`, `▶`) with 300ms hover-repeat scrolling.
* `HoverOverlaySnippetRow`: In-place sliding row holding 5 icons per page with a 500ms auto-reveal timer.
* `pynput.mouse.Listener`: Captures right-clicks system-wide to show the menu at the cursor position.
* `QSystemTrayIcon`: System tray icon with options to open **Settings** or **Exit**.



---

## Execution Flow

```text
               ┌──────────────────────────┐
               │    python main.py        │
               └────────────┬─────────────┘
                            │
               ┌────────────┴─────────────┐
               ▼                          ▼
     [Right-Click Mouse]          [System Tray Icon]
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  Show Popup Snippet Menu │  │  Open Settings Panel GUI │
│  (Hover / Auto-reveal)   │  │  (Edit Snippets/Timings) │
└──────────────┬───────────┘  └───────────┬──────────────┘
               │                          │
               │   ┌──────────────────┐   │
               └──>│   config.json    │<──┘
                   └──────────────────┘

```

---

## Summary

By separating the logic into **4 distinct files**, the UI settings window remains decoupled from the background mouse listener, making your project clean, scalable, and bug-free.
