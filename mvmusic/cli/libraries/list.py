import click

from mvmusic.helpers.library import list_libraries


@click.command('list')
def list_():
    """List existing libraries"""

    list_libraries()
