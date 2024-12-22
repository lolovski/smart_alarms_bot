import datetime

from database.models import async_session, User, Alarms
from sqlalchemy import select


async def set_alarms(user_id, date):
    async with async_session() as session:
        session.add(Alarms(user_id=user_id, date=date))
        await session.commit()


async def get_actually_alarms(mac):
    async with async_session() as session:
        user = await session.scalar(
            select(User)
            .where(User.mac == mac)
        )
        alarms = await session.scalars(
            select(Alarms)
            .where(
                Alarms.user_id == user.tg_id,
                Alarms.date > datetime.datetime.now()
            )
            .order_by(Alarms.date.asc())
        )
        return alarms.first() if alarms else None
