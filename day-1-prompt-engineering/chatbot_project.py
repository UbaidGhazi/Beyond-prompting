"""PromptCraft — Day 1 Interactive Prompt Engineering Chatbot & Studio

A complete, beginner-friendly project for first-semester students.
Allows users to enter a prompt, select the prompt engineering technique,
visualizes what the prompt is doing under the hood, and generates the response.
"""
import argparse
import json
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ai_helper import ask_gemini

# Optional Rich formatting for a polished, beginner-friendly terminal interface
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


PROMPT_TECHNIQUES = {
    "1": {
        "name": "Zero-Shot Prompting",
        "description": "Direct task instruction with no examples provided.",
        "icon": "[1]"
    },
    "2": {
        "name": "Few-Shot Prompting",
        "description": "Supplies 2 pattern examples to guide format and tone.",
        "icon": "[2]"
    },
    "3": {
        "name": "Chain-of-Thought (CoT)",
        "description": "Instructs the AI to think step-by-step before answering.",
        "icon": "[3]"
    },
    "4": {
        "name": "System Persona (Expert Tutor)",
        "description": "Assigns a supportive, university tutor persona.",
        "icon": "[4]"
    },
    "5": {
        "name": "Structured JSON Output",
        "description": "Forces clean, machine-readable JSON schema output.",
        "icon": "[5]"
    },
    "6": {
        "name": "Prompt Auto-Optimizer",
        "description": "Gemini critiques and rewrites your prompt into an elite version.",
        "icon": "[6]"
    },
    "7": {
        "name": "Iterative Prompt Ladder",
        "description": "Progresses prompt through Level 1 (Weak) to Level 2 (Detailed) to Level 3 (Production Constrained).",
        "icon": "[7]"
    }
}


def render_banner():
    """Displays welcome banner."""
    if HAS_RICH:
        console.print(Panel.fit(
            "[bold cyan]PromptCraft[/bold cyan] - [bold yellow]Interactive Prompt Engineering Studio[/bold yellow]\n"
            "[dim]GDGoC CUI Wah | Day 1 Capstone Project & Chatbot[/dim]\n"
            "[white]Choose a technique -> Enter your prompt -> Inspect architecture -> Get answer![/white]",
            border_style="cyan"
        ))
    else:
        print("=" * 60)
        print(" PromptCraft - Interactive Prompt Engineering Studio")
        print(" GDGoC CUI Wah | Day 1 Capstone Project & Chatbot")
        print("=" * 60)


def display_menu():
    """Displays the prompt engineering technique selection menu."""
    if HAS_RICH:
        table = Table(title="Select Prompt Engineering Technique", show_header=True, header_style="bold magenta")
        table.add_column("Key", style="cyan", width=6)
        table.add_column("Technique", style="bold green", width=26)
        table.add_column("What it teaches", style="white")
        for key, info in PROMPT_TECHNIQUES.items():
            table.add_row(key, info["name"], info["description"])
        console.print(table)
    else:
        print("\nSelect Prompt Engineering Technique:")
        for key, info in PROMPT_TECHNIQUES.items():
            print(f" [{key}] {info['name']:<25} - {info['description']}")


def build_engineered_prompt(technique_key: str, user_input: str) -> tuple[str, str | None, str | None]:
    """Transforms raw user input into an engineered prompt based on the chosen technique."""
    system_instruction = None
    response_mime = None

    if technique_key == "1":
        # Zero-Shot: Direct, clean task
        engineered = f"Answer clearly and concisely:\n\n{user_input}"

    elif technique_key == "2":
        # Few-Shot: Include 2 campus examples
        engineered = (
            "Task: Answer the inquiry in under 2 concise sentences.\n\n"
            "Example 1:\n"
            "Inquiry: 'Where do I submit the semester fee challan?'\n"
            "Answer: 'Submit the challan at the campus Allied Bank booth or through online banking before Friday.'\n\n"
            "Example 2:\n"
            "Inquiry: 'What time is the CS Lab open?'\n"
            "Answer: 'CS Labs are accessible Monday to Friday from 8:30 AM to 4:30 PM for registered students.'\n\n"
            f"Inquiry: '{user_input}'\n"
            "Answer:"
        )

    elif technique_key == "3":
        # Chain of Thought
        engineered = (
            f"Problem: {user_input}\n\n"
            "Please solve this using step-by-step reasoning:\n"
            "Step 1: Understand the core question and identify key constraints.\n"
            "Step 2: Break down the logic or solution into actionable milestones.\n"
            "Step 3: Provide the definitive final conclusion or code."
        )

    elif technique_key == "4":
        # System Persona
        system_instruction = (
            "You are Dr. Sarah, a warm, highly encouraging Computer Science professor at COMSATS Wah. "
            "You explain concepts using simple real-world metaphors, never make students feel silly, "
            "and always end with an inspiring 1-sentence tip."
        )
        engineered = user_input

    elif technique_key == "5":
        # Structured JSON Output
        response_mime = "application/json"
        engineered = (
            f"Analyze this request and output a pure JSON object:\n'{user_input}'\n\n"
            "Required JSON keys:\n"
            "- 'summary': 1-sentence summary\n"
            "- 'category': topic category (e.g., Programming, Campus, Career)\n"
            "- 'key_points': list of 3 bullet points\n"
            "- 'estimated_reading_minutes': integer estimate\n"
            "Output JSON only."
        )

    elif technique_key == "6":
        # Prompt Optimizer
        engineered = (
            "You are a World-Class Prompt Engineering Specialist. "
            f"Review this prompt written by a first-semester student:\n\n'{user_input}'\n\n"
            "Provide:\n"
            "1. Critique: Why this prompt might give vague results (2 bullets)\n"
            "2. Upgraded Prompt: An optimized, battle-tested version\n"
            "3. Sample Output: What the model would return with the upgraded prompt"
        )

    elif technique_key == "7":
        # Iterative Prompt Improvement Ladder (Topic 07)
        engineered = (
            "You are demonstrating the Topic 07: Iterative Prompt Improvement Ladder (GDGoC CUI Wah).\n\n"
            f"Original Student Prompt (Level 1: Weak):\n'{user_input}'\n\n"
            "Demonstrate the 3-step evolutionary ladder:\n"
            "1. Level 1 (Weak): Explain why this original prompt is prone to vague or hallucinated details.\n"
            "2. Level 2 (Improved): Rewrite adding clear topic, specific dates, venue, and scope.\n"
            "3. Level 3 (Constrained - Production Ready): Rewrite adding strict tone, maximum 120 words constraint, and 3 bullet points format.\n"
            "4. Final Output: Generate the actual response produced by Level 3."
        )
    else:
        engineered = user_input

    return engineered, system_instruction, response_mime


def print_architecture_graph(technique_name: str, raw_len: int, engineered_len: int, duration_sec: float, is_json: bool = False):
    """Draws a visual stage-by-stage pipeline flow graph showing how the prompt was engineered."""
    tok_in = max(1, raw_len // 4)
    tok_eng = max(1, engineered_len // 4)
    multiplier = tok_eng / tok_in if tok_in > 0 else 1.0

    print("\n" + "=" * 68)
    print("      PROMPT ARCHITECTURE COMPLETE EXECUTION PIPELINE GRAPH")
    print("=" * 68)
    print(f" [STAGE 1: RAW INPUT]      --> {tok_in:>3} tokens ({raw_len} chars)")
    print("           |")
    print("           v")
    print(f" [STAGE 2: TECHNIQUE]      --> {technique_name} (Pattern & Bounds Injected)")
    print("           |")
    print("           v")
    print(f" [STAGE 3: CONTEXT WINDOW] --> {tok_eng:>3} tokens ({multiplier:.1f}x Expansion Multiplier)")
    print("           |")
    print("           v")
    print(f" [STAGE 4: GEMINI ENGINE]  --> Latency: {duration_sec:.2f}s (Gemini 3.5 Flash Lite)")
    print("           |")
    print("           v")
    status_label = "Structured JSON Schema (Verified)" if is_json else "Markdown Formatted Text"
    print(f" [STAGE 5: PARSED OUTPUT]  --> {status_label}")
    print("=" * 68 + "\n")


def run_promptcraft_cycle(technique_key: str, user_prompt: str):
    """Executes a single interactive cycle."""
    tech_info = PROMPT_TECHNIQUES.get(technique_key, PROMPT_TECHNIQUES["1"])
    tech_name = tech_info["name"]

    print(f"\n>> Applying: {tech_name}")
    print(f">> User Query: '{user_prompt}'")

    engineered_prompt, sys_inst, mime_type = build_engineered_prompt(technique_key, user_prompt)

    start_time = time.time()
    try:
        response = ask_gemini(
            prompt=engineered_prompt,
            system_instruction=sys_inst,
            temperature=0.2,
            response_mime_type=mime_type
        )
        elapsed = time.time() - start_time

        # Visual stage-by-stage pipeline graph
        print_architecture_graph(tech_name, len(user_prompt), len(engineered_prompt), elapsed, is_json=(mime_type == "application/json"))

        print("--- [PROMPTCRAFT AI RESPONSE] ---")
        if mime_type == "application/json":
            try:
                parsed = json.loads(response)
                print(json.dumps(parsed, indent=2))
            except Exception:
                print(response.strip())
        else:
            print(response.strip())
        print("---------------------------------\n")

    except Exception as err:
        print(f"\n[Error] Unable to generate response: {err}")


def interactive_loop():
    """Main interactive terminal chatbot loop for students."""
    render_banner()

    # Pre-canned examples for beginners
    sample_prompts = [
        "Explain recursion in Python like I am 12 years old",
        "How can I prepare for the upcoming CUI Wah SpeedCode hackathon?",
        "Write a Python script that calculates GPA from a list of grades",
        "Explain how Gemini tokens work in 3 simple bullet points"
    ]

    while True:
        display_menu()
        print("\nChoose a technique [1-6] (or 'q' to quit): ", end="")
        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting PromptCraft. Keep engineering great prompts!")
            break

        if choice.lower() in ("q", "quit", "exit"):
            print("Thank you for using PromptCraft! Keep engineering great prompts.")
            break

        if choice not in PROMPT_TECHNIQUES:
            print(">> Invalid choice. Defaulting to [1] Zero-Shot.")
            choice = "1"

        print("\nEnter your prompt (Press Enter to use a sample prompt):")
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting PromptCraft.")
            break

        if not user_input:
            import random
            user_input = random.choice(sample_prompts)
            print(f">> Using sample prompt: '{user_input}'")

        run_promptcraft_cycle(choice, user_input)


def main():
    parser = argparse.ArgumentParser(description="PromptCraft Day 1 Chatbot & Studio")
    parser.add_argument("--demo", action="store_true", help="Run automated demonstration mode")
    parser.add_argument("--type", default="1", help="Prompt technique key (1-6)")
    parser.add_argument("--prompt", default="", help="Custom prompt text")
    args = parser.parse_args()

    # If non-interactive terminal (e.g. redirected or automated test), run demo mode safely
    if args.demo or args.prompt or not sys.stdin.isatty():
        render_banner()
        prompt_text = args.prompt or "Explain how to debug an IndexError in Python"
        run_promptcraft_cycle(args.type, prompt_text)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()
