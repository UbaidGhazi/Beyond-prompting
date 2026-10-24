"""
solution.py
===========
Day 2 Capstone Challenge: Instructor Reference Solution
GDGoC CUI Wah — 2-Day AI Bootcamp

Demonstrates an exemplar, production-grade Context-Grounded Campus Assistant:
1. Clean dataset loading and error handling.
2. Transparent programmatic keyword retrieval with case-insensitive tokenization.
3. Strict grounding prompt that suppresses hallucinations and guarantees polite refusals.
4. Genuine Google Gemini API interaction with clear error pathways.
5. Complete answer key for the 5 Knowledge-Check questions.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ai_helper import ask_gemini

DATA_PATH = REPO_ROOT / "day-2-context-engineering" / "data" / "campus_events.json"


def load_dataset() -> list:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset missing at {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve_relevant_events(query: str, events: list) -> list:
    """Case-insensitive keyword retrieval across title, category, venue, and description."""
    keywords = [w.lower() for w in query.replace("?", "").replace(",", "").split() if len(w) > 3]
    matches = []
    for evt in events:
        blob = f"{evt['title']} {evt['category']} {evt['venue']} {evt['description']}".lower()
        if any(kw in blob for kw in keywords):
            matches.append(evt)
    return matches


def build_grounded_prompt(query: str, retrieved_events: list) -> str:
    """Packages retrieved records with bulletproof grounding and refusal directives."""
    if retrieved_events:
        blocks = []
        for e in retrieved_events:
            blocks.append(
                f"[ID: {e['id']}] {e['title']}\n"
                f"  Category: {e['category']} | Date: {e['date']} ({e.get('time', 'N/A')})\n"
                f"  Venue: {e['venue']}\n"
                f"  Target Audience: {e['target_audience']}\n"
                f"  Fee: {e.get('fee', 'N/A')} | Deadline: {e.get('registration_deadline', 'N/A')}\n"
                f"  Link: {e.get('registration_link', 'N/A')}\n"
                f"  Description: {e['description']}"
            )
        records_context = "\n\n".join(blocks)
    else:
        records_context = "[NO MATCHING RECORDS LOCATED IN CAMPUS DATABASE]"

    return (
        "You are the official CUI Wah Campus Event Concierge.\n"
        "STRICT GROUNDING DIRECTIVES (MANDATORY):\n"
        "1. You must answer the student's question EXCLUSIVELY using facts from the Verified Campus Records below.\n"
        "2. If the question asks for information not explicitly documented in the records, reply strictly:\n"
        "   'Information unavailable in verified campus records.'\n"
        "3. Never guess, extrapolate, or invent details regarding unverified facilities or dates.\n\n"
        f"Verified Campus Records:\n{records_context}\n\n"
        f"Student Query: {query}\n"
        "Answer:"
    )


def process_query(query: str, events: list):
    print("\n" + "=" * 70)
    print(f"Student Query: \"{query}\"")

    # Step 1: Retrieval
    matched = retrieve_relevant_events(query, events)
    print(f"\n>> [TRANSPARENCY] Retrieved {len(matched)} relevant event record(s):")
    for m in matched:
        print(f"   - [{m['id']}] {m['title']} (Venue: {m['venue']})")

    # Step 2: Grounded Prompt Construction
    prompt = build_grounded_prompt(query, matched)

    # Step 3: Live Gemini Model Call
    print("\n>> Executing Live Gemini API Call...")
    try:
        response = ask_gemini(prompt=prompt, temperature=0.1)
        print("\n>> [LIVE GEMINI RESPONSE]:")
        print(response.strip())
    except Exception as err:
        print(f"\n>> [API ERROR] Request failed: {err}")


def main():
    print("=" * 70)
    print("  GDGoC CUI Wah — Day 2 Challenge: Instructor Reference Solution")
    print("=" * 70)

    events = load_dataset()
    print(f"Loaded {len(events)} campus records successfully.")

    # 1. Answerable Test
    process_query("Where is the SpeedCode Hackathon happening and how much is the fee?", events)

    # 2. Unanswerable Test
    process_query("What time does the campus swimming pool open on weekends?", events)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

"""
================================================================================
INSTRUCTOR ANSWER KEY FOR 5 KNOWLEDGE-CHECK QUESTIONS:

Q1: Why must we display retrieved notes before calling the model?
Answer: Transparency and auditability. It allows students and engineers to see
what factual evidence the model was given, separating retrieval errors (finding
the wrong document) from generation errors (misreading the document).

Q2: Why should Gemini say 'Information unavailable' for a swimming pool question?
Answer: To prevent hallucinations! If the model uses general internet knowledge,
it might invent plausible-sounding pool hours for a campus that doesn't even have
a swimming pool, misleading students.

Q3: What happens if keyword search misses a synonym like 'football' for 'futsal'?
Answer: The retrieval step returns 0 matches, and the model truthfully states
'Information unavailable'. This illustrates the limitation of lexical search
and motivates semantic vector search (embeddings).

Q4: What is the difference between Application-Side Caching and Provider Caching?
Answer: Application-Side Caching stores full prompt responses in local memory/Redis
to bypass the API entirely (0ms latency, free). Provider Caching (Gemini SDK)
caches large context prefixes (32k+ tokens) on Google's cloud to reduce input token
costs during subsequent model inferences.

Q5: Why does injecting 100 unrelated campus notices degrade performance?
Answer: It inflates token costs, increases latency, dilutes model attention,
and increases the probability of 'Lost in the Middle' retrieval degradation.
================================================================================
"""
