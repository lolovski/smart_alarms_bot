from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.alarms import DatetimeCallback, AlarmsCallback
from callbacks.board import BoardCallback
from callbacks.menu import MenuCallback


def show_board_alarms_keyboard(boards) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for board in boards:
        keyboard.button(text=str(board.id), callback_data=AlarmsCallback(action='main_alarms_board', board_id=board.id).pack())

    return keyboard.adjust(1).as_markup()


def main_alarms_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Добавить будильник', callback_data=AlarmsCallback(action='set_alarms', alarm_id=None).pack())
#    keyboard.button(text='Настройки', callback_data=AlarmsCallback(action='settings', alarm_id=None).pack())
    keyboard.button(text='Просмотреть будильники', callback_data=AlarmsCallback(action='view_alarms', alarm_id=None).pack())
    keyboard.button(text='Назад', callback_data=MenuCallback(action='alarms').pack())
    return keyboard.adjust(1).as_markup()


def create_date_picker() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    # Кнопки для точной настройки
    keyboard.button(text="➖ День", callback_data=DatetimeCallback(date_or_time='date', action='minus', datetime_type='day').pack())
    keyboard.button(text="➕ День", callback_data=DatetimeCallback(date_or_time='date', action='plus', datetime_type='day').pack())
    keyboard.button(text="➖ Месяц", callback_data=DatetimeCallback(date_or_time='date', action='minus', datetime_type='month').pack())
    keyboard.button(text="➕ Месяц", callback_data=DatetimeCallback(date_or_time='date', action='plus', datetime_type='month').pack())

    # Кнопка подтверждения
    keyboard.button(text="Подтвердить", callback_data=DatetimeCallback(action='confirm', date_or_time='date', datetime_type=None).pack())
    keyboard.adjust(2)  # 2 кнопки в ряд
    return keyboard.as_markup()


def create_time_picker() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    # Кнопки для точной настройки
    keyboard.button(text="➖ Час", callback_data=DatetimeCallback(date_or_time='time', action='minus', datetime_type='hour').pack())
    keyboard.button(text="➕ Час", callback_data=DatetimeCallback(date_or_time='time', action='plus', datetime_type='hour').pack())
    keyboard.button(text="➖ Минута", callback_data=DatetimeCallback(date_or_time='time', action='minus', datetime_type='minute').pack())
    keyboard.button(text="➕ Минута", callback_data=DatetimeCallback(date_or_time='time', action='plus', datetime_type='minute').pack())
    keyboard.button(text="➖ 10 минут",
                    callback_data=DatetimeCallback(date_or_time='time', action='minus', datetime_type='10 minutes').pack())
    keyboard.button(text="➕ 10 минут",
                    callback_data=DatetimeCallback(date_or_time='time', action='plus', datetime_type='10 minutes').pack())

    keyboard.button(text="➖ 5 часов",
                    callback_data=DatetimeCallback(date_or_time='time', action='minus', datetime_type='5 hours').pack())
    keyboard.button(text="➕ 5 часов",
                    callback_data=DatetimeCallback(date_or_time='time', action='plus', datetime_type='5 hours').pack())
    # Кнопка подтверждения
    keyboard.button(text="Подтвердить", callback_data=DatetimeCallback(action='confirm', date_or_time='time', datetime_type=None).pack())

    keyboard.adjust(2)  # 4 кнопки в ряд
    return keyboard.as_markup()


def my_alarms_keyboard(list_alarms) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for alarm in list_alarms:
        text = f'{alarm.date.date().strftime("%d.%m.%y")} {alarm.date.time().strftime("%H:%M")}'
        keyboard.button(
            text=text,
            callback_data=AlarmsCallback(action='my_alarms', alarm_id=alarm.id).pack()
        )
    keyboard.button(text='Назад', callback_data=AlarmsCallback(action='main_alarms', alarm_id=None).pack())
    return keyboard.adjust(1).as_markup()


def alarms_control_keyboard(alarm_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Удалить', callback_data=AlarmsCallback(action='delete_alarms', alarm_id=alarm_id).pack())
#    keyboard.button(text='Изменить', callback_data=AlarmsCallback(action='edit_alarms', alarm_id=alarm_id).pack())
    keyboard.button(text='Назад', callback_data=AlarmsCallback(action='view_alarms', alarm_id=alarm_id).pack())
    return keyboard.adjust(1).as_markup()


def go_to_profile_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Перейти в профиль', callback_data=MenuCallback(action='profile').pack())
    return keyboard.as_markup()
