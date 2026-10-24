"""
starter_code.py
===============
Day 1 Capstone Challenge: Fictional Campus Announcement Generator
GDGoC CUI Wah — 2-Day AI Bootcamp

STUDENT NAME: [Enter Your Name Here]
STUDENT REGISTRATION: [e.g. SP26-BCS-000]

INSTRUCTIONS:
1. Review the fictional event brief in README.md.
2. Build your custom 5-pillar prompt inside `build_capstone_prompt()`.
3. Run this script to test your prompt against the live Gemini API.
4. Record your reflection at the bottom of this file.
"""

import sys
from pathlib import Path

# Add repository root to path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ai_helper import ask_gemini


def build_capstone_prompt() -> str:
    """
    TODO: Construct your 5-pillar prompt here.
    Remember to include:
      1. Role: GDGoC Community Lead at CUI Wah
      2. Task: Draft a workshop announcement
      3. Context: Git & GitHub Essentials, Nov 27, CS Lab 05, Free entry
      4. Constraints: 90 - 130 words, energetic tone, zero intimidating jargon
      5. Format: Headline -> Hook -> Snapshot -> 3 Takeaways -> Call to Action
    """

    # --- STUDENT EDIT START ---
    prompt = (
        "TODO: Replace this entire placeholder string with your engineered prompt!\n"
        "Refer to the 5 pillars from Lesson 02 and Lesson 07."
    )
    # --- STUDENT EDIT END ---

    return prompt


def main():
    print("=" * 70)
    print("  GDGoC CUI Wah — Day 1 Capstone Challenge: Announcement Generator")
    print("=" * 70)

    prompt = build_capstone_prompt()
    print("\n[YOUR SUBMITTED PROMPT]:")
    print("-" * 50)
    print(prompt.strip())
    print("-" * 50)

    if "TODO:" in prompt:
        print("\n[ALERT] You have not replaced the TODO placeholder yet!")
        print("Please edit build_capstone_prompt() before calling the model.")
        return

    print("\nCalling Google Gemini API...")
    try:
        response = ask_gemini(prompt=prompt, temperature=0.7)
        print("\n--- [LIVE GEMINI GENERATED ANNOUNCEMENT] ---")
        print(response.strip())
        print("-" * 50)

        # Word count check
        words = len(response.strip().split())
        print(f"\n[DIAGNOSTIC] Generated Word Count: {words} words.")
        if 90 <= words <= 130:
            print(">> [PASS] Word count satisfies the 90-130 constraint!")
        else:
            print(f">> [NOTE] Word count is {words}. Adjust constraints to get between 90 and 130 words.")

    except Exception as err:
        print(f"\n[API ERROR] {err}")
        print("Please check your .env file and network connectivity.")


if __name__ == "__main__":
    main()

"""
================================================================================
STUDENT REFLECTION (Fill in after running your live API call):
1. Did the AI respect all event facts (CS Lab 05, Nov 27, Free)?
   Answer: [Your reflection here]

2. How close was the generated word count to the 90-130 range?
   Answer: [Your reflection here]

3. Which prompt element (Role, Constraints, or Format) had the greatest effect?
   Answer: [Your reflection here]
================================================================================
"""
