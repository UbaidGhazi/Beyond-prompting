# 🔑 Instructor Guide: Day 2 Answer Key & Discussion Guide

---

## 🧭 Teaching Philosophy Reminder
> **Crucial Rule:** In Day 2, emphasize the shift from *crafting words* to *engineering data pipelines*.  
> Students should realize that models don't fail because they are "dumb"; they fail because developers feed them incomplete, stale, or noisy context!

---

## 📝 Topic-by-Topic Exercise Answer Key

### Topic 01: What Is Context Engineering?
- **Expected Student Insight:** A prompt tells the model what action to perform; context supplies the ground truth data. Without context, an LLM cannot know private campus facts created after its training cutoff.

### Topic 02: Prompt vs Context
- **Expected Student Insight:** Holding the user instruction constant while changing the context proves that the model is conditioned by external evidence. Changing data does not require rewriting prompts or retraining models.

### Topic 03: Context Window & Tokens
- **Expected Student Insight:** 1 token $\approx$ 4 characters in English. Context windows are hard upper limits. Cramming unneeded documents wastes API quota, increases response time, and causes the model to overlook critical facts ("Lost in the Middle").

### Topic 04: Selecting Relevant Information
- **Expected Student Insight:** Raw databases contain thousands of records. Programmatically filtering for relevant records in Python before calling the LLM saves 70–90% of token volume while maintaining 100% accuracy.

### Topic 05: Context Compression & Summarization
- **Expected Student Insight:** Compressing 20-page documents into 4 bullet points enables fast, cheap downstream QA. However, compression is lossy; fine-grained details (like exceptions or minor rules) can be lost.

### Topic 06: Conversation History, Memory, and State
- **Expected Student Insight:** Modern LLM APIs are stateless HTTP endpoints. When a chatbot seems to "remember" a user's name across turns, it is because developer code saved the state in a local variable/database and re-injected it into the prompt.

### Topic 07: Mini-RAG & Grounded Generation
- **Expected Student Insight:** RAG connects external search with LLM generation. When a student asks about missing facilities (like a campus swimming pool), a properly grounded prompt forces the model to admit *"Information unavailable in records"* rather than inventing imaginary details.

### Topic 08: Tools & External Information
- **Expected Student Insight:** LLMs cannot directly access live university databases. A Python function (tool) executes the database query and passes the dynamic output into the model's context.

### Topic 09: Context Efficiency & Caching
- **Expected Student Insight:** Application-side caching stores previous responses in a local key-value store. Recurring student questions can be answered in under 1 millisecond with zero API tokens consumed.

### Topic 10: The Production AI Workflow
- **Expected Student Insight:** Production AI combines non-AI deterministic code (regex, string searches, schema validation) with probabilistic LLM generation. If an AI output fails validation, the pipeline intercepts the error before delivery.

---

## 🏆 Day 2 Capstone Challenge Reference Rubric (10 Points)

1. **Question Handling (1 Point):**
   - *1 pt:* Program cleanly receives and logs the student's question.

2. **Relevant Note Retrieval (2 Points):**
   - *2 pts:* Correctly searches `campus_events.json`, finds matching records, and prints retrieved notes for transparency.
   - *1 pt:* Retrieval logic is hardcoded or missing case-insensitivity.
   - *0 pts:* Retrieval fails or dumps all records indiscriminately.

3. **Proper Context Construction (2 Points):**
   - *2 pts:* Packages event fields cleanly and incorporates strict grounding directives (refuse to extrapolate).
   - *1 pt:* Context formatted poorly or missing refusal directive.
   - *0 pts:* Context not injected.

4. **Real Gemini API Call (2 Points):**
   - *2 pts:* Calls `ask_gemini()` with appropriate temperature (0.1–0.3) and handles errors cleanly without mocks.
   - *1 pt:* Makes API call but crashes on network failure.
   - *0 pts:* Does not execute live API call.

5. **Missing-Information Handling (2 Points):**
   - *2 pts:* Model accurately states "Information unavailable in campus records" when asked about the swimming pool.
   - *1 pt:* Model gives a hesitant or partially hallucinated answer.
   - *0 pts:* Model completely hallucinates fictional swimming pool hours.

6. **Code Readability & Reflection (1 Point):**
   - *1 pt:* Well-commented Python code with thoughtful responses to the 5 Knowledge-Check questions.
