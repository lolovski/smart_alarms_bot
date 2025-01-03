from typing import Optional

from aiogram.filters.callback_data import CallbackData


class BoardCallback(CallbackData, prefix='board'):
    action: str
    board_id: Optional[int] = None
    user_id: Optional[int] = None