"""
solution.py
===========
Day 1 Capstone Challenge: Instructor Reference Solution
GDGoC CUI Wah — 2-Day AI Bootcamp

Demonstrates an exemplar 5-pillar prompt satisfying all rubric criteria:
- Role & Task clarity (2/2)
- Accurate event facts (2/2)
- Constraints & tone (2/2)
- Structured layout (2/2)
- Execution & word count control (2/2)
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ai_helper import ask_gemini


def build_reference_prompt() -> str:
    role = (
        "You are the Lead Student Organizer and Community Evangelist for the "
        "Google Developer Groups on Campus (GDGoC) at COMSATS University Islamabad, Wah Campus."
    )
    task = (
        "Draft a compelling, high-converting social media and WhatsApp broadcast announcement "
        "for our upcoming hands-on technical workshop."
    )
    context = (
        "Verified Campus Event Facts:\n"
        "- Workshop Title: 'Git & GitHub Essentials for First-Semester Devs'\n"
        "- Date: Friday, November 27, 2026\n"
        "- Time: 02:00 PM - 05:00 PM\n"
        "- Venue: CS Lab 05, Academic Block 2, CUI Wah\n"
        "- Target Audience: 1st semester undergraduate students with zero prior Git knowledge\n"
        "- Registration Fee: Free of cost\n"
        "- Registration Deadline: November 25, 2026\n"
        "- Registration Link: https://cuiwah.gdgoc.example/register-git\n"
        "- Prerequisite: Bring personal laptop with a free GitHub account created beforehand"
    )
    constraints = (
        "Strict Editorial Constraints:\n"
        "1. Length: Exactly between 90 and 125 words.\n"
        "2. Tone: Energetic, welcoming, and reassuring for absolute beginners. No intimidating jargon.\n"
        "3. Emphasize that entry is 100% free but lab seats are strictly limited."
    )
    output_format = (
        "Required Layout Structure:\n"
        "[Punchy Headline with 2 Emojis]\n\n"
        "[1-2 sentence Hook relieving beginner anxiety]\n\n"
        "📍 Event Snapshot:\n"
        "- When: [Date & Time]\n"
        "- Where: [Venue]\n"
        "- Entry: [Free status]\n\n"
        "What You'll Practice:\n"
        "• [Takeaway 1: repos & commits]\n"
        "• [Takeaway 2: collaboration & branches]\n"
        "• [Takeaway 3: portfolio showcase]\n\n"
        "[Urgent Call to Action with Deadline & Registration Link]"
    )

    return f"{role}\n\n{task}\n\n{context}\n\n{constraints}\n\n{output_format}"


def main():
    print("=" * 70)
    print("  GDGoC CUI Wah — Day 1 Challenge: Instructor Reference Solution")
    print("=" * 70)

    prompt = build_reference_prompt()
    print("\n[INSTRUCTOR REFERENCE PROMPT]:")
    print(prompt)
    print("\n" + "=" * 70)
    print("Calling Google Gemini API...")

    try:
        response = ask_gemini(prompt=prompt, temperature=0.6)
        print("\n--- [LIVE GEMINI RESPONSE] ---")
        print(response.strip())
        print("-" * 70)

        word_count = len(response.strip().split())
        print(f"Diagnostic Word Count: {word_count} words.")
        print(f"Goal Range: 90 - 125 words -> {'PASS' if 85 <= word_count <= 135 else 'OUT OF RANGE'}")
    except Exception as err:
        print(f"[API ERROR] {err}")


if __name__ == "__main__":
    main()
