import asyncio
import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv

from commands.handlers import router
from db import database
from db import db_utils

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def init_db():
    db = database.Database()
    session = await db.get_session()
    br = db_utils.BudgetModel(session)
    await db.create_db()
    await db.close()


async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" ")
