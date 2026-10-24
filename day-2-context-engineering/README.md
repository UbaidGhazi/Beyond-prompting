# 📅 Day 2: Context Engineering & Grounded Systems

Welcome to **Day 2** of the GDGoC CUI Wah AI Bootcamp!  
Today, we transition from writing instructions (*Prompt Engineering*) to managing information (*Context Engineering*)—learning how to supply models with verified private data, build Mini-RAG search pipelines, utilize tools, implement caching, and assemble production AI workflows.

---

## 🗺️ Day 2 Curriculum & Navigation

| # | Topic | Core Concept | Lesson Guide | Runnable Demo |
| :-: | :--- | :--- | :--- | :--- |
| **01** | **What Is Context Engineering?** | Prompt = Action, Context = Information | [Lesson 01](lessons/01-what-is-context-engineering.md) | [demo_01](demos/demo_01_what_is_context_engineering.py) |
| **02** | **Prompt vs Context** | Constant Query with Changing Evidence | [Lesson 02](lessons/02-prompt-vs-context.md) | [demo_02](demos/demo_02_prompt_vs_context.py) |
| **03** | **Context Window & Tokens** | Token Limits, Budgets & Bloat Reduction | [Lesson 03](lessons/03-context-window-and-tokens.md) | [demo_03](demos/demo_03_context_window_and_tokens.py) |
| **04** | **Selecting Relevant Info** | Programmatic Filtering (Signal vs Noise) | [Lesson 04](lessons/04-selecting-relevant-information.md) | [demo_04](demos/demo_04_selecting_relevant_information.py) |
| **05** | **Context Compression** | Condensing Long Documents via LLMs | [Lesson 05](lessons/05-context-compression-and-summarization.md) | [demo_05](demos/demo_05_context_compression_and_summarization.py) |
| **06** | **Conversation & Memory** | Stateless APIs & Application State | [Lesson 06](lessons/06-conversation-history-and-memory.md) | [demo_06](demos/demo_06_conversation_history_and_memory.py) |
| **07** | **Mini-RAG & Grounding** | Local Search, Grounding & Refusals | [Lesson 07](lessons/07-rag-and-grounding.md) | [demo_07](demos/demo_07_rag_and_grounding.py) |
| **08** | **Tools & External Context** | Simulated Campus Timetable Function | [Lesson 08](lessons/08-tools-and-external-context.md) | [demo_08](demos/demo_08_tools_and_external_context.py) |
| **09** | **Context Efficiency & Cache**| In-Memory Cache Store (0ms Hits) | [Lesson 09](lessons/09-context-efficiency-and-caching.md) | [demo_09](demos/demo_09_context_efficiency_and_caching.py) |
| **10** | **Basic AI Workflow** | 6-Stage Production Pipeline with Validation | [Lesson 10](lessons/10-basic-ai-workflow.md) | [demo_10](demos/demo_10_basic_ai_workflow.py) |
| **11** | **Production Mini-RAG** | Multi-Doc Chunking, Scoring & Citation RAG | [Demo 11 Guide](demos/demo_11_mini_rag_application.py) | [demo_11](demos/demo_11_mini_rag_application.py) |

---

## 🤖 Day 2 Capstone Project & Chatbot: CampusMind
Students can test every context engineering strategy interactively:
👉 **Run Chatbot:** `python day-2-context-engineering/chatbot_project.py`
- Compare Zero-Context vs Full Context vs Filtered vs Mini-RAG vs Memory
- Inspect live Context Meter, Signal-to-Noise ratio, and grounded citations!

---

## 🌐 Full Interactive Web Frontend & Server
Experience the Mini-RAG Assistant through a modern glassmorphism web interface:
👉 **Start Web Server:** `python day-2-context-engineering/rag_web_server.py`  
👉 **Open Browser:** [http://localhost:8000](http://localhost:8000)

- **Features:**
  - Ask **any** arbitrary query (not constrained to fixed task lists).
  - Real-time 4-step pipeline tracker (Ingestion -> Scoring -> Injection -> Answer).
  - Shows grounded responses with verified citations (e.g. `[DOC-HOSTEL-C2]`).
  - Interactive evidence cards showing chunk texts & similarity match scores.
  - Generates & downloads a complete consultation session document (`.md`).

## 🏆 Day 2 Capstone Challenge
At the end of Day 2, all students complete the:  
👉 **[Context-Grounded Campus Assistant Challenge](challenge/README.md)**  
Dataset is in [`data/campus_events.json`](data/campus_events.json) and starter code in [`challenge/starter_code.py`](challenge/starter_code.py).

---

## 🎮 Interactive Lab Games & Exercises
- **[Day 2 Exercises & Games](exercises/day_2_exercises.md)**
  - *The Context Detective* (Minimal context competition)
  - *The Missing-Information Challenge* (Hallucination defense)
  - *The Cache Challenge* (Proving 0ms latency)

---

## 🏃 Quick Command Cheat Sheet (Windows PowerShell)

```powershell
# Run Topic 1 Demo
python day-2-context-engineering/demos/demo_01_what_is_context_engineering.py

# Run Topic 7 Mini-RAG Demo
python day-2-context-engineering/demos/demo_07_rag_and_grounding.py

# Run Day 2 Capstone Assistant
python day-2-context-engineering/challenge/starter_code.py
```
