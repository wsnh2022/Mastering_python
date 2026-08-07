# AI Development & Architecture Context

## Project Overview
**QuickSnippet** is a desktop snippet launcher utility written in Python using PyQt6 and `pynput`.
Its defining feature is a horizontal sliding row (`HoverOverlaySnippetRow`) that replaces standard vertical context submenus.

---
## Current Architecture & State
- **Pattern:** Component-based PyQt6 UI with JSON persistence and background event hooks.
- **Horizontal Sliding:** Rows animate along the X-axis using `QPropertyAnimation(slider_container, b"pos")`. Page index offset formula: `target_x = -ROW_WIDTH * page_index`.
- **Page Layout:**
  - `Page 0`: Category Label (Text View)
  - `Page 1`: Variant Icons $1 \dots 5$
  - `Page 2`: Variant Icons $6 \dots 9$
- **State Flow:** `main.py` instantiates `SnippetApp` $\rightarrow$ launches `pynput.mouse.Listener` $\rightarrow$ emits Qt signal on right click $\rightarrow$ reloads `config.json` $\rightarrow$ constructs `QMenu`.

---
## Known Constraints & Invariants
1. **Never use vertical accordion sliding for rows:** Horizontal sliding must be preserved to keep category vertical positions stable.
2. **Signal Threading Safety:** `pynput` runs in a separate thread. Always trigger UI events in `main.py` through PyQt Signals (`pyqtSignal`), never directly from `pynput` callbacks.
3. **Data Integrity:** `config_manager.py` must maintain fallback dictionaries if `config.json` is missing or corrupted.
4. **PyQt6 Type Safety:** Ensure `QApplication.style()` and header objects are null-checked before accessing properties to prevent static analyzer errors.

---
## Future Backlog / Next Steps
- [ ] Refactor root directory structure into a modular package (`src/` directory pattern).
- [ ] Add `requirements.txt` / `pyproject.toml` for standardized dependency locking.
- [ ] Implement smart screen edge detection (flip popup direction near monitor boundaries).
- [ ] Add a global keyboard shortcut (e.g., `Ctrl+Shift+V`) alongside the right-click listener.
- [ ] Package into a single executable (`.exe`) via PyInstaller.

---

## 3. Best Practices for Project Code & File Maintenance

To transition this MVP into a clean, maintainable project codebase, adopt these structural improvements:

### A. Recommended Directory Organization (`src/` Pattern)

Instead of keeping all scripts scattered in the root folder, separate configuration, UI components, and application logic:

```text
snippet_manager/
│
├── .gitignore
├── AI.md
├── README.md
├── config.json
├── requirements.txt
│
└── src/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── config_manager.py    # Configuration loader & validator
    │   └── paste_engine.py      # System clipboard / keyboard simulation
    │
    ├── ui/
    │   ├── __init__.py
    │   ├── components/
    │   │   ├── __init__.py
    │   │   ├── edge_arrow.py    # EdgeArrowButton component
    │   │   └── snippet_row.py   # HoverOverlaySnippetRow component
    │   │
    │   ├── settings_gui.py      # Settings Window Dialog
    │   └── menu_overlay.py      # QMenu popup manager
    │
    └── app.py                   # Main entry point runner

```

### B. Core Refactoring Goals

1. **Decouple the Input Listener:** Move `pynput` logic out of `main.py` into a dedicated `listeners/` module.
2. **Add Dependency Management:** Create a `requirements.txt` file listing explicit versions:
```text
PyQt6>=6.5.0
pynput>=1.7.6
```


3. **Add `.gitignore`:** Exclude runtime files and virtual environments from version control:

```text
__pycache__/
*.pyc
.venv/
dist/
build/
```
---
