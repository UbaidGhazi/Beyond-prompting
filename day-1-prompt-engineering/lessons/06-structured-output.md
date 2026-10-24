# Lesson 06: Structured Output (JSON Generation & Validation)

---

## 1. Learning Goal
By the end of this lesson, you will learn how to compel Google Gemini to return machine-readable structured formats (specifically JSON), how to configure `response_mime_type="application/json"`, and how to programmatically parse and validate fields in Python.

---

## 2. Definition in Simple English
When an AI outputs unstructured paragraphs, it is easy for human eyes to read, but difficult for software applications to store in a database or render in an app.  
**Structured Output** is text constrained to standard data serialization formats—such as **JSON** (JavaScript Object Notation), markdown tables, or key-value pairs—that can be parsed directly into Python dictionaries or lists. Rather than hoping the model does not include conversational introductory text (like *"Sure, here is your JSON:"*), modern SDKs support schema constraints that enforce syntactic JSON generation at the decoding level.

---

## 3. Roman Urdu Explanation
*Agar aap AI se kaho: "Bhai mujhe event ki details do," toh woh lambi kahani likh dega: "Hey friends! Hum Friday ko event kar rahe hain...".*  
*Lekin agar aapko CUI Wah ke student portal ya mobile app mein yeh data save karna ho, toh kahani kaam nahi aayegi. App ko chahiye key-value data: jaise `date`, `venue`, aur `title`.*  
*Google GenAI SDK mein `response_mime_type="application/json"` set karne se AI majboor ho jata hai ke woh faltu batein kiye baghair sirf aur sirf valid JSON return kare, jise Python foran `json.loads()` kar ke dictionary bana leta hai!*

---

## 4. Visual Diagram

### Concept Flowchart (Mermaid)
```mermaid
graph LR
    A[Structured Prompt: Keys & Types] --> B(Gemini API with JSON Mode)
    B --> C[Raw JSON String: '{...}']
    C --> D[Python json.loads]
    D --> E{Validation Check}
    E -->|All Keys Present| F[Valid Python Dict: Store / Render]
    E -->|Key Missing| G[Raise Schema Error]

    style A fill:#4285F4,stroke:#1a73e8,color:#fff
    style B fill:#1E293B,stroke:#334155,color:#fff
    style C fill:#FBBC05,stroke:#f29900,color:#1a1a2e
    style D fill:#673AB7,stroke:#512da8,color:#fff
    style F fill:#34A853,stroke:#137333,color:#fff
    style G fill:#EA4335,stroke:#c5221f,color:#fff
```

### Standalone Architectural Diagram
![Topic 06 Diagram](../diagrams/topic_06_structured_output.svg)

---

## 5. Campus-Based Practical Example
Imagine you are building a campus notification bot for **GDGoC CUI Wah**. Your Python script fetches workshop info from Gemini and sends SMS alerts to enrolled students.
If the AI returns conversational text, your SMS script crashes! But if it returns:
```json
{
  "event_name": "Git Workshop",
  "venue": "CS Lab 05",
  "date": "2026-11-27"
}
```
Your script can easily extract `data["venue"]` and send: *"Reminder: See you at CS Lab 05!"*

---

## 6. Real AI Experiment
In this experiment:
1. We request an event record with explicit schema keys (`event_name`, `date`, `venue`, `target_semester`, `prerequisites`).
2. We pass `response_mime_type="application/json"` via the official SDK helper.
3. We feed the raw string into Python's `json.loads()` and inspect the resulting dictionary keys.

---

## 7. Complete Runnable Python Code
Run this demonstration from the repository root:
```bash
python day-1-prompt-engineering/demos/demo_06_structured_output.py
```

```python
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ai_helper import ask_gemini

prompt = (
    "Generate a structured JSON record for an introductory campus workshop at "
    "COMSATS University Wah. Include exactly these JSON keys:\n"
    "  - \"event_name\": string\n"
    "  - \"date\": string (YYYY-MM-DD)\n"
    "  - \"venue\": string (specific CUI Wah lab)\n"
    "  - \"target_semester\": integer (e.g. 1 or 2)\n"
    "  - \"prerequisites\": list of strings\n"
    "Return ONLY the JSON object."
)

# Call Gemini with JSON MIME type configuration
raw_json = ask_gemini(
    prompt=prompt,
    response_mime_type="application/json",
    temperature=0.3
)

print("--- [RAW API STRING] ---")
print(raw_json.strip())

# Parse with Python
data = json.loads(raw_json)

# Validate required schema fields
required = ["event_name", "date", "venue", "target_semester", "prerequisites"]
missing = [k for k in required if k not in data]

if not missing:
    print("\n[VALIDATION SUCCESS] All required fields verified:")
    print(f"Title: {data['event_name']} | Lab: {data['venue']}")
else:
    print(f"\n[VALIDATION FAILED] Missing keys: {missing}")
```

---

## 8. Illustrative Sample Output
> *Illustrative output — actual Gemini responses may vary.*

```text
--- [RAW API STRING] ---
{
  "event_name": "Python for Freshers: From Zero to Logic",
  "date": "2026-11-05",
  "venue": "CS Lab 03, Academic Block 2, CUI Wah",
  "target_semester": 1,
  "prerequisites": [
    "Personal laptop",
    "Python 3.11+ installed",
    "Curiosity to learn"
  ]
}

[VALIDATION SUCCESS] All required fields verified:
Title: Python for Freshers: From Zero to Logic | Lab: CS Lab 03, Academic Block 2, CUI Wah
```

---

## 9. What the Code Does
1. Sets `response_mime_type="application/json"` in the API configuration. This activates constrained decoding so Gemini produces strict JSON without markdown backticks or conversational filler.
2. Uses Python's native `json.loads(...)` to parse the string into an in-memory dictionary.
3. Implements deterministic validation by looping over `required_keys`. If an expected key is missing, it alerts the developer instead of crashing silently.

---

## 10. Try It Yourself
Exercise: Write a prompt that requests a **3-Item Programming Study Plan** in JSON format:
```json
{
  "subject": "Programming Fundamentals (CSC101)",
  "study_sessions": [
    {"topic": "...", "duration_minutes": 45, "practice_exercise": "..."}
  ]
}
```
Run it in Python and verify that `len(data["study_sessions"]) == 3`.

---

## 11. Reflection Question
What is the danger of relying purely on prompt instructions like *"Please only output JSON, don't say anything else"* without SDK-level configuration or Python validation?  
*(Hint: What happens if the model writes "Sure! Here is the JSON: ```json ... ```"? Will `json.loads` succeed?)*
