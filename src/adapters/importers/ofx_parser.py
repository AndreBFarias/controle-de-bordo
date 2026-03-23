"""Parser de extrato OFX genérico - compatível com múltiplos bancos."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from src.domain.entities.transaction import Transaction, TransactionCategory, TransactionType

logger = logging.getLogger(__name__)


class OFXImporter:
    """Importa extratos no formato OFX (Open Financial Exchange).

    Compatível com: Itaú, Banco do Brasil, Bradesco, Inter, Santander e outros.
    Usa a biblioteca ofxparse para processar o formato.
    """

    @property
    def bank_name(self) -> str:
        return "OFX Genérico"

    @property
    def supported_formats(self) -> list[str]:
        return [".ofx", ".qfx"]

    def detect(self, file_path: Path) -> bool:
        """Verifica se o arquivo é OFX válido."""
        try:
            with open(file_path, encoding="latin-1") as f:
                content = f.read(500)
                return "OFXHEADER" in content or "<OFX>" in content.upper()
        except Exception:
            return False

    def parse(self, file_path: Path) -> list[Transaction]:
        """Lê arquivo OFX e retorna transações normalizadas."""
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        try:
            from ofxparse import OfxParser
        except ImportError as err:
            logger.error("ofxparse não instalado: pip install ofxparse")
            raise ImportError("Instale ofxparse: pip install ofxparse") from err

        transactions: list[Transaction] = []
        now = datetime.now()

        with open(file_path, "rb") as f:
            ofx = OfxParser.parse(f)

        bank_id = ""
        if hasattr(ofx, "account") and ofx.account:
            bank_id = getattr(ofx.account, "institution", None)
            if hasattr(bank_id, "organization"):
                bank_id = bank_id.organization or ""
            else:
                bank_id = str(bank_id) if bank_id else ""

        account = ofx.account if hasattr(ofx, "account") else None
        statement = account.statement if account and hasattr(account, "statement") else None

        if statement is None:
            logger.warning("Arquivo OFX sem extrato: %s", file_path)
            return []

        for ofx_tx in statement.transactions:
            try:
                tx = self._convert_transaction(ofx_tx, bank_id, now)
                if tx:
                    transactions.append(tx)
            except Exception as exc:
                logger.warning("Erro ao converter transação OFX: %s", exc)

        logger.info("Importadas %d transações OFX de %s", len(transactions), file_path.name)
        return transactions

    def _convert_transaction(self, ofx_tx, bank_id: str, import_time: datetime) -> Transaction | None:
        """Converte transação OFX para formato do domínio."""
        tx_date = ofx_tx.date
        if isinstance(tx_date, datetime):
            tx_date = tx_date.date()

        amount = float(ofx_tx.amount)
        description = getattr(ofx_tx, "memo", "") or getattr(ofx_tx, "payee", "") or ""

        if not description:
            description = getattr(ofx_tx, "name", "Sem descrição")

        tx_type = TransactionType.INCOME if amount > 0 else TransactionType.EXPENSE
        category = self._categorize(description)

        return Transaction(
            date=tx_date,
            description=description.strip(),
            amount=amount,
            type=tx_type,
            category=category,
            bank=bank_id.lower() if bank_id else "ofx",
            imported_at=import_time,
        )

    def _categorize(self, description: str) -> TransactionCategory:
        """Categorização por palavras-chave."""
        from src.domain.services.categorizer import categorize_by_description

        return categorize_by_description(description)
