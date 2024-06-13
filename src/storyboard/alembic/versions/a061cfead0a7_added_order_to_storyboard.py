"""Added order to storyboard

Revision ID: a061cfead0a7
Revises: 9911f9993b59
Create Date: 2024-06-12 13:20:32.416156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a061cfead0a7'
down_revision: Union[str, None] = '9911f9993b59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'script',
               existing_type=sa.VARCHAR(length=2500),
               type_=sa.String(length=25000),
               existing_nullable=True)
    op.alter_column('storyboards', 'scene_description',
               existing_type=sa.VARCHAR(length=2500),
               type_=sa.String(length=25000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('storyboards', 'scene_description',
               existing_type=sa.String(length=25000),
               type_=sa.VARCHAR(length=2500),
               existing_nullable=True)
    op.alter_column('projects', 'script',
               existing_type=sa.String(length=25000),
               type_=sa.VARCHAR(length=2500),
               existing_nullable=True)
    # ### end Alembic commands ###
