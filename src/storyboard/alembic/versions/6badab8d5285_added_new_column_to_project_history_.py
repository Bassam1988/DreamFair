"""Added new column to Project history, storyboard history

Revision ID: 6badab8d5285
Revises: 25bfa57e66e8
Create Date: 2025-01-26 09:31:15.040605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6badab8d5285'
down_revision: Union[str, None] = '25bfa57e66e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
