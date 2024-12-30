import calendar
import os
import re
import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv
from pytz import timezone

from FSM.alarms import AlarmsState
from callbacks.alarms import DatetimeCallback, AlarmsCallback
from database.requests.alarms import set_alarms, get_actually_alarms, delete_alarms, get_duplicate_alarms
from database.requests.user import get_user_by_tg_id, set_user
from keyboard.inline.alarms import create_date_picker, create_time_picker, main_alarms_keyboard, my_alarms_keyboard, \
    alarms_control_keyboard
from keyboard.inline.auth import channel_url_keyboard, adopt_rules
from keyboard.reply.auth import start_reply_keyboard
from phrases.profile import *

load_dotenv()
router = Router(name=__name__)
admin_id = os.getenv("ADMIN_ID")


@router.message(F.text == 'Профиль')
async def show_profile_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext):
    user = await get_user_by_tg_id(tg_id)
    if user is not None:
        await message.answer_sticker(profile_sticker)
        await message.answer(show_profile_phrase(user))
