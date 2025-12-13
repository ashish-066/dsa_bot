import discord
import re
import requests
import os
from datetime import datetime

WEBHOOK_URL = "YOUR_WEBHOOK_URL"
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def extract(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!dsa"):
        text = message.content
        
        day   = extract(r"Day:\s*(\d+)", text)

        p1    = extract(r"P1:\s*(.+)", text)
        diff1 = extract(r"Diff1:\s*(.+)", text)
        time1 = extract(r"Time1:\s*(\d+)", text)

        p2    = extract(r"P2:\s*(.+)", text)
        diff2 = extract(r"Diff2:\s*(.+)", text)
        time2 = extract(r"Time2:\s*(\d+)", text)

        p3    = extract(r"P3:\s*(.+)", text)
        diff3 = extract(r"Diff3:\s*(.+)", text)
        time3 = extract(r"Time3:\s*(\d+)", text)

        notes = extract(r"Notes:\s*(.+)", text) or ""
        completed = extract(r"Completed:\s*(Y|N)", text) or "Y"

        # Validate
        if not all([day, p1, diff1, time1, p2, diff2, time2, p3, diff3, time3]):
            await message.reply("❌ Invalid format. Missing fields.")
            return

        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "day": int(day),

            "problem1": p1,
            "diff1": diff1,
            "time1": int(time1),

            "problem2": p2,
            "diff2": diff2,
            "time2": int(time2),

            "problem3": p3,
            "diff3": diff3,
            "time3": int(time3),

            "notes": notes,
            "completed": completed
        }

        r = requests.post(WEBHOOK_URL, json=data)

        if r.status_code == 200:
            await message.reply("🔥 DSA Updated Successfully!")
        else:
            await message.reply("❌ Failed to update Google Sheet.")

client.run(TOKEN)
