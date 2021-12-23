import click

from mvmusic.helpers.user import add_user


@click.command('add')
@click.option('--name', prompt=True, help='user name')
@click.password_option(help='user password')
@click.option('--admin', is_flag=True, help='user is an admin')
def add_(name, password, admin):
    """Add a user"""

    add_user(name, password, admin)
