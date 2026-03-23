"""Entidade Conta a Pagar - boletos, mensalidades, compromissos financeiros."""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class BillStatus(str, Enum):
    """Estado da conta."""

    PENDING = "pendente"
    PAID = "paga"
    OVERDUE = "atrasada"
    CANCELLED = "cancelada"


class BillRecurrence(str, Enum):
    """Frequência de recorrência."""

    ONCE = "única"
    MONTHLY = "mensal"
    YEARLY = "anual"
    WEEKLY = "semanal"


class Bill(BaseModel):
    """Conta a pagar ou compromisso financeiro.

    Suporta contas únicas e recorrentes. O sistema monitora vencimentos
    e envia alertas configuráveis via notificador.
    """

    id: int | None = None
    name: str
    amount: float = Field(gt=0, description="Valor em reais")
    due_date: date
    category: str = "geral"
    status: BillStatus = BillStatus.PENDING
    recurrence: BillRecurrence = BillRecurrence.ONCE
    auto_debit: bool = Field(default=False, description="Débito automático ativo")
    reminder_days: int = Field(default=3, description="Dias antes para lembrar")
    notes: str = ""
    paid_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def is_overdue(self) -> bool:
        return self.status == BillStatus.PENDING and self.due_date < date.today()

    @property
    def days_until_due(self) -> int:
        return (self.due_date - date.today()).days

    @property
    def needs_reminder(self) -> bool:
        return self.status == BillStatus.PENDING and 0 <= self.days_until_due <= self.reminder_days

    def mark_paid(self) -> None:
        """Marca como paga."""
        self.status = BillStatus.PAID
        self.paid_at = datetime.now()

    def to_storage_dict(self) -> dict:
        data = self.model_dump()
        data["due_date"] = self.due_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        if self.paid_at:
            data["paid_at"] = self.paid_at.isoformat()
        return data

    @classmethod
    def from_storage_dict(cls, data: dict) -> "Bill":
        return cls(**data)
