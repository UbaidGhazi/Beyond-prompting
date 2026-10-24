"""Topic 02: Anatomy of a Good Prompt (The 5 Pillars)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# The 5 Core Pillars:
role = "Role: You are the GDGoC Lead at CUI Wah."
task = "Task: Write an energetic WhatsApp announcement for freshers."
context = "Context: Git workshop on Friday Nov 27, 2 PM in CS Lab 05."
constraints = "Constraints: Under 80 words, friendly tone, no jargon."
output_format = "Format: Headline with emoji -> Date/Venue -> 3 bullets -> CTA"

full_prompt = f"{role}\n{task}\n{context}\n{constraints}\n{output_format}"

print("--- [5-PILLAR STRUCTURED PROMPT] ---")
print(ask_gemini(full_prompt).strip())
