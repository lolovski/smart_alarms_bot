"""error

Revision ID: 8128613302dc
Revises: 2c7202d265dd
Create Date: 2025-01-20 15:30:24.971887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8128613302dc'
down_revision: Union[str, None] = '2c7202d265dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('error',
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('message', sa.String(length=2048), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('error')
    # ### end Alembic commands ###
