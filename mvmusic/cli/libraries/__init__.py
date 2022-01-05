import click

from .add import add_
from .list import list_
from .scan import scan_


@click.group()
def libraries():
    """Manage music libraries"""

    pass


libraries.add_command(add_)
libraries.add_command(list_)
libraries.add_command(scan_)
