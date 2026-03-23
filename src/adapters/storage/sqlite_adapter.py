"""Adaptador SQLite - persistência local-first com WAL mode."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

ALLOWED_TABLES = frozenset(
    {
        "schema_version",
        "transactions",
        "bills",
        "goals",
        "habits",
        "habit_logs",
        "health_records",
        "study_sessions",
        "events_log",
    }
)

SCHEMA_VERSION = 1

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL DEFAULT 'despesa',
    category TEXT NOT NULL DEFAULT 'outros',
    bank TEXT NOT NULL DEFAULT 'manual',
    account TEXT NOT NULL DEFAULT 'principal',
    tags TEXT DEFAULT '',
    is_impulse INTEGER DEFAULT 0,
    is_recurring INTEGER DEFAULT 0,
    notes TEXT DEFAULT '',
    imported_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    due_date TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'geral',
    status TEXT NOT NULL DEFAULT 'pendente',
    recurrence TEXT NOT NULL DEFAULT 'única',
    auto_debit INTEGER DEFAULT 0,
    reminder_days INTEGER DEFAULT 3,
    notes TEXT DEFAULT '',
    paid_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    type TEXT NOT NULL DEFAULT 'pessoal',
    status TEXT NOT NULL DEFAULT 'ativa',
    target_value REAL NOT NULL DEFAULT 100.0,
    current_value REAL NOT NULL DEFAULT 0.0,
    unit TEXT NOT NULL DEFAULT '%',
    start_date TEXT NOT NULL,
    deadline TEXT,
    tags TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    frequency TEXT NOT NULL DEFAULT 'diário',
    target_per_day INTEGER DEFAULT 1,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    last_completed TEXT,
    is_active INTEGER DEFAULT 1,
    tags TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    completed INTEGER DEFAULT 1,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_type TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    value REAL NOT NULL,
    unit TEXT DEFAULT '',
    subtype TEXT DEFAULT '',
    description TEXT DEFAULT '',
    duration_minutes INTEGER,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    platform TEXT NOT NULL DEFAULT 'outro',
    course_name TEXT DEFAULT '',
    topic TEXT DEFAULT '',
    duration_minutes INTEGER NOT NULL DEFAULT 0,
    progress_percent REAL,
    notes TEXT DEFAULT '',
    language TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS events_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    data TEXT NOT NULL DEFAULT '{}',
    source TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_bills_due_date ON bills(due_date);
CREATE INDEX IF NOT EXISTS idx_bills_status ON bills(status);
CREATE INDEX IF NOT EXISTS idx_goals_status ON goals(status);
CREATE INDEX IF NOT EXISTS idx_habits_active ON habits(is_active);
CREATE INDEX IF NOT EXISTS idx_health_date ON health_records(date);
CREATE INDEX IF NOT EXISTS idx_health_type ON health_records(record_type);
CREATE INDEX IF NOT EXISTS idx_study_date ON study_sessions(date);
CREATE INDEX IF NOT EXISTS idx_events_type ON events_log(event_type);
"""


class SQLiteAdapter:
    """Implementação de IStorage usando SQLite com modo WAL.

    Garante persistência ACID, leituras concorrentes e zero dependência
    de serviços externos. A fonte da verdade do sistema local-first.
    """

    def __init__(self, db_path: str | Path = "data/bordo.db") -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    def _validate_table(self, table: str) -> None:
        """Valida nome de tabela contra whitelist para prevenir SQL injection."""
        if table not in ALLOWED_TABLES:
            raise ValueError(f"Tabela '{table}' não permitida. Válidas: {sorted(ALLOWED_TABLES)}")

    @property
    def connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(
                str(self._db_path),
                check_same_thread=False,
            )
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.execute("PRAGMA busy_timeout=5000")
        return self._conn

    def initialize(self) -> None:
        """Cria tabelas e aplica migrações."""
        cursor = self.connection.cursor()
        cursor.executescript(SCHEMA_SQL)

        version_rows = cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1").fetchone()
        current_version = version_rows["version"] if version_rows else 0

        if current_version < SCHEMA_VERSION:
            self._migrate(current_version, SCHEMA_VERSION)
            cursor.execute(
                "INSERT INTO schema_version (version) VALUES (?)",
                (SCHEMA_VERSION,),
            )

        self.connection.commit()
        logger.info("SQLite inicializado em %s (versão %d)", self._db_path, SCHEMA_VERSION)

    def _migrate(self, from_version: int, to_version: int) -> None:
        """Aplica migrações incrementais entre versões."""
        logger.info("Migrando schema de v%d para v%d", from_version, to_version)

    def insert(self, table: str, data: dict[str, Any]) -> int:
        """Insere registro e retorna o ID gerado."""
        self._validate_table(table)
        filtered = {k: v for k, v in data.items() if k != "id"}
        columns = ", ".join(filtered.keys())
        placeholders = ", ".join(["?"] * len(filtered))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = self.connection.execute(sql, tuple(filtered.values()))
        self.connection.commit()
        row_id = cursor.lastrowid or 0
        logger.debug("Inserido em %s: id=%d", table, row_id)
        return row_id

    def update(self, table: str, record_id: int, data: dict[str, Any]) -> bool:
        """Atualiza registro pelo ID."""
        self._validate_table(table)
        filtered = {k: v for k, v in data.items() if k != "id"}
        if not filtered:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in filtered)
        sql = f"UPDATE {table} SET {set_clause} WHERE id = ?"

        cursor = self.connection.execute(sql, (*filtered.values(), record_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def delete(self, table: str, record_id: int) -> bool:
        """Remove registro pelo ID."""
        self._validate_table(table)
        cursor = self.connection.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_by_id(self, table: str, record_id: int) -> dict[str, Any] | None:
        """Busca registro pelo ID."""
        self._validate_table(table)
        row = self.connection.execute(f"SELECT * FROM {table} WHERE id = ?", (record_id,)).fetchone()
        return dict(row) if row else None

    def query(
        self,
        table: str,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Busca registros com filtros."""
        self._validate_table(table)
        sql = f"SELECT * FROM {table}"
        params: list[Any] = []

        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, (list, tuple)):
                    placeholders = ", ".join(["?"] * len(value))
                    conditions.append(f"{key} IN ({placeholders})")
                    params.extend(value)
                else:
                    conditions.append(f"{key} = ?")
                    params.append(value)
            sql += " WHERE " + " AND ".join(conditions)

        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"

        rows = self.connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    def execute_sql(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        """Executa SQL arbitrário para consultas complexas."""
        rows = self.connection.execute(sql, params or ()).fetchall()
        return [dict(row) for row in rows]

    def count(self, table: str, filters: dict[str, Any] | None = None) -> int:
        """Conta registros com filtros."""
        self._validate_table(table)
        sql = f"SELECT COUNT(*) as cnt FROM {table}"
        params: list[Any] = []

        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            sql += " WHERE " + " AND ".join(conditions)

        row = self.connection.execute(sql, params).fetchone()
        return row["cnt"] if row else 0

    def close(self) -> None:
        """Fecha a conexão."""
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info("Conexão SQLite fechada")

    def __del__(self) -> None:
        self.close()
