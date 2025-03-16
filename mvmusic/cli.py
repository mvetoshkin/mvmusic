from pathlib import Path

import click
from alembic.command import downgrade, revision, upgrade
from alembic.config import Config

from mvmusic.api.app import create_app
from mvmusic.libs.library import add_library, list_libraries
from mvmusic.libs.scanner import scan_libraries
from mvmusic.libs.user import add_user, add_user_library, list_users, \
    modify_user
from mvmusic.version import version

ALEMBIC_DIRECTORY = "migrations"


def get_alembic_config(directory):
    config = Config()
    config.config_file_name = Path(directory) / "alembic.ini"

    return config


@click.group()
@click.version_option(version)
def cli():
    pass


@cli.command("api")
@click.option("--host", "-h", help="The interface to bind to")
@click.option("--port", "-p", default=8080, help="The port to bind to")
def api_cmd(host, port):
    """Run a development server"""

    app = create_app()
    app.run(host=host, port=port, load_dotenv=False)


@cli.group("libraries")
def libs_group():
    """Manage music libraries"""

    pass


@libs_group.command("add")
@click.option("--path", required=True, help="path to the music library")
@click.option("--name", help="music library name")
def add_library_cmd(path, name):
    """Add a music library"""

    add_library(path, name)


@libs_group.command("list")
def list_libraries_cmd():
    """List existing libraries"""

    list_libraries()


@libs_group.command("scan")
@click.option("--library", "libraries", multiple=True,
              help="library identifier")
@click.option("--full", is_flag=True, help="rescan the entire library")
def scan_libraries_cmd(libraries, full):
    """Scan libraries"""

    scan_libraries(libraries, full)


@cli.group("db")
def db_group():
    """Database migrations"""

    pass


@db_group.command("downgrade")
@click.option("--directory", default=ALEMBIC_DIRECTORY,
              help="path to the migrations directory")
@click.option("--rev", default="-1",
              help="revision target or range for --sql mode")
@click.option("--sql", is_flag=True,
              help="dump the script out as a SQL string; when specified, "
                   "the script is dumped to stdout")
@click.option("--tag", help="an arbitrary tag that can be intercepted by "
                            "custom `env.py` scripts")
def downgrade_db_cmd(directory, rev, sql, tag):
    """Revert to a previous version."""

    if sql and rev == "-1":
        rev = "head:-1"

    config = get_alembic_config(directory)
    downgrade(config, rev, sql=sql, tag=tag)


@db_group.command("revision")
@click.option("--directory", default=ALEMBIC_DIRECTORY,
              help="path to the migrations directory")
@click.option("--message", help="message to apply to the revision")
@click.option("--autogenerate", is_flag=True, default=True,
              help="autogenerate the script from the database")
@click.option("--sql", is_flag=True,
              help="dump the script out as a SQL string; when specified, "
                   "the script is dumped to stdout")
@click.option("--head", default="head",
              help="head revision to build the new revision upon as a parent")
@click.option("--splice", is_flag=True,
              help="the new revision should be made into a new head of its "
                   "own; is required when the given `head` is not itself a "
                   "head")
@click.option("--branch-label", help="label to apply to the branch")
@click.option("--version-path", help="symbol identifying a specific version "
                                     "path from the configuration")
@click.option("--rev_id", help="revision identifier to use instead of having "
                               "one generated")
def db_revision_cmd(directory, message, autogenerate, sql, head, splice,
                    branch_label, version_path, rev_id):
    """Create a new revision file."""

    config = get_alembic_config(directory)
    revision(config, message=message, autogenerate=autogenerate, sql=sql,
             head=head, splice=splice, branch_label=branch_label,
             version_path=version_path, rev_id=rev_id)


@db_group.command("upgrade")
@click.option("--directory", default=ALEMBIC_DIRECTORY,
              help="path to the migrations directory")
@click.option("--rev", default="head",
              help="revision target or range for --sql mode")
@click.option("--sql", is_flag=True,
              help="dump the script out as a SQL string; when specified, "
                   "the script is dumped to stdout")
@click.option("--tag", help="an arbitrary tag that can be intercepted by "
                            "custom `env.py` scripts")
def upgrade_db_cmd(directory, rev, sql, tag):
    """Upgrade to a later version."""

    config = get_alembic_config(directory)
    upgrade(config, rev, sql=sql, tag=tag)


@cli.group("users")
def users_group():
    """Manage music libraries"""

    pass


@users_group.command("add")
@click.option("--name", prompt=True, help="user name")
@click.password_option(help="user password")
@click.option("--admin", is_flag=True, help="user is an admin")
def add_user_cmd(name, password, admin):
    """Add a user"""

    add_user(name, password, admin)


@users_group.command("add-library")
@click.option("--user", required=True, help="user identifier")
@click.option("--library", required=True, help="library identifier")
def add_library_cmd(user, library):
    """Add library to user"""

    add_user_library(user, library)


@users_group.command("list")
def list_users_cmd():
    """List existing users"""

    list_users()


@users_group.command("modify")
@click.option("--user", required=True, help="user identifier")
@click.option("--name", help="user name")
@click.password_option(prompt_required=False, help="user password")
@click.option("--admin", type=bool, help="user is an admin")
def modify_user_cmd(user, name, password, admin):
    """Modify existing user"""

    modify_user(user, name, password, admin)
