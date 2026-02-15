import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
import database
from handlers import start, rates, calculator, chart, extras

async def main():
    # Logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    # Init DB
    await database.init_db()

    # Bot & Dispatcher
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Register Routers
    dp.include_router(start.router)
    dp.include_router(rates.router)
    dp.include_router(calculator.router)
    dp.include_router(chart.router)
    dp.include_router(extras.router)

    # Start Polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
