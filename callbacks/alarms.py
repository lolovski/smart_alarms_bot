import datetime
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class DatetimeCallback(CallbackData, prefix='datetime'):
    date_or_time: Optional[str]
    datetime_type: Optional[str]
    action: Optional[str]


class AlarmsCallback(CallbackData, prefix='alarms'):
    action: str
    alarm_id: Optional[int]