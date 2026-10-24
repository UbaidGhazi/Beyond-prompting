"""
CampusMind — Live Chatbot & RAG Web Server (Day 2)
=================================================
Connects CampusMind Context Engineering Chatbot directly with the
CUI Wah Grounded RAG Web Server on http://localhost:8000.
Supports Google Gemini multi-key auto-failover.
"""

import argparse
import os
import sys
import webbrowser
from pathlib import Path

# Add project root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.ai_helper import check_api_setup
import chatbot_project
from rag_web_server import run_server, PORT


def print_banner(setup_info):
    keys_count = setup_info.get("key_count", 0)
    primary_mask = setup_info.get("api_key_masked", "NOT_SET")
    failover_status = "ACTIVE (Multi-Key Failover Enabled)" if setup_info.get("failover_enabled") else "Single Key"

    print("\n" + "=" * 70)
    print(" 🤖 CampusMind — Live Context Engineering Chatbot & RAG Server")
    print("    COMSATS University Islamabad • Wah Campus (GDGoC Bootcamp)")
    print("=" * 70)
    print(f" 🔑 API Key Status  : {keys_count} key(s) detected [{primary_mask}]")
    print(f" 🔄 Auto-Failover   : {failover_status}")
    print(f" 🧠 Default Model   : {setup_info.get('configured_model')}")
    print(f" 🌐 Web Host URL    : http://localhost:{PORT}")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="CampusMind Live Chatbot & RAG Web Server on Localhost"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run interactive terminal CLI chatbot instead of localhost web server"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help=f"Port to run the localhost server on (default: {PORT})"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open default web browser"
    )
    args = parser.parse_args()

    setup_info = check_api_setup()
    print_banner(setup_info)

    if args.cli:
        print(">> Launching Terminal Interactive Mode...\n")
        chatbot_project.interactive_loop()
    else:
        url = f"http://localhost:{args.port}"
        print(f"🚀 Starting Live Chatbot & RAG Web Server on {url} ...")
        if not args.no_browser:
            try:
                # Open browser slightly after start
                import threading
                threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            except Exception:
                pass
        run_server(port=args.port)


if __name__ == "__main__":
    main()
