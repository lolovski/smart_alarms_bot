import datetime
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class DatetimeCallback(CallbackData, prefix='datetime'):
    date_or_time: Optional[str] = None
    datetime_type: Optional[str] = None
    action: Optional[str] = None


class AlarmsCallback(CallbackData, prefix='alarms'):
    action: str
    alarm_id: Optional[int] = None
    board_id: Optional[int] = None