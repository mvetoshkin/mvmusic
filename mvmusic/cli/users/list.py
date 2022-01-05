import click

from mvmusic.libs.user import list_users


@click.command('list')
def list_():
    """List existing users"""

    list_users()
