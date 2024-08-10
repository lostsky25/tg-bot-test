import os
import asyncio
import logging
from dotenv import load_dotenv, dotenv_values

from aiogram import Bot, Dispatcher
from app.database.models import async_main

from app.sync_data.sync_data import add_categories_to_db

from app.handlers import router

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher() # Может иметь несколько ботов

async def main():
    await async_main()
    await add_categories_to_db()

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')