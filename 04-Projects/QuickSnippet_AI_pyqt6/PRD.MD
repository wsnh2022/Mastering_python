# `PRD.md` — QuickSnippet AI (Version 2.0)

> **Project Name:** QuickSnippet AI
> **Status:** Architecture Approved / Production Specification
> **Base Codebase:** QuickSnippet Menu Overlay v1.0 (PyQt6 + `pynput`)
> **Core Concept:** A non-blocking, cursor-adjacent desktop utility that transforms selected text through deterministic, multi-level JSON AI chains using OpenRouter, featuring a floating micro-HUD for real-time tracking.

---

## 1. Executive Summary & Vision

QuickSnippet AI evolves the static text snippet menu into an **interactive, local AI execution engine**.

Instead of waiting for slow API responses inside a locked context menu, the menu closes in under **$50\text{ms}$** upon selecting an AI action. A lightweight, background-threaded **Floating Micro-HUD** opens non-blockingly, running a sequence of 3 to 5 JSON-enforced AI prompts via OpenRouter. Intermediate outputs pass directly from level to level ($L_{N-1} \rightarrow L_N$) using template variable interpolation to minimize token consumption. Once complete, the final target text is automatically pasted at the active cursor position.

---

## 2. Key Objectives & Architectural Principles

1. **Zero Menu-Lock (Non-Blocking):** The popup snippet menu must dismiss instantly so the user can continue working or fire another task.
2. **Zero Framework Overhead:** No heavy agent frameworks (e.g., CrewAI, LangChain). The application uses direct, lightweight `asyncio` + `httpx` calls to OpenRouter for maximum speed and minimal RAM ($<30\text{MB}$).
3. **Strict JSON State-Passing & Schema Guardrails:** Every prompt level forces OpenRouter's `response_format: {"type": "json_object"}` alongside explicit system-prompt schema injections. Level $N$ receives *only* the structured JSON output of Level $N-1$, preventing token explosion and chat noise.
4. **Pre-Trigger OS Focus & Clipboard Snapshotting:** Text selection and target window handles (`HWND`) are captured *before* the PyQt menu steals focus, guaranteeing 100% reliable `Ctrl+C` / `Ctrl+V` operation across Electron, Terminal, and IDE applications.
5. **No Voice / Audio Overhead:** Focus exclusively on rapid, deterministic text transformation and auto-pasting.

---

## 3. System Architecture & Component Design

```
[ Right-Click Mouse Listener Trigger ]
           │
           ▼ (Pre-Trigger HWND Capture + Ctrl+C into Memory)
┌───────────────────────┐
│ QuickSnippet Menu     │ ──> (Menu Closes instantly < 50ms)
└──────────┬────────────┘
           │
           ▼ (Fires Background asyncio.Task Worker)
┌─────────────────────────────────────────────────────────────┐
│ OpenRouter Async Execution Chain Engine                     │
│                                                             │
│ Level 1 (L1) ──> OpenRouter (Fast Model)  ──> JSON Output 1 │
│                                                      │      │
│ Level 2 (L2) ──> OpenRouter (Smart Model) ──> JSON Output 2 │
│                                                      │      │
│ Level 3 (L3) ──> OpenRouter (Smart Model) ──> Final JSON    │
└──────────┬──────────────────────────────────────────────────┘
           │
           ├─────────────────────────┐
           ▼                         ▼
┌─────────────────────────────┐   ┌────────────────────────────────┐
│ Floating Micro-HUD Window   │   │ Auto-Paste Engine              │
│ (Pip Nodes, Model, Tokens,  │   │ (Restore Target HWND Focus +   │
│ Cancel / Retry / Error UX)  │   │  Clipboard Restoral + Ctrl+V)  │
└─────────────────────────────┘   └────────────────────────────────┘

```

---

## 4. Edge Cases & Failure Resilience Strategy

Building a desktop overlay that interacts with local OS hooks and external cloud APIs requires defensive, production-grade engineering:

| Scenario / Edge Case | Failure Risk | Prevention & Architectural Best Practice |
| --- | --- | --- |
| **OS Focus Loss on Menu Launch** | High | **Pre-Trigger Selection Capture:** Capture target Window Handle (`HWND`) and fire `Ctrl+C` *before* or *simultaneously with* launching the PyQt `QMenu` widget to avoid focus-stealing issues in IDEs/Terminals. |
| **No Text Selected** | Medium | If `Ctrl+C` returns unchanged/empty text within $150\text{ms}$, auto-fallback to an inline micro-text input inside the HUD or alert via toast notification without firing API calls. |
| **Clipboard Pollution / User Conflict** | High | **Snapshot & Restore:** Store active selection in isolated memory. Restore user's previous OS clipboard contents $100\text{ms}$ after auto-pasting completes so their system clipboard isn't ruined. |
| **OpenRouter Model Incompatibility / Invalid JSON** | High | **Dual-Layer JSON Enforcement:** Combine `response_format: {"type": "json_object"}` with strict JSON schema instructions injected directly into the `system_prompt`. If `json.loads()` fails, execute a regex fallback (`\{.*\}`). If unparseable, perform 1 automatic retry nudge before marking node 🔴. |
| **API Rate Limits / Credit Exhaustion (`402` / `429`)** | High | Specific HTTP status handlers for `402 Payment Required` and `429 Too Many Requests`. The affected HUD pip node turns 🔴 and surfaces a **"Quota Exceeded / Check OpenRouter Balance"** banner. |
| **Excessively Large Selection** | Medium | **Pre-Flight Token Guard:** Check string length (e.g., max 25,000 characters). If exceeded, prompt a confirmation in the HUD before spending OpenRouter credits. |
| **API Timeout / Connection Loss** | Medium | Enforce a $15\text{s}$ timeout per level via `httpx.Timeout(15.0)`. Display an interactive 🔴 pip node that allows clicking to view error/retry *only* that failed level without restarting the chain. |
| **User Abort / Task Cancellation** | Medium | Provide an instant **Cancel (`✕`) Button** on the Micro-HUD that cancels the active `asyncio.Task` and aborts all pending `httpx` HTTP requests immediately. |
| **Target Application Focus Loss during Auto-Paste** | High | Before firing `Ctrl+V`, re-verify/re-focus the captured target HWND. If focus cannot be established, do *not* paste blindly; flash HUD with a **"Click to Copy Result"** button. |

---

## 5. Feature Specifications & Requirements

### Feature 1: Dynamic Settings Panel Expansion

* **JSON Schema Update:** Expand `config.json` to store OpenRouter API key, default model, and chain definitions.
* **Template Variable Syntax:** Support variable injection templates in System Prompts:
* `{input_text}`: Initial selection captured from cursor.
* `{prev_output}`: Full raw JSON string from Level $N-1$.
* `{prev_output.key}`: Targeted extraction of a specific key from Level $N-1$'s JSON.



### Feature 2: Asynchronous Chain Engine (`ai_engine.py`)

* Built using `httpx.AsyncClient` wrapped in an `asyncio.Task` worker thread.
* Parses usage headers and payload response bodies to record exact prompt and completion tokens.
* Enforces single-step context passing with template interpolation.

### Feature 3: Floating Micro-HUD (`hud_gui.py`)

* A frameless, dark-themed, stays-on-top PyQt6 window positioned **near the cursor or active screen boundary**.
* **Interactive Pip Progress Nodes:**
* 🟢 **Green:** Step complete. Click node to copy its output to clipboard (flashes `✓ Copied` feedback).
* 🟡 **Pulsing Yellow:** Active OpenRouter HTTP request.
* 🔴 **Red:** Error/Timeout/Rate Limit (click node to view error message and retry step).
* ⚪ **Gray:** Pending step.


* **Control Actions:** Includes a **Cancel (`✕`)** button to abort running tasks instantly.

---

## 6. Phase-by-Phase Development Roadmap

The project will be built incrementally from a copy of the QuickSnippet v1.0 codebase:

```
[ Copy QuickSnippet v1.0 Codebase ]
                │
                ├──> Phase 1: Configuration, Template Engine & Async AI Core
                ├──> Phase 2: Micro-HUD GUI & Cancellation Controls
                ├──> Phase 3: Pre-Trigger HWND Capture, Menu & Clipboard Engine
                └──> Phase 4: Settings GUI Update & Polish

```

### Phase 1: Configuration, Template Engine & Async AI Core

* [ ] Duplicate the QuickSnippet v1.0 folder into `QuickSnippet_AI/`.
* [ ] Implement `config_manager.py` schema supporting `openrouter_api_key`, `chains`, and `{prev_output.key}` template interpolation.
* [ ] Build `ai_engine.py` using `asyncio` and `httpx` to execute multi-step JSON prompt chains with token metrics.
* [ ] Implement dual-layer JSON fallback parsing and strict timeout/HTTP status (`402`, `429`) error handling.

### Phase 2: Micro-HUD GUI & Cancellation Controls

* [ ] Build `hud_gui.py` using PyQt6 for the floating, frameless status window near cursor/screen boundaries.
* [ ] Implement custom pip node widgets (`🟢`, `🟡`, `🔴`, `⚪`) and live signal bindings for step updates.
* [ ] Add copy-to-clipboard functionality with visual `✓ Copied` feedback when clicking any finished pip node.
* [ ] Add a **Cancel (`✕`)** button hooked to `asyncio.Task.cancel()` to abort running requests.

### Phase 3: Pre-Trigger HWND Capture, Menu & Clipboard Engine

* [ ] Update `main.py` right-click trigger to capture the target window handle (`HWND`) and execute `Ctrl+C` selection capture *before* menu render.
* [ ] Integrate background worker thread to fire the AI chain and launch the Micro-HUD simultaneously.
* [ ] Close the main popup menu instantly ($<50\text{ms}$) upon selecting a chain.
* [ ] Implement target window refocusing, safe auto-paste (`Ctrl+V`), and clipboard snapshot/restore logic.

### Phase 4: Settings GUI Update & Polish

* [ ] Update `settings_gui.py` to support editing prompt chain sequences, variable templates, models, and API keys.
* [ ] Implement auto-minimize to system tray option for the HUD.
* [ ] Full end-to-end testing across all edge cases (focus restoration, rate limits, JSON repair fallbacks, task cancellations).

---

## 7. Target Project File Structure

```text
QuickSnippet_AI/
│
├── config.json           # Stores OpenRouter key, chains, and menu preferences
├── config_manager.py     # Schema validator, template interpolator, and JSON I/O
├── ai_engine.py          # Lightweight asyncio + httpx chain execution module
├── hud_gui.py            # PyQt6 floating micro-HUD status window & pip controls
├── settings_gui.py       # PyQt6 settings panel (Updated for prompt chains)
├── main.py               # Main tray runner, HWND/mouse listener, & menu overlay
├── README.md             # End-user documentation
└── PRD.md                # Product requirement document

```
---

## "Where & What to Change" Specification Map

### 1. File Structure Differences

| File | Status | What Changes from v1.0 |
| --- | --- | --- |
| `config.json` | **Update** | Add OpenRouter API key, selected model, and change `snippets` to support multi-step prompt chains (`chains`). |
| `config_manager.py` | **Update** | Add template variable interpolation (handling `{input_text}`, `{prev_output}`, `{prev_output.key}`). |
| `ai_engine.py` | **NEW FILE** | Add the lightweight `asyncio` + `httpx` runner for OpenRouter API calls (runs in the background). |
| `hud_gui.py` | **NEW FILE** | Add the floating, frameless PyQt6 status window with interactive pip nodes (`🟢`, `🟡`, `🔴`, `⚪`), token counters, and a Cancel (`✕`) button. |
| `main.py` | **Update** | 1. Capture active text/Window Handle (`HWND`) *before* showing the menu.<br>

<br>2. Dismiss menu in $<50\text{ms}$ on selection.<br>

<br>3. Launch `hud_gui.py` and `ai_engine.py` in a background thread.<br>

<br>4. Auto-paste result and restore the user's original clipboard afterwards. |
| `settings_gui.py` | **Update** | Replace the static text version editor ($v_1 \dots v_9$) with a Chain Editor (System Prompts, Model dropdowns, target keys). |

---

## 2. What Needs to Be Modified (Code-Level Details)

### Modification A: `config.json` Data Model Transformation

#### **v1.0 (Static Text):**

```json
"Email Signature": {
  "color": "#10b981",
  "versions": {
    "v1": "Best regards,\nAlex",
    "v2": "Thanks,\nAlex"
  }
}

```

#### **v2.0 (Prompt Chains):**

```json
"openrouter_api_key": "sk-or-v1-...",
"default_model": "anthropic/claude-3.5-sonnet",
"chains": {
  "Code Security Audit": {
    "color": "#a855f7",
    "steps": [
      {
        "step_id": "L1",
        "name": "Parse & Extract",
        "model": "meta-llama/llama-3.1-8b-instruct",
        "system_prompt": "Analyze code input: {input_text}. Return JSON: {\"language\": \"\", \"functions\": []}"
      },
      {
        "step_id": "L2",
        "name": "Security Audit",
        "model": "anthropic/claude-3.5-sonnet",
        "system_prompt": "Input JSON: {prev_output}. Find vulnerabilities. Return JSON: {\"vulnerabilities\": [], \"severity\": \"\"}"
      },
      {
        "step_id": "L3",
        "name": "Generate Fix",
        "model": "anthropic/claude-3.5-sonnet",
        "system_prompt": "Fix vulnerabilities: {prev_output.vulnerabilities}. Return JSON: {\"clean_code\": \"\"}",
        "output_key": "clean_code"
      }
    ]
  }
}

```

---

### Modification B: `main.py` Execution Flow

#### **v1.0 Flow:**

`Right Click` $\rightarrow$ `Show QMenu` $\rightarrow$ `User clicks static string` $\rightarrow$ `Copy string to clipboard` $\rightarrow$ `Simulate Ctrl+V`

#### **v2.0 Flow:**

1. `Right Click Trigger` $\rightarrow$ **Capture target Window Handle (`HWND`) and execute `Ctrl+C` into background memory first.**
2. `Show QMenu` $\rightarrow$ User selects an AI Chain (e.g., *Code Security Audit*).
3. **Menu closes instantly ($<50\text{ms}$).**
4. `main.py` fires `ai_engine.py` inside a background `asyncio` task and opens `hud_gui.py` near the cursor.
5. As each level finishes, `hud_gui.py` updates its pip nodes (`🟢 L1` $\rightarrow$ `🟡 L2`).
6. Upon final step completion:
* Refocus the captured target `HWND`.
* Paste the target JSON output key via `Ctrl+V`.
* Restore the user's original clipboard buffer after a $100\text{ms}$ delay.



---

### Modification C: Adding the 2 New Core Files

1. **`ai_engine.py`**:
* Uses `httpx.AsyncClient` to send requests to `[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)`.
* Passes `response_format: {"type": "json_object"}`.
* Extracts token metrics (`usage.prompt_tokens`, `usage.completion_tokens`) to pass to the HUD.
* Handles `402` (Quota Error), `429` (Rate Limit), and $15\text{s}$ timeouts gracefully.


2. **`hud_gui.py`**:
* A frameless PyQt6 window using `Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint`.
* Displays horizontal pip nodes that change state: ⚪ (Pending) $\rightarrow$ 🟡 (Pulsing/Active) $\rightarrow$ 🟢 (Done) or 🔴 (Error).
* Has a `✕` button that triggers `task.cancel()` in `ai_engine.py`.



---

## Step-by-Step Transition Plan

```text
Step 1: Create a folder named "QuickSnippet_AI" and copy main.py, settings_gui.py,
        config_manager.py, and config.json into it.

Step 2: Save the updated PRD.md inside QuickSnippet_AI/.

Step 3: Build Phase 1 (config_manager.py updates & ai_engine.py).

Step 4: Build Phase 2 (hud_gui.py).

Step 5: Connect Phase 3 (main.py background execution, HWND capture, and auto-paste).

```
