
from database.models import async_session, User
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        session.add(User(tg_id=tg_id))
        await session.commit()


async def get_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        if user is not None:
            return user.id
        return None


async def get_user_by_tg_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        if user is None:
            return None
        return user