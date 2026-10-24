# ⏱️ Instructor Guide: 2-Day Teaching Schedule

**Bootcamp:** Interactive 2-Day Prompt Engineering & Context Engineering Bootcamp  
**Host:** Google Developer Groups on Campus (GDGoC) — COMSATS University Islamabad, Wah Campus  
**Target Audience:** First-semester undergraduate computing students (CS, SE, AI)  
**Pedagogical Style:** Interactive AI Laboratory (Concept -> Roman Urdu Analogy -> Live AI Call -> Student Modification)

---

## 📅 DAY 1: PROMPT ENGINEERING (09:00 AM – 04:30 PM)

| Time Window | Session Block | Primary Activities & Demos |
| :--- | :--- | :--- |
| **09:00 AM - 09:30 AM** | **Welcome & Orientation** | • Welcome address by GDGoC Lead & Faculty Advisor.<br>• Why GenAI is a software skill, not magic.<br>• Environment & API key smoke test check (`scripts/api_smoke_test.py`). |
| **09:30 AM - 10:15 AM** | **Topic 01: What Is a Prompt?** | • Vague vs specific prompts.<br>• *Roman Urdu:* Canteen waiter analogy.<br>• Run `demo_01_what_is_a_prompt.py`.<br>• Student task: Refine icebreaker prompt. |
| **10:15 AM - 11:00 AM** | **Topic 02: Anatomy of a Good Prompt** | • The 5 Pillars: Role, Task, Context, Constraints, Format.<br>• Run `demo_02_anatomy_of_a_good_prompt.py`.<br>• Live exercise: Crafting a workshop announcement. |
| **11:00 AM - 11:20 AM** | ☕ **Tea & Refreshment Break** | Networking & troubleshooting any remaining environment issues. |
| **11:20 AM - 12:00 PM** | **Topic 03: Zero-Shot & Few-Shot** | • In-context learning without fine-tuning.<br>• Run `demo_03_zero_shot_and_few_shot.py`.<br>• *Game:* Few-Shot Classification Game. |
| **12:00 PM - 12:45 PM** | **Topic 04: Task Decomposition** | • Breaking complex tasks into chained sub-tasks.<br>• Run `demo_04_task_decomposition.py`.<br>• Discussion: When does decomposition help vs when is it overkill? |
| **12:45 PM - 01:45 PM** | 🍱 **Lunch & Prayer Break** | Central Cafeteria & Campus Mosque. |
| **01:45 PM - 02:30 PM** | **Topic 05: System vs User Prompts** | • Persistent personas vs dynamic user queries.<br>• Run `demo_05_system_vs_user_instructions.py`.<br>• *Lab Activity:* Strict Professor vs Roman Urdu Senior Mentor. |
| **02:30 PM - 03:15 PM** | **Topic 06: Structured Output (JSON)** | • Why raw text breaks apps; schema constraints with `response_mime_type`.<br>• Run `demo_06_structured_output.py`.<br>• Python validation with `json.loads()`. |
| **03:15 PM - 03:45 PM** | **Topic 07 & 08: Improvement & Safety** | • Iterative prompt ladder (Weak -> Constrained).<br>• Prompt injection & delimiter isolation (`<tags>`).<br>• Run `demo_07` and `demo_08`. |
| **03:45 PM - 04:15 PM** | 🏆 **Day 1 Capstone Challenge** | Students execute `challenge/starter_code.py` to generate the Git Workshop announcement. |
| **04:15 PM - 04:30 PM** | **Day 1 Wrap-up & Reflection** | Awarding "Prompt Battle" winners and previewing Day 2. |

---

## 📅 DAY 2: CONTEXT ENGINEERING & GROUNDED SYSTEMS (09:00 AM – 04:30 PM)

| Time Window | Session Block | Primary Activities & Demos |
| :--- | :--- | :--- |
| **09:00 AM - 09:20 AM** | **Day 1 Recap & Opening** | Reviewing key learnings: "Prompts dictate actions, but who dictates the facts?" |
| **09:20 AM - 10:00 AM** | **Topic 01 & 02: Context Fundamentals** | • What is Context Engineering? Date sheet analogy.<br>• Holding question constant, changing context.<br>• Run `demo_01` and `demo_02`. |
| **10:00 AM - 10:45 AM** | **Topic 03 & 04: Tokens & Relevance** | • Token math (~4 chars/token); context window limits.<br>• Signal vs Noise: Local Python keyword filtering.<br>• Run `demo_03` and `demo_04`. |
| **10:45 AM - 11:05 AM** | ☕ **Tea & Refreshment Break** | Campus lawn / Academic Block 2 courtyard. |
| **11:05 AM - 11:45 AM** | **Topic 05 & 06: Compression & State** | • Context compression trade-offs (savings vs detail loss).<br>• Stateless APIs & Python Application Memory.<br>• Run `demo_05` and `demo_06`. |
| **11:45 AM - 12:45 PM** | **Topic 07: Mini-RAG & Grounding** | • Architecture of RAG: Retrieve -> Augment -> Generate.<br>• Enforcing refusal rules for unrecorded info.<br>• Run `demo_07_rag_and_grounding.py`.<br>• *Game:* The Missing-Information Challenge. |
| **12:45 PM - 01:45 PM** | 🍱 **Lunch & Prayer Break** | Central Cafeteria & Campus Mosque. |
| **01:45 PM - 02:30 PM** | **Topic 08 & 09: Tools & Caching** | • Dynamic context from local Python functions (`get_timetable`).<br>• Application-side in-memory response caching (0ms hits).<br>• Run `demo_08` and `demo_09`. |
| **02:30 PM - 03:15 PM** | **Topic 10: The Production AI Workflow** | • 6-Stage Pipeline: Rules -> Context -> API -> Inspection -> Python Validation -> Delivery.<br>• Run `demo_10_basic_ai_workflow.py`. |
| **03:15 PM - 04:00 PM** | 🏆 **Day 2 Capstone Challenge** | Students build the Context-Grounded Campus Assistant (`challenge/starter_code.py`). |
| **04:00 PM - 04:30 PM** | 🎓 **Certificate Ceremony & Closing** | • Submission verification & grading against rubrics.<br>• Presentation of GDGoC Bootcamp Completion Certificates.<br>• Group photo & next steps in open-source AI development. |
