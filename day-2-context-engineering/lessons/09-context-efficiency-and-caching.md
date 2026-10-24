# Lesson 09: Context Efficiency and Application Caching

---

## 1. Learning Goal
By the end of this lesson, you will understand how **Application-Side Response Caching** eliminates redundant AI calls, speeds up campus applications by hundreds of times, and saves precious API quota. You will also understand how application caching differs from **Provider-Side Context Caching**.

---

## 2. Definition in Simple English
When hundreds of university students ask the exact same recurring question (e.g., *"When is the programming quiz?"* or *"Where is Lab 03?"*), repeatedly making live API calls to Google's servers wastes money, burns rate limits, and adds unnecessary internet latency.  
- **Application-Side Response Caching:** Storing previously generated responses in a local key-value store (such as a Python dictionary or Redis database) keyed by a hash of the prompt. If an identical query arrives, your server immediately returns the stored answer without contacting Gemini.
- **Provider-Side Context Caching (Google GenAI):** Server-side caching on Google's cloud infrastructure for extremely large reference documents (such as whole codebases or 500-page textbooks). This feature typically requires minimum token thresholds (e.g., 32,768+ tokens) and specific account tiers.

---

## 3. Roman Urdu Explanation
*Caching ko samajhne ke liye CUI Wah ke photocopy shop ki misaal lein:*  
*Jab class ke 50 bache baari baari aate hain aur kehte hain: "Bhai, Programming Fundamentals ki assignment 1 ka print do!"*  
*Agar photostate wala har bache ke liye teacher ko call kare aur bole: "Sir assignment ki nayi copy email karein"—toh kitna waqt zaya hoga?*  
*Photostate wala kya karta hai? Pehli baar print nikal kar ek master copy apne paas draz (drawer) mein rakh leta hai. Agla jo bhi bacha aata hai, woh seedha draz se nikaal kar foran thama deta hai!*  
*Ise **Cache Hit** kehte hain. Internet ki zero latency aur zero API cost!*

---

## 4. Visual Diagram

### Concept Flowchart (Mermaid)
```mermaid
graph TD
    A[Student Query: 'Where is Lab 03?'] --> B[Calculate Prompt Hash]
    B --> C{Key in Local CACHE_STORE?}
    C -->|Yes: CACHE HIT| D[Instant Local Return (0.001s, 0 Tokens)]
    C -->|No: CACHE MISS| E(Call Gemini 2.5 Flash API)
    E --> F[Store in CACHE_STORE]
    F --> G[Return Live Response to Student (1.2s)]

    style A fill:#4285F4,stroke:#1a73e8,color:#fff
    style B fill:#1E293B,stroke:#334155,color:#fff
    style C fill:#FBBC05,stroke:#f29900,color:#1a1a2e
    style D fill:#34A853,stroke:#137333,color:#fff
    style E fill:#EA4335,stroke:#c5221f,color:#fff
    style G fill:#dcfce7,stroke:#22c55e,color:#166534
```

### Standalone Architectural Diagram
![Day 2 Topic 09 Diagram](../diagrams/topic_09_caching_flow.svg)

---

## 5. Campus-Based Practical Example
During registration week for the **GDGoC Python Bootcamp**, over 200 students ask the bot:  
`"Do I need to bring my own laptop to the workshop?"`
- Without caching: Your bot makes 200 separate internet requests to Google Gemini, risking a `429 Rate Limit Exceeded` error.
- With caching: The 1st student triggers a live API call (Cache Miss). The next 199 students receive the stored answer in under 1 millisecond (Cache Hit)!

---

## 6. Real AI Experiment
In this experiment, we execute 3 sequential requests:
1. **Request 1:** Query A (first time). Gemini is called via the internet (Cache Miss, ~1.2s latency).
2. **Request 2:** Query A again (duplicate). The response is served directly from local Python memory (Cache Hit, ~0.0001s latency).
3. **Request 3:** Query C (modified question). The cache detects a new prompt and makes a genuine API call.

---

## 7. Complete Runnable Python Code
Run this demonstration from the repository root:
```bash
python day-2-context-engineering/demos/demo_09_context_efficiency_and_caching.py
```

```python
import hashlib
import time
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ai_helper import ask_gemini

CACHE_STORE = {}

def cached_ask_gemini(prompt: str):
    key = hashlib.md5(prompt.strip().lower().encode("utf-8")).hexdigest()
    t0 = time.perf_counter()
    if key in CACHE_STORE:
        return CACHE_STORE[key], "CACHE_HIT", time.perf_counter() - t0
    res = ask_gemini(prompt, temperature=0.1)
    CACHE_STORE[key] = res
    return res, "CACHE_MISS", time.perf_counter() - t0

q1 = "What are the prerequisites for the GDGoC Git workshop at CUI Wah?"
q2 = "What are the prerequisites for the GDGoC Git workshop at CUI Wah?" # Duplicate

res1, status1, t1 = cached_ask_gemini(q1)
print(f"Request 1: [{status1}] in {t1:.3f}s")

res2, status2, t2 = cached_ask_gemini(q2)
print(f"Request 2: [{status2}] in {t2:.6f}s")
```

---

## 8. Illustrative Sample Output
> *Illustrative output — actual Gemini responses may vary.*

```text
Request 1: [CACHE_MISS (Generated via live Google Gemini API call)] in 1.185s
Response: The prerequisites for the Git workshop are a personal laptop and a free GitHub account...

Request 2: [CACHE_HIT (Served locally from Python memory)] in 0.000042s
Response: The prerequisites for the Git workshop are a personal laptop and a free GitHub account...
Speedup: ~28000x faster with 0 API tokens consumed!
```

---

## 9. What the Code Does
1. Uses MD5 hashing to create a deterministic lookup key for any incoming prompt.
2. Checks `key in CACHE_STORE` before calling `ask_gemini(...)`.
3. Measures and prints actual execution latency using `time.perf_counter()`, demonstrating instantaneous local response times on cache hits.

---

## 10. Try It Yourself
Exercise: What happens if a student asks:
- Query 1: *"Where is CS Lab 05?"*
- Query 2: *"where is cs lab 05?"* (all lowercase)
- Query 3: *"Where is CS Lab 05 located?"* (different wording)

Does Query 2 trigger a cache hit if we normalize text with `.strip().lower()`? Does Query 3 trigger a cache hit with an MD5 hash?

---

## 11. Reflection Question
What is the risk of caching responses indefinitely? If a workshop venue changes from CS Lab 03 to CS Lab 05, how should your application invalidate (clear) the cache?
