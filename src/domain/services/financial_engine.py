"""Motor financeiro - regras de negócio para gestão de finanças pessoais."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from src.domain.entities.bill import Bill, BillStatus
from src.domain.entities.transaction import Transaction, TransactionCategory, TransactionType
from src.domain.ports.storage import IStorage
from src.domain.services.categorizer import categorize_by_description

logger = logging.getLogger(__name__)


class FinancialEngine:
    """Regras de negócio para gestão financeira.

    Responsável por: categorização automática, cálculo de saldos,
    resumos financeiros, alertas de contas e projeções.
    """

    def __init__(self, storage: IStorage, event_bus: Any | None = None) -> None:
        self._storage = storage
        self._event_bus = event_bus

    def categorize_transaction(self, description: str) -> TransactionCategory:
        """Categoriza automaticamente com base em palavras-chave na descrição."""
        return categorize_by_description(description)

    def add_transaction(
        self,
        date_val: date,
        description: str,
        amount: float,
        transaction_type: TransactionType | None = None,
        category: TransactionCategory | None = None,
        bank: str = "manual",
        **kwargs: Any,
    ) -> Transaction:
        """Registra uma transação com categorização automática."""
        if transaction_type is None:
            transaction_type = TransactionType.INCOME if amount > 0 else TransactionType.EXPENSE

        if category is None:
            category = self.categorize_transaction(description)

        tx = Transaction(
            date=date_val,
            description=description,
            amount=amount,
            type=transaction_type,
            category=category,
            bank=bank,
            **kwargs,
        )

        data = tx.to_storage_dict()
        data.pop("id", None)
        tx_id = self._storage.insert("transactions", data)
        tx.id = tx_id

        logger.info("Transação registrada: %s R$ %.2f [%s]", description, amount, category.value)

        if self._event_bus:
            from src.events.events import TransactionCreated

            self._event_bus.emit(
                TransactionCreated(
                    transaction_id=tx_id,
                    amount=amount,
                    category=category.value,
                    is_impulse=tx.is_impulse,
                ),
                source="financial_engine",
            )

        return tx

    def get_financial_summary(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict[str, Any]:
        """Calcula resumo financeiro do período."""
        if start_date is None:
            start_date = date.today().replace(day=1)
        if end_date is None:
            end_date = date.today()

        rows = self._storage.execute_sql(
            """
            SELECT
                COALESCE(SUM(CASE WHEN type = 'receita' THEN amount ELSE 0 END), 0) as receitas,
                COALESCE(SUM(CASE WHEN type = 'despesa' THEN ABS(amount) ELSE 0 END), 0) as despesas,
                COUNT(*) as total_transacoes
            FROM transactions
            WHERE date BETWEEN ? AND ?
            """,
            (start_date.isoformat(), end_date.isoformat()),
        )

        row = rows[0] if rows else {"receitas": 0, "despesas": 0, "total_transacoes": 0}
        receitas = float(row["receitas"])
        despesas = float(row["despesas"])

        return {
            "receitas": receitas,
            "despesas": despesas,
            "saldo": receitas - despesas,
            "total_transacoes": row["total_transacoes"],
            "período_início": start_date.isoformat(),
            "período_fim": end_date.isoformat(),
        }

    def get_expenses_by_category(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """Agrupa despesas por categoria no período."""
        if start_date is None:
            start_date = date.today().replace(day=1)
        if end_date is None:
            end_date = date.today()

        return self._storage.execute_sql(
            """
            SELECT category, SUM(ABS(amount)) as total, COUNT(*) as count
            FROM transactions
            WHERE type = 'despesa' AND date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (start_date.isoformat(), end_date.isoformat()),
        )

    def get_pending_bills(self) -> list[Bill]:
        """Retorna contas pendentes ordenadas por vencimento."""
        rows = self._storage.query(
            "bills",
            filters={"status": BillStatus.PENDING.value},
            order_by="due_date ASC",
        )
        return [Bill.from_storage_dict(r) for r in rows]

    def get_overdue_bills(self) -> list[Bill]:
        """Retorna contas atrasadas."""
        today = date.today().isoformat()
        rows = self._storage.execute_sql(
            "SELECT * FROM bills WHERE status = 'pendente' AND due_date < ? ORDER BY due_date ASC",
            (today,),
        )
        return [Bill.from_storage_dict(r) for r in rows]

    def get_upcoming_bills(self, days: int = 7) -> list[Bill]:
        """Retorna contas que vencem nos próximos N dias."""
        today = date.today()
        limit_date = today + timedelta(days=days)
        rows = self._storage.execute_sql(
            "SELECT * FROM bills WHERE status = 'pendente' AND due_date BETWEEN ? AND ? ORDER BY due_date ASC",
            (today.isoformat(), limit_date.isoformat()),
        )
        return [Bill.from_storage_dict(r) for r in rows]

    def add_bill(
        self,
        name: str,
        amount: float,
        due_date: date,
        category: str = "geral",
        **kwargs: Any,
    ) -> Bill:
        """Registra uma conta a pagar."""
        bill = Bill(name=name, amount=amount, due_date=due_date, category=category, **kwargs)
        data = bill.to_storage_dict()
        data.pop("id", None)
        bill_id = self._storage.insert("bills", data)
        bill.id = bill_id
        logger.info("Conta registrada: %s R$ %.2f vence %s", name, amount, due_date)
        return bill

    def pay_bill(self, bill_id: int) -> bool:
        """Marca uma conta como paga."""
        from datetime import datetime

        return self._storage.update(
            "bills",
            bill_id,
            {
                "status": BillStatus.PAID.value,
                "paid_at": datetime.now().isoformat(),
            },
        )
