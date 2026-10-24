"""Topic 03: Zero-Shot vs Few-Shot Prompting"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Fictional message to categorize
message = "Can a software house sponsor energy drinks for the hackathon?"

# 1. Zero-Shot (Task only, no examples)
zero_shot = f"Classify into [REGISTRATION], [VENUE], or [SPONSORSHIP]:\n{message}"
print("--- [1] ZERO-SHOT OUTPUT ---")
print(ask_gemini(zero_shot, temperature=0.1).strip())

# 2. Few-Shot (With 2 pattern examples)
few_shot = (
    "Classify into: [REGISTRATION], [VENUE], [SPONSORSHIP]\n\n"
    "Example 1: 'Where is Lab 03?' -> [VENUE]\n"
    "Example 2: 'I filled the form' -> [REGISTRATION]\n\n"
    f"Message: '{message}'\nCategory:"
)
print("\n--- [2] FEW-SHOT OUTPUT ---")
print(ask_gemini(few_shot, temperature=0.1).strip())
