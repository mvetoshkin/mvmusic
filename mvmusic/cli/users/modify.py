import click

from mvmusic.libs.user import modify_user


@click.command('modify')
@click.option('--user', required=True, help='user identifier')
@click.option('--name', help='user name')
@click.password_option(prompt_required=False, help='user password')
@click.option('--admin', type=bool, help='user is an admin')
def modify_(user, name, password, admin):
    """Modify existing user"""

    modify_user(user, name, password, admin)
