# 🛠️ Setup Guide: GDGoC CUI Wah AI Bootcamp

Welcome to the **GDGoC CUI Wah 2-Day Prompt Engineering & Context Engineering Bootcamp**!  
This guide will walk you through setting up your computer step-by-step. Even if this is your very first time using Python or working with APIs, don't worry—follow these instructions and you'll be running live AI models in just a few minutes!

---

## 📋 Prerequisites

Before we start, make sure you have:
1. **A computer running Windows, macOS, or Linux.**
2. **Python 3.10, 3.11, or 3.12 installed.**  
   Check in your terminal/command prompt:
   ```bash
   python --version
   ```
   *(If not installed, download from [python.org](https://www.python.org/downloads/). On Windows, make sure to check **"Add python.exe to PATH"** during installation!)*
3. **An internet connection** (needed for contacting the Gemini API).
4. **A Google account** (to get a free Gemini API key).

---

## 🔑 Step 1: Get Your Free Google Gemini API Key

We will be interacting with Google's state-of-the-art **Gemini** models. Google provides a generous free tier for developers and students!

> [!NOTE]
> You **do not** need a credit card to get a free API key for educational learning.

1. Open your browser and navigate to **Google AI Studio**:  
   👉 [https://aistudio.google.com/](https://aistudio.google.com/)
2. Sign in with your standard Google account.
3. Click on the blue **"Get API key"** button (in the top-left or navigation bar).
4. Click **"Create API key"** and select **"Create API key in new project"**.
5. Copy the generated key (it looks like a string starting with `AIzaSy...`).

> [!IMPORTANT]
> **API Key Safety Rule:**  
> Never share your API key with anyone, never post it on WhatsApp groups or Discord, and **never commit it to GitHub**. Treat it like your ATM PIN or university portal password!

---

## 💻 Step 2: Open Terminal & Navigate to Project

Open your favorite terminal or editor (like VS Code or Windows Terminal) and navigate to the bootcamp directory:

### On Windows (PowerShell):
```powershell
cd c:\Users\HP\OneDrive\Desktop\Bootcamp
```

### On macOS / Linux:
```bash
cd /path/to/Bootcamp
```

---

## 🐍 Step 3: Create & Activate a Python Virtual Environment

A virtual environment keeps your project dependencies clean and isolated.

### On Windows (PowerShell):
```powershell
# 1. Create the virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1
```

*(If PowerShell shows a script execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then activate again).*

### On macOS / Linux:
```bash
# 1. Create the virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate
```

When activated, you will see `(venv)` at the beginning of your terminal prompt!

---

## 📦 Step 4: Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `google-genai`: Google's official, modern Python SDK for Gemini models.
- `python-dotenv`: Automatically loads environment variables from a `.env` file.
- `jupyter`: Enables interactive Jupyter Notebooks.
- `colorama`: Pretty terminal colors for easy reading.

---

## 🔐 Step 5: Configure Your API Key in `.env`

In the root of the repository, copy the provided `.env.example` file to create your own `.env` file:

### On Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

### On macOS / Linux:
```bash
cp .env.example .env
```

Now open `.env` in any text editor (Notepad, VS Code, etc.) and replace `your_gemini_api_key_here` with your actual key:

```env
GEMINI_API_KEY=AIzaSyYourActualKeyHere12345
GEMINI_MODEL=gemini-2.5-flash
```

Save and close the file.  
*(Notice that `.env` is listed in `.gitignore`, so Git will never accidentally publish your key).*

---

## 🧪 Step 6: Run the API Smoke Test

Let's verify that your environment, packages, and API key are working properly!

Run:
```bash
python scripts/api_smoke_test.py
```

### What You Should See:
- **SDK Check:** `[PASS] Official 'google-genai' SDK is installed.`
- **Config Check:** `[PASS] GEMINI_API_KEY detected`
- **Live Call:** Sends a tiny test message to Gemini and displays its genuine live response:
  ```text
  [LIVE RESPONSE FROM GEMINI]
  "GDGoC Wah AI Test OK: Model is online and ready!"
  [PASS] Live Gemini API connection successful!
  ```

---

## 🚀 Step 7: How to Run Lessons & Demos

You can run lessons in two ways:

### Option A: As Standalone Python Scripts
Run any demo directly from the repository root:
```bash
# Day 1 - Topic 1
python day-1-prompt-engineering/demos/demo_01_what_is_a_prompt.py

# Day 2 - Topic 1
python day-2-context-engineering/demos/demo_01_what_is_context_engineering.py
```

### Option B: As Interactive Jupyter Notebooks
Launch Jupyter Notebook to experiment interactively:
```bash
jupyter notebook
```
Your browser will open! Click on any notebook in `day-1-prompt-engineering/notebooks/` or `day-2-context-engineering/notebooks/` and press **Shift + Enter** to execute cells one by one.

---

## ❓ Troubleshooting Common Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `[GDGoC Error] GEMINI_API_KEY is not configured!` | Missing `.env` file or key is still placeholder. | Check that `.env` exists in the repo root and contains your real key. |
| `Invalid Gemini API Key (401 Unauthorized)` | Typos in the API key string. | Re-copy the key from [Google AI Studio](https://aistudio.google.com/) and paste without extra spaces. |
| `Rate Limit or Quota Exceeded (429)` | Too many requests in 60 seconds on free tier. | Wait 60 seconds and run the script again. Free-tier quotas refresh automatically. |
| `ModuleNotFoundError: No module named 'google'` | Dependencies not installed in active environment. | Ensure `(venv)` is active and run `pip install -r requirements.txt`. |
| `Script Execution Policy Error` (PowerShell) | Windows default policy restricts `.ps1` execution. | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in your PowerShell window. |

---

Happy learning! You are now ready to begin **Day 1: Prompt Engineering**! 🌟
