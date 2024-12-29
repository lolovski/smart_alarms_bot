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
moscow_tz = timezone('Europe/Moscow')

load_dotenv()
router = Router(name=__name__)
admin_id = os.getenv("ADMIN_ID")


@router.message(F.text == 'Мои будильники')
async def show_alarms_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext):
    await message.answer('Выберите функцию:', reply_markup=main_alarms_keyboard())


@router.callback_query(AlarmsCallback.filter(F.action == 'main_alarms'))
async def show_alarms_call_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    await call.message.edit_text('Выберите функцию:', reply_markup=main_alarms_keyboard())
    await call.message.edit_text('Выберите функцию:', reply_markup=main_alarms_keyboard())


@router.callback_query(AlarmsCallback.filter(F.action == 'set_alarms'))
async def set_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    now = datetime.datetime.now(moscow_tz)
    await call.message.edit_text(f'Выберите дату\n {now.strftime('%d.%m.%Y')}', reply_markup=create_date_picker())

    await state.set_state(AlarmsState.date)
    await state.update_data(date=now)


@router.callback_query(DatetimeCallback.filter(F.date_or_time == 'date'))
async def date_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    data = await state.get_data()
    state_data = call.data.split(':')
    date = data['date']
    match state_data[2]:
        case 'day':
            match state_data[3]:
                case 'plus':
                    date += datetime.timedelta(days=1)
                case 'minus':
                    date -= datetime.timedelta(days=1)
        case 'month':
            match state_data[3]:
                case 'plus':
                    days = calendar.monthrange(date.year, date.month)[-1]
                    date += datetime.timedelta(days=days)
                case 'minus':
                    last_date = date - datetime.timedelta(days=(date.day + 1))
                    days = calendar.monthrange(last_date.year, last_date.month)[-1]
                    date -= datetime.timedelta(days=days)

    if state_data[3] == 'confirm':
        date = date.replace(tzinfo=moscow_tz)
        if date.date() < datetime.datetime.now(moscow_tz).date():
            return await call.message.edit_text(
                f'Выбранная дата уже прошла. Пожалуйста, введите новую дату.\n{date.strftime("%d.%m.%Y")}',
                reply_markup=create_date_picker()
            )

        await state.set_state(AlarmsState.time)
        time = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
        await state.update_data(time=time)
        return await call.message.edit_text(f'Выберите время\n {time.strftime("%H:%M")}', reply_markup=create_time_picker())

    await call.message.edit_text(f'{date.strftime('%d.%m.%Y')}', reply_markup=create_date_picker())
    await state.update_data(date=date)


@router.callback_query(DatetimeCallback.filter(F.date_or_time == 'time'))
async def time_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    data = await state.get_data()
    time = data['time']
    state_data = call.data.split(':')
    match state_data[2]:
        case 'hour':
            match state_data[3]:
                case 'plus':
                    time += datetime.timedelta(hours=1)
                case 'minus':
                    time -= datetime.timedelta(hours=1)
        case 'minute':
            match state_data[3]:
                case 'plus':
                    time += datetime.timedelta(minutes=1)
                case'minus':
                    time -= datetime.timedelta(minutes=1)
        case '10 minutes':
            match state_data[3]:
                case 'plus':
                    time += datetime.timedelta(minutes=10)
                case'minus':
                    time -= datetime.timedelta(minutes=10)
        case '5 hours':
            match state_data[3]:
                case 'plus':
                    time += datetime.timedelta(hours=5)
                case'minus':
                    time -= datetime.timedelta(hours=5)

    if state_data[3] == 'confirm':
        date = data['date']
        date_time = datetime.datetime.combine(date.date(), time.time())
        date_time = date_time.replace(tzinfo=moscow_tz)
        if date_time > datetime.datetime.now(moscow_tz):
            duplicate_alarms = await get_duplicate_alarms(tg_id=tg_id, date_time=date_time)
            if duplicate_alarms is None:
                await set_alarms(user_id=tg_id, date=date_time)
                await call.message.edit_text('Будильник успешно установлен!\n'
                                          f'Дата: {date_time.date().strftime("%d.%m.%y")}\n'
                                          f'Время: {date_time.time().strftime("%H:%M")}')
                await state.clear()
                await call.message.answer('Выберите функцию:', reply_markup=main_alarms_keyboard())
            else:
                await call.message.edit_text(
                    f'Между будильниками должен быть диапазон 15 минут. Пожалуйста, введите новое время\n {time.strftime("%H:%M")}',
                    reply_markup=create_time_picker()
                )
        else:
            await call.message.edit_text(
                f'Выбранное время уже прошло. Пожалуйста, введите новое время\n {time.strftime("%H:%M")}',
                reply_markup=create_time_picker()
            )
        return

    await call.message.edit_text(f'{time.strftime("%H:%M")}', reply_markup=create_time_picker())
    await state.update_data(time=time)


@router.callback_query(AlarmsCallback.filter(F.action == 'view_alarms'))
async def view_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    alarms = await get_actually_alarms(tg_id=tg_id)
    if not alarms:
        return await call.message.edit_text(
            'У вас нет установленных будильников.',
            reply_markup=main_alarms_keyboard()
        )

    await call.message.edit_text('Ваши будильники:', reply_markup=my_alarms_keyboard(alarms))


@router.callback_query(AlarmsCallback.filter(F.action == 'my_alarms'))
async def my_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    state_data = call.data.split(':')
    await call.message.edit_text(text='Управление будильником', reply_markup=alarms_control_keyboard(state_data[-1]))


@router.callback_query(AlarmsCallback.filter(F.action == 'delete_alarms'))
async def delete_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    state_data = call.data.split(':')
    alarm_id = state_data[-1]
    await delete_alarms(alarm_id=alarm_id)
    alarms = await get_actually_alarms(tg_id=tg_id)
    await call.message.edit_text(text='Будильник успешно удален.', reply_markup=my_alarms_keyboard(alarms))