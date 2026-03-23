"""Porta de persistência - interface para armazenamento de dados."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IStorage(Protocol):
    """Contrato para adaptadores de persistência.

    Qualquer implementação (SQLite, JSON, Supabase) deve seguir esta interface.
    O domínio depende APENAS desta abstração, nunca de implementações concretas.
    """

    def initialize(self) -> None:
        """Inicializa o storage (criação de tabelas, migrações)."""
        ...

    def insert(self, table: str, data: dict[str, Any]) -> int:
        """Insere um registro e retorna o ID gerado."""
        ...

    def update(self, table: str, record_id: int, data: dict[str, Any]) -> bool:
        """Atualiza um registro pelo ID. Retorna True se encontrou."""
        ...

    def delete(self, table: str, record_id: int) -> bool:
        """Remove um registro pelo ID. Retorna True se encontrou."""
        ...

    def get_by_id(self, table: str, record_id: int) -> dict[str, Any] | None:
        """Busca um registro pelo ID."""
        ...

    def query(
        self,
        table: str,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Busca registros com filtros opcionais."""
        ...

    def execute_sql(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        """Executa SQL arbitrário (para consultas complexas)."""
        ...

    def count(self, table: str, filters: dict[str, Any] | None = None) -> int:
        """Conta registros com filtros opcionais."""
        ...
