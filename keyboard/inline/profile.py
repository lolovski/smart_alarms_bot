from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.auth import AuthCallback
from callbacks.board import BoardCallback


def show_board_keyboard(user_id):
    buttons = [
        [InlineKeyboardButton(text='Мои платы', callback_data=BoardCallback(action='show_boards', user_id=user_id).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
