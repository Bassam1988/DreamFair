"""add storyboards table

Revision ID: d1df1d874025
Revises: 8fdef480fbaf
Create Date: 2024-05-17 14:49:49.058148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1df1d874025'
down_revision: Union[str, None] = '8fdef480fbaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text2text_operation_storyboard',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('text2text_operation_id', sa.UUID(), nullable=False),
    sa.Column('generated_text', sa.String(length=10000), nullable=True),
    sa.ForeignKeyConstraint(['text2text_operation_id'], ['text2text_operation.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('generated_text')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('text2text_operation_storyboard')
    # ### end Alembic commands ###
