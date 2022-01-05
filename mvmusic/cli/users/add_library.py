import click

from mvmusic.libs.user import add_library


@click.command('add-library')
@click.option('--user', required=True, help='user identifier')
@click.option('--library', required=True, help='library identifier')
def add_library_(user, library):
    """Add library to user"""

    add_library(user, library)
