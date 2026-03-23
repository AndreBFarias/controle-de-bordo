"""Parser de extrato CSV do Nubank."""

from __future__ import annotations

import csv
import logging
from datetime import date, datetime
from pathlib import Path

from src.domain.entities.transaction import Transaction, TransactionCategory, TransactionType

logger = logging.getLogger(__name__)

NUBANK_HEADERS = {"Data", "Valor", "Identificador", "Descrição"}
NUBANK_HEADERS_ALT = {"date", "amount", "id", "description"}


class NubankCSVImporter:
    """Importa extratos CSV exportados do app/site do Nubank.

    Formato esperado:
        Data,Valor,Identificador,Descrição
        2026-03-15,-45.90,abc123,IFOOD *RESTAURANTE
    """

    @property
    def bank_name(self) -> str:
        return "Nubank"

    @property
    def supported_formats(self) -> list[str]:
        return [".csv"]

    def detect(self, file_path: Path) -> bool:
        """Verifica se o CSV é do formato Nubank."""
        try:
            with open(file_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header is None:
                    return False
                header_set = {h.strip() for h in header}
                return bool(header_set & NUBANK_HEADERS) or bool(header_set & NUBANK_HEADERS_ALT)
        except Exception:
            return False

    def parse(self, file_path: Path) -> list[Transaction]:
        """Lê CSV do Nubank e retorna transações normalizadas."""
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        if file_path.suffix.lower() != ".csv":
            raise ValueError(f"Formato não suportado: {file_path.suffix}")

        transactions: list[Transaction] = []
        now = datetime.now()

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    tx = self._parse_row(row, now)
                    if tx:
                        transactions.append(tx)
                except Exception as exc:
                    logger.warning("Erro ao parsear linha do Nubank: %s - %s", row, exc)

        logger.info("Importadas %d transações do Nubank de %s", len(transactions), file_path.name)
        return transactions

    def _parse_row(self, row: dict, import_time: datetime) -> Transaction | None:
        """Converte uma linha do CSV em Transaction."""
        date_str = row.get("Data") or row.get("date", "")
        amount_str = row.get("Valor") or row.get("amount", "")
        description = row.get("Descrição") or row.get("description", "")

        if not date_str or not amount_str:
            return None

        tx_date = date.fromisoformat(date_str.strip())
        amount = float(amount_str.strip().replace(",", "."))

        tx_type = TransactionType.INCOME if amount > 0 else TransactionType.EXPENSE
        category = self._categorize(description)

        return Transaction(
            date=tx_date,
            description=description.strip(),
            amount=amount,
            type=tx_type,
            category=category,
            bank="nubank",
            imported_at=import_time,
        )

    def _categorize(self, description: str) -> TransactionCategory:
        """Categorização básica por palavras-chave."""
        from src.domain.services.categorizer import categorize_by_description

        return categorize_by_description(description)
