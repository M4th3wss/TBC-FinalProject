"""add GameRequest model

Revision ID: 81544fd4dd1d
Revises: 
Create Date: 2025-07-17 19:59:50.633607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81544fd4dd1d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_name', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game_request')
    # ### end Alembic commands ###
