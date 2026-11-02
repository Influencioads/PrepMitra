from logging.config import fileConfig

from alembic import context
from sqlalchemy import JSON, create_engine, pool

import app.models  # noqa: F401  (registers all tables on Base.metadata)
from app.config import get_settings
from app.db import Base, Embedding, TZDateTime

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _url() -> str:
    # Tests pass an explicit URL through the Alembic config; otherwise use DATABASE_URL.
    return config.get_main_option("sqlalchemy.url") or get_settings().database_url


def render_item(type_, obj, autogen_context):
    """Migrations always target PostgreSQL: render the portable model types as native Postgres types."""
    if type_ != "type":
        return False
    if isinstance(obj, TZDateTime):
        return "sa.DateTime(timezone=True)"
    if isinstance(obj, Embedding):
        autogen_context.imports.add("import pgvector.sqlalchemy")
        return f"pgvector.sqlalchemy.Vector({obj.dim})"
    if isinstance(obj, JSON) and "postgresql" in getattr(obj, "_variant_mapping", {}):
        autogen_context.imports.add("from sqlalchemy.dialects import postgresql")
        return "postgresql.JSONB(astext_type=sa.Text())"
    return False


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True, compare_type=True,
                      render_item=render_item)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True,
                          render_item=render_item)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
