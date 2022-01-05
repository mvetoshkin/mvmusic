import click

from mvmusic.libs.scanner import scan_libraries


@click.command('scan')
@click.option('--library', 'libraries', multiple=True,
              help='library identifier')
def scan_(libraries):
    """Scan libraries"""

    scan_libraries(libraries)
