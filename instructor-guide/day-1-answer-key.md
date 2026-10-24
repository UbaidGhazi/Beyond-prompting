# 🔑 Instructor Guide: Day 1 Answer Key & Discussion Guide

---

## 🧭 Teaching Philosophy Reminder
> **Crucial Rule:** Never grade students on whether their AI's output matches an illustrative sample word-for-word!  
> LLMs are probabilistic token predictors. Two students submitting the identical prompt may receive slightly different wording.  
> **Grade students on:** prompt construction, presence of the 5 pillars, factual accuracy, adherence to constraints (e.g., word limits), and thoughtful reflection.

---

## 📝 Topic-by-Topic Exercise Answer Key

### Topic 01: What Is a Prompt?
- **Expected Student Insight:** Vague prompts force the model to hallucinate or default to broad training averages. Adding constraints anchors the model to the target audience (first-semester CS freshers at CUI Wah).
- **Instructor Tip:** Ask a student to read their vague output aloud. Then ask: *"Could this activity be done in CS Lab 03 in 30 minutes without money?"* The class will instantly grasp why specificity matters.

### Topic 02: Anatomy of a Good Prompt
- **Expected Student Insight:** Prompts with all 5 pillars (Role, Task, Context, Constraints, Format) produce copy that can be directly pasted into student WhatsApp groups without manual rewriting.
- **Grading Check:** Did the student include:
  1. Role (GDGoC Lead / Organizer)
  2. Task (Write announcement)
  3. Context (Date, Lab 05, CUI Wah)
  4. Constraints (Length ceiling, tone)
  5. Format (Headlines + Bullets)

### Topic 03: Zero-Shot vs Few-Shot Prompting
- **Expected Student Insight:** In Zero-Shot classification, models often output conversational pleasantries (*"The following message belongs to the category of..."*). Few-Shot examples suppress chatter and force exact syntax `[CATEGORY]`.
- **Discussion Prompt:** *"If you add an incorrect example in your prompt, what happens?"* (Demonstrate that the model will faithfully reproduce human errors—garbage in, garbage out!).

### Topic 04: Task Decomposition
- **Expected Student Insight:** Monolithic prompts result in rushed schedules with missing logistics. Decomposing into 3 sequential steps allows the human developer to inspect and approve the intermediate plan before generating the public announcement.
- **Trade-off Discussion:** Point out that 3 sequential API calls take ~3x longer and use more cumulative tokens than 1 monolithic prompt. Use decomposition when quality outweighs latency.

### Topic 05: System Instructions vs User Prompts
- **Expected Student Insight:** System instructions establish persistent boundaries and tone that apply across all interactions.
- **Code Check:** Ensure students passed `system_instruction` via the SDK parameter rather than simply appending text into the prompt.

### Topic 06: Structured Output (JSON)
- **Expected Student Insight:** Without `response_mime_type="application/json"`, models frequently wrap JSON in markdown backticks (```` ```json ````) or add conversational preamble, causing `json.loads()` to crash with a `JSONDecodeError`.
- **Code Check:** Ensure students ran Python validation checking that required keys (`event_name`, `venue`, `date`) exist in the parsed dictionary.

### Topic 07: Prompt Improvement
- **Expected Student Insight:** Prompt engineering is an iterative ladder. Adding constraints (word count limits, bullet structures) prevents verbosity.
- **Discussion:** Clarify that even a Level 3 constrained prompt cannot guarantee 100% factual accuracy without grounded context.

### Topic 08: Prompt Safety
- **Expected Student Insight:** LLMs cannot distinguish instructions from data unless explicit delimiters (e.g. `<student_note>...</student_note>`) and system rules are enforced.
- **Security Reality Check:** Emphasize to students that prompt isolation is an educational defense-in-depth step, not an unhackable firewall. In production systems, sensitive operations require programmatic permission checks.

---

## 🏆 Day 1 Capstone Challenge Reference Rubric (10 Points)

1. **Role & Task Clarity (2 Points):**
   - *2 pts:* Clearly states GDGoC Lead persona and specifies an announcement task.
   - *1 pt:* Vaguely specifies persona or task.
   - *0 pts:* Persona missing entirely.

2. **Accurate Campus Facts (2 Points):**
   - *2 pts:* Faithfully includes Git workshop, Friday Nov 27, 2 PM, CS Lab 05, and Free entry.
   - *1 pt:* Missing one key fact or minor hallucination.
   - *0 pts:* Multiple hallucinated facts.

3. **Audience, Tone & Length Constraints (2 Points):**
   - *2 pts:* Targets beginners, maintains encouraging tone, word count strictly within 90–130 words.
   - *1 pt:* Word count slightly off (e.g., 80 or 140 words) or tone slightly too formal.
   - *0 pts:* Wildly off-length or intimidating jargon.

4. **Clear Output Structure (2 Points):**
   - *2 pts:* Features Headline, Hook, Event Snapshot, 3 Takeaways, and CTA.
   - *1 pt:* Missing one structural section.
   - *0 pts:* Unstructured block paragraph.

5. **API Execution & Reflection (2 Points):**
   - *2 pts:* Successfully executed live against Gemini and completed reflection questions.
   - *1 pt:* Executed call but missing reflection.
   - *0 pts:* Did not run live API call.
