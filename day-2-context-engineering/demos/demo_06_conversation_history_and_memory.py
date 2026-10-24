"""Topic 06: Conversation History, Memory, and Application State"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Application state saved locally in Python
student_state = {
    "name": "Zainab",
    "major": "Software Engineering",
    "semester": 1,
    "level": "Absolute Beginner"
}

# Turn 2 question
query = "What workshop should I register for first?"

# Inject state memory into Gemini's context
prompt = (
    f"Student Profile: {student_state}\n"
    f"Available Workshops: [Python for Beginners, Cloud Kubernetes, Advanced C++]\n"
    f"Question: {query}\n"
    "Address the student by name and recommend the best workshop for their level."
)

print("--- [STATE-AWARE PERSONALIZED RESPONSE] ---")
print(ask_gemini(prompt).strip())
