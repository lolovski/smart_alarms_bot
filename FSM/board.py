from aiogram.fsm.state import StatesGroup, State


class BoardForm(StatesGroup):
    board_id = State()
    user_id = State()
