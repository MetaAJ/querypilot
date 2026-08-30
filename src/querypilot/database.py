"""Read-only SQLite access used by the analytics workflow."""

import sqlite3
from pathlib import Path

from .safety import validate_read_only_sql


def connect(database_path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def execute_read_only(connection: sqlite3.Connection, query: str) -> list[dict[str, object]]:
    cursor = connection.execute(validate_read_only_sql(query))
    columns = [description[0] for description in cursor.description or []]
    return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]


def schema_summary(connection: sqlite3.Connection) -> dict[str, list[str]]:
    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    return {
        table[0]: [row[1] for row in connection.execute(f'PRAGMA table_info("{table[0]}")')]
        for table in tables
    }
