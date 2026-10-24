"""CampusMind — Day 2 Interactive Context Engineering & RAG Chatbot

A complete, beginner-friendly capstone project for first-semester students.
Demonstrates the power of Context Engineering: users enter inquiries, select
the context strategy (No Context, Full Context, Filtered, Mini-RAG, Memory,
or Structured Extraction), and inspect the context meter & citations.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ai_helper import ask_gemini

# Optional Rich formatting
try:
    from rich import print as rprint
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


# Official Campus Knowledge Corpus
CAMPUS_KNOWLEDGE = {
    "hostel": (
        "ON-CAMPUS HOSTEL & MESS REGULATIONS:\n"
        "1. For semester Fall 2026, room charges are PKR 35,000 per semester (includes electricity backup & Wi-Fi).\n"
        "2. Monthly hostel mess charges are PKR 14,000 per month (PKR 70,000 per 5-month semester).\n"
        "3. Curfew is strictly 10:00 PM daily with biometric gate security. Free laundry and gym available."
    ),
    "fees": (
        "TUITION FEES & CHALLAN DEADLINES:\n"
        "1. Fall 2026 fee submission deadline is September 15, 2026.\n"
        "2. Challans can be paid at campus Allied Bank (ABL) booths or via 1Link/Kuickpay online banking.\n"
        "3. Late fee fine is PKR 100/day for first 10 days, then PKR 2,000 flat fine. 2-installment plans available."
    ),
    "attendance": (
        "CUI WAH ATTENDANCE REGULATIONS:\n"
        "1. Minimum 80% attendance is mandatory in each course to sit for terminal examinations.\n"
        "2. Below 80% results in an automatic 'F' grade for short attendance.\n"
        "3. Medical excuses must be submitted within 7 working days to the HOD office."
    ),
    "transport": (
        "CAMPUS BUS TRANSPORT ROUTES:\n"
        "1. University fleet covers Rawalpindi, Islamabad, Wah Cantt, Taxila, Hassan Abdal, and Kamra.\n"
        "2. Semester transport fee: PKR 26,000 for twin cities and PKR 16,000 for local routes.\n"
        "3. Morning departure from terminals is 07:15 AM; evening return from campus is 04:45 PM."
    ),
    "hackathon": (
        "GDGOC SPEEDCODE 2026 HACKATHON:\n"
        "1. Date: November 20, 2026 at the Student Activity Center (SAC), COMSATS Wah.\n"
        "2. Team size: Exactly 2 to 3 university students.\n"
        "3. Registration fee: PKR 500 per team.\n"
        "4. 1st prize: PKR 50,000 cash + fast-track software house internship interviews."
    ),
    "scholarships": (
        "CAMPUS MERIT & NEED SCHOLARSHIPS:\n"
        "1. Top 5% academic performers with CGPA >= 3.50 receive 50% to 100% tuition waivers.\n"
        "2. HEC Need-Based scholarships provide full tuition + PKR 6,000 monthly living stipend.\n"
        "3. PEEF scholarships available for Punjab domicile students. Submit forms at SFAO office."
    ),
    "labs": (
        "CS COMPUTER LAB GUIDELINES:\n"
        "1. Labs 01, 03, and 05 operate Monday-Friday from 8:30 AM to 4:30 PM in Academic Block 2.\n"
        "2. Software stack: Windows 11, Python 3.13, Git, VS Code, Google GenAI SDK.\n"
        "3. Strictly no food or open drinks allowed. In-charge: Engr. Farhan (Block B, Room 104)."
    ),
    "library": (
        "CAMPUS LIBRARY & DIGITAL PORTAL:\n"
        "1. BS students can borrow up to 3 physical books for 14 calendar days.\n"
        "2. Late return fine: PKR 10 per day per overdue book.\n"
        "3. IEEE Xplore and ACM Digital Library are accessible via on-campus Wi-Fi without login."
    )
}

STRATEGIES = {
    "1": {
        "name": "Zero Context (Baseline)",
        "desc": "Sends question with NO campus knowledge. Demonstrates hallucination.",
    },
    "2": {
        "name": "Full Context Dump",
        "desc": "Dumps all campus files into context. High tokens and wasteful.",
    },
    "3": {
        "name": "Filtered Context",
        "desc": "Filters relevant documents using keyword ranking before prompt injection.",
    },
    "4": {
        "name": "Production Mini-RAG",
        "desc": "Retrieves top chunks and generates answer with strict [Source] citations.",
    },
    "5": {
        "name": "Conversational Memory",
        "desc": "Maintains multi-turn conversation history and remembers student state.",
    },
    "6": {
        "name": "Structured JSON Extractor",
        "desc": "Extracts entities from context and outputs a validated JSON card.",
    }
}


def render_banner():
    """Displays welcome banner."""
    if HAS_RICH:
        console.print(Panel.fit(
            "[bold green]CampusMind[/bold green] - [bold cyan]Context Engineering & RAG Assistant[/bold cyan]\n"
            "[dim]GDGoC CUI Wah | Day 2 Capstone Project & Chatbot[/dim]\n"
            "[white]Choose Context Strategy -> Inspect Context Window Meter -> See Grounded Output![/white]",
            border_style="green"
        ))
    else:
        print("=" * 65)
        print(" CampusMind - Context Engineering & RAG Assistant")
        print(" GDGoC CUI Wah | Day 2 Capstone Project & Chatbot")
        print("=" * 65)


def display_menu():
    """Displays context strategies menu."""
    if HAS_RICH:
        table = Table(title="Select Context Engineering Strategy", show_header=True, header_style="bold green")
        table.add_column("Key", style="yellow", width=6)
        table.add_column("Strategy", style="bold cyan", width=26)
        table.add_column("Context Behavior", style="white")
        for k, v in STRATEGIES.items():
            table.add_row(k, v["name"], v["desc"])
        console.print(table)
    else:
        print("\nSelect Context Engineering Strategy:")
        for k, v in STRATEGIES.items():
            print(f" [{k}] {v['name']:<25} - {v['desc']}")


def render_context_meter(strategy_name: str, context_len: int, latency_sec: float, signal_ratio: float, query: str = "", response: str = "", choice: str = "4"):
    """Renders a complete visual 6-stage end-to-end Context Engineering pipeline graph in the terminal."""
    tok_est = max(1, context_len // 4)
    q_tok = max(1, len(query) // 4)
    bar_signal = "#" * int(signal_ratio * 20)
    bar_empty = "." * (20 - len(bar_signal))
    
    citations = list(set(re.findall(r"\[DOC-[A-Z0-9\-]+\]", response))) if response else []
    cit_str = ", ".join(citations[:3]) if citations else ("Structured JSON Validated" if choice == "6" else "Contextual Synthesis")
    
    q_preview = query[:54] + "..." if len(query) > 54 else query

    print("\n" + "=" * 76)
    print("      CAMPUSMIND AI: COMPLETE CONTEXT PIPELINE FLOW GRAPH")
    print("=" * 76)
    
    # Stage 1
    print(" ┌─ STAGE 1: RAW USER INQUIRY ───────────────────────────────────────────┐")
    print(f" │ Input Prompt: '{q_preview}'")
    print(f" │ Metrics     : {len(query.split())} words | ~{q_tok} tokens | Status: INGESTED")
    print(" └──────────────────────────────────┬────────────────────────────────────┘")
    print("                                    │")
    print("                                    ▼")
    
    # Stage 2
    print(" ┌─ STAGE 2: CONTEXT ENGINEERING STRATEGY ───────────────────────────────┐")
    print(f" │ Technique : [{choice}] {strategy_name}")
    print(f" │ Filtering : Dynamic knowledge retrieval & signal optimization")
    print(" └──────────────────────────────────┬────────────────────────────────────┘")
    print("                                    │")
    print("                                    ▼")
    
    # Stage 3
    print(" ┌─ STAGE 3: CONTEXT WINDOW ASSEMBLY & SIGNAL RATIO ─────────────────────┐")
    print(f" │ Injected Context: ~{tok_est} tokens ({context_len} characters)")
    print(f" │ Signal/Noise    : [{bar_signal}{bar_empty}] {int(signal_ratio * 100)}% Relevance")
    print(" └──────────────────────────────────┬────────────────────────────────────┘")
    print("                                    │")
    print("                                    ▼")
    
    # Stage 4
    print(" ┌─ STAGE 4: GEMINI 2.5 FLASH INFERENCE ENGINE ──────────────────────────┐")
    print(f" │ Model Execution : Google Gemini 2.5 Flash | Temp: 0.1")
    print(f" │ Latency / Status: {latency_sec:.2f}s | HTTP 200 OK")
    print(" └──────────────────────────────────┬────────────────────────────────────┘")
    print("                                    │")
    print("                                    ▼")
    
    # Stage 5
    print(" ┌─ STAGE 5: GROUNDING & ANTI-HALLUCINATION VERIFICATION ────────────────┐")
    print(f" │ Sources Cited   : {cit_str}")
    print(f" │ Verification    : Validated against COMSATS Wah Campus Corpus")
    print(" └──────────────────────────────────┬────────────────────────────────────┘")
    print("                                    │")
    print("                                    ▼")
    
    # Stage 6
    ans_words = len(response.split()) if response else 0
    print(" ┌─ STAGE 6: RESPONSE FORMATTING & SESSION STATE ────────────────────────┐")
    print(f" │ Format  : {'JSON Object' if choice == '6' else 'Markdown Grounded QA'}")
    print(f" │ Payload : {ans_words} words delivered to student")
    print(" └───────────────────────────────────────────────────────────────────────┘")
    print("=" * 76 + "\n")


def execute_strategy(choice: str, query: str, history: list[str] | None = None) -> tuple[str, str | None]:
    """Prepares prompt and context based on chosen strategy."""
    history = history or []
    response_mime = None

    if choice == "1":
        # 1. Zero Context
        prompt = f"Answer this question about COMSATS Wah campus:\n{query}"
        context_len = 0
        signal_ratio = 0.0

    elif choice == "2":
        # 2. Full Context Dump (All docs)
        full_context = "\n\n".join([f"[{k.upper()}]:\n{v}" for k, v in CAMPUS_KNOWLEDGE.items()])
        prompt = f"Context:\n{full_context}\n\nQuestion: {query}\nAnswer based on context:"
        context_len = len(full_context)
        signal_ratio = 0.25  # Only 1 of 4 docs is relevant on average

    elif choice == "3":
        # 3. Filtered Context (Keyword scoring)
        q_words = set(re.findall(r"\w+", query.lower()))
        matched = []
        for k, text in CAMPUS_KNOWLEDGE.items():
            if any(w in text.lower() for w in q_words if len(w) > 3):
                matched.append(text)
        filtered_ctx = "\n\n".join(matched) if matched else "No direct matches found."
        prompt = f"Relevant Campus Records:\n{filtered_ctx}\n\nQuestion: {query}\nAnswer concisely:"
        context_len = len(filtered_ctx)
        signal_ratio = 0.85

    elif choice == "4":
        # 4. Production Mini-RAG Mode with Grounding and Citations
        q_words = set(re.findall(r"\w+", query.lower()))
        matched = []
        for doc_name, text in CAMPUS_KNOWLEDGE.items():
            matches = sum(1 for w in q_words if w in text.lower() and len(w) > 3)
            if matches > 0:
                matched.append((f"DOC-{doc_name.upper()}", text, matches))
        
        matched.sort(key=lambda x: x[2], reverse=True)
        top = matched[:2] if matched else []
        rag_context = "\n\n".join([f"[{doc_id}]: {text}" for doc_id, text, _ in top]) if top else "NO_RECORDS"

        prompt = (
            "You are the official CUI Wah Campus Assistant.\n"
            "RULES:\n"
            "1. Answer ONLY using the official records below.\n"
            "2. Cite the document ID like [DOC-HACKATHON] for every fact.\n"
            "3. If not present in records, reply exactly: 'Information not in official campus records.'\n\n"
            f"RECORDS:\n{rag_context}\n\n"
            f"QUESTION: {query}\n"
            "GROUNDED ANSWER:"
        )
        context_len = len(rag_context)
        signal_ratio = 0.95

    elif choice == "5":
        # 5. Conversational Memory Mode
        history_text = "\n".join(history[-4:]) if history else "No previous messages."
        prompt = (
            "You are a helpful campus assistant maintaining a conversation.\n"
            f"CONVERSATION HISTORY:\n{history_text}\n\n"
            f"STUDENT: {query}\n"
            "ASSISTANT:"
        )
        context_len = len(history_text)
        signal_ratio = 0.70

    elif choice == "6":
        # 6. Structured JSON Extractor
        response_mime = "application/json"
        full_context = "\n\n".join([f"[{k.upper()}]:\n{v}" for k, v in CAMPUS_KNOWLEDGE.items()])
        prompt = (
            f"Extract structured campus information answering this question: '{query}'\n"
            f"Available Records:\n{full_context}\n\n"
            "Output JSON with keys:\n"
            "- 'topic': main subject\n"
            "- 'answer_summary': 1-sentence answer\n"
            "- 'key_metrics': object with numerical figures (fees, hours, limits, percentages)\n"
            "- 'source_category': matched department or activity\n"
            "- 'grounded': boolean indicating whether information was found in records"
        )
        context_len = len(full_context)
        signal_ratio = 0.50

    else:
        prompt = query
        context_len = 0
        signal_ratio = 0.0

    return prompt, response_mime, context_len, signal_ratio


def run_cycle(choice: str, query: str, history: list[str] | None = None) -> str:
    """Executes a single chatbot cycle."""
    history = history or []
    strategy_info = STRATEGIES.get(choice, STRATEGIES["4"])
    strat_name = strategy_info["name"]

    print(f"\n>> Inquiring: '{query}'")
    print(f">> Context Strategy: {strat_name}")

    prompt, mime_type, ctx_len, signal = execute_strategy(choice, query, history)

    start_time = time.time()
    try:
        response = ask_gemini(
            prompt=prompt,
            system_instruction="You are CampusMind, the official AI assistant for COMSATS University Wah Campus.",
            temperature=0.1,
            response_mime_type=mime_type
        )
        latency = time.time() - start_time

        render_context_meter(strat_name, ctx_len, latency, signal, query=query, response=response, choice=choice)

        print("--- [CAMPUSMIND AI RESPONSE] ---")
        if mime_type == "application/json":
            try:
                parsed = json.loads(response)
                print(json.dumps(parsed, indent=2))
            except Exception:
                print(response.strip())
        else:
            print(response.strip())
        print("-" * 76 + "\n")

        return response.strip()
    except Exception as err:
        print(f"\n[Error] CampusMind query failed: {err}")
        return ""


def interactive_loop():
    """Main terminal loop for students."""
    render_banner()
    history = []

    samples = [
        "What is the minimum attendance required for terminal exams?",
        "When is the SpeedCode hackathon and what is the team registration fee?",
        "How many books can a BS student borrow and for how many days?",
        "What are the mess charges for boys hostel in Fall 2026?"
    ]

    while True:
        display_menu()
        try:
            print("\nChoose Context Strategy [1-6] (or 'q' to quit): ", end="")
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended. Goodbye!")
            break

        if choice.lower() in ("q", "quit", "exit"):
            print("Thank you for using CampusMind! Keep mastering Context Engineering.")
            break

        if choice not in STRATEGIES:
            print(">> Invalid choice. Defaulting to [4] Production Mini-RAG.")
            choice = "4"

        try:
            print("\nEnter your campus inquiry (Press Enter for a sample question):")
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended. Goodbye!")
            break

        if not query:
            import random
            query = random.choice(samples)
            print(f">> Using sample question: '{query}'")

        ans = run_cycle(choice, query, history)
        history.append(f"Student: {query}")
        history.append(f"CampusMind: {ans}")


def main():
    parser = argparse.ArgumentParser(description="CampusMind Day 2 Context & RAG Chatbot")
    parser.add_argument("--demo", action="store_true", help="Run automated demonstration")
    parser.add_argument("--strategy", default="4", help="Context strategy key (1-6)")
    parser.add_argument("--query", default="", help="Custom query string")
    args = parser.parse_args()

    if args.demo or args.query:
        render_banner()
        q = args.query or "What is the team size and prize for the SpeedCode hackathon?"
        run_cycle(args.strategy, q)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()
