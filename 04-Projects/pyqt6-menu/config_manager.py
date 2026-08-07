import json
import os

# Ensure config.json is created in the exact directory where config_manager.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "settings": {
        "auto_reveal_delay_ms": 500,
        "arrow_scroll_delay_ms": 300,
        "menu_width_px": 230,
        "auto_paste_enabled": True,
    },
    "snippets": {
        "Email Signature": {
            "color": "#10b981",
            "hover_border": "#34d399",
            "versions": {
                "v1": "Best regards,\nAlex Developer\nalex@example.com",
                "v2": "Thanks,\nAlex",
            },
        },
        "Python Template": {
            "color": "#a855f7",
            "hover_border": "#c084fc",
            "versions": {
                "v1": "if __name__ == '__main__':\n    main()",
            },
        },
    },
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        # If file is corrupted or unreadable, rewrite clean default
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
