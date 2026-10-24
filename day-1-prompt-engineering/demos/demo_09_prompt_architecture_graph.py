"""Topic 09: Complete Prompt Architecture & Pipeline Flow Graph

Demonstrates the 5 layers of production prompt engineering, visualizes
the architecture in the terminal, and validates structured output.
"""
import json
import sys
import time
from pathlib import Path
from pydantic import BaseModel, Field

# Setup path for ai_helper
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini


# 1. Pydantic Schema for Structured Output Validation
class EventCard(BaseModel):
    title: str = Field(description="Name of the university event")
    category: str = Field(description="Workshop, Seminar, Hackathon, or Sports")
    target_audience: str = Field(description="Target student semester or department")
    key_takeaway: str = Field(description="Main skill or knowledge gained")
    duration_hours: float = Field(description="Estimated event duration in hours")


def estimate_tokens(text: str) -> int:
    """Simple estimation: ~4 chars per token."""
    return max(1, len(text) // 4)


def render_pipeline_graph(layers: dict, total_tokens: int, duration_sec: float):
    """Prints a visual terminal graph of the prompt architecture."""
    print("=" * 65)
    print("        PROMPT ARCHITECTURE EXECUTION PIPELINE GRAPH")
    print("=" * 65)
    print(" [Raw User Request]")
    print("        |")
    print("        v")
    print("+---------------------------------------------------------------+ ")
    for idx, (name, content) in enumerate(layers.items(), 1):
        tokens = estimate_tokens(content)
        pct = (tokens / total_tokens) * 100
        bar = "#" * int(pct / 5)
        print(f"| [{idx}] {name:<20} | {tokens:>3} toks | {bar:<15} ({pct:>4.1f}%) |")
    print("+---------------------------------------------------------------+ ")
    print(f"        |===> Total Prompt Footprint: {total_tokens} tokens")
    print("        v")
    print(" [Gemini 3.5 Flash Lite Engine]")
    print(f"        |===> Inference Latency: {duration_sec:.2f} seconds")
    print("        v")
    print(" [Pydantic Schema Validation: EventCard]")
    print("=" * 65)


def main():
    # Raw student input
    raw_query = "Can you organize a hands-on Python and Gemini API session for 1st-semester CS students next Friday?"

    # The 5 Architectural Layers of a Robust Prompt
    layers = {
        "System Persona": "You are the Senior Academic Coordinator for GDGoC CUI Wah.",
        "Rules & Bounds": "Output pure JSON strictly adhering to schema. No conversational filler.",
        "Dynamic Context": "Campus: COMSATS Wah. Term: Fall 2026. Available labs: CS Lab 03.",
        "Few-Shot Sample": "Example: 'Git class' -> {'title':'Git 101','category':'Workshop','target_audience':'All','key_takeaway':'Git commits','duration_hours':2.0}",
        "User Task Query": f"Synthesize this student proposal into an official event card:\n'{raw_query}'"
    }

    # Assemble complete architecture
    prompt_assembled = (
        f"CONTEXT:\n{layers['Dynamic Context']}\n\n"
        f"FEW-SHOT DEMONSTRATION:\n{layers['Few-Shot Sample']}\n\n"
        f"TASK:\n{layers['User Task Query']}\n\n"
        f"INSTRUCTION: {layers['Rules & Bounds']}"
    )

    total_tokens = sum(estimate_tokens(c) for c in layers.values())

    print("\n--- [STAGE 1: GENERATING WITH ARCHITECTURE] ---")
    start_time = time.time()
    raw_response = ask_gemini(
        prompt=prompt_assembled,
        system_instruction=layers["System Persona"],
        temperature=0.1,
        response_mime_type="application/json"
    )
    elapsed = time.time() - start_time

    # Render Visual Flow Graph in Output
    render_pipeline_graph(layers, total_tokens, elapsed)

    # Validate Structured Output with Pydantic
    try:
        data = json.loads(raw_response)
        event = EventCard.model_validate(data)
        print("\n--- [STAGE 2: VALIDATED STRUCTURED OUTPUT] ---")
        print(f" Event Title   : {event.title}")
        print(f" Category      : {event.category}")
        print(f" Audience      : {event.target_audience}")
        print(f" Key Takeaway  : {event.key_takeaway}")
        print(f" Duration      : {event.duration_hours} Hours")
        print(" Validation    : PASSED (Schema verified)")
    except Exception as e:
        print(f"JSON Output: {raw_response}")
        print(f"Validation Error: {e}")


if __name__ == "__main__":
    main()
