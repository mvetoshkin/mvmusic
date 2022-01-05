import click

from mvmusic.libs.library import list_libraries


@click.command('list')
def list_():
    """List existing libraries"""

    list_libraries()
