from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests.alarms import get_actually_alarms
from schemes.alarms import AlarmsRead

router = APIRouter()


@router.get(
    '/get_time',
    response_model=Optional[AlarmsRead],
)
async def get_classes(
        mac: str = Query(...),
):
    alarms = await get_actually_alarms(mac=mac)
    if alarms is not None:
        alarms.date = alarms.date.strftime('%d.%m.%y %H:%M:%S')
    return alarms