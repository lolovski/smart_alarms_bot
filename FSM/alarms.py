from aiogram.fsm.state import StatesGroup, State


class AlarmsState(StatesGroup):
    date = State()
    time = State()
