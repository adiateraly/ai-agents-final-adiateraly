"""Model client: sends a request to an LLM API and returns the answer.

This file uses only the standard Python library (no pip install needed).
It works with the OpenAI Chat Completions API.

Settings are read from the .env file:
    LLM_API_KEY   your secret API key (never share it)
    LLM_MODEL     the model name, for example gpt-4o-mini
    LLM_BASE_URL  optional, default is https://api.openai.com/v1
"""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://api.openai.com/v1"
TIMEOUT_SECONDS = 60
MAX_RETRIES = 2  # how many times we try again after a temporary error
RETRY_WAIT_SECONDS = 2


class LLMError(Exception):
    """Raised when the LLM request fails. The message is safe to show (no key)."""


def load_env(path=".env"):
    """Read KEY=VALUE lines from a .env file and put them in os.environ.

    Values that already exist in the environment are not changed.
    If the file does not exist, nothing happens.
    """
    env_file = Path(path)
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _get_settings():
    """Return (api_key, model, base_url) or raise LLMError if something is missing."""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    model = os.environ.get("LLM_MODEL", "").strip()
    base_url = os.environ.get("LLM_BASE_URL", "").strip() or DEFAULT_BASE_URL
    if not api_key:
        raise LLMError("LLM_API_KEY is missing. Add it to your .env file.")
    if not model:
        raise LLMError("LLM_MODEL is missing. Add it to your .env file.")
    return api_key, model, base_url.rstrip("/")


def _post_json(url, payload, api_key):
    """Send one POST request and return the parsed JSON answer.

    Raises urllib errors. The caller decides what to do with them.
    """
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def _error_text(http_error):
    """Make a short, clear message from an HTTP error (without the key)."""
    code = http_error.code
    try:
        body = json.loads(http_error.read().decode("utf-8"))
        detail = body.get("error", {}).get("message", "")
    except Exception:
        detail = ""
    if code == 401:
        hint = "The API key is wrong or not active."
    elif code == 404:
        hint = "The model name may be wrong. Check LLM_MODEL."
    elif code == 429:
        hint = "Too many requests or no credit on the account."
    elif code >= 500:
        hint = "The API server has a problem."
    else:
        hint = "The API rejected the request."
    return "API error {}: {} {}".format(code, hint, detail).strip()


def _parse_answer(result):
    """Turn the raw API answer into {"text": str, "tool_calls": list}."""
    try:
        message = result["choices"][0]["message"]
    except (KeyError, IndexError, TypeError):
        raise LLMError("The API answer has an unexpected format.")

    text = message.get("content") or ""
    tool_calls = []
    for call in message.get("tool_calls") or []:
        try:
            name = call["function"]["name"]
            raw_args = call["function"].get("arguments") or "{}"
            arguments = json.loads(raw_args)
        except (KeyError, TypeError, json.JSONDecodeError):
            raise LLMError("The model sent a tool call that cannot be read.")
        if not isinstance(arguments, dict):
            raise LLMError("The tool arguments must be a JSON object.")
        tool_calls.append({"id": call.get("id", ""), "name": name, "arguments": arguments})
    return {"text": text, "tool_calls": tool_calls}


def complete(messages, tools=None):
    """Send messages to the LLM and return {"text": ..., "tool_calls": [...]}.

    messages: list like [{"role": "user", "content": "Hello"}]
    tools:    optional list of tool descriptions (used from week 13)
    """
    if not isinstance(messages, list) or not messages:
        raise LLMError("messages must be a non-empty list.")

    api_key, model, base_url = _get_settings()
    payload = {"model": model, "messages": messages}
    if tools:
        payload["tools"] = tools

    url = base_url + "/chat/completions"
    last_error = "Unknown error."
    for attempt in range(MAX_RETRIES + 1):
        try:
            result = _post_json(url, payload, api_key)
            return _parse_answer(result)
        except urllib.error.HTTPError as error:
            last_error = _error_text(error)
            # Only temporary problems are worth a retry.
            if error.code not in (429, 500, 502, 503, 504):
                raise LLMError(last_error)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = "Network problem: {}".format(getattr(error, "reason", error))
        except json.JSONDecodeError:
            raise LLMError("The API answer is not valid JSON.")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_WAIT_SECONDS)
    raise LLMError(last_error)
