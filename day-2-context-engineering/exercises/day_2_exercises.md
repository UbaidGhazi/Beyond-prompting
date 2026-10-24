# 🏋️ Day 2 Exercises & Interactive Lab Games

Welcome to the hands-on practice arena for Day 2: Context Engineering!  
These lab games and exercises will cement your understanding of grounding, retrieval, token budgeting, and caching.

---

## 🔍 Game 1: The Context Detective (20 Minutes)
**Objective:** Select the absolute smallest subset of campus notes needed to answer a student's inquiry, measuring character reduction.

### Scenario:
You have all 6 events from `campus_events.json` (Python, AI Bootcamp, SpeedCode, Git, Futsal, Cafeteria Notice).  
**Student Question:** *"What are the prerequisites for participating in the SpeedCode Hackathon?"*

### Challenge Tasks:
1. Identify which single event record is needed (`EVT-003`).
2. Write a 2-line Python snippet to extract only `EVT-003["prerequisites"]`.
3. Compute the token reduction compared to sending all 6 records!
4. Send the minimal context to Gemini and verify it answers in under 20 words.

---

## 🚫 Game 2: The Missing-Information Challenge (15 Minutes)
**Objective:** Test whether your grounded prompt can resist hallucination when asked trick questions about campus life.

### Student Task:
Send these three trick questions to your Day 2 assistant:
1. *"What is the WiFi password for the central campus cafeteria?"*
2. *"Can 1st-semester students borrow laptops from the departmental library?"*
3. *"Is there a swimming competition at CUI Wah this semester?"*

### Success Condition:
In all 3 cases, Gemini must declare that **information is unavailable in verified campus records**, rather than guessing plausible WiFi passwords or library rules!

---

## ⚡ Game 3: The Cache Challenge (15 Minutes)
**Objective:** Prove to your lab partner that an application-side cache eliminates API network calls.

### Steps:
1. Run `day-2-context-engineering/demos/demo_09_context_efficiency_and_caching.py`.
2. Inspect the elapsed time for Request 1 vs Request 2.
3. Modify the question by adding a single extra space at the end.
4. Explain to your partner why whitespace normalization (`.strip().lower()`) is essential for reliable cache keys!

---

## ✍️ Individual Practice Exercises

### Exercise 2.1: Semantic Keyword Search Extension
Open `starter_code.py` in the Day 2 challenge.  
Currently, if a student searches for *"football"*, the keyword search fails because the record says *"futsal"*.  
**Task:** Add a small synonym mapping dictionary in Python:
```python
SYNONYMS = {
    "football": "futsal",
    "soccer": "futsal",
    "coding": "python",
    "git": "github"
}
```
Update `retrieve_relevant_events` to expand query keywords using this mapping and verify that searching *"Where is the football match?"* successfully retrieves the Futsal Cup event!

### Exercise 2.2: The Timetable Tool Extension
In `demo_08_tools_and_external_context.py`, add a second simulated schedule:
- Course: `CSC103 (Object Oriented Programming)`
- Day: `Tuesday 10:00 AM - 11:30 AM` in `Academic Block 1, Room 104`.
Test your tool by querying Gemini for CSC103!
