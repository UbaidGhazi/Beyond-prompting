"""Topic 10: A Basic AI Workflow (Pipeline with Validation)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Stage 1 & 2: Define Rules and Gather Context
event_data = {"title": "Python Workshop", "date": "Nov 05", "venue": "CS Lab 03"}
system_rules = "You are a campus assistant. Write a short WhatsApp broadcast containing Event, Date, and Venue."
prompt = f"Event Data: {event_data}\nDraft announcement."

# Stage 3: Call Model
print("Calling Gemini model...")
response = ask_gemini(prompt, system_instruction=system_rules, temperature=0.3).strip()

# Stage 4 & 5: Inspect and Deterministically Validate with Python
checks = {
    "has_venue": "lab 03" in response.lower(),
    "has_date": "nov" in response.lower(),
    "length_ok": len(response.split()) <= 80
}
print(f"Validation Report: {checks}")

# Stage 6: Deliver approved output
if all(checks.values()):
    print("\n--- [DELIVERABLE APPROVED] ---")
    print(response)
else:
    print("\n[ALERT] Output failed validation rules.")
