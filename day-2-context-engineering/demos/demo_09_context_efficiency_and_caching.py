"""Topic 09: Context Efficiency and Application Caching"""
import hashlib
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.ai_helper import ask_gemini

# In-memory dictionary cache
CACHE = {}

def cached_ask(prompt: str):
    key = hashlib.md5(prompt.strip().lower().encode()).hexdigest()
    t0 = time.perf_counter()
    if key in CACHE:
        return CACHE[key], "CACHE_HIT (0ms)", time.perf_counter() - t0
    res = ask_gemini(prompt, temperature=0.1)
    CACHE[key] = res
    return res, "CACHE_MISS (Called API)", time.perf_counter() - t0

query = "What are the prerequisites for the Git workshop at CUI Wah?"

# Request 1: Fresh call
res1, stat1, t1 = cached_ask(query)
print(f"Request 1: [{stat1}] in {t1:.3f}s")
print(f"Answer: {res1.strip()[:100]}...\n")

# Request 2: Duplicate call (Served instantly from local memory!)
res2, stat2, t2 = cached_ask(query)
print(f"Request 2: [{stat2}] in {t2:.6f}s")
print(f"Answer: {res2.strip()[:100]}...")
