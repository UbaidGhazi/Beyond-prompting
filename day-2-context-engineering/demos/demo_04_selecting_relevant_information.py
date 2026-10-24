"""Topic 04: Selecting Relevant Information (Filtering Signal from Noise)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Campus database of notices
NOTICES = [
    {"id": "N1", "title": "Futsal Cup", "text": "Futsal starts Dec 02 at campus grounds."},
    {"id": "N2", "title": "Python Workshop", "text": "Python workshop in Lab 03 on Nov 05. Free entry."},
    {"id": "N3", "title": "Library Notice", "text": "Library digital lab relocated to Seminar Room A."}
]

# Simple Python filter: match keywords
def filter_notices(query, notices):
    keywords = [w.lower() for w in query.split() if len(w) > 3]
    return [n for n in notices if any(kw in n["text"].lower() for kw in keywords)]

query = "Where is the Python workshop happening and is there a fee?"
selected = filter_notices(query, NOTICES)

print(f"Filtered {len(selected)} of {len(NOTICES)} notices: {[s['id'] for s in selected]}")
ctx = selected[0]["text"] if selected else "No records found"

print("\n--- [GEMINI RESPONSE WITH FILTERED CONTEXT] ---")
print(ask_gemini(f"Context: {ctx}\nQuestion: {query}").strip())
