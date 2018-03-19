"""empty message

Revision ID: 1d5034c73fed
Revises: a1c21813da79
Create Date: 2018-03-19 19:14:35.975060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d5034c73fed'
down_revision = 'a1c21813da79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('userId', sa.String(length=255), nullable=False))
    op.drop_constraint('watchlists_ibfk_1', 'watchlists', type_='foreignkey')
    op.drop_column('users', 'accessToken')
    op.create_primary_key('pk_user', 'users', ['userId'])
    op.add_column('watchlists', sa.Column('userId', sa.String(length=255), nullable=True))
    op.drop_column('watchlists', 'accessToken')
    op.create_foreign_key(None, 'watchlists', 'users', ['userId'], ['userId'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('watchlists', sa.Column('accessToken', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'watchlists', type_='foreignkey')
    op.create_foreign_key('watchlists_ibfk_1', 'watchlists', 'users', ['accessToken'], ['accessToken'])
    op.drop_column('watchlists', 'userId')
    op.add_column('users', sa.Column('accessToken', mysql.VARCHAR(length=255), nullable=False))
    op.drop_column('users', 'userId')
    # ### end Alembic commands ###
