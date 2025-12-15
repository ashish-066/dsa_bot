# DSA Discipline Bot 🚀

A strict Discord bot that enforces daily DSA consistency using **verified LeetCode submissions**.

This is **not** a casual tracker.  
This system is designed to reward **discipline, honesty, and consistency**.

---

## 🔥 What This Bot Does

- Verifies problems directly from **LeetCode**
- Accepts only **Accepted** submissions
- Accepts only problems solved **today**
- Permanently blocks duplicate problems
- Caps daily points to prevent farming
- Tracks streaks automatically
- Sends a daily reminder at **9:00 PM IST**

No screenshots.  
No manual checking.  
No excuses.

---

## 📜 Rules (Read Carefully)

These rules are **strict and non-negotiable**.

1. You must register your LeetCode username once.
2. Only problems solved **today** are accepted.
3. A problem can be submitted **only once ever**.
4. Daily points are awarded for the **first 5 valid submissions only**.
5. Extra submissions are stored but give **0 points**.
6. Duplicate problems are blocked permanently.
7. Verification is automatic — manual claims are ignored.

If a submission breaks any rule, it is rejected.

---

## 🤖 Bot Commands

### Register
Register your Discord account with your LeetCode profile.

/register <leetcode_username>

makefile
Copy code

Example:
/register john_doe

yaml
Copy code

---

### Submit a Problem
Submit a problem you solved **today**.

/submit <leetcode_problem_url>

makefile
Copy code

Example:
/submit https://leetcode.com/problems/two-sum/

yaml
Copy code

Conditions:
- Must be **Accepted**
- Must be solved **today**
- Must not be submitted before (ever)

---

### Leaderboard
View rankings based on total points and streaks.

/leaderboard

yaml
Copy code

---

## 🧮 Scoring System

| Difficulty | Points |
|-----------|--------|
| Easy      | 10     |
| Medium    | 20     |
| Hard      | 30     |

### Important Notes

- Only the **first 5 submissions per day** give points
- Submissions after 5 are logged but give **0 points**
- Streak = consecutive days with at least **one valid submission**

---

## ⛔ What This Bot Does NOT Track

- Time spent solving problems
- Solution quality
- Whether you copied or not
- Revision attempts

This system measures **discipline and consistency**, not effort.

---

## ⏰ Daily Reminder

The bot sends a reminder every day at **9:00 PM IST** to help users maintain their streak.

---

## ⚠️ Final Note

This system is intentionally strict.

If you are looking for:
- Flexibility
- Manual overrides
- Excuses

This bot is **not for you**.

Consistency beats motivation.  
Discipline beats talent.

---

## 🛠️ Tech Stack (For Developers)

- Python
- discord.py
- SQLite (persistent storage)
- LeetCode GraphQL (read-only verification)

---

## 📌 Summary

- Real verification
- Zero manual admin work
- No duplicate farming
- No leaderboard inflation
- No shortcuts

Show up daily or fall behind.
