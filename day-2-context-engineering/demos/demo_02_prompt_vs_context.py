"""Topic 02: Prompt vs Context (Holding Question Constant)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# The question stays identical
question = "What is the registration fee and deadline for the hackathon?"

# Context A
ctx_a = "Event: SpeedCode Hackathon 2026. Fee: PKR 500. Deadline: Nov 16. Venue: SAC."
print("--- [1] EVALUATING WITH CONTEXT A ---")
print(ask_gemini(f"Context:\n{ctx_a}\nQuestion: {question}").strip())

# Context B
ctx_b = "Event: DataHack 2026. Fee: Free (sponsored). Deadline: Dec 05. Venue: Auditorium."
print("\n--- [2] EVALUATING WITH CONTEXT B ---")
print(ask_gemini(f"Context:\n{ctx_b}\nQuestion: {question}").strip())
