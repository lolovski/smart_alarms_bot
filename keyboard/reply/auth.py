from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_reply_keyboard():
    buttons = [
        [KeyboardButton(text="Мои будильники")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
