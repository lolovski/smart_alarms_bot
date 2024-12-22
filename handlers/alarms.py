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

from database.requests.alarms import set_alarms
from database.requests.user import get_user_by_tg_id, set_user
from keyboard.inline.start import channel_url_keyboard, adopt_rules
from keyboard.reply.start import start_keyboard

load_dotenv()
router = Router(name=__name__)
admin_id = os.getenv("ADMIN_ID")


class AlarmsState(StatesGroup):
    date = State()
    time = State()


@router.message(F.text.startswith('Поставить будильник'))
async def start_alarms_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext):
    await message.answer('Выберите дату\n'
                         'В формате 12.02.24')
    await state.set_state(AlarmsState.date)


@router.message(AlarmsState.date)
async def set_date_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext):
    date_str = message.text
    try:
        date = datetime.datetime.strptime(date_str, '%d.%m.%y')
        if date + datetime.timedelta(days=1) < datetime.datetime.now():
            await message.answer('Выбранная дата уже прошла. Пожалуйста, введите новую дату.')
            return
        await state.update_data(date=date_str)
        await state.set_state(AlarmsState.time)
        await message.answer('Выберите время\n'
                             'В формате 12:00')
    except ValueError:
        await message.answer('Введен некорректный формат даты. Пожалуйста, введите дату в формате 12.02.24')


@router.message(AlarmsState.time)
async def set_time_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext):
    time_str = message.text
    try:
        data = await state.get_data()
        date_time_str = data.get('date') + ' ' + time_str
        date_time = datetime.datetime.strptime(date_time_str, '%d.%m.%y %H:%M')
        if date_time > datetime.datetime.now():
            await set_alarms(user_id=tg_id, date=date_time)
            await message.answer('Будильник успешно установлен!\n'
                                 f'Дата: {date_time.date().strftime("%d.%m.%y")}\n'
                                 f'Время: {date_time.time().strftime("%H:%M")}')
        else:
            await message.answer('Выбранное время уже прошло. Пожалуйста, введите новое время.')
            return

    except Exception as e:
        print(e)
        await message.answer('Введен некорректный формат времени. Пожалуйста, введите время в формате 12:00')