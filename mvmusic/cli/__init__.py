import click

from mvmusic.cli.libraries import libraries
from mvmusic.cli.migration import migration
from mvmusic.cli.subsonic_api import subsonic_api
from mvmusic.cli.users import users
from mvmusic.version import version


@click.group()
@click.version_option(version)
def cli():
    pass


cli.add_command(libraries)
cli.add_command(migration)
cli.add_command(subsonic_api)
cli.add_command(users)
