"""PromptCraft Web - Flask localhost server for chatbot_project.py"""
import json
import sys
import time
from pathlib import Path
from flask import Flask, request, jsonify, render_template

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ai_helper import ask_gemini

app = Flask(__name__)

PROMPT_TECHNIQUES = {
    "1": {"name": "Zero-Shot Prompting",          "description": "Direct task instruction with no examples."},
    "2": {"name": "Few-Shot Prompting",            "description": "Supplies 2 pattern examples to guide format and tone."},
    "3": {"name": "Chain-of-Thought (CoT)",        "description": "Instructs the AI to think step-by-step before answering."},
    "4": {"name": "System Persona (Expert Tutor)", "description": "Assigns a supportive university tutor persona."},
    "5": {"name": "Structured JSON Output",        "description": "Forces clean, machine-readable JSON schema output."},
    "6": {"name": "Prompt Auto-Optimizer",         "description": "Gemini critiques and rewrites your prompt into an elite version."},
    "7": {"name": "Iterative Prompt Ladder",       "description": "Progresses from Weak to Detailed to Production Constrained prompt."},
}

SAMPLE_PROMPTS = [
    "Explain recursion in Python like I am 12 years old",
    "How can I prepare for the upcoming CUI Wah SpeedCode hackathon?",
    "Write a Python script that calculates GPA from a list of grades",
    "Explain how Gemini tokens work in 3 simple bullet points",
]


def build_engineered_prompt(technique_key, user_input):
    system_instruction = None
    response_mime = None
    if technique_key == "1":
        engineered = f"Answer clearly and concisely:\n\n{user_input}"
    elif technique_key == "2":
        engineered = (
            "Task: Answer the inquiry in under 2 concise sentences.\n\n"
            "Example 1:\nInquiry: 'Where do I submit the semester fee challan?'\n"
            "Answer: 'Submit the challan at the campus Allied Bank booth or through online banking before Friday.'\n\n"
            "Example 2:\nInquiry: 'What time is the CS Lab open?'\n"
            "Answer: 'CS Labs are accessible Monday to Friday from 8:30 AM to 4:30 PM for registered students.'\n\n"
            f"Inquiry: '{user_input}'\nAnswer:"
        )
    elif technique_key == "3":
        engineered = (
            f"Problem: {user_input}\n\n"
            "Please solve this using step-by-step reasoning:\n"
            "Step 1: Understand the core question and identify key constraints.\n"
            "Step 2: Break down the logic or solution into actionable milestones.\n"
            "Step 3: Provide the definitive final conclusion or code."
        )
    elif technique_key == "4":
        system_instruction = (
            "You are Dr. Sarah, a warm, highly encouraging Computer Science professor at COMSATS Wah. "
            "You explain concepts using simple real-world metaphors, never make students feel silly, "
            "and always end with an inspiring 1-sentence tip."
        )
        engineered = user_input
    elif technique_key == "5":
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
        engineered = (
            "You are a World-Class Prompt Engineering Specialist. "
            f"Review this prompt written by a first-semester student:\n\n'{user_input}'\n\n"
            "Provide:\n"
            "1. Critique: Why this prompt might give vague results (2 bullets)\n"
            "2. Upgraded Prompt: An optimized, battle-tested version\n"
            "3. Sample Output: What the model would return with the upgraded prompt"
        )
    elif technique_key == "7":
        engineered = (
            "You are demonstrating the Topic 07: Iterative Prompt Improvement Ladder (GDGoC CUI Wah).\n\n"
            f"Original Student Prompt (Level 1: Weak):\n'{user_input}'\n\n"
            "Demonstrate the 3-step evolutionary ladder:\n"
            "1. Level 1 (Weak): Explain why this original prompt is prone to vague or hallucinated details.\n"
            "2. Level 2 (Improved): Rewrite adding clear topic, specific dates, venue, and scope.\n"
            "3. Level 3 (Constrained): Rewrite adding strict tone, max 120 words, 3 bullet points.\n"
            "4. Final Output: Generate the actual response produced by Level 3."
        )
    else:
        engineered = user_input
    return engineered, system_instruction, response_mime


@app.route("/")
def index():
    return render_template("index.html",
                           techniques=PROMPT_TECHNIQUES,
                           samples=SAMPLE_PROMPTS)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    technique_key = data.get("technique", "1")
    user_prompt   = data.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"error": "Empty prompt."})
    engineered_prompt, sys_inst, mime_type = build_engineered_prompt(technique_key, user_prompt)
    tech_name = PROMPT_TECHNIQUES.get(technique_key, PROMPT_TECHNIQUES["1"])["name"]
    start = time.time()
    try:
        response = ask_gemini(
            prompt=engineered_prompt,
            system_instruction=sys_inst,
            temperature=0.2,
            response_mime_type=mime_type,
        )
        elapsed = round(time.time() - start, 2)
    except Exception as e:
        return jsonify({"error": str(e)})
    raw_tokens = max(1, len(user_prompt) // 4)
    eng_tokens = max(1, len(engineered_prompt) // 4)
    multiplier = round(eng_tokens / raw_tokens, 1)
    is_json = mime_type == "application/json"
    parsed_response = response
    if is_json:
        try:
            parsed_response = json.loads(response)
        except Exception:
            parsed_response = response
    return jsonify({
        "response": parsed_response,
        "is_json":  is_json,
        "pipeline": {
            "technique":   tech_name,
            "raw_chars":   len(user_prompt),
            "raw_tokens":  raw_tokens,
            "eng_tokens":  eng_tokens,
            "multiplier":  multiplier,
            "latency":     elapsed,
            "output_type": "Structured JSON Schema" if is_json else "Markdown Formatted Text",
        }
    })


if __name__ == "__main__":
    print("\n  PromptCraft Web starting...")
    print("  Open: http://localhost:5000\n")
    app.run(debug=True, port=5000)
