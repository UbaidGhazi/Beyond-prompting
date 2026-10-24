"""Topic 07: Mini-RAG & Grounded Generation"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Campus database
RECORDS = [
    {"id": "REC-01", "text": "Git workshop is on Nov 27 in CS Lab 05 at 2 PM. Free entry."},
    {"id": "REC-02", "text": "SpeedCode Hackathon is on Nov 20 in the SAC. Fee is PKR 500."}
]

def mini_rag(query: str) -> str:
    # 1. Retrieve
    matched = [r["text"] for r in RECORDS if any(w in r["text"].lower() for w in query.lower().split() if len(w) > 3)]
    ctx = "\n".join(matched) if matched else "No records found"
    
    # 2. Augment with strict grounding rule
    prompt = (
        "Answer ONLY using this context. If not present, state 'Information unavailable'.\n\n"
        f"Context:\n{ctx}\n\nQuestion: {query}"
    )
    # 3. Generate
    return ask_gemini(prompt, temperature=0.1).strip()

print("--- [1] ANSWERABLE QUESTION ---")
print(mini_rag("When is the Git workshop and which lab is it in?"))

print("\n--- [2] UNANSWERABLE QUESTION (Missing from records) ---")
print(mini_rag("What time does the campus swimming pool open?"))
