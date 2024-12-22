import os
import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv

from database.requests.user import get_user_by_tg_id, set_user
from keyboard.inline.start import channel_url_keyboard, adopt_rules
from keyboard.reply.start import start_keyboard

load_dotenv()
router = Router(name=__name__)

admin_id = os.getenv("ADMIN_ID")


class UserForm(StatesGroup):
    mac = State()


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, command: CommandObject, tg_id: str, state: FSMContext) -> None:
    await state.clear()
    user = await get_user_by_tg_id(tg_id)

    if user is None:
        await message.answer('Введите свой mac')
        await state.set_state(UserForm.mac)
    else:
        await message.answer(f"<b>С возвращением!\n</b>",
                             reply_markup=start_keyboard)


@router.message(UserForm.mac)
async def mac_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext) -> None:
    mac = message.text
    await set_user(tg_id=tg_id, mac=mac)
    await message.answer(f"<b>Добро пожаловать!\n</b>",
                         reply_markup=start_keyboard)
    await state.clear()


"""@router.message(F.text.startswith('Hello'))
async def hello_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext) -> None:
    await message.answer(f"<b>Привет, {message.from_user.first_name}!</b>\n\n"
                         "�� - бот-ассистент для управления умным устройством.\n\n"
                         "Чтобы начать работу, отправьте мне свой MAC-адрес.\n\n"
                         "Если у вас есть вопросы или пожелания, пишите мне в чате @smart_alarms_bot",
                         reply_markup=start_keyboard)"""