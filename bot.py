import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import aiosqlite

from database import init_db, DB_NAME
from leetcode import solved_today, fetch_problem_difficulty

TOKEN = os.getenv("TOKEN")   
REMINDER_CHANNEL_ID = 1449955258150162462 
POINTS = {"Easy": 10, "Medium": 20, "Hard": 30}
DAILY_POINT_LIMIT = 5

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await init_db()
    daily_reminder.start()
    print("Bot is online")

@bot.command()
async def register(ctx, leetcode_username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users(discord_id, leetcode_username) VALUES (?,?)",
            (str(ctx.author.id), leetcode_username)
        )
        await db.commit()
    await ctx.send(" LeetCode username registered")

@bot.command()
async def submit(ctx, problem_url: str):
    slug = problem_url.rstrip("/").split("/")[-1]
    discord_id = str(ctx.author.id)
    today = datetime.now().date().isoformat()

    async with aiosqlite.connect(DB_NAME) as db:
        # Fetch user
        cur = await db.execute(
            "SELECT leetcode_username, streak, last_active_date FROM users WHERE discord_id=?",
            (discord_id,)
        )
        user = await cur.fetchone()

        if not user:
            await ctx.send("Register first using `/register <leetcode_username>`")
            return

        username, streak, last_date = user

        cur = await db.execute("""
            SELECT 1 FROM submissions
            WHERE discord_id=? AND problem_slug=? AND submission_date=?
        """, (discord_id, slug, today))
        if await cur.fetchone():
            await ctx.send(" You already submitted this problem today")
            return

        # Verify with LeetCode
        try:
            if not solved_today(username, slug):
                await ctx.send(" No accepted submission today on LeetCode")
                return
            difficulty = fetch_problem_difficulty(slug)
        except Exception:
            await ctx.send("LeetCode error. Try again later.")
            return

        cur = await db.execute("""
            SELECT COUNT(*) FROM submissions
            WHERE discord_id=? AND submission_date=?
        """, (discord_id, today))
        count_today = (await cur.fetchone())[0]

        if count_today < DAILY_POINT_LIMIT:
            reward_points = POINTS[difficulty]
            reward_msg = f"+{reward_points} points"
        else:
            reward_points = 0
            reward_msg = "No points (daily limit reached)"

        if last_date == today:
            new_streak = streak
        elif last_date:
            gap = (datetime.fromisoformat(today) -
                   datetime.fromisoformat(last_date)).days
            new_streak = streak + 1 if gap == 1 else 1
        else:
            new_streak = 1

        await db.execute("""
            INSERT INTO submissions(discord_id, problem_slug, difficulty, submission_date)
            VALUES (?,?,?,?)
        """, (discord_id, slug, difficulty, today))

        await db.execute("""
            UPDATE users
            SET total_points = total_points + ?,
                streak = ?,
                last_active_date = ?
            WHERE discord_id = ?
        """, (reward_points, new_streak, today, discord_id))

        await db.commit()

    await ctx.send(
        f" **Verified**\n"
        f"Difficulty: `{difficulty}`\n"
        f"{reward_msg}\n"
        f" Streak: {new_streak}\n"
        f" Today: {count_today + 1}/{DAILY_POINT_LIMIT}"
    )

@bot.command()
async def leaderboard(ctx):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("""
            SELECT leetcode_username, total_points, streak
            FROM users
            ORDER BY total_points DESC
        """)
        rows = await cur.fetchall()

    if not rows:
        await ctx.send("No data yet.")
        return

    msg = " **Leaderboard**\n\n"
    for i, r in enumerate(rows, start=1):
        msg += f"{i}. `{r[0]}` — {r[1]} pts |  {r[2]}\n"

    await ctx.send(msg)


@tasks.loop(time=time(hour=15, minute=30))
async def daily_reminder():
    channel = bot.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        await channel.send(
            " **Daily Reminder**\n"
            "Solve at least **1 LeetCode problem today** to keep your streak alive \n"
            "Use `/submit <problem_url>` after solving."
        )

bot.run(TOKEN)
