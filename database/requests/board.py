from database.models import async_session, User, Board, BoardUser
from sqlalchemy import select


async def set_board(tg_id, board_id):
    async with async_session() as session:
        board = await session.scalar(
            select(Board)
            .where(Board.id == board_id)
        )
        if board is None:
            board = Board(id=board_id)
            session.add(board)
            await session.commit()
            await session.refresh(board)
        user = await session.scalar(
            select(User)
            .where(User.tg_id == str(tg_id))
        )
        session.add(BoardUser(user_id=user.id, board_id=board.id))
        await session.commit()


async def get_user_boards(user_id):
    async with async_session() as session:
        boards = await session.scalars(
            select(Board)
            .join(BoardUser)
            .where(BoardUser.user_id == user_id)
        )
        return boards.all()

async def delete_user_board(user_id, board_id):
    async with async_session() as session:
        board = await session.scalar(
            select(BoardUser)
            .where(BoardUser.user_id == user_id, BoardUser.board_id == board_id)
        )
        if board is not None:
            await session.delete(board)
            await session.commit()


