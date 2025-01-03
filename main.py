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

from handlers.basic import router as basic_router
from handlers.auth import router as auth_router
from handlers.alarms import router as alarm_router
from handlers.profile import router as profile_router
from handlers.board import router as board_router
app = FastAPI()
app.include_router(alarms_router)

dp = Dispatcher()

dot = load_dotenv('.env')

API_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.update.middleware.register(UserMiddleware(bot=bot))


async def main() -> None:
    # wait async_main()
    dp.include_router(basic_router)
    dp.include_router(auth_router)
    dp.include_router(alarm_router)
    dp.include_router(profile_router)
    dp.include_router(board_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
