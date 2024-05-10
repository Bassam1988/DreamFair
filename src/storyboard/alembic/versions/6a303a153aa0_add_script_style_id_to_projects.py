"""Add script_style_id to projects

Revision ID: 6a303a153aa0
Revises: 
Create Date: 2024-05-08 16:10:33.482725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a303a153aa0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('synopsis', sa.String(length=2500), nullable=True),
    sa.Column('script', sa.String(length=2500), nullable=True),
    sa.Column('script_style_id', sa.UUID(), nullable=True),
    sa.Column('storyboard_style', sa.UUID(), nullable=True),
    sa.Column('VideoDuration', sa.UUID(), nullable=True),
    sa.Column('aspect_ratio', sa.UUID(), nullable=True),
    sa.Column('boards_per_min', sa.UUID(), nullable=True),
    sa.Column('test', sa.String(length=2500), nullable=True),
    sa.ForeignKeyConstraint(['VideoDuration'], ['video_durations.id'], ),
    sa.ForeignKeyConstraint(['aspect_ratio'], ['aspect_ratios.id'], ),
    sa.ForeignKeyConstraint(['boards_per_min'], ['boards_per_mins.id'], ),
    sa.ForeignKeyConstraint(['script_style_id'], ['script_styles.id'], ),
    sa.ForeignKeyConstraint(['storyboard_style'], ['storyboard_styles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('storyboards',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('project', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('image', sa.String(length=2500), nullable=True),
    sa.Column('scene_description', sa.String(length=2500), nullable=True),
    sa.ForeignKeyConstraint(['project'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('script_styles_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('script_styles_id',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('code_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='script_styles_pkey'),
    sa.UniqueConstraint('code_name', name='script_styles_code_name_key'),
    sa.UniqueConstraint('name', name='script_styles_name_key')
    )
    op.drop_table('storyboards')
    op.drop_table('projects')
    # ### end Alembic commands ###