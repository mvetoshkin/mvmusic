import click

from mvmusic.helpers.library import add_library


@click.command('add')
@click.option('--path', required=True, help='path to the music library')
@click.option('--name', help='music library name')
def add_(path, name):
    """Add a music library"""

    add_library(path, name)
