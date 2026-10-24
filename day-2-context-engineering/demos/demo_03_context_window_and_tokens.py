"""Topic 03: Context Window & Token Limits"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

question = "When does registration close for the Python workshop?"

# Lean context (Only the essential facts)
lean_ctx = "Python Workshop: Nov 05 in CS Lab 03. Registration deadline: Nov 03."

# Bloated context (Unnecessary cafeteria and shuttle bus notices)
bloated_ctx = (
    "Notice 1: Cafeteria closed. Notice 2: Futsal tournament. "
    "Notice 3: Python Workshop Nov 05, deadline Nov 03 in Lab 03. "
    "Notice 4: Library study hall relocated. Notice 5: Shuttle bus timings."
)

print(f"Lean text:    {len(lean_ctx)} characters (~{len(lean_ctx)//4} tokens)")
print(f"Bloated text: {len(bloated_ctx)} characters (~{len(bloated_ctx)//4} tokens)")

print("\n--- [RESPONSE WITH LEAN CONTEXT] ---")
print(ask_gemini(f"Context: {lean_ctx}\nQuestion: {question}").strip())
