"""empty message

Revision ID: 6c3d8a8dd473
Revises: 4e7e72d20ab7
Create Date: 2016-11-17 13:48:02.062731

"""

# revision identifiers, used by Alembic.
revision = '6c3d8a8dd473'
down_revision = '4e7e72d20ab7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lat', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('lng', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lng')
    op.drop_column('users', 'lat')
    ### end Alembic commands ###
