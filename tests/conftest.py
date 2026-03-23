"""Fixtures compartilhadas para testes E2E."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.adapters.storage.sqlite_adapter import SQLiteAdapter
from src.events.bus import EventBus


@pytest.fixture
def tmp_db(tmp_path: Path) -> Path:
    """Caminho temporário para banco de dados de teste."""
    return tmp_path / "test_bordo.db"


@pytest.fixture
def storage(tmp_db: Path) -> SQLiteAdapter:
    """Storage SQLite inicializado em diretório temporário."""
    adapter = SQLiteAdapter(tmp_db)
    adapter.initialize()
    yield adapter
    adapter.close()


@pytest.fixture
def event_bus() -> EventBus:
    """Event bus limpo para testes."""
    return EventBus()


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Arquivo CSV de exemplo no formato Nubank."""
    csv_content = """Data,Valor,Identificador,Descrição
2026-03-15,-45.90,abc123,IFOOD *RESTAURANTE TESTE
2026-03-14,-89.00,def456,AMAZON.COM.BR
2026-03-13,-120.00,ghi789,ACADEMIA SMARTFIT
2026-03-12,-15.50,jkl012,PADARIA BOM PÃO
2026-03-01,18000.00,mno345,SALARIO EMPRESA LTDA
2026-03-10,-250.00,pqr678,ALUGUEL MAR/2026
"""
    csv_path = tmp_path / "extrato-nubank.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    return csv_path
