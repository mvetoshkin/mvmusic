"""empty message

Revision ID: 15b19081b752
Revises: 03e4df158f95
Create Date: 2022-07-06 11:13:01.116740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15b19081b752'
down_revision = '03e4df158f95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('starred_artist',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.Column('artist_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_starred_artist_artist_id'), 'starred_artist', ['artist_id'], unique=False)
    op.create_index(op.f('ix_starred_artist_user_id'), 'starred_artist', ['user_id'], unique=False)
    op.create_table('starred_directory',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.Column('directory_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['directory_id'], ['directory.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_starred_directory_directory_id'), 'starred_directory', ['directory_id'], unique=False)
    op.create_index(op.f('ix_starred_directory_user_id'), 'starred_directory', ['user_id'], unique=False)
    op.create_table('starred_album',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.Column('album_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_starred_album_album_id'), 'starred_album', ['album_id'], unique=False)
    op.create_index(op.f('ix_starred_album_user_id'), 'starred_album', ['user_id'], unique=False)
    op.create_table('starred_media',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.Column('media_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['media_id'], ['media.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_starred_media_media_id'), 'starred_media', ['media_id'], unique=False)
    op.create_index(op.f('ix_starred_media_user_id'), 'starred_media', ['user_id'], unique=False)
    op.alter_column('history', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('history', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_starred_media_user_id'), table_name='starred_media')
    op.drop_index(op.f('ix_starred_media_media_id'), table_name='starred_media')
    op.drop_table('starred_media')
    op.drop_index(op.f('ix_starred_album_user_id'), table_name='starred_album')
    op.drop_index(op.f('ix_starred_album_album_id'), table_name='starred_album')
    op.drop_table('starred_album')
    op.drop_index(op.f('ix_starred_directory_user_id'), table_name='starred_directory')
    op.drop_index(op.f('ix_starred_directory_directory_id'), table_name='starred_directory')
    op.drop_table('starred_directory')
    op.drop_index(op.f('ix_starred_artist_user_id'), table_name='starred_artist')
    op.drop_index(op.f('ix_starred_artist_artist_id'), table_name='starred_artist')
    op.drop_table('starred_artist')
    # ### end Alembic commands ###
