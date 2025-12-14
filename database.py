import aiosqlite

DB_NAME = "dsa.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            discord_id TEXT PRIMARY KEY,
            leetcode_username TEXT UNIQUE,
            streak INTEGER DEFAULT 0,
            last_active_date TEXT,
            total_points INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT,
            problem_slug TEXT,
            difficulty TEXT,
            submission_date TEXT
        )
        """)
        await db.commit()
