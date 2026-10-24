# 🧠 Instructor Guide: Knowledge-Check Answers

This document provides the canonical answers, grading criteria, and common student misconceptions for the **5 Knowledge-Check Questions** included in the Day 2 Capstone Challenge.

---

### Question 1
**Why must we display the retrieved notes before calling the model in a transparent AI system?**

#### Canonical Answer:
Displaying retrieved notes provides **observability and auditability**. In modern AI engineering, it allows developers and users to see the exact factual context that grounded the model's answer.  
Crucially, this separates **Retrieval Errors** from **Generation Errors**:
- If the model gives a wrong answer because the retrieval step fetched the wrong document, the developer fixes the *search algorithm*.
- If the model had the correct document but misinterpreted it, the developer fixes the *prompt instructions*.  
Without displaying retrieved notes, developers have no way to diagnose why an AI failed.

#### Common Student Misconception:
Students often believe displaying notes is just for "aesthetic output". Clarify that transparency is a fundamental debugging requirement in production enterprise systems.

---

### Question 2
**If a student asks about a "swimming pool", why should Gemini say "Information unavailable" instead of using its general world knowledge?**

#### Canonical Answer:
Because foundation models possess vast, generalized internet training data, they know what a swimming pool is, standard university opening hours, and typical pool rules. If allowed to use general knowledge when answering campus-specific queries, the model will generate plausible-sounding fictional opening hours (e.g., *"The CUI Wah swimming pool is open Saturdays from 8 AM to 2 PM"*), even though COMSATS Wah may not even have a swimming pool!  
Enforcing strict grounding and polite refusal prevents dangerous **factual hallucinations** and maintains user trust.

#### Common Student Misconception:
Students often think a "smart" AI should always try to answer every question. Teach them that in enterprise software, **knowing when to say "I don't know" is the hallmark of reliability**.

---

### Question 3
**What happens if our keyword search fails to find an event because the student used a synonym (e.g. "football" instead of "futsal")?**

#### Canonical Answer:
Lexical (keyword) matching looks for exact character string matches. If the student searches for `"football"` but the dataset uses the word `"futsal"`, the keyword filter will find 0 matching records. Consequently, the prompt will state that no records exist, and the model will report *"Information unavailable"*.  
This illustrates the primary vulnerability of lexical search and motivates the use of **Semantic Vector Search (Embeddings)**, which maps words based on conceptual meaning rather than exact spellings.

#### Common Student Misconception:
Students assume AI automatically understands synonyms even during the Python retrieval step. Remind them that standard Python `if "football" in text:` does not understand English semantics!

---

### Question 4
**What is the difference between Application-Side Caching and Google GenAI Provider-Side Context Caching?**

#### Canonical Answer:
- **Application-Side Caching (Client/Server level):** Managed in local Python memory, Redis, or a database. It stores the final generated response keyed by a hash of the prompt. If an identical query arrives, the entire API call is bypassed. **Latency is 0 ms, and API cost is 0 tokens.**
- **Provider-Side Context Caching (Google Cloud level):** A specialized feature of the Google GenAI API where massive, shared context prefixes (e.g., 32,768+ tokens from a legal document or large codebase) are held in memory on Google's GPU/TPU servers. When subsequent prompts query that same large document, Google charges a reduced rate for processing the cached prefix. The model still generates a live, novel completion.

#### Common Student Misconception:
Students often conflate caching with model training. Explain that caching never updates model weights—it merely stores data to avoid recomputing.

---

### Question 5
**Why does injecting 100 unrelated campus notices into every prompt degrade performance?**

#### Canonical Answer:
Injecting excessive, noisy notices causes several major problems:
1. **Financial & Quota Waste:** Processing 100 notices burns hundreds or thousands of input tokens per request, rapidly exhausting free-tier quotas.
2. **Increased Latency:** Larger inputs require longer attention matrix calculations, slowing response times for students.
3. **Attention Degradation ("Lost in the Middle"):** Large Language Models exhibit an attention bias where information in the middle of a massive context block is more frequently overlooked than information at the very beginning or end.
4. **Distraction & Hallucination Risk:** Unrelated notices create competing token associations, increasing the risk of the model confusing rules from one event with another.
