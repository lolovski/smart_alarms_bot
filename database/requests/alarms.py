import datetime
from pytz import timezone

from database.models import async_session, User, Alarms, Board
from sqlalchemy import select


async def set_alarms(board_id, date):
    async with async_session() as session:
        session.add(Alarms(board_id=board_id, date=date))
        await session.commit()


async def get_actually_alarms(board_id=None):
    moscow_tz = timezone('Europe/Moscow')
    async with async_session() as session:
        alarms = await session.scalars(
            select(Alarms)
            .where(
                Alarms.board_id == board_id ,
                Alarms.date > datetime.datetime.now(moscow_tz)
            )
            .order_by(Alarms.date.asc())
        )
        return alarms.all()


async def delete_alarms(alarm_id):
    async with async_session() as session:
        alarm = await session.scalar(
            select(Alarms)
            .where(Alarms.id == int(alarm_id))
        )
        if alarm is not None:
            await session.delete(alarm)
            await session.commit()


async def get_duplicate_alarms(date_time, board_id):
    async with async_session() as session:
        date_range = []
        for i in range(-15, 16):
            date_range.append(date_time + datetime.timedelta(minutes=i))
        board = await session.scalar(
            select(Board)
            .where(Board.id == int(board_id))
        )
        alarms = await session.scalar(
            select(Alarms)
            .where(
                Alarms.board_id == board.id,
                Alarms.date.in_(date_range)
            )
        )
        return alarms if alarms is not None else None