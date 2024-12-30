from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_reply_keyboard():
    buttons = [
        [KeyboardButton(text="Мои будильники"), KeyboardButton(text="Профиль")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
