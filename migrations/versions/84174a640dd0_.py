"""empty message

Revision ID: 84174a640dd0
Revises: d678b690a5d9
Create Date: 2021-12-29 23:17:22.022547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84174a640dd0'
down_revision = 'd678b690a5d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('directory', 'library_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('media', 'library_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media', 'library_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('directory', 'library_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###