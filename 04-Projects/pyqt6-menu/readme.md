Here is a professional, production-ready `README.md` and `AI.md` tailored for your snippet menu project, along with a clear breakdown of best practices for project organization and future maintenance.

---

## 1. Professional `README.md`

Create a file named `README.md` in your project root directory:

```markdown
# QuickSnippet Overlay

A lightweight, high-speed productivity overlay built with PyQt6. Designed to eliminate deep submenu navigation, **QuickSnippet** presents horizontal multi-variant actions directly under your cursor with zero vertical travel penalty.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## Features

- **Zero-Distance Interaction:** Hovering over a category automatically slides in multi-variant actions horizontally ($1️⃣ \dots 5️⃣$), keeping cursor movement minimal.
- **Auto-Reveal Timer:** Configurable delay (default $500\text{ms}$) before icons slide into view, preventing accidental triggers during standard scanning.
- **Edge Arrow Hotspots:** Built-in directional hotspots (`◀`, `▶`) with auto-scroll repeats ($300\text{ms}$) for multi-page icon pagination ($v_1 \dots v_9$).
- **Live Settings Panel:** Fully dark-themed PyQt6 GUI window for managing snippet categories, variant texts, accent colors, and animation delays without restarting the application.
- **System-Wide Hotkey/Mouse Trigger:** Listens globally for right-clicks via background thread hooks.
- **Auto-Paste Integration:** Automatically copies the selected snippet to clipboard and simulates `Ctrl+V`.

---

## Project Structure

```text
snippet_manager/
│
├── config.json           # Dynamic database & app settings (Auto-generated)
├── config_manager.py     # Thread-safe JSON I/O & fallback configuration
├── settings_gui.py       # PyQt6 Dark-themed Settings GUI panel
└── main.py               # System tray runner, mouse listener, & overlay menu

```

---

## Quick Start

### 1. Prerequisites & Installation

Ensure you have Python 3.10+ installed. Install the required dependencies:

```bash
pip install PyQt6 pynput

```

### 2. Running the Application

```bash
python main.py

```

* **Show Menu:** Right-click anywhere system-wide to trigger the popup overlay.
* **Access Settings:** Right-click the System Tray Icon in your taskbar and select **⚙️ Settings**.

---

## Configuration (`config.json`)

Settings and snippets are saved to `config.json` automatically upon execution:

```json
{
  "settings": {
    "auto_reveal_delay_ms": 500,
    "arrow_scroll_delay_ms": 300,
    "menu_width_px": 230,
    "auto_paste_enabled": true
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

## License

MIT License — Free for personal and commercial modification.

```
