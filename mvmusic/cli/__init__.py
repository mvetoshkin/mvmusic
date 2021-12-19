import click

from mvmusic.cli.migration import migration
from mvmusic.cli.subsonic_api import subsonic_api
from mvmusic.version import version


@click.group()
@click.version_option(version)
def cli():
    pass


cli.add_command(migration)
cli.add_command(subsonic_api)
