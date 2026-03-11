import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from handlers import start, chat, mood, goals
from services.db_service import connect_db
from logger import get_logger

load_dotenv()

log = get_logger(__name__)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(mood.router)
dp.include_router(goals.router)
dp.include_router(chat.router)

async def main():
    await connect_db()
    log.info("База данных подключена!")
    log.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())