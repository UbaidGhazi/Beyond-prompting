# 🏆 Day 1 Capstone Challenge: Fictional Campus Announcement Generator

Welcome to your **Day 1 Capstone Challenge**!  
You have learned the 5 pillars of prompt anatomy, few-shot conditioning, task decomposition, system instructions, structured output, and safety. Now it's time to put your skills to the test by creating a production-quality, constrained announcement generator for a fictional GDGoC campus event.

---

## 🎯 Learning Objective
Synthesize all Day 1 prompt engineering techniques to craft, configure, and execute a live prompt against Google's Gemini API that generates a structured, tone-calibrated, campus-accurate event announcement.

---

## 📋 The Fictional Event Brief
Your student chapter (**GDGoC CUI Wah**) is hosting an official workshop. Here are the **unalterable, verified facts** you must integrate:

- **Event Name:** `Git & GitHub Essentials for First-Semester Devs`
- **Organizing Society:** `Google Developer Groups on Campus (GDGoC) — COMSATS University Islamabad, Wah Campus`
- **Date & Day:** `Friday, November 27, 2026`
- **Time:** `02:00 PM - 05:00 PM`
- **Venue:** `CS Lab 05, Academic Block 2, CUI Wah`
- **Target Audience:** `First-year undergraduate students (CS, SE, AI) who have never pushed code before`
- **Fee:** `100% Free of Cost`
- **Registration Deadline:** `November 25, 2026`
- **Registration Link:** `https://cuiwah.gdgoc.example/register-git`
- **Prerequisites:** `Personal laptop + Free GitHub account created beforehand`
- **Tone:** `Energetic, encouraging, welcoming, free of intimidating jargon`
- **Length Constraint:** `Between 90 and 130 words`

*(Note: All dates, venues, and links above are fictional teaching data for this bootcamp).*

---

## 📝 Required Output Structure
Your generated announcement must include the following distinct visual blocks:
1. **Catchy Headline:** High energy with relevant emojis.
2. **Hook:** 1–2 sentences addressing first-semester students and relieving anxiety about git conflicts.
3. **Event Snapshot:** Clear bullet list of Date, Time, Venue, and Free Entry status.
4. **Key Takeaways:** 3 bullet points outlining what students will actually practice.
5. **Call to Action (CTA):** Clear deadline and registration link placeholder.

---

## 🚀 Step-by-Step Student Instructions
1. Open [`starter_code.py`](starter_code.py).
2. Review the `build_capstone_prompt()` function.
3. Replace the `TODO` placeholders with your crafted prompt implementing all 5 pillars:
   - **Role:** GDGoC Student Community Lead.
   - **Task:** Write an announcement for the workshop.
   - **Context:** Embed all facts from the Event Brief.
   - **Constraints:** 90–130 words, energetic tone, zero jargon.
   - **Format:** The 5-block structure outlined above.
4. Execute the Python script against the real Gemini API:
   ```bash
   python day-1-prompt-engineering/challenge/starter_code.py
   ```
5. Inspect the live model output. If the response is too long, missing details, or vague, adjust your constraints and re-run.
6. Write a short 3-sentence reflection in the comments answering:
   - Did Gemini follow the word limit?
   - Did it include all campus facts accurately?
   - What prompt tweak made the biggest difference?

---

## 📄 Illustrative Sample Output
> *Illustrative output — actual Gemini responses may vary.*

```text
🔥 Stop Fearing the Terminal: Master Git & GitHub! 💻

Hey 1st-Semester Devs! Worried about losing your semester code or panicking over your first group project? GDGoC CUI Wah has your back!

📍 Event Snapshot:
• When: Friday, Nov 27, 2026 | 2:00 PM – 5:00 PM
• Where: CS Lab 05, Academic Block 2, CUI Wah
• Entry: 100% Free!

What You Will Build:
🚀 Initialize, commit, and push your first repository
🤝 Collaborate on open-source projects without merge tears
✨ Showcase your projects proudly on your GitHub profile

Laptop required + free GitHub account.
Seats are limited in Lab 05! Register before Nov 25:
👉 https://cuiwah.gdgoc.example/register-git
```

---

## 📊 Grading Rubric (10 Points Total)

| Criterion | Points | Description |
| :--- | :---: | :--- |
| **Role & Task Definition** | **2 pts** | Clearly defines the AI persona (GDGoC Lead) and the exact goal (WhatsApp/LinkedIn announcement). |
| **Accurate Campus Facts** | **2 pts** | Faithfully incorporates all brief facts (date, lab 5, free entry, deadline) without hallucinations. |
| **Constraints & Tone** | **2 pts** | Successfully enforces length (90–130 words) and an encouraging, student-friendly tone. |
| **Output Structure** | **2 pts** | Response contains headline, hook, event snapshot, 3 takeaways, and CTA. |
| **Execution & Reflection** | **2 pts** | Student runs the live API call and provides thoughtful reflection on the model's actual response. |

---

## ✅ Submission Checklist
- [ ] Modified `starter_code.py` with your custom prompt.
- [ ] Ran the script and verified a live Gemini response is printed.
- [ ] Verified word count falls within 90–130 words.
- [ ] Confirmed CS Lab 05 and Nov 27 are accurately mentioned.
- [ ] Completed the reflection block in the script.
