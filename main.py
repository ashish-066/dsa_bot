import discord
import re
import json
import requests
import os

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxEjJHTd6gvXOyxXkAKCwSKNnDbNYIhYYh9fmBB47_9f5qSN2r3r_XcirpC76-o4mWfRw/exec"
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!dsa"):
        text = message.content

        day = re.search(r"Day:\s*(\d+)", text)
        p1 = re.search(r"P1:\s*(.*?),\s*(.*?),\s*(\d+)", text)
        p2 = re.search(r"P2:\s*(.*?),\s*(.*?),\s*(\d+)", text)
        p3 = re.search(r"P3:\s*(.*?),\s*(.*?),\s*(\d+)", text)
        notes = re.search(r"Notes:\s*(.*)", text)

        if not (day and p1 and p2 and p3):
            await message.reply("❌ Invalid format. Use:\n```\n!dsa\nDay: 1\nP1: name, diff, time\nP2: name, diff, time\nP3: name, diff, time\nNotes: text\n```")
            return

        data = {
            "day": int(day.group(1)),
            "date": "AUTO",
            "problem1": p1.group(1),
            "diff1": p1.group(2),
            "time1": int(p1.group(3)),
            "problem2": p2.group(1),
            "diff2": p2.group(2),
            "time2": int(p2.group(3)),
            "problem3": p3.group(1),
            "diff3": p3.group(2),
            "time3": int(p3.group(3)),
            "notes": notes.group(1) if notes else "",
            "completed": "Y"
        }

        r = requests.post(WEBHOOK_URL, json=data)

        if r.status_code == 200:
            await message.reply("🔥 DSA Updated Successfully!")
        else:
            await message.reply("❌ Failed to update Google Sheet.")

client.run(TOKEN)
