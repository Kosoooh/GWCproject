"""empty message

Revision ID: 3d6811f9fb31
Revises: 460d5afabcc1
Create Date: 2020-12-16 00:00:15.816401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d6811f9fb31'
down_revision = '460d5afabcc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'reservation', 'space', ['roomID'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reservation', type_='foreignkey')
    # ### end Alembic commands ###