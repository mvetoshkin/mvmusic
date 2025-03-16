import importlib
from pathlib import Path

from click.exceptions import ClickException

from mvmusic import models
from mvmusic.cli import cli
from mvmusic.libs.database import session
from mvmusic.libs.logger import init_logger
from mvmusic.models import BaseModel

init_logger()

for file in Path(models.__file__).parent.iterdir():
    if not file.name.startswith("__") and file.suffix == ".py":
        importlib.import_module(f"{models.__package__}.{file.stem}")


def main():
    # noinspection PyBroadException
    try:
        cli.main(standalone_mode=False)
        session.commit()
    except ClickException as exc:
        exc.show()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.remove()
