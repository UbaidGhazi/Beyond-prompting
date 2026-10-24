"""
chatbot.py (Repository Root Entrypoint)
=======================================
Quick-launch entrypoint for CampusMind Live Chatbot & RAG Web Server.
Connects with Google Gemini (Auto-Failover Multi-Key) & CUI Wah Grounded RAG Corpus.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "day-2-context-engineering"))

from chatbot import main

if __name__ == "__main__":
    main()
