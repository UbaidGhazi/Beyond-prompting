"""Topic 06: Structured Output (JSON Generation & Validation)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

prompt = (
    "Generate a table for a CUI Wah coding workshop.\n"
    "Keys required: 'title', 'venue', 'date', 'fee'.\n"
    "Output JSON only."
)

# 1. Ask Gemini with response_mime_type="application/json"
raw_json = ask_gemini(prompt, response_mime_type="application/json", temperature=0.1)
print("--- [1] RAW JSON STRING FROM GEMINI ---")
print(raw_json.strip())

# 2. Parse with Python
data = json.loads(raw_json)
print("\n--- [2] PARSED PYTHON DICTIONARY ---")
print(f"Title: {data.get('title')}")
print(f"Venue: {data.get('venue')}")
print(f"Fee:   {data.get('fee')}")
