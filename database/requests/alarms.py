import datetime
from pytz import timezone

from database.models import async_session, User, Alarms
from sqlalchemy import select


async def set_alarms(user_id, date):
    async with async_session() as session:
        session.add(Alarms(user_id=user_id, date=date))
        await session.commit()


async def get_actually_alarms(mac=None, tg_id=None):
    moscow_tz = timezone('Europe/Moscow')
    async with async_session() as session:
        if tg_id is not None:
            alarms = await session.scalars(
                select(Alarms)
                .where(
                    Alarms.user_id == str(tg_id),
                    Alarms.date > datetime.datetime.now(moscow_tz)
                )
                .order_by(Alarms.date.asc())
            )
            return alarms.all() if alarms else None

        user = await session.scalar(
            select(User)
            .where(User.mac == str(mac))
        )
        alarms = await session.scalars(
            select(Alarms)
            .where(
                Alarms.user_id == user.tg_id,
                Alarms.date > datetime.datetime.now(moscow_tz)
            )
            .order_by(Alarms.date.asc())
        )
        return alarms.first() if alarms else None


async def delete_alarms(alarm_id):
    async with async_session() as session:
        alarm = await session.scalar(
            select(Alarms)
            .where(Alarms.id == int(alarm_id))
        )
        if alarm is not None:
            await session.delete(alarm)
            await session.commit()


async def get_duplicate_alarms(tg_id, date_time):
    async with async_session() as session:
        date_range = []
        for i in range(-15, 16):
            date_range.append(date_time + datetime.timedelta(minutes=i))
        alarms = await session.scalar(
            select(Alarms)
            .where(
                Alarms.user_id == str(tg_id),
                Alarms.date.in_(date_range)
            )
        )
        return alarms if alarms is not None else None