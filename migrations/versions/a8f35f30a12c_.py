"""empty message

Revision ID: a8f35f30a12c
Revises: 39a552eb65ac
Create Date: 2022-01-10 18:21:24.709435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8f35f30a12c'
down_revision = '39a552eb65ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('album', sa.Column('year', sa.Integer(), nullable=True))
    op.add_column('media', sa.Column('disc_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('media', 'disc_number')
    op.drop_column('album', 'year')
    # ### end Alembic commands ###
