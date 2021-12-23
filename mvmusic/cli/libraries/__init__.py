import click

from .add import add_
from .list import list_


@click.group()
def libraries():
    """Manage music libraries"""

    pass


libraries.add_command(add_)
libraries.add_command(list_)
