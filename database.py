import aiosqlite
from datetime import datetime

DB_PATH = "users.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                status      TEXT DEFAULT 'new',
                -- new | funnel | link_sent | registered | done
                registered_at   TEXT,
                reminded_1  INTEGER DEFAULT 0,
                reminded_2  INTEGER DEFAULT 0,
                reminded_3  INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.commit()

async def upsert_user(user_id: int, username: str, first_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO NOTHING
        """, (user_id, username, first_name))
        await db.commit()

async def set_status(user_id: int, status: str):
    ts = datetime.now().isoformat() if status == "registered" else None
    async with aiosqlite.connect(DB_PATH) as db:
        if ts:
            await db.execute(
                "UPDATE users SET status=?, registered_at=? WHERE user_id=?",
                (status, ts, user_id)
            )
        else:
            await db.execute(
                "UPDATE users SET status=? WHERE user_id=?",
                (status, user_id)
            )
        await db.commit()

async def get_users_for_reminder(day: int):
    """Возвращает user_id тех, кому пора слать N-е напоминание."""
    col = f"reminded_{day}"
    # Зарегистрировались X дней назад и ещё не получали это напоминание
    from config import REMINDER_DAY_1, REMINDER_DAY_2, REMINDER_DAY_3
    days_map = {1: REMINDER_DAY_1, 2: REMINDER_DAY_2, 3: REMINDER_DAY_3}
    delta = days_map[day]

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(f"""
            SELECT user_id FROM users
            WHERE {col} = 0
              AND status IN ('link_sent', 'registered')
              AND registered_at IS NOT NULL
              AND julianday('now') - julianday(registered_at) >= ?
        """, (delta,))
        rows = await cursor.fetchall()
        return [r[0] for r in rows]

async def mark_reminded(user_id: int, day: int):
    col = f"reminded_{day}"
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE users SET {col}=1 WHERE user_id=?", (user_id,))
        await db.commit()

async def all_users_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT status, COUNT(*) FROM users GROUP BY status
        """)
        return await cursor.fetchall()
