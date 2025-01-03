import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import os
from sqlalchemy.sql import func
from dotenv import load_dotenv
load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    tg_id: Mapped[str] = mapped_column(String(32))
    boards: Mapped[List['Board']] = relationship(
        back_populates='users',
        secondary='boarduser',
        lazy='selectin'
    )


class Board(Base):
    users: Mapped[List['User']] = relationship(
        back_populates='boards',
        secondary='boarduser',
        lazy='selectin'
    )


class BoardUser(Base):
    id = None
    user_id: Mapped[int] = mapped_column(ForeignKey(
        'user.id', ondelete='CASCADE'
    ), primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey(
        'board.id', ondelete='CASCADE'
    ), primary_key=True)


class Alarms(Base):
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'))
    date: Mapped[datetime.datetime] = mapped_column(DateTime)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

