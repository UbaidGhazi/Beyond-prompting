"""Topic 05: System Instructions vs User Prompts"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Same user question
user_question = "Explain what a Python for loop is in 2 sentences."

# Persona 1: Strict Professor
system_prof = "You are a strict CS professor. Be formal, concise, and academic."
print("--- [1] STRICT PROFESSOR PERSONA ---")
print(ask_gemini(user_question, system_instruction=system_prof).strip())

# Persona 2: Friendly Roman Urdu Senior
system_urdu = "Aap CUI Wah ke friendly senior ho. Roman Urdu mein canteen ki misaal de kar samjhao."
print("\n--- [2] ROMAN URDU SENIOR MENTOR ---")
print(ask_gemini(user_question, system_instruction=system_urdu).strip())
