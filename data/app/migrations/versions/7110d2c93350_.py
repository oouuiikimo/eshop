"""empty message

Revision ID: 7110d2c93350
Revises: d5617da8ffbb
Create Date: 2020-03-23 14:56:44.926874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7110d2c93350'
down_revision = 'd5617da8ffbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###