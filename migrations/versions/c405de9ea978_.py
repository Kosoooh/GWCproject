"""empty message

Revision ID: c405de9ea978
Revises: f35d8e23a483
Create Date: 2020-12-15 18:26:37.655136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c405de9ea978'
down_revision = 'f35d8e23a483'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('reservation_roomID_fkey', 'reservation', type_='foreignkey')
    op.create_foreign_key(None, 'reservation', 'user', ['user_id'], ['id'])
    op.drop_column('reservation', 'roomID')
    op.drop_column('reservation', 'name')
    op.drop_column('reservation', 'is_reserved')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('is_reserved', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('reservation', sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('reservation', sa.Column('roomID', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'reservation', type_='foreignkey')
    op.create_foreign_key('reservation_roomID_fkey', 'reservation', 'space', ['roomID'], ['id'])
    op.drop_column('reservation', 'user_id')
    # ### end Alembic commands ###
