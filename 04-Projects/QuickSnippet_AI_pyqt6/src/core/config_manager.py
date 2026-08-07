import json
import os
import re

# Ensure config.json is created in the exact directory where config_manager.py lives
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
PROMPTS_FILE = os.path.join(BASE_DIR, "prompts.json")

DEFAULT_CONFIG = {
    "settings": {
        "auto_reveal_delay_ms": 500,
        "arrow_scroll_delay_ms": 300,
        "menu_width_px": 230,
        "auto_paste_enabled": True,
    },
    "openrouter_api_key": "",
    "default_model": "anthropic/claude-3.5-sonnet",
    "chains": {
        "Code Security Audit": {
            "color": "#a855f7",
            "hover_border": "#c084fc",
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
                    "system_prompt": "Input JSON: {previous_step_result}. Find vulnerabilities. Return JSON: {\"vulnerabilities\": [], \"severity\": \"\"}"
                },
                {
                    "step_id": "L3",
                    "name": "Generate Fix",
                    "model": "anthropic/claude-3.5-sonnet",
                    "system_prompt": "Fix vulnerabilities: {previous_step_result.vulnerabilities}. Return JSON: {\"clean_code\": \"\"}",
                    "output_key": "clean_code"
                }
            ]
        },
        "Professional Email": {
            "color": "#10b981",
            "hover_border": "#34d399",
            "steps": [
                {
                    "step_id": "L1",
                    "name": "Rewrite",
                    "model": "meta-llama/llama-3.1-8b-instruct",
                    "system_prompt": "Rewrite this roughly drafted email professionally: {input_text}. Return JSON: {\"email\": \"\"}",
                    "output_key": "email"
                }
            ]
        }
    }
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

def load_prompts():
    if not os.path.exists(PROMPTS_FILE):
        return {"prompts": []}
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"prompts": []}

def save_prompts(data):
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def interpolate_template(template_str: str, input_text: str, previous_step_result: dict | str | None = None) -> str:
    """
    Interpolates variables into the template string.
    Supported variables:
    - {input_text}
    - {previous_step_result}
    - {previous_step_result.key.subkey}
    """
    result = template_str.replace("{input_text}", input_text)
    
    if previous_step_result is not None:
        if isinstance(previous_step_result, dict):
            # Replace full previous_step_result with JSON string representation
            result = result.replace("{previous_step_result}", json.dumps(previous_step_result))
            
            # Find and replace deep keys like {previous_step_result.vulnerabilities}
            matches = re.findall(r'\{previous_step_result\.([^\}]+)\}', result)
            for match in matches:
                keys = match.split('.')
                val = previous_step_result
                for key in keys:
                    if isinstance(val, dict):
                        val = val.get(key, "")
                    else:
                        val = ""
                        break
                
                # Convert the extracted value to string (or JSON if dict/list)
                if isinstance(val, (dict, list)):
                    val_str = json.dumps(val)
                else:
                    val_str = str(val)
                    
                result = result.replace(f"{{previous_step_result.{match}}}", val_str)
        else:
            # If previous_step_result is just a string
            result = result.replace("{previous_step_result}", str(previous_step_result))
            
    return result
