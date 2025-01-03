import os
import re

from charset_normalizer.utils import is_katakana

from database.requests.board import get_user_boards, delete_user_board
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv

from FSM.board import BoardForm
from callbacks.auth import AuthCallback
from callbacks.board import BoardCallback
from database.requests.board import set_board
from database.requests.user import get_user_by_tg_id, set_user
from keyboard.reply.auth import start_reply_keyboard
from keyboard.inline.board import add_board_keyboard, list_board_keyboard, view_board_keyboard
from phrases.auth import *
from phrases.board import *

load_dotenv()
router = Router(name=__name__)


@router.callback_query(BoardCallback.filter(F.action == "add_board"))
async def send_board_id_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext) -> None:
    await call.message.edit_text(send_board_id, )
    await state.set_state(BoardForm.board_id)


@router.message(BoardForm.board_id)
async def board_id_handler(message: Message, bot: Bot, tg_id: str, state: FSMContext, username: str) -> None:
    board_id = message.text
    user = await get_user_by_tg_id(tg_id)
    try:
        board_id = int(board_id)
        await set_board(tg_id=tg_id, board_id=board_id)
        boards = await get_user_boards(user_id=user.id)
        await message.answer(confirm_board,
                             reply_markup=list_board_keyboard(boards, user.id))
    except Exception as e:
        await message.answer(no_correct_board_id)


@router.callback_query(BoardCallback.filter(F.action == "show_boards"))
async def show_boards_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext) -> None:
    callback_data = call.data.split(':')
    user_id = int(callback_data[-1])

    boards = await get_user_boards(user_id=user_id)
    if boards:
        await call.message.edit_text(
            list_board,
            reply_markup=list_board_keyboard(boards, user_id)
        )
    else:
        await call.message.edit_text(no_boards, reply_markup=add_board_keyboard())


@router.callback_query(BoardCallback.filter(F.action == 'view_board'))
async def view_board_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext) -> None:
    callback_data = call.data.split(":")
    board_id, user_id = callback_data[2:]
    await call.message.edit_text(view_board(board_id), reply_markup=view_board_keyboard(board_id=board_id, user_id=user_id))


@router.callback_query(BoardCallback.filter(F.action == 'delete_board'))
async def delete_board_handler(call: CallbackQuery, bot: Bot, tg_id: str, state: FSMContext) -> None:
    callback_data = call.data.split(":")
    board_id, user_id = map(int, callback_data[2:])
    await delete_user_board(user_id=user_id, board_id=board_id)
    boards = await get_user_boards(user_id=user_id)
    if boards:
        await call.message.edit_text(
            delete_board_confirm,
            reply_markup=list_board_keyboard(boards, user_id)
        )
    else:
        await call.message.edit_text(no_boards, reply_markup=add_board_keyboard())