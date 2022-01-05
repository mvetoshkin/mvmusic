import click

from mvmusic.libs.scanner import scan_libraries


@click.command('scan')
@click.option('--library', 'libraries', multiple=True,
              help='library identifier')
@click.option('--full', is_flag=True, help='rescan the entire library')
def scan_(libraries, full):
    """Scan libraries"""

    scan_libraries(libraries, full)
