"""Topic 07: Prompt Improvement (Weak vs Constrained)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# 1. Weak Prompt (vague, causes hallucinations)
weak = "Write a post for GDGoC."
print("--- [1] WEAK PROMPT OUTPUT ---")
print(ask_gemini(weak).strip()[:200] + "...\n")

# 2. Constrained Prompt (Role, facts, word limit)
constrained = (
    "Role: GDGoC CUI Wah Social Lead.\n"
    "Event: Python for Absolute Beginners | Date: Nov 05 | Lab: CS Lab 03 | Fee: Free.\n"
    "Constraints: Under 70 words, 3 emoji bullet points, 1 registration link placeholder."
)
print("--- [2] CONSTRAINED PROMPT OUTPUT ---")
print(ask_gemini(constrained).strip())
