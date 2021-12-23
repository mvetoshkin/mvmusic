import click

from .add import add_
from .add_library import add_library_
from .list import list_
from .modify import modify_


@click.group()
def users():
    """Manage users"""

    pass


users.add_command(add_)
users.add_command(add_library_)
users.add_command(list_)
users.add_command(modify_)
