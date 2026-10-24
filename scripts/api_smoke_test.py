"""
scripts/api_smoke_test.py
=========================
API Smoke Test for GDGoC CUI Wah Bootcamp.

Validates:
1. Python environment and required package imports.
2. Safe environment configuration (checks .env without revealing keys).
3. Live Gemini API connection (if credentials are provided).

Distinguishes syntax/config validation from live API testing.
"""

import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.ai_helper import check_api_setup, ask_gemini


def run_smoke_test():
    print("=" * 65)
    print("  GDGoC CUI Wah: 2-Day AI Bootcamp — Environment Smoke Test")
    print("=" * 65)

    setup = check_api_setup()
    print(f"\n[1/3] SDK Verification:")
    if setup["sdk_installed"]:
        print("  [PASS] Official 'google-genai' SDK is installed.")
    else:
        print("  [FAIL] 'google-genai' SDK is missing! Run: pip install -r requirements.txt")
        return False

    print(f"\n[2/3] Configuration Check:")
    print(f"  Configured Model: {setup['configured_model']}")
    if setup["key_present"]:
        print(f"  [PASS] GEMINI_API_KEY detected (Masked: {setup['api_key_masked']})")
    else:
        print("  [INFO] GEMINI_API_KEY is NOT set or still uses placeholder in .env")
        print("         Follow SETUP.md to create your free key at https://aistudio.google.com/")
        print("\n  >> Syntax and environment validation PASSED.")
        print("  >> Live API execution not tested: valid credentials were not available.")
        print("=" * 65)
        return True

    print(f"\n[3/3] Live Gemini API Smoke Test:")
    print("  Sending genuine test request to Google Gemini API...")
    try:
        response = ask_gemini(
            prompt="Respond with the exact phrase: 'GDGoC Wah AI Test OK: Model is online and ready!'",
            max_output_tokens=30
        )
        print("\n  [LIVE RESPONSE FROM GEMINI]")
        print(f"  \"{response.strip()}\"")
        print("\n  [PASS] Live Gemini API connection successful!")
        print("=" * 65)
        return True
    except Exception as err:
        print(f"\n  [ERROR] Live API call failed:")
        print(f"  {err}")
        print("=" * 65)
        return False


if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)
