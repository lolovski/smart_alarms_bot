from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.auth import AuthCallback
from callbacks.board import BoardCallback
from callbacks.menu import MenuCallback


def add_board_keyboard():
    buttons = [
        [InlineKeyboardButton(text='Добавить плату', callback_data=BoardCallback(action='add_board').pack())],
        [InlineKeyboardButton(text='Назад', callback_data=MenuCallback(action='profile').pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def list_board_keyboard(boards, user_id):
    keyboard = InlineKeyboardBuilder()
    for board in boards:
        keyboard.button(
            text=str(board.id),
            callback_data=BoardCallback(action='view_board', board_id=board.id, user_id=user_id).pack()
        )
    keyboard.button(text='Добавить плату', callback_data=BoardCallback(action='add_board').pack())
    keyboard.button(text='Назад', callback_data=MenuCallback(action='profile'))
    return keyboard.adjust(1).as_markup()


def view_board_keyboard(board_id, user_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Удалить', callback_data=BoardCallback(action='delete_board', user_id=user_id, board_id=board_id).pack())
#    keyboard.button(text='Изменить', callback_data=AlarmsCallback(action='edit_alarms', alarm_id=alarm_id).pack())
    keyboard.button(text='Назад', callback_data=BoardCallback(action='show_boards', user_id=user_id, board_id=board_id).pack())
    return keyboard.adjust(1).as_markup()