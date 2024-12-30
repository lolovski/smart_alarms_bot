import os
import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv

from FSM.auth import AuthForm
from callbacks.auth import AuthCallback
from database.requests.user import get_user_by_tg_id, set_user
from keyboard.inline.auth import channel_url_keyboard, adopt_rules, auth_keyboard
from keyboard.reply.auth import start_reply_keyboard
from phrases.auth import start_text, welcome_text, send_mac_address

load_dotenv()
router = Router(name=__name__)

admin_id = os.getenv("ADMIN_ID")


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, command: CommandObject, tg_id: str, state: FSMContext, username: str) -> None:
    await state.clear()
    user = await get_user_by_tg_id(tg_id)

    if user is None:
        await message.answer(welcome_text(username),
                             reply_markup=auth_keyboard())

    else:
        await message.answer(start_text(username),
                             reply_markup=start_reply_keyboard())


@router.callback_query(AuthCallback.filter(F.action == "start"))
async def send_mac_handler(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await call.message.edit_text(send_mac_address)
    await state.set_state(AuthForm.mac)


@router.message(AuthForm.mac)
async def mac_handler(message: Message, bot: Bot, state: FSMContext, username: str) -> None:
    board_id = message.text
    tg_id = message.from_user.id
    await set_user(tg_id=tg_id, board_id=board_id)
    await message.answer(start_text(username),
                         reply_markup=start_reply_keyboard())
    await state.clear()