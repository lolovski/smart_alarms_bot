from aiogram.fsm.state import StatesGroup, State


class AlarmsForm(StatesGroup):
    board_id = State()
    date = State()
    time = State()
