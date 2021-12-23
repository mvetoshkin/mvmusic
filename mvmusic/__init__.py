import importlib
import os

from click.exceptions import ClickException

from mvmusic import models
from mvmusic.cli import cli
from mvmusic.common.database import db
from mvmusic.logger import init_logger
from mvmusic.models import BaseModel


def main():
    init_logger()
    import_models()

    # noinspection PyBroadException
    try:
        cli.main(standalone_mode=False)
        db.session.commit()
    except ClickException as exc:
        exc.show()
    except Exception as exc:
        db.session.rollback()
        raise exc
    finally:
        db.session.remove()


def import_models():
    for file in os.listdir(os.path.dirname(models.__file__)):
        if not file.startswith('__') and file.endswith('.py'):
            name = file.rpartition('.')[0]
            importlib.import_module(f'{models.__package__}.{name}')
