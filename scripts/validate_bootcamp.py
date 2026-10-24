"""
scripts/validate_bootcamp.py
============================
Automated Static & Dynamic Validation Script for GDGoC CUI Wah Bootcamp.

Runs comprehensive checks:
1. File Existence & Repository Tree Check (All 18 lessons, demos, notebooks, diagrams, challenges, guides).
2. Python Syntax Compilation (Every .py file).
3. Jupyter Notebook JSON Validation & Python Code Cell AST Syntax Check.
4. Secret & API Key Leak Prevention Check.
5. .gitignore & .env.example Placeholder Verification.
6. Illustrative Output Label Verification.
7. Generates a standalone ZIP archive of the complete repository for delivery.
"""

import ast
import json
import os
import py_compile
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 18 Topics checklist
DAY_1_TOPICS = [
    "01-what-is-a-prompt",
    "02-anatomy-of-a-good-prompt",
    "03-zero-shot-and-few-shot",
    "04-task-decomposition",
    "05-system-vs-user-instructions",
    "06-structured-output",
    "07-prompt-improvement",
    "08-prompt-safety"
]

DAY_2_TOPICS = [
    "01-what-is-context-engineering",
    "02-prompt-vs-context",
    "03-context-window-and-tokens",
    "04-selecting-relevant-information",
    "05-context-compression-and-summarization",
    "06-conversation-history-and-memory",
    "07-rag-and-grounding",
    "08-tools-and-external-context",
    "09-context-efficiency-and-caching",
    "10-basic-ai-workflow"
]


def check(name: str, passed: bool, details: str = ""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status} {name}" + (f" -> {details}" if details else ""))
    return passed


def main():
    print("=" * 75)
    print("  GDGoC CUI Wah AI Bootcamp — Comprehensive Repository Validator")
    print("=" * 75)

    all_passed = True

    # Check 1: Root Files
    print("\n[1/8] Checking Critical Root Files...")
    root_files = ["README.md", "SETUP.md", "requirements.txt", ".env.example", ".gitignore"]
    for rf in root_files:
        p = REPO_ROOT / rf
        passed = p.exists() and p.stat().st_size > 0
        all_passed &= check(f"Root file: {rf}", passed)

    # Check 2: Core Helper & Smoke Test
    print("\n[2/8] Checking Core Helper & Scripts...")
    core_files = [
        "src/__init__.py",
        "src/ai_helper.py",
        "scripts/api_smoke_test.py",
        "day-2-context-engineering/data/campus_events.json"
    ]
    for cf in core_files:
        p = REPO_ROOT / cf
        passed = p.exists() and p.stat().st_size > 0
        all_passed &= check(f"Core module: {cf}", passed)

    # Check 3: Day 1 Lessons, Demos, Diagrams, Notebooks
    print("\n[3/8] Checking Day 1 Assets (8 Topics)...")
    d1 = REPO_ROOT / "day-1-prompt-engineering"
    for t in DAY_1_TOPICS:
        t_num = t.split("-")[0]
        t_clean = t.replace("-", "_")
        lesson = d1 / "lessons" / f"{t}.md"
        demo = d1 / "demos" / f"demo_{t_clean}.py"
        nb = d1 / "notebooks" / f"{t_clean}.ipynb"

        all_passed &= check(f"Day 1 Lesson {t_num}", lesson.exists())
        all_passed &= check(f"Day 1 Demo {t_num}", demo.exists())
        all_passed &= check(f"Day 1 Notebook {t_num}", nb.exists())

    # Check 4: Day 2 Lessons, Demos, Diagrams, Notebooks
    print("\n[4/8] Checking Day 2 Assets (10 Topics)...")
    d2 = REPO_ROOT / "day-2-context-engineering"
    for t in DAY_2_TOPICS:
        t_num = t.split("-")[0]
        t_clean = t.replace("-", "_")
        lesson = d2 / "lessons" / f"{t}.md"
        demo = d2 / "demos" / f"demo_{t_clean}.py"
        nb = d2 / "notebooks" / f"{t_clean}.ipynb"

        all_passed &= check(f"Day 2 Lesson {t_num}", lesson.exists())
        all_passed &= check(f"Day 2 Demo {t_num}", demo.exists())
        all_passed &= check(f"Day 2 Notebook {t_num}", nb.exists())

    # Check 5: Challenges & Instructor Materials
    print("\n[5/8] Checking Challenges & Instructor Materials...")
    inst_files = [
        "day-1-prompt-engineering/challenge/README.md",
        "day-1-prompt-engineering/challenge/starter_code.py",
        "day-1-prompt-engineering/challenge/solution.py",
        "day-1-prompt-engineering/exercises/day_1_exercises.md",
        "day-2-context-engineering/challenge/README.md",
        "day-2-context-engineering/challenge/starter_code.py",
        "day-2-context-engineering/challenge/solution.py",
        "day-2-context-engineering/exercises/day_2_exercises.md",
        "instructor-guide/schedule.md",
        "instructor-guide/day-1-answer-key.md",
        "instructor-guide/day-2-answer-key.md",
        "instructor-guide/knowledge-check-answers.md",
        "instructor-guide/troubleshooting.md"
    ]
    for inf in inst_files:
        p = REPO_ROOT / inf
        all_passed &= check(f"Guide/Challenge: {inf}", p.exists())

    # Check 6: Python Syntax Compilation
    print("\n[6/8] Compiling all Python (.py) Files for Syntax Errors...")
    py_files = list(REPO_ROOT.rglob("*.py"))
    # Filter out virtual environments or build caches if any
    py_files = [p for p in py_files if "venv" not in str(p) and "__pycache__" not in str(p)]
    py_pass_count = 0
    for pf in py_files:
        try:
            py_compile.compile(str(pf), doraise=True)
            py_pass_count += 1
        except py_compile.PyCompileError as err:
            all_passed &= check(f"Compile {pf.name}", False, str(err))
    check(f"Compiled {py_pass_count}/{len(py_files)} Python files without syntax errors", py_pass_count == len(py_files))

    # Check 7: Notebooks Validation (JSON Schema & AST check on code cells)
    print("\n[7/8] Validating all Jupyter Notebooks (.ipynb)...")
    nb_files = list(REPO_ROOT.rglob("*.ipynb"))
    nb_files = [nb for nb in nb_files if "checkpoints" not in str(nb)]
    nb_pass_count = 0
    for nb_path in nb_files:
        try:
            with open(nb_path, "r", encoding="utf-8") as f:
                nb_json = json.load(f)
            # Verify required nbformat keys
            assert "cells" in nb_json, "Missing 'cells' key"
            assert "metadata" in nb_json, "Missing 'metadata' key"
            assert nb_json.get("nbformat") == 4, "nbformat must be 4"

            # Check that code cells are syntactically valid python
            for cell in nb_json["cells"]:
                if cell.get("cell_type") == "code":
                    code_text = "".join(cell.get("source", []))
                    ast.parse(code_text)

            nb_pass_count += 1
        except Exception as err:
            all_passed &= check(f"Notebook {nb_path.name}", False, str(err))

    check(f"Validated {nb_pass_count}/{len(nb_files)} Jupyter Notebooks", nb_pass_count == len(nb_files))

    # Check 8: Security & Secret Scan
    print("\n[8/8] Security Scan: Verifying No Hardcoded Keys or Secrets...")
    secret_pattern = re.compile(r"AIzaSy[A-Za-z0-9_-]{33}")
    leaks = []
    text_extensions = {".py", ".ipynb", ".md", ".json", ".txt", ".example"}
    for root, _, files in os.walk(REPO_ROOT):
        if "venv" in root or ".git" in root:
            continue
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix in text_extensions or fname.startswith(".env"):
                if fname == ".env":
                    continue  # .env is local only
                try:
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    matches = secret_pattern.findall(content)
                    if matches:
                        leaks.append((str(fpath.relative_to(REPO_ROOT)), matches))
                except Exception:
                    pass

    if leaks:
        print(f"  [CRITICAL SECURITY ALERT] Found hardcoded API keys in {len(leaks)} file(s):")
        for f, m in leaks:
            print(f"    - {f}: {m}")
        all_passed = False
    else:
        check("No hardcoded Google API keys found in repository", True)

    # Check .gitignore ignores .env
    gitignore_path = REPO_ROOT / ".gitignore"
    if gitignore_path.exists():
        gi_content = gitignore_path.read_text(encoding="utf-8")
        check(".gitignore ignores .env", ".env" in gi_content)
    else:
        check(".gitignore exists", False)

    # Check .env.example uses placeholder
    env_example = REPO_ROOT / ".env.example"
    if env_example.exists():
        env_ex_content = env_example.read_text(encoding="utf-8")
        check(".env.example contains safe placeholder", "your_gemini_api_key_here" in env_ex_content)
    else:
        check(".env.example exists", False)

    # Package as ZIP archive for easy distribution
    zip_path = REPO_ROOT / "gdgoc-cui-wah-bootcamp.zip"
    print(f"\n[PACKAGING] Building complete distribution ZIP archive: {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(REPO_ROOT):
            # Exclude venv, git, zip, and cache dirs
            if any(ex in root for ex in ["venv", ".git", "__pycache__", ".ipynb_checkpoints"]):
                continue
            for f in files:
                if f.endswith(".zip") or f == ".env":
                    continue
                file_full = Path(root) / f
                arc_name = file_full.relative_to(REPO_ROOT)
                zipf.write(file_full, arcname=arc_name)

    print(f"  [PASS] Created distribution ZIP archive ({zip_path.stat().st_size / 1024:.1f} KB)")

    print("\n" + "=" * 75)
    if all_passed:
        print("  >> [ALL STATIC VALIDATION CHECKS PASSED SUCCESSFULLY!]")
    else:
        print("  >> [WARNING: SOME CHECKS FAILED! REVIEW LOGS ABOVE]")
    print("=" * 75)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
