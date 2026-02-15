import aiosqlite
import asyncio
from datetime import datetime
import config

async def init_db():
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT,
                buy_rate REAL,
                sell_rate REAL,
                cb_rate REAL,
                updated_at DATETIME
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                subscribed BOOLEAN DEFAULT 1,
                joined_at DATETIME
            )
        ''')
        await db.commit()

async def save_rate(currency, buy, sell, cb):
    async with aiosqlite.connect(config.DB_NAME) as db:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute('''
            INSERT INTO rates (currency, buy_rate, sell_rate, cb_rate, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (currency, buy, sell, cb, now))
        await db.commit()

async def get_latest_rate(currency="USD"):
    async with aiosqlite.connect(config.DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT * FROM rates WHERE currency = ? ORDER BY id DESC LIMIT 1
        ''', (currency,)) as cursor:
            return await cursor.fetchone()

async def get_history(currency="USD", days=7):
    async with aiosqlite.connect(config.DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        # Get one rate per day approx, or just last N entries if we scrape daily
        async with db.execute('''
            SELECT * FROM rates WHERE currency = ? ORDER BY id DESC LIMIT ?
        ''', (currency, days)) as cursor:
            rows = await cursor.fetchall()
            return rows[::-1] # Reverse to get chronological order

async def add_user(user_id, username):
    async with aiosqlite.connect(config.DB_NAME) as db:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, username, joined_at)
            VALUES (?, ?, ?)
        ''', (user_id, username, now))
        await db.commit()

async def toggle_subscription(user_id):
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute("SELECT subscribed FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                new_status = not row[0]
                await db.execute("UPDATE users SET subscribed = ? WHERE user_id = ?", (new_status, user_id))
                await db.commit()
                return new_status
            else:
                return False

async def get_subscribers():
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users WHERE subscribed = 1") as cursor:
            return [row[0] for row in await cursor.fetchall()]
