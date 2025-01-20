from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.config import any_async

from database.models import async_session, User, Board, BoardUser, Error
from sqlalchemy import select


async def set_error(
        error,
):
    async with async_session() as session:
        obj_in_data = error.dict()
        db_obj = Error(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


async def get_errors(
        board_id: int
):
    async with async_session() as session:
        errors = await session.scalars(
            select(Error)
            .where(Error.board_id == board_id)
            .order_by(Error.date.desc())
        )
        return errors.all()


async def get_error(
        error_id: int
):
    async with async_session() as session:
        error = await session.scalar(
            select(Error)
            .where(Error.id == error_id)
        )
        return error


async def delete_error(
        error_id: int
):
    async with async_session() as session:
        error = await session.scalar(
            select(Error)
            .where(Error.id == error_id)
        )
        if error is not None:
            await session.delete(error)
            await session.commit()
