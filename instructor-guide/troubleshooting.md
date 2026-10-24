# 🛠️ Instructor Guide: Troubleshooting & Debugging Handbook

This handbook contains solutions for the most frequent issues encountered by first-semester students during the **GDGoC CUI Wah AI Bootcamp**.

---

## 🛑 Top 8 Common Errors & Rapid Fixes

### 1. `[GDGoC Error] GEMINI_API_KEY is not configured!`
- **Root Cause:** The student has not created a `.env` file, or the `.env` file still contains the placeholder `your_gemini_api_key_here`.
- **Rapid Fix:**
  1. Verify that a file literally named `.env` exists in the repository root (not `.env.txt` or `.env.example`).
  2. In Windows File Explorer, ensure **"File name extensions"** is enabled under the View tab.
  3. Ensure the key inside `.env` begins with `AIzaSy...`:
     ```env
     GEMINI_API_KEY=AIzaSyB...
     ```
  4. Run `python scripts/api_smoke_test.py` to confirm detection.

---

### 2. `Invalid Gemini API Key (401 Unauthorized)`
- **Root Cause:** Typo in the API key string or accidental trailing whitespace.
- **Rapid Fix:**
  1. Open [Google AI Studio](https://aistudio.google.com/) and re-copy the key.
  2. In `.env`, paste the key directly without quotes or spaces:
     ```env
     GEMINI_API_KEY=AIzaSyYourActualKeyHere
     ```
  3. Restart the terminal or Jupyter kernel to reload environment variables.

---

### 3. `Rate Limit or Quota Exceeded (429 RESOURCE_EXHAUSTED)`
- **Root Cause:** Multiple rapid requests triggered the free-tier **Requests-Per-Minute (RPM)** or **Daily Requests Limit**.
- **Rapid Fix:**
  1. **Wait 60 seconds:** The free-tier rate limits reset automatically every minute.
  2. If a student loop triggered dozens of calls, terminate the terminal (`Ctrl + C`) and restart.
  3. If their daily free quota is fully exhausted, have them generate a fresh API key in a new project in Google AI Studio or pair-program with a lab partner.

---

### 4. `ModuleNotFoundError: No module named 'google'`
- **Root Cause:** Dependencies were installed globally or in a different Python version, and the current virtual environment is not active.
- **Rapid Fix (Windows PowerShell):**
  ```powershell
  # 1. Activate venv
  .\venv\Scripts\Activate.ps1
  # 2. Verify pip location
  Get-Command python
  # 3. Reinstall requirements
  pip install -r requirements.txt
  ```

---

### 5. PowerShell Execution Policy Restriction
- **Symptom:** `File ...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`
- **Root Cause:** Windows default PowerShell execution policy restricts unsigned `.ps1` scripts.
- **Rapid Fix:** Run this command in your PowerShell window:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  Then run `.\venv\Scripts\Activate.ps1` again.

---

### 6. `JSONDecodeError: Expecting value: line 1 column 1`
- **Root Cause:** In Topic 06, the model was called without setting `response_mime_type="application/json"`, causing the model to wrap output in markdown backticks (```` ```json ````) or conversational preamble.
- **Rapid Fix:** Ensure `ask_gemini` is passed `response_mime_type="application/json"`:
  ```python
  response = ask_gemini(prompt=prompt, response_mime_type="application/json")
  ```

---

### 7. `ModuleNotFoundError: No module named 'src'`
- **Root Cause:** A student opened a subfolder (e.g. `cd day-1-prompt-engineering/demos`) and executed `python demo_01.py`, so Python did not have the repo root in `sys.path`.
- **Rapid Fix:** All demo files in this repository include automatic root detection:
  ```python
  REPO_ROOT = Path(__file__).resolve().parent.parent.parent
  if str(REPO_ROOT) not in sys.path:
      sys.path.insert(0, str(REPO_ROOT))
  ```
  Alternatively, run all scripts from the repository root:
  ```powershell
  python day-1-prompt-engineering/demos/demo_01_what_is_a_prompt.py
  ```

---

### 8. Jupyter Notebook Uses the Wrong Python Kernel
- **Symptom:** Terminal script works, but notebook in Jupyter says `No module named 'google'`.
- **Root Cause:** Jupyter is using a global Python kernel instead of the virtual environment.
- **Rapid Fix:**
  Install `ipykernel` inside your activated `(venv)`:
  ```powershell
  pip install ipykernel
  python -m ipykernel install --user --name=bootcamp-venv --display-name="Python (Bootcamp Venv)"
  ```
  In Jupyter's menu, select **Kernel -> Change Kernel -> Python (Bootcamp Venv)**.
