import discord
from discord import app_commands
import requests
import os
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxEjJHTd6gvXOyxXkAKCwSKNnDbNYIhYYh9fmBB47_9f5qSN2r3r_XcirpC76-o4mWfRw/exec"
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot logged in as {client.user}")
    print("Slash commands synced")

@tree.command(name="dsa", description="Log daily DSA progress")
async def dsa(
    interaction: discord.Interaction,
    day: int,

    problem1: str,
    time1: int,

    problem2: str,
    time2: int,

    problem3: str,
    time3: int,

    notes: str = ""
):
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "day": day,

        "problem1": problem1,
        "time1": time1,

        "problem2": problem2,
        "time2": time2,

        "problem3": problem3,
        "time3": time3,

        "notes": notes
    }

    r = requests.post(WEBHOOK_URL, json=data)

    if r.status_code == 200:
        await interaction.response.send_message(
            "🔥 DSA logged successfully!", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ Failed to update Google Sheet.", ephemeral=True
        )

client.run(TOKEN)

