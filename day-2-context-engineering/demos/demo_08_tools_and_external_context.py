"""Topic 08: Tools and External Information"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Local simulated tool (Python function)
def get_timetable(course_code: str) -> dict:
    timetable = {
        "CSC101": {"room": "CS Lab 02", "time": "09:00 AM", "teacher": "Engr. Muhammad Ali"}
    }
    return timetable.get(course_code.upper(), {"error": "Course not found"})

# 1. Python executes the local tool
live_data = get_timetable("CSC101")
print(f"Tool Returned: {live_data}\n")

# 2. Inject tool data into Gemini's context
prompt = (
    f"Campus Timetable Live Result: {live_data}\n"
    "Student Question: Where is my CSC101 class this morning?\n"
    "Answer in a friendly, conversational sentence."
)

print("--- [TOOL-AUGMENTED GEMINI RESPONSE] ---")
print(ask_gemini(prompt).strip())
