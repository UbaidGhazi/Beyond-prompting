"""Topic 01: What Is a Prompt? (Vague vs Specific)"""
import sys
from pathlib import Path

# Add project root to path so we can import src.ai_helper
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# 1. A vague prompt with no details
vague_prompt = "Suggest an activity for university students."
print("--- [1] VAGUE PROMPT ---")
print(ask_gemini(vague_prompt).strip())

# 2. A specific prompt with venue, audience, and constraints
specific_prompt = (
    "Suggest a 30-minute icebreaker for 40 first-semester CS students at "
    "COMSATS University Wah. Zero budget, classroom setting, learn names."
)
print("\n--- [2] SPECIFIC PROMPT ---")
print(ask_gemini(specific_prompt).strip())
