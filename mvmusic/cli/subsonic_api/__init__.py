import click

from .run import run_


@click.group()
def subsonic_api():
    pass


subsonic_api.add_command(run_)
