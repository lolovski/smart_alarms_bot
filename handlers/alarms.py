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

from FSM.alarms import AlarmsForm
from callbacks.alarms import DatetimeCallback, AlarmsCallback
from callbacks.menu import MenuCallback
from database.requests.alarms import set_alarms, get_actually_alarms, delete_alarms, get_duplicate_alarms
from database.requests.board import get_user_boards
from database.requests.user import get_user_by_tg_id, set_user
from keyboard.inline.alarms import create_date_picker, create_time_picker, main_alarms_keyboard, my_alarms_keyboard, \
    alarms_control_keyboard, show_board_alarms_keyboard, go_to_profile_keyboard
from keyboard.inline.board import add_board_keyboard

from keyboard.reply.auth import start_reply_keyboard
from phrases.alarms import *
from phrases.board import no_boards

moscow_tz = timezone('Europe/Moscow')

load_dotenv()
router = Router(name=__name__)
admin_id = os.getenv("ADMIN_ID")


@router.message(F.text == 'Мои будильники')
async def show_alarms_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext):
    await message.answer_sticker(alarms_sticker)
    user = await get_user_by_tg_id(tg_id)
    boards = await get_user_boards(user.id)
    if boards:
        await message.answer(choice_board_phrase, reply_markup=show_board_alarms_keyboard(boards))
        await state.set_state(AlarmsForm.board_id)
    else:
        await message.answer(no_boards, reply_markup=go_to_profile_keyboard())


@router.callback_query(MenuCallback.filter(F.action == 'alarms'))
async def show_alarms_call_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    user = await get_user_by_tg_id(tg_id)
    boards = await get_user_boards(user.id)
    if boards:
        await call.message.edit_text(choice_board_phrase, reply_markup=show_board_alarms_keyboard(boards))
        await state.set_state(AlarmsForm.board_id)
    else:
        await call.message.edit_text(no_boards, reply_markup=go_to_profile_keyboard())


@router.callback_query(AlarmsCallback.filter(F.action == 'main_alarms_board'))
async def main_alarms_board_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    callback_data = call.data.split(':')
    await state.update_data(board_id=callback_data[-1])
    await call.message.edit_text(main_alarms_phrase, reply_markup=main_alarms_keyboard())


@router.callback_query(AlarmsCallback.filter(F.action == 'main_alarms'))
async def main_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    await call.message.edit_text(main_alarms_phrase, reply_markup=main_alarms_keyboard())


@router.callback_query(AlarmsCallback.filter(F.action == 'set_alarms'))
async def set_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    now = datetime.datetime.now(moscow_tz)
    await call.message.edit_text(select_date_phrase(now), reply_markup=create_date_picker())
    await state.set_state(AlarmsForm.date)
    await state.update_data(date=now)


@router.callback_query(DatetimeCallback.filter(F.date_or_time == 'date'))
async def date_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    state_data = await state.get_data()
    callback_data = call.data.split(':')
    date = state_data['date']
    match callback_data[2]:
        case 'day':
            match callback_data[3]:
                case 'plus':
                    date += datetime.timedelta(days=1)
                case 'minus':
                    date -= datetime.timedelta(days=1)
        case 'month':
            match callback_data[3]:
                case 'plus':
                    days = calendar.monthrange(date.year, date.month)[-1]
                    date += datetime.timedelta(days=days)
                case 'minus':
                    last_date = date - datetime.timedelta(days=(date.day + 1))
                    days = calendar.monthrange(last_date.year, last_date.month)[-1]
                    date -= datetime.timedelta(days=days)

    if callback_data[3] == 'confirm':
        date = date.replace(tzinfo=moscow_tz)
        if date.date() < datetime.datetime.now(moscow_tz).date():
            return await call.message.edit_text(
                passed_date_phrase(date),
                reply_markup=create_date_picker()
            )

        await state.set_state(AlarmsForm.time)
        time = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
        await state.update_data(time=time)
        return await call.message.edit_text(select_time_phrase(time), reply_markup=create_time_picker())

    await call.message.edit_text(date_phrase(date), reply_markup=create_date_picker())
    await state.update_data(date=date)


@router.callback_query(DatetimeCallback.filter(F.date_or_time == 'time'))
async def time_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    state_data = await state.get_data()
    time = state_data['time']
    callback_data = call.data.split(':')
    match callback_data[2]:
        case 'hour':
            match callback_data[3]:
                case 'plus':
                    time += datetime.timedelta(hours=1)
                case 'minus':
                    time -= datetime.timedelta(hours=1)
        case 'minute':
            match callback_data[3]:
                case 'plus':
                    time += datetime.timedelta(minutes=1)
                case'minus':
                    time -= datetime.timedelta(minutes=1)
        case '10 minutes':
            match callback_data[3]:
                case 'plus':
                    time += datetime.timedelta(minutes=10)
                case'minus':
                    time -= datetime.timedelta(minutes=10)
        case '5 hours':
            match callback_data[3]:
                case 'plus':
                    time += datetime.timedelta(hours=5)
                case'minus':
                    time -= datetime.timedelta(hours=5)

    if callback_data[3] == 'confirm':
        date = state_data['date']
        board_id = state_data['board_id']
        date_time = datetime.datetime.combine(date.date(), time.time())
        date_time = date_time.replace(tzinfo=moscow_tz)
        if date_time > datetime.datetime.now(moscow_tz):
            duplicate_alarms = await get_duplicate_alarms(date_time=date_time, board_id=board_id)
            if duplicate_alarms is None:
                await set_alarms(board_id=board_id, date=date_time)
                await call.message.edit_text(set_alarms_phrase(date_time))
                await call.message.answer_sticker(set_alarms_sticker)
                await call.message.answer(main_alarms_phrase, reply_markup=main_alarms_keyboard())
            else:
                await call.message.edit_text(
                    time_range_phrase(time),
                    reply_markup=create_time_picker()
                )
        else:
            await call.message.edit_text(
                passed_time_phrase(time),
                reply_markup=create_time_picker()
            )
        return

    await call.message.edit_text(time_phrase(time), reply_markup=create_time_picker())
    await state.update_data(time=time)


@router.callback_query(AlarmsCallback.filter(F.action == 'view_alarms'))
async def view_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    state_data = await state.get_data()
    alarms = await get_actually_alarms(board_id=state_data['board_id'])

    if not alarms:
        return await call.message.edit_text(
            no_alarms_phrase,
            reply_markup=main_alarms_keyboard()
        )

    await call.message.edit_text(alarms_list_phrase, reply_markup=my_alarms_keyboard(alarms))


@router.callback_query(AlarmsCallback.filter(F.action == 'my_alarms'))
async def my_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    callback_data = call.data.split(':')
    await call.message.edit_text(text=control_alarms_phrase, reply_markup=alarms_control_keyboard(callback_data[-2]))


@router.callback_query(AlarmsCallback.filter(F.action == 'delete_alarms'))
async def delete_alarms_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext):
    callback_data = call.data.split(':')
    state_data = await state.get_data()
    alarm_id = callback_data[-2]
    await delete_alarms(alarm_id=alarm_id)
    alarms = await get_actually_alarms(board_id=state_data.get('board_id'))
    await call.message.edit_text(text=delete_alarms_phrase, reply_markup=my_alarms_keyboard(alarms))