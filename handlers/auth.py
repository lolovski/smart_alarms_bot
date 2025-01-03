import os
import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv

from callbacks.auth import AuthCallback
from database.requests.user import get_user_by_tg_id, set_user
from keyboard.reply.auth import start_reply_keyboard
from keyboard.inline.board import add_board_keyboard
from phrases.auth import *

load_dotenv()
router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, command: CommandObject, tg_id: str, state: FSMContext, username: str) -> None:
    await state.clear()
    user = await get_user_by_tg_id(tg_id)
    await message.answer_sticker(welcome_sticker, reply_markup=start_reply_keyboard())
    if user is None:
        await set_user(tg_id)
        await message.answer(registration_text(username),
                             reply_markup=add_board_keyboard())

    else:
        await message.answer(start_text(username))
