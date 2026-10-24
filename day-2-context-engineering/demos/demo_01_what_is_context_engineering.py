"""Topic 01: What Is Context Engineering? (With vs Without Context)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

question = "Where and at what time is the AI Robotics Workshop happening at CUI Wah?"

# 1. Asking without context
print("--- [1] WITHOUT CONTEXT ---")
print(ask_gemini(question).strip()[:180] + "...\n")

# 2. Asking with injected verified context
notice = "Robotics Workshop: Nov 18, 11:30 AM in Electrical Lab 02, Block 1, CUI Wah."
prompt = f"Use ONLY this notice to answer:\n{notice}\n\nQuestion: {question}"

print("--- [2] WITH GROUNDED CONTEXT ---")
print(ask_gemini(prompt).strip())
