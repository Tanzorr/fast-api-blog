from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

import models  # noqa: F401 — registers every model on Base.metadata
from config import settings
from database import Base

# The Alembic Config object: the values from alembic.ini.
config = context.config

# Set up Python logging from alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# autogenerate compares this metadata (our models) with the database.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Write the SQL to the screen, without a database (`alembic upgrade --sql`)."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Connect to the database and run the migrations."""
    connectable = create_engine(settings.database_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
