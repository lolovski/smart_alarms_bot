import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from database.requests.alarms import get_actually_alarms
from database.requests.error import set_error
from database.session import get_async_session
from schemes.alarms import AlarmsRead
from schemes.error import ErrorCreate, ErrorRead

router = APIRouter()
moscow_tz = timezone('Europe/Moscow')

@router.post(
    '/error',
    response_model=ErrorRead
)
async def create_error_handler(
        error: ErrorCreate,
        session: AsyncSession = Depends(get_async_session)
):
    error = await set_error(error)
    return error


