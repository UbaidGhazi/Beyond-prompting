# 🚀 GDGoC CUI Wah: Interactive 2-Day Prompt Engineering & Context Engineering Bootcamp

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Google GenAI SDK](https://img.shields.io/badge/Google-GenAI%20SDK-4285F4.svg)](https://ai.google.dev/)
[![Gemini 2.5](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-34A853.svg)](https://aistudio.google.com/)
[![Community](https://img.shields.io/badge/GDGoC-COMSATS%20Wah-EA4335.svg)](https://gdg.community.dev/)

Welcome to the official, hands-on repository for the **Google Developer Groups on Campus (GDGoC) COMSATS University Islamabad (CUI), Wah Campus** 2-Day Bootcamp!

This repository is built as an **Interactive AI Laboratory** designed specifically for first-semester university students. You will not just read theory or look at mock outputs—**every single lesson connects to Google's real Gemini models** using the official `google-genai` Python SDK!

---

## 🎯 Learning Objectives

By the end of this 2-day bootcamp, you will be able to:
1. **Master Prompt Engineering:** Craft clear, role-defined, constrained prompts that reliably extract desired outputs from modern LLMs.
2. **Understand Few-Shot Learning & Task Decomposition:** Guide AI behavior through concrete examples and structured multi-step thinking.
3. **Control Output Structures:** Generate and programmatically parse machine-readable JSON data with strict schemas.
4. **Practice Prompt Safety:** Identify untrusted inputs, defend against prompt injection attacks, and avoid AI hallucinations.
5. **Engineer Context Like an Expert:** Understand token budgets, filter signal from noise, and compress large documents into actionable context.
6. **Build Grounded Systems (Mini-RAG):** Connect external data sources and local tools so an AI only answers from verified campus records.
7. **Deploy Reliable AI Workflows:** Combine instructions, context retrieval, model inference, and automated validation into robust pipelines.

---

## 🗓️ 2-Day Curriculum Roadmap

```
GDGoC CUI Wah AI Bootcamp
│
├── 📅 DAY 1: PROMPT ENGINEERING (8 Topics + 1 Capstone Challenge)
│   ├── Topic 01: What Is a Prompt? (Vague vs Specific Inputs)
│   ├── Topic 02: Anatomy of a Good Prompt (Role, Task, Context, Constraints, Format)
│   ├── Topic 03: Zero-Shot vs Few-Shot Prompting (In-context learning with campus club notes)
│   ├── Topic 04: Task Decomposition (Breaking complex goals into manageable steps)
│   ├── Topic 05: System Instructions vs User Prompts (Persona & behavioral rules)
│   ├── Topic 06: Structured Output (Machine-readable JSON & Python validation)
│   ├── Topic 07: Prompt Improvement (Weak -> Improved -> Constrained iterations)
│   ├── Topic 08: Prompt Safety (Untrusted input, injection defense & verification)
│   └── 🏆 Day 1 Capstone Challenge: Fictional Campus Announcement Generator
│
└── 📅 DAY 2: CONTEXT ENGINEERING (10 Topics + 1 Capstone Challenge)
    ├── Topic 01: What Is Context Engineering? (Prompt = Action, Context = Information)
    ├── Topic 02: Prompt vs Context (Constant prompt with changing ground truth)
    ├── Topic 03: Context Window & Token Limits (Budgets, truncation & token math)
    ├── Topic 04: Selecting Relevant Information (Filtering signal from campus noise)
    ├── Topic 05: Context Compression & Summarization (Condensing large documents)
    ├── Topic 06: Conversation History, Memory, & State (Cross-turn application state)
    ├── Topic 07: RAG & Grounded Generation (Keyword search over campus records)
    ├── Topic 08: Tools & External Context (Simulated campus timetable integration)
    ├── Topic 09: Context Efficiency & Caching (In-memory application caching)
    ├── Topic 10: A Basic AI Workflow (Pipeline: Instructions -> Context -> AI -> Validation)
    └── 🏆 Day 2 Capstone Challenge: Context-Grounded Campus Assistant
```

---

## 🧭 Repository Structure

```text
c:\Users\HP\OneDrive\Desktop\Bootcamp\
├── README.md                           # Master repo overview (You are here!)
├── SETUP.md                            # Step-by-step beginner setup guide
├── requirements.txt                    # Pinned Python package dependencies
├── .env.example                        # Safe environment template
├── .gitignore                          # Protects your private keys & cache files
│
├── src/                                # Core shared utilities
│   ├── __init__.py
│   └── ai_helper.py                    # Shared official Gemini SDK helper (no mocks!)
│
├── scripts/                            # Verification & utility scripts
│   ├── api_smoke_test.py               # Tests local setup & live API connection
│   └── validate_bootcamp.py            # Static validation script for entire repo
│
├── day-1-prompt-engineering/
│   ├── README.md                       # Day 1 guide, games & schedule
│   ├── lessons/                        # 8 Markdown lessons (Template structured)
│   ├── demos/                          # 8 Independent runnable Python scripts
│   ├── notebooks/                      # 8 Interactive Jupyter Notebooks (.ipynb)
│   ├── diagrams/                       # 8 Visual SVG concept flowcharts
│   ├── exercises/                      # Student practice exercises
│   └── challenge/                      # Day 1 Capstone Announcement Generator
│
├── day-2-context-engineering/
│   ├── README.md                       # Day 2 guide, games & schedule
│   ├── data/                           # Fictional campus dataset (campus_events.json)
│   ├── lessons/                        # 10 Markdown lessons
│   ├── demos/                          # 10 Independent runnable Python scripts
│   ├── notebooks/                      # 10 Interactive Jupyter Notebooks (.ipynb)
│   ├── diagrams/                       # 10 Visual SVG concept flowcharts
│   ├── exercises/                      # Student practice exercises
│   └── challenge/                      # Day 2 Capstone Campus Assistant
│
└── instructor-guide/                   # Dedicated instructor resources
    ├── schedule.md                     # Hour-by-hour teaching timetable
    ├── day-1-answer-key.md             # Complete solutions & teaching notes
    ├── day-2-answer-key.md             # Complete solutions & teaching notes
    ├── knowledge-check-answers.md      # Detailed answers to knowledge checks
    └── troubleshooting.md              # Common student errors & quick fixes
```

---

## ⚡ Quick Start in 4 Steps

### 1. Clone or Open the Repository
```bash
cd c:\Users\HP\OneDrive\Desktop\Bootcamp
```

### 2. Create Virtual Environment & Install Dependencies
```powershell
# Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Your Free API Key
Get your key from [Google AI Studio](https://aistudio.google.com/), then copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` and paste your key:
```env
GEMINI_API_KEY=AIzaSyYourActualKeyHere
GEMINI_MODEL=gemini-2.5-flash
```

### 4. Run the Environment Smoke Test
```powershell
python scripts/api_smoke_test.py
```
If you see `[PASS] Live Gemini API connection successful!`, you're 100% ready to go!

---

## 🏃 Running Demos & Notebooks

### Running Standalone Python Files:
Every topic has a self-contained `.py` file that can be executed directly from terminal:
```powershell
# Run Topic 1
python day-1-prompt-engineering/demos/demo_01_what_is_a_prompt.py

# Run Day 2 RAG Demo
python day-2-context-engineering/demos/demo_07_rag_and_grounding.py
```

### Running Interactive Jupyter Notebooks:
```powershell
jupyter notebook
```
Navigate to any notebook in `day-1-prompt-engineering/notebooks/` or `day-2-context-engineering/notebooks/` to experiment interactively.

---

## 🔒 Crucial Security Rule
> [!CAUTION]
> **NEVER HARDCODE API KEYS IN PYTHON FILES OR NOTEBOOKS!**  
> All code in this bootcamp automatically loads `GEMINI_API_KEY` from your local `.env` file via `src/ai_helper.py`.  
> `.gitignore` is pre-configured to ensure `.env` is never committed to source control.

---

## 🎮 Fun Interactive Activities Included!
- **Prompt Battle:** Teams compete to produce the best event announcement.
- **Guess the Output:** Predict model behavior before running live API calls.
- **Few-Shot Classification Game:** Teach the model custom campus labels with minimal examples.
- **Prompt & Context Detectives:** Track down missing constraints and noisy data.
- **Cache Challenge:** Inspect live API calls vs instantaneous cache hits!

---

## 🤝 Community & Credits
Organized by **Google Developer Groups on Campus (GDGoC) — COMSATS University Islamabad, Wah Campus**.  
Curriculum designed for first-semester undergraduate students in Computer Science, Software Engineering, and AI.
