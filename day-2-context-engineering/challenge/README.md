# 🏆 Day 2 Capstone Challenge: Context-Grounded Campus Assistant

Welcome to your **Day 2 Capstone Challenge**!  
Today, you will build a complete, transparent, grounded **Campus Event Assistant** in Python using Google Gemini and our verified campus dataset.

---

## 🎯 Learning Objective
Synthesize your context engineering skills—loading structured datasets, implementing transparent local retrieval, constructing grounded prompts with refusal guardrails, executing live Gemini API calls, and gracefully handling missing information.

---

## 📁 Dataset Reference
Your assistant queries [`day-2-context-engineering/data/campus_events.json`](../data/campus_events.json), containing 6 verified fictional event records:
1. `EVT-001`: Python for Absolute Beginners Workshop
2. `EVT-002`: Interactive Prompt & Context Engineering Bootcamp
3. `EVT-003`: Wah SpeedCode Hackathon 2026
4. `EVT-004`: Git & GitHub Essentials for First-Semester Devs
5. `EVT-005`: Annual Inter-Departmental Futsal Cup 2026
6. `EVT-006`: Central Cafeteria & Library Renovation Notice

*(All dates, locations, and registration links are fictional teaching data).*

---

## 📋 Required System Behavior
Your Python program must:
1. **Accept a student question.**
2. **Perform local keyword retrieval:** Search `campus_events.json` and select only matching event notes.
3. **Display selected notes for transparency:** Print which event records were retrieved before sending them to the model.
4. **Construct a strictly grounded prompt:**
   - Instruct the model to answer *only* from the supplied notes.
   - Instruct the model to state `"Information unavailable in campus records"` if the context lacks the answer.
5. **Call the live Gemini API:** Execute a real API call using `ask_gemini()`.
6. **Gracefully handle errors:** Clearly report any network or quota errors without fabricating a fake answer.
7. **Test both scenarios:**
   - **Scenario A (Answerable):** A question whose answer exists in `campus_events.json` (e.g., *"Where is the SpeedCode Hackathon happening and how much is the fee?"*).
   - **Scenario B (Unanswerable):** A question about missing information (e.g., *"What time does the campus swimming pool or gym open?"*).

---

## 🚀 Step-by-Step Student Instructions
1. Open [`starter_code.py`](starter_code.py).
2. Complete the `retrieve_relevant_events()` function to filter events based on question keywords.
3. Complete the `build_grounded_prompt()` function enforcing strict context grounding.
4. Run your program against the live Gemini model:
   ```bash
   python day-2-context-engineering/challenge/starter_code.py
   ```
5. Test both Scenario A and Scenario B.
6. Answer the 5 Knowledge-Check Questions below in your script or notebook comments.

---

## 🧠 5 Knowledge-Check Questions (Answer in your submission)
1. **Q1:** Why must we display the retrieved notes before calling the model in a transparent AI system?
2. **Q2:** If a student asks about a "swimming pool", why should Gemini say "Information unavailable" instead of using its general world knowledge?
3. **Q3:** What happens if our keyword search fails to find an event because the student used a synonym (e.g. "football" instead of "futsal")?
4. **Q4:** What is the difference between Application-Side Caching and Google GenAI Provider-Side Context Caching?
5. **Q5:** Why does injecting 100 unrelated campus notices into every prompt degrade performance?

---

## 📄 Illustrative Sample Output
> *Illustrative output — actual Gemini responses may vary.*

```text
======================================================================
  GDGoC CUI Wah — Day 2 Capstone: Context-Grounded Campus Assistant
======================================================================

[TEST 1: ANSWERABLE QUESTION]
Student Query: "Where is the SpeedCode Hackathon happening and how much is the fee?"

>> [TRANSPARENCY] Retrieved 1 relevant event record(s):
   - [EVT-003] Wah SpeedCode Hackathon 2026 (Student Activity Center)

>> [LIVE GEMINI RESPONSE]:
The Wah SpeedCode Hackathon 2026 will take place in the Student Activity Center (SAC) on the Ground Floor at CUI Wah. The registration fee is PKR 500 per team.

======================================================================
[TEST 2: UNANSWERABLE QUESTION]
Student Query: "What time does the campus swimming pool open on weekends?"

>> [TRANSPARENCY] Retrieved 0 relevant event record(s):
   (No keyword matches found in campus_events.json)

>> [LIVE GEMINI RESPONSE]:
Information unavailable in campus records. None of the provided event records mention a campus swimming pool or weekend pool hours.
```

---

## 📊 Grading Rubric (10 Points Total)

| Criterion | Points | Description |
| :--- | :---: | :--- |
| **Question Handling** | **1 pt** | Program cleanly accepts and processes incoming questions. |
| **Relevant Note Retrieval** | **2 pts** | Programmatically filters `campus_events.json` and prints retrieved records for transparency. |
| **Proper Context Construction** | **2 pts** | Prompt cleanly packages retrieved facts and includes strict grounding and refusal directives. |
| **Real Gemini API Call** | **2 pts** | Makes an actual API call via `ask_gemini()`, handling exceptions cleanly without mocks. |
| **Missing-Information Handling** | **2 pts** | AI accurately refuses to invent answers when asked about unrecorded campus facilities. |
| **Code Readability & Reflection** | **1 pt** | Clean, well-commented Python code with completed knowledge-check responses. |
