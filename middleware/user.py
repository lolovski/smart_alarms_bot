import os
import re
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram import Bot
from aiogram.types import Message
from aiogram.types import Update
from dotenv import load_dotenv

load_dotenv()

class UserMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:

        current_event = event.message or event.callback_query
        if isinstance(current_event, Message):
            tg_id = current_event.from_user.id
            username = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ\s]', '', current_event.from_user.full_name)
            data['username'] = username
            print(tg_id)
            data['tg_id'] = tg_id
        return await handler(event, data)