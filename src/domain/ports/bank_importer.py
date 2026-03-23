"""Porta de importação bancária - interface para parsers de extrato."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from src.domain.entities.transaction import Transaction


@runtime_checkable
class IBankImporter(Protocol):
    """Contrato para importadores de dados bancários.

    Cada banco/formato (CSV Nubank, OFX genérico, etc) implementa esta interface.
    """

    @property
    def bank_name(self) -> str:
        """Nome do banco suportado."""
        ...

    @property
    def supported_formats(self) -> list[str]:
        """Extensões suportadas (ex: ['.csv', '.ofx'])."""
        ...

    def parse(self, file_path: Path) -> list[Transaction]:
        """Lê um arquivo de extrato e retorna transações normalizadas.

        Args:
            file_path: Caminho para o arquivo de extrato.

        Returns:
            Lista de transações no formato padronizado do domínio.

        Raises:
            ValueError: Se o formato do arquivo não é suportado.
            FileNotFoundError: Se o arquivo não existe.
        """
        ...

    def detect(self, file_path: Path) -> bool:
        """Verifica se este importador consegue processar o arquivo.

        Analisa cabeçalhos ou estrutura para determinar compatibilidade.
        """
        ...
