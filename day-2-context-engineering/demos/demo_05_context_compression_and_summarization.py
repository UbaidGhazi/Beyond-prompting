"""Topic 05: Context Compression and Summarization"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# Long campus lab policy
long_policy = (
    "COMSATS WAH COMPUTING LAB POLICY 2026: "
    "1. All students entering CS Labs 01-06 must display university ID cards. "
    "2. Backpacks must be placed on wooden storage racks near the door. "
    "3. Absolutely no food items or chips permitted near terminals. "
    "4. For hackathons past 5:00 PM, an approved gate pass signed 24h prior is mandatory."
)

# 1. Compress long policy into 3 bullets
summary = ask_gemini(f"Condense this policy into 3 concise bullet points:\n{long_policy}").strip()
print("--- [1] GENERATED COMPACT SUMMARY ---")
print(summary)

# 2. Answer question using the compact summary
question = "Can I bring my backpack and chips into CS Lab 03?"
print("\n--- [2] ANSWER USING COMPRESSED CONTEXT ---")
print(ask_gemini(f"Context:\n{summary}\n\nQuestion: {question}").strip())
