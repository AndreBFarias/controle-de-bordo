"""Entidade Transação - registro de movimentação financeira."""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    """Tipo da transação."""

    INCOME = "receita"
    EXPENSE = "despesa"
    TRANSFER = "transferência"


class TransactionCategory(str, Enum):
    """Categorias padrão para classificação automática."""

    MORADIA = "moradia"
    ALIMENTACAO = "alimentação"
    TRANSPORTE = "transporte"
    SAUDE = "saúde"
    EDUCACAO = "educação"
    LAZER = "lazer"
    VESTUARIO = "vestuário"
    ASSINATURAS = "assinaturas"
    INVESTIMENTO = "investimento"
    SALARIO = "salário"
    FREELANCE = "freelance"
    PRESENTE = "presente"
    PET = "pet"
    BELEZA = "beleza"
    TECNOLOGIA = "tecnologia"
    VIAGEM = "viagem"
    OUTROS = "outros"


class Transaction(BaseModel):
    """Transação financeira normalizada.

    Independente do banco de origem - o importador converte para este formato.
    """

    id: int | None = None
    date: date
    description: str
    amount: float = Field(description="Valor em reais. Positivo = receita, negativo = despesa")
    type: TransactionType
    category: TransactionCategory = TransactionCategory.OUTROS
    bank: str = Field(default="manual", description="Banco de origem (nubank, itau, bb, manual)")
    account: str = Field(default="principal", description="Conta associada")
    tags: list[str] = Field(default_factory=list)
    is_impulse: bool = Field(default=False, description="Marcada como compra por impulso")
    is_recurring: bool = Field(default=False, description="Gasto recorrente (assinatura, aluguel)")
    notes: str = ""
    imported_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def is_expense(self) -> bool:
        return self.type == TransactionType.EXPENSE

    @property
    def is_income(self) -> bool:
        return self.type == TransactionType.INCOME

    @property
    def absolute_amount(self) -> float:
        return abs(self.amount)

    def to_storage_dict(self) -> dict:
        """Converte para dicionário compatível com o storage."""
        data = self.model_dump()
        data["date"] = self.date.isoformat()
        data["tags"] = ",".join(self.tags) if self.tags else ""
        data["created_at"] = self.created_at.isoformat()
        if self.imported_at:
            data["imported_at"] = self.imported_at.isoformat()
        return data

    @classmethod
    def from_storage_dict(cls, data: dict) -> "Transaction":
        """Reconstrói a partir de dicionário do storage."""
        if isinstance(data.get("tags"), str):
            data["tags"] = [t.strip() for t in data["tags"].split(",") if t.strip()]
        return cls(**data)
