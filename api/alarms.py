import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests.alarms import get_actually_alarms
from schemes.alarms import AlarmsRead

router = APIRouter()
moscow_tz = timezone('Europe/Moscow')




@router.get(
    '/get_time',
    response_model=Optional[AlarmsRead],
)
async def get_time(
        board_id: str = Query(...),
):
    alarms = await get_actually_alarms(board_id=board_id)
    if alarms:
        date = alarms[0].date.replace(tzinfo=moscow_tz)
        now = datetime.datetime.now().replace(tzinfo=moscow_tz)
        time_difference = (date - now).total_seconds()
        return {'date': int(time_difference)}
    return {'date': -1}


@router.get(
    '/now'
)
async def get_now():
    now = datetime.datetime.now(moscow_tz)
    return now.strftime('%d.%m.%y %H:%M:%S')

