import asyncio
import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv

from commands.handlers import router

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" ")
