import asyncio
import json
import re

import httpx

from src.core.config_manager import interpolate_template


class AIEngineError(Exception):
    pass


class TokenLimitError(Exception):
    pass


async def execute_step(
    client: httpx.AsyncClient,
    api_key: str,
    model: str,
    system_prompt: str,
    timeout_s: float = 60.0,  # 15s was too short for real models; 60s is a safe default
):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/QuickSnippet",
        "X-Title": "QuickSnippet AI",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Produce the requested JSON output."},
        ],
        "response_format": {"type": "json_object"},
    }

    response = await client.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=timeout_s,
    )

    if response.status_code == 402:
        raise AIEngineError("Quota Exceeded / Check OpenRouter Balance")
    elif response.status_code == 429:
        raise AIEngineError("Rate Limit Exceeded")

    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)

    return content, prompt_tokens, completion_tokens


def extract_json_fallback(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


async def execute_chain(
    chain_data: dict,
    input_text: str,
    api_key: str,
    default_model: str,
    callbacks: dict,
    require_confirmation=False,
):
    """
    Executes a chain of prompt steps sequentially.
    callbacks is a dict of functions:
      - on_step_start(step_id, name)
      - on_step_complete(step_id, output, tokens)
      - on_step_error(step_id, error_message)
      - on_chain_complete(final_output)
      - on_token_warning(character_count) -> bool (returns True to continue)
    """

    if len(input_text) > 25000:
        if "on_token_warning" in callbacks:
            should_continue = callbacks["on_token_warning"](len(input_text))
            if not should_continue:
                raise TokenLimitError("Task aborted due to large text size.")
        elif require_confirmation:
            raise TokenLimitError("Input text too large (>25k chars).")

    previous_step_result = None
    steps = chain_data.get("steps", [])

    async with httpx.AsyncClient() as client:
        for step in steps:
            step_id = step.get("step_id")
            step_name = step.get("name")

            if "on_step_start" in callbacks:
                callbacks["on_step_start"](step_id, step_name)

            model = step.get("model") or default_model
            raw_system_prompt = step.get("system_prompt", "")

            system_prompt = interpolate_template(
                raw_system_prompt,
                input_text=input_text,
                previous_step_result=previous_step_result,
            )

            # Up to 1 retry if JSON parsing fails completely
            max_retries = 1
            success = False
            last_error = ""

            for attempt in range(max_retries + 1):
                try:
                    content, p_tok, c_tok = await execute_step(
                        client, api_key, model, system_prompt
                    )

                    try:
                        parsed_json = json.loads(content)
                    except json.JSONDecodeError:
                        parsed_json = extract_json_fallback(content)
                        if parsed_json is None:
                            raise ValueError("Response was not parseable JSON.")

                    # Update previous_step_result for the next level
                    previous_step_result = parsed_json

                    if "on_step_complete" in callbacks:
                        callbacks["on_step_complete"](
                            step_id, parsed_json, (p_tok, c_tok)
                        )

                    success = True
                    break

                except Exception as e:
                    last_error = str(e)
                    if isinstance(e, asyncio.CancelledError):
                        raise  # propagate cancellation
                    if isinstance(e, AIEngineError):
                        if "on_step_error" in callbacks:
                            callbacks["on_step_error"](step_id, last_error)
                        return  # Abort chain immediately

                    # If this was the last attempt, it fails
                    if attempt == max_retries:
                        if "on_step_error" in callbacks:
                            callbacks["on_step_error"](step_id, last_error)
                        return  # Abort chain

            if not success:
                break

    # Final step extraction
    final_step = steps[-1] if steps else None
    if final_step and previous_step_result:
        output_key = final_step.get("output_key")
        if output_key and isinstance(previous_step_result, dict):
            final_text = str(previous_step_result.get(output_key, previous_step_result))
        else:
            final_text = json.dumps(previous_step_result, indent=2)

        if "on_chain_complete" in callbacks:
            callbacks["on_chain_complete"](final_text)

    return previous_step_result
