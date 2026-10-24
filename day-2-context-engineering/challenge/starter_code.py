"""
starter_code.py
===============
Day 2 Capstone Challenge: Context-Grounded Campus Assistant
GDGoC CUI Wah — 2-Day AI Bootcamp

STUDENT NAME: [Enter Your Name Here]
STUDENT REGISTRATION: [e.g. SP26-BCS-000]

INSTRUCTIONS:
1. Load `campus_events.json` from the `data/` directory.
2. Complete `retrieve_relevant_events()` to filter events by keyword.
3. Complete `build_grounded_prompt()` enforcing strict context grounding.
4. Run live Gemini API calls for both Answerable and Unanswerable questions.
5. Answer the 5 Knowledge-Check questions at the bottom of this file.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ai_helper import ask_gemini

# Load the verified campus events dataset
DATA_PATH = REPO_ROOT / "day-2-context-engineering" / "data" / "campus_events.json"


def load_dataset() -> list:
    """Loads the 6 verified campus event records."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Cannot find dataset at {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve_relevant_events(query: str, events: list) -> list:
    """
    TODO: Build simple keyword retrieval.
    1. Extract keywords from `query` (words longer than 3 characters, lowercase).
    2. Check if any keyword appears in the event's 'title', 'description', or 'category'.
    3. Return the list of matching event dictionaries.
    """
    # --- STUDENT EDIT START ---
    keywords = [word.lower() for word in query.split() if len(word) > 3]
    matches = []
    for evt in events:
        searchable_text = f"{evt['title']} {evt['description']} {evt['category']} {evt['venue']}".lower()
        if any(kw in searchable_text for kw in keywords):
            matches.append(evt)
    return matches
    # --- STUDENT EDIT END ---


def build_grounded_prompt(query: str, retrieved_events: list) -> str:
    """
    TODO: Construct a strictly grounded prompt.
    1. Format each retrieved event with its title, date, venue, fee, and details.
    2. If retrieved_events is empty, indicate that no records matched.
    3. Include strict instructions:
       - Answer ONLY from the provided notes.
       - If the information is not present, state: 'Information unavailable in campus records.'
       - Do not guess or hallucinate.
    """
    # --- STUDENT EDIT START ---
    if retrieved_events:
        context_blocks = []
        for e in retrieved_events:
            block = (
                f"- Event ID: {e['id']}\n"
                f"  Title: {e['title']}\n"
                f"  Date: {e['date']} ({e.get('time', 'N/A')})\n"
                f"  Venue: {e['venue']}\n"
                f"  Fee: {e.get('fee', 'N/A')}\n"
                f"  Details: {e['description']}\n"
            )
            context_blocks.append(block)
        context_str = "\n".join(context_blocks)
    else:
        context_str = "[No matching event records found in campus dataset]"

    prompt = (
        "You are the official GDGoC CUI Wah Campus Assistant.\n"
        "STRICT GROUNDING DIRECTIVES:\n"
        "1. Base your answer EXCLUSIVELY on the verified Campus Records below.\n"
        "2. If the answer cannot be found in the records, state: "
        "'Information unavailable in campus records.'\n"
        "3. Do not assume or extrapolate details not explicitly documented.\n\n"
        f"Verified Campus Records:\n{context_str}\n\n"
        f"Student Query: {query}\n"
        "Assistant Response:"
    )
    return prompt
    # --- STUDENT EDIT END ---


def answer_student_query(query: str, events: list):
    print("\n" + "=" * 70)
    print(f"Student Query: \"{query}\"")

    # Step 1: Retrieval
    matched = retrieve_relevant_events(query, events)
    print(f"\n>> [TRANSPARENCY] Retrieved {len(matched)} relevant event record(s):")
    if matched:
        for m in matched:
            print(f"   - [{m['id']}] {m['title']} | Venue: {m['venue']}")
    else:
        print("   (No matching records found in dataset)")

    # Step 2: Prompt Construction
    prompt = build_grounded_prompt(query, matched)

    # Step 3: Live Gemini Model Call
    print("\n>> Calling Google Gemini API...")
    try:
        response = ask_gemini(prompt=prompt, temperature=0.1)
        print("\n>> [LIVE GEMINI RESPONSE]:")
        print(response.strip())
    except Exception as err:
        print(f"\n>> [API ERROR] Could not complete request: {err}")


def main():
    print("=" * 70)
    print("  GDGoC CUI Wah — Day 2 Capstone: Context-Grounded Campus Assistant")
    print("=" * 70)

    events = load_dataset()
    print(f"Loaded {len(events)} verified campus event records from JSON.")

    # Test Scenario A: Answerable Query
    q_answerable = "Where is the SpeedCode Hackathon happening and how much is the fee?"
    answer_student_query(q_answerable, events)

    # Test Scenario B: Unanswerable Query (Missing Information)
    q_unanswerable = "What time does the campus swimming pool or gym open on weekends?"
    answer_student_query(q_unanswerable, events)

    print("\n" + "=" * 70)
    print("Challenge complete! Don't forget to answer the Knowledge-Check questions below.")


if __name__ == "__main__":
    main()

"""
================================================================================
STUDENT KNOWLEDGE-CHECK RESPONSES:
Q1: Why must we display the retrieved notes before calling the model in a transparent AI system?
Answer: [Your response here]

Q2: If a student asks about a "swimming pool", why should Gemini say "Information unavailable" instead of using its general world knowledge?
Answer: [Your response here]

Q3: What happens if our keyword search fails to find an event because the student used a synonym (e.g. "football" instead of "futsal")?
Answer: [Your response here]

Q4: What is the difference between Application-Side Caching and Google GenAI Provider-Side Context Caching?
Answer: [Your response here]

Q5: Why does injecting 100 unrelated campus notices into every prompt degrade performance?
Answer: [Your response here]
================================================================================
"""
