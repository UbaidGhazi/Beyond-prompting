# 📅 Day 1: Prompt Engineering Mastery

Welcome to **Day 1** of the GDGoC CUI Wah AI Bootcamp!  
Today is dedicated to mastering the art and science of **Prompt Engineering**—learning how to communicate with Large Language Models with precision, intent, and safety.

---

## 🗺️ Day 1 Curriculum & Navigation

| # | Topic | Core Concept | Lesson Guide | Runnable Demo |
| :-: | :--- | :--- | :--- | :--- |
| **01** | **What Is a Prompt?** | Vague vs Specific Inputs | [Lesson 01](lessons/01-what-is-a-prompt.md) | [demo_01](demos/demo_01_what_is_a_prompt.py) |
| **02** | **Anatomy of a Good Prompt** | Role, Task, Context, Constraints, Format | [Lesson 02](lessons/02-anatomy-of-a-good-prompt.md) | [demo_02](demos/demo_02_anatomy_of_a_good_prompt.py) |
| **03** | **Zero-Shot & Few-Shot** | In-Context Learning & Labeling | [Lesson 03](lessons/03-zero-shot-and-few-shot.md) | [demo_03](demos/demo_03_zero_shot_and_few_shot.py) |
| **04** | **Task Decomposition** | Breaking Complex Tasks into Sub-Tasks | [Lesson 04](lessons/04-task-decomposition.md) | [demo_04](demos/demo_04_task_decomposition.py) |
| **05** | **System vs User Prompts** | Persona Conditioning & Behavioral Rules | [Lesson 05](lessons/05-system-vs-user-instructions.md) | [demo_05](demos/demo_05_system_vs_user_instructions.py) |
| **06** | **Structured Output** | JSON Generation & Python Validation | [Lesson 06](lessons/06-structured-output.md) | [demo_06](demos/demo_06_structured_output.py) |
| **07** | **Prompt Improvement** | Weak -> Improved -> Constrained Ladder | [Lesson 07](lessons/07-prompt-improvement.md) | [demo_07](demos/demo_07_prompt_improvement.py) |
| **08** | **Prompt Safety** | Untrusted Input & Injection Defense | [Lesson 08](lessons/08-prompt-safety.md) | [demo_08](demos/demo_08_prompt_safety.py) |
| **09** | **Prompt Architecture Graph** | 5 Layers, Token Bar Graph & Pydantic Validation | [Demo 09 Guide](demos/demo_09_prompt_architecture_graph.py) | [demo_09](demos/demo_09_prompt_architecture_graph.py) |

---

## 🤖 Day 1 Capstone Project & Chatbot: PromptCraft
Students can test every prompt engineering technique interactively:
👉 **Run Chatbot:** `python day-1-prompt-engineering/chatbot_project.py`
- Select techniques (Zero-Shot, Few-Shot, CoT, Persona, JSON Schema, Auto-Optimizer)
- View the under-the-hood architecture graph and token count in real time!

---

## 🌐 PromptCraft Full Web Studio & Server
Experience the Day 1 Prompt Engineering Studio through a sleek web interface:
👉 **Start Web Server:** `python day-1-prompt-engineering/promptcraft_web_server.py`  
👉 **Open Browser:** [http://localhost:8001](http://localhost:8001)

- **Features:**
  - Visual cards for all 6 prompt techniques.
  - Live **Prompt Architecture Inspector** showing token expansion ratio & layer breakdown.
  - Transformed prompt template preview before sending to model.
  - Interactive JSON output viewer for schema generation.
  - Download experiment notes directly as markdown (`promptcraft_experiments.md`).

## 🏆 Day 1 Capstone Challenge
At the end of Day 1, all students complete the:  
👉 **[Fictional Campus Announcement Generator Challenge](challenge/README.md)**  
Starter code is provided in [`challenge/starter_code.py`](challenge/starter_code.py).

---

## 🎮 Interactive Lab Games & Exercises
- **[Day 1 Exercises & Games](exercises/day_1_exercises.md)**
  - *The Prompt Battle* (Team competition)
  - *Prompt Detective* (Spotting missing constraints)
  - *Few-Shot Classification Game*

---

## 🏃 Quick Command Cheat Sheet (Windows PowerShell)

```powershell
# Run Topic 1 Demo
python day-1-prompt-engineering/demos/demo_01_what_is_a_prompt.py

# Run Topic 6 Structured JSON Demo
python day-1-prompt-engineering/demos/demo_06_structured_output.py

# Run Capstone Starter
python day-1-prompt-engineering/challenge/starter_code.py
```
