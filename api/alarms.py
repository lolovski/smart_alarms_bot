from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests.alarms import get_actually_alarms
from schemes.alarms import AlarmsRead

router = APIRouter()


@router.get(
    '/get_time',
    response_model=Optional[AlarmsRead],
)
async def get_classes(
        board_id: str = Query(...),
):
    alarms = await get_actually_alarms(board_id=board_id)
    if alarms is not None:
        alarms.date = alarms.date.strftime('%d.%m.%y %H:%M:%S')
    return alarms


@router.get(
    '/now'
)
async def get_now():
    moscow_tz = timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    return now.strftime('%d.%m.%y %H:%M:%S')