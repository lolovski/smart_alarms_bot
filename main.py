import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI

from middleware.user import UserMiddleware
from api.alarms import router as alarms_router
app = FastAPI()
app.include_router(alarms_router)

dp = Dispatcher()

dot = load_dotenv('.env')

API_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.update.middleware.register(UserMiddleware(bot=bot))


async def main() -> None:
    # wait async_main()
    # await add_visits()
    from handlers.basic import router as basic_router
    dp.include_router(basic_router)
    from handlers.start import router as start_router
    dp.include_router(start_router)
    from handlers.alarms import router as alarm_router
    dp.include_router(alarm_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
