import click

from mvmusic.helpers.user import list_users


@click.command('list')
def list_():
    """List existing users"""

    list_users()
