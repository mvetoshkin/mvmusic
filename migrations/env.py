from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from mvmusic.models import BaseModel
from mvmusic.settings import MIGRATIONS_EXCLUDE_TABLES, SQLALCHEMY_DATABASE_URI

config = context.config
fileConfig(config.config_file_name)
target_metadata = BaseModel.metadata
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)


# noinspection PyUnusedLocal
def include_symbol(tablename, schema=None):
    return tablename not in MIGRATIONS_EXCLUDE_TABLES


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_symbol=include_symbol
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_symbol=include_symbol
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
