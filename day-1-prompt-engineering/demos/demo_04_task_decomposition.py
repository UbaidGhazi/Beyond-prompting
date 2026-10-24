"""Topic 04: Task Decomposition (Step-by-Step Chaining)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Step 1: Goals and Audience
step1 = "Define 3 clear goals for a 1-day CUI Wah hackathon. Max 50 words."
goals = ask_gemini(step1, temperature=0.3).strip()
print("--- [STEP 1: GOALS] ---")
print(goals)

# Step 2: Schedule using the output of Step 1
step2 = f"Based on these goals:\n{goals}\nMake a 4-point schedule for CS Lab 01."
schedule = ask_gemini(step2, temperature=0.3).strip()
print("\n--- [STEP 2: SCHEDULE] ---")
print(schedule)

# Step 3: Announcement using the output of Step 2
step3 = f"Using this schedule:\n{schedule}\nWrite a 40-word WhatsApp student broadcast."
announcement = ask_gemini(step3, temperature=0.7).strip()
print("\n--- [STEP 3: ANNOUNCEMENT] ---")
print(announcement)
