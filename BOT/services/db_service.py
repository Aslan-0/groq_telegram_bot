import asyncpg
import os
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

log = get_logger(__name__)
db_pool = None

async def connect_db():
    global db_pool
    db_pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    log.info("База данных подключена! ✅")

async def save_user(user_id: int, name: str):
    await db_pool.execute(
        """
        INSERT INTO users (user_id, name) 
        VALUES ($1, $2) 
        ON CONFLICT (user_id) 
        DO UPDATE SET name = $2
        """,
        user_id, name
    )
    log.info(f"Пользователь {user_id} сохранён с именем: {name}")

async def save_message(user_id: int, role: str, message: str):
    await db_pool.execute(
        "INSERT INTO conversations (user_id, role, message) VALUES ($1, $2, $3)",
        user_id, role, message
    )

async def get_history(user_id: int):
    rows = await db_pool.fetch(
        "SELECT role, message FROM conversations WHERE user_id = $1 ORDER BY created_at ASC LIMIT 20",
        user_id
    )
    return rows

async def save_mood(user_id: int, mood: str):
    await db_pool.execute(
        "INSERT INTO mood_logs (user_id, mood) VALUES ($1, $2)",
        user_id, mood
    )
    log.info(f"Настроение пользователя {user_id} сохранено: {mood}")
    
async def get_user(user_id: int):
    row = await db_pool.fetchrow(
        "SELECT * FROM users WHERE user_id = $1",
        user_id
    )
    return row

async def get_all_users():
    rows = await db_pool.fetch(
        "SELECT user_id, name, created_at FROM users ORDER BY created_at DESC"
    )
    return rows

async def get_total_users():
    count = await db_pool.fetchval("SELECT COUNT(*) FROM users")
    return count

async def get_messages_today():
    count = await db_pool.fetchval(
        "SELECT COUNT(*) FROM conversations WHERE DATE(created_at) = CURRENT_DATE"
    )
    return count

async def get_mood_stats():
    rows = await db_pool.fetch(
        """
        SELECT mood, COUNT(*) as count 
        FROM mood_logs 
        WHERE DATE(created_at) = CURRENT_DATE 
        GROUP BY mood
        """
    )
    return rows

async def get_user_conversations(user_id: int):
    rows = await db_pool.fetch(
        """
        SELECT role, message, created_at 
        FROM conversations 
        WHERE user_id = $1 
        ORDER BY created_at ASC
        """,
        user_id
    )
    return rows


async def save_goal(user_id: int, goal_text: str):
    # Деактивируем старые цели
    await db_pool.execute(
        "UPDATE goals SET is_active = FALSE WHERE user_id = $1",
        user_id
    )
    # Создаём новую цель
    goal_id = await db_pool.fetchval(
        "INSERT INTO goals (user_id, goal_text) VALUES ($1, $2) RETURNING id",
        user_id, goal_text
    )
    log.info(f"Цель пользователя {user_id} сохранена: {goal_text}")
    return goal_id

async def get_active_goal(user_id: int):
    row = await db_pool.fetchrow(
        "SELECT * FROM goals WHERE user_id = $1 AND is_active = TRUE ORDER BY created_at DESC LIMIT 1",
        user_id
    )
    return row

async def save_goal_progress(goal_id: int, user_id: int, completed: bool):
    await db_pool.execute(
        "INSERT INTO goal_progress (goal_id, user_id, completed) VALUES ($1, $2, $3)",
        goal_id, user_id, completed
    )
    log.info(f"Прогресс цели {goal_id} для пользователя {user_id}: {completed}")

async def get_goal_streak(user_id: int, goal_id: int):
    rows = await db_pool.fetch(
        """
        SELECT completed, date 
        FROM goal_progress 
        WHERE user_id = $1 AND goal_id = $2 
        ORDER BY date DESC
        """,
        user_id, goal_id
    )
    
    streak = 0
    for row in rows:
        if row['completed']:
            streak += 1
        else:
            break
    
    return streak