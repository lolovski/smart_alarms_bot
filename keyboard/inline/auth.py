from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.auth import AuthCallback

channel_url_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться 1', url='https://t.me/+sYXDBJmF7jo2ZGIy')],
    [InlineKeyboardButton(text='Подписаться 2', url='https://t.me/+UlaqmVGZgCJlM2Ri')],
    [InlineKeyboardButton(text='Я подписан', callback_data='check_subscription')],
])
adopt_rules = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начнем', callback_data='adopt rules')]
])


def auth_keyboard():
    buttons = [
        [InlineKeyboardButton(text='Авторизоваться', callback_data=AuthCallback(action='start').pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)