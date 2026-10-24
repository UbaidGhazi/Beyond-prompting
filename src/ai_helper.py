"""
src/ai_helper.py
================
Official Gemini API Helper for GDGoC CUI Wah Bootcamp.
Clean, beginner-friendly wrapper around Google's official `google-genai` SDK
with Multi-Key Automatic Rotation and Failover support.
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# Ensure UTF-8 output on Windows consoles so emojis never crash cp1252
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 1. Automatically load .env from repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
env_file = REPO_ROOT / ".env"


def reload_env():
    """Reloads environment variables from root .env file."""
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
        except Exception:
            # Fallback: Parse .env directly if python-dotenv is not installed
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")


reload_env()

# 2. Import official Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

# Default model: gemini-2.5-flash / gemini-3.5-flash-lite
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = [
    DEFAULT_MODEL,
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

# Track global active API key index for smooth multi-key rotation
_active_key_index: int = 0


def mask_key(key: str) -> str:
    """Masks an API key for safe display in logs and UI."""
    if not key or key == "your_gemini_api_key_here":
        return "NOT_SET"
    if len(key) <= 12:
        return f"{key[:3]}...{key[-3:]}"
    return f"{key[:6]}...{key[-6:]}"


def get_api_keys() -> List[str]:
    """
    Retrieves all configured API keys from environment.
    Supports:
      - GEMINI_API_KEYS (comma or semicolon separated)
      - GEMINI_API_KEY
      - GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3...
    """
    reload_env()
    raw_keys: List[str] = []

    # 1. Comma/semicolon delimited list
    multi = os.getenv("GEMINI_API_KEYS", "")
    if multi:
        for item in multi.replace(";", ",").split(","):
            cleaned = item.strip().strip('"').strip("'")
            if cleaned:
                raw_keys.append(cleaned)

    # 2. Standard single key
    single = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    if single:
        raw_keys.append(single)

    # 3. Numbered keys (GEMINI_API_KEY_1, GEMINI_API_KEY_2, ...)
    for idx in range(1, 10):
        k = os.getenv(f"GEMINI_API_KEY_{idx}", "").strip().strip('"').strip("'")
        if k:
            raw_keys.append(k)

    # Filter out empty or placeholder keys and deduplicate while keeping order
    valid_keys: List[str] = []
    seen = set()
    for k in raw_keys:
        if k and k != "your_gemini_api_key_here" and k not in seen:
            seen.add(k)
            valid_keys.append(k)

    return valid_keys


def get_active_api_key() -> str:
    """Returns currently selected active API key."""
    global _active_key_index
    keys = get_api_keys()
    if not keys:
        return ""
    _active_key_index = _active_key_index % len(keys)
    return keys[_active_key_index]


def get_active_key_index() -> int:
    """Returns the 0-based index of the currently active key."""
    global _active_key_index
    keys = get_api_keys()
    if not keys:
        return 0
    return _active_key_index % len(keys)


def rotate_api_key(reason: str = "quota limit / rate limit (429)") -> str:
    """
    Switches to the next configured Gemini API key when a rate limit
    or quota exhaustion event is detected.
    """
    global _active_key_index
    keys = get_api_keys()
    if len(keys) <= 1:
        return keys[0] if keys else ""

    old_idx = _active_key_index % len(keys)
    _active_key_index = (old_idx + 1) % len(keys)
    old_masked = mask_key(keys[old_idx])
    new_masked = mask_key(keys[_active_key_index])

    print("\n" + "=" * 65)
    print(" ⚠️  [GEMINI API KEY FAILOVER TRIGGERED]")
    print(f" • Key #{old_idx + 1} ({old_masked}) encountered: {reason}")
    print(f" • Automatically rotating to Key #{_active_key_index + 1} ({new_masked})")
    print(" • Request will be retried seamlessly without interruption.")
    print("=" * 65 + "\n")

    return keys[_active_key_index]


def check_api_setup() -> Dict[str, Any]:
    """Checks environment, SDK presence, and all configured API keys."""
    keys = get_api_keys()
    active_key = get_active_api_key()
    return {
        "sdk_installed": genai is not None,
        "key_present": len(keys) > 0,
        "key_count": len(keys),
        "configured_model": os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        "api_key_masked": mask_key(active_key) if active_key else "NOT_SET",
        "all_keys_masked": [mask_key(k) for k in keys],
        "active_key_index": get_active_key_index(),
        "failover_enabled": len(keys) > 1
    }


def is_rate_limit_error(err: Exception) -> bool:
    """Detects whether an error corresponds to rate limits or quota exhaustion."""
    err_str = str(err).lower()
    quota_indicators = [
        "429",
        "resource_exhausted",
        "quota",
        "rate limit",
        "rate_limit",
        "too many requests",
        "exceeded your current quota"
    ]
    return any(indicator in err_str for indicator in quota_indicators)


def ask_gemini(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: Optional[float] = None,
    response_mime_type: Optional[str] = None,
    max_output_tokens: Optional[int] = None,
    model: Optional[str] = None
) -> str:
    """
    Sends a prompt to Google Gemini and returns the model's response text.
    Automatically rotates between configured API keys if a rate limit or quota
    exhaustion error occurs.

    Args:
        prompt: The question or instruction for the AI.
        system_instruction: Optional persona or persistent rules.
        temperature: Controls creativity (0.0 = strict, 1.0 = creative).
        response_mime_type: Set to 'application/json' for JSON outputs.
        max_output_tokens: Maximum response length limit.
        model: Model name (defaults to GEMINI_MODEL or gemini-2.5-flash).
    """
    if genai is None or types is None:
        raise RuntimeError("Please install google-genai: pip install -r requirements.txt")

    keys = get_api_keys()
    if not keys:
        raise RuntimeError("GEMINI_API_KEY is missing! Please configure your key in .env")

    # Configure generation parameters
    config_dict = {}
    if system_instruction:
        config_dict["system_instruction"] = system_instruction
    if temperature is not None:
        config_dict["temperature"] = float(temperature)
    if response_mime_type:
        config_dict["response_mime_type"] = response_mime_type
    if max_output_tokens is not None:
        config_dict["max_output_tokens"] = int(max_output_tokens)

    config = types.GenerateContentConfig(**config_dict) if config_dict else None

    # Primary model plus fallbacks
    primary_model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    deduped_models: List[str] = [primary_model]
    for m in FALLBACK_MODELS:
        if m not in deduped_models:
            deduped_models.append(m)

    num_keys = len(keys)
    last_error = None

    # Outer loop: Try available API keys with automatic failover
    for key_round in range(num_keys):
        active_key = get_active_api_key()
        client = genai.Client(api_key=active_key)
        switched_key = False

        for target_model in deduped_models:
            for attempt in range(2):
                try:
                    res = client.models.generate_content(
                        model=target_model,
                        contents=prompt,
                        config=config
                    )
                    if res and res.text:
                        return res.text
                except Exception as err:
                    last_error = err
                    err_str = str(err).lower()

                    # 1. Rate Limit / Quota Exceeded -> Trigger Key Failover
                    if is_rate_limit_error(err):
                        if num_keys > 1 and key_round < num_keys - 1:
                            rotate_api_key(reason=str(err)[:120])
                            switched_key = True
                            break  # Exit model loop to immediately retry with next key
                        else:
                            # Only 1 key or already cycled through all keys
                            if attempt < 1:
                                time.sleep(2)
                                continue
                            else:
                                break

                    # 2. Server Temporary Overload (503 / 500)
                    elif any(c in err_str for c in ["503", "500", "overloaded", "unavailable"]):
                        if attempt < 1:
                            time.sleep(2)
                            continue
                        else:
                            break

                    # 3. Model Not Found (404) -> Fall back to next model
                    elif "404" in err_str:
                        break

                    # 4. Other fatal error
                    else:
                        raise RuntimeError(f"Gemini API Error: {err}") from err

            if switched_key:
                break  # Proceed to next key immediately

        if not switched_key:
            # If we didn't switch key and didn't return, we exhausted models on this key
            if num_keys > 1 and key_round < num_keys - 1:
                rotate_api_key(reason="Model failure on key")
            else:
                break

    raise RuntimeError(
        f"Gemini API failed across all {num_keys} configured API key(s) and fallback models. "
        f"Last error: {last_error}"
    )
