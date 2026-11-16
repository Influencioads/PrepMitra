"""Copy every row of the local SQLite dev database (backend/dev.db) into a PostgreSQL database.

    cd backend && .venv/Scripts/python scripts/sqlite_to_postgres.py postgresql+psycopg://prepmitra:prepmitra@localhost:5433/prepmitra

The PostgreSQL schema is created first with the real Alembic migrations, its tables are emptied, then rows are copied
table by table in foreign-key order. Columns that exist only on one side are skipped. dev.db is only read.
"""

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from sqlalchemy import create_engine, inspect, text  # noqa: E402

import app.models  # noqa: E402,F401
from app.db import Base  # noqa: E402

BATCH = 2000
_NONE = object()


def _fallback(col):
    """The value a NOT NULL column gets when the old row has none: its Python default, else a type-based zero."""
    d = col.default
    if d is not None and getattr(d, "is_scalar", False):
        return d.arg
    if d is not None and getattr(d, "is_callable", False):
        try:
            return d.arg(None)
        except TypeError:
            return d.arg()
    try:
        py = col.type.python_type
    except NotImplementedError:
        return _NONE
    return {int: 0, float: 0.0, str: "", bool: False, dict: {}, list: []}.get(py, _NONE)


def main(pg_url: str, sqlite_path: Path) -> None:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "alembic"))
    cfg.set_main_option("sqlalchemy.url", pg_url.replace("%", "%%"))
    command.upgrade(cfg, "head")

    src = create_engine(f"sqlite:///{sqlite_path.as_posix()}")
    dst = create_engine(pg_url)
    src_tables = set(inspect(src).get_table_names())
    dst_cols = {t: {c["name"] for c in inspect(dst).get_columns(t)} for t in inspect(dst).get_table_names()}
    src_cols = {t: {c["name"] for c in inspect(src).get_columns(t)} for t in src_tables}

    tables = [t for t in Base.metadata.sorted_tables if t.name in src_tables and t.name in dst_cols]
    with dst.begin() as conn:
        conn.execute(text("TRUNCATE " + ", ".join(f'"{t.name}"' for t in tables) + " RESTART IDENTITY CASCADE"))

    for table in tables:
        cols = [c for c in table.columns if c.name in src_cols[table.name] and c.name in dst_cols[table.name]]
        # dev.db gained some NOT NULL columns later without a backfill; give their NULLs the column's default.
        fill = {c.name: _fallback(c) for c in cols if not c.nullable}
        sel = table.select().with_only_columns(*cols)
        copied = 0
        with src.connect() as s, dst.begin() as d:
            result = s.execution_options(stream_results=True).execute(sel)
            while rows := result.fetchmany(BATCH):
                batch = []
                for r in rows:
                    row = dict(r._mapping)
                    for k, v in fill.items():
                        if row.get(k) is None and v is not _NONE:
                            row[k] = v
                    batch.append(row)
                d.execute(table.insert(), batch)
                copied += len(rows)
        print(f"{table.name}: {copied}")

    # Integer primary keys: move each sequence past the copied rows.
    with dst.begin() as conn:
        for table in tables:
            for col in table.primary_key.columns:
                if col.autoincrement is True or (col.type.python_type is int and col.autoincrement == "auto"):
                    seq = conn.scalar(text("SELECT pg_get_serial_sequence(:t, :c)"), {"t": table.name, "c": col.name})
                    if seq:
                        conn.execute(text(f'SELECT setval(:s, COALESCE((SELECT MAX("{col.name}") FROM "{table.name}"), 0) + 1, false)'),
                                     {"s": seq})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], Path(sys.argv[2]) if len(sys.argv) > 2 else BACKEND / "dev.db")
