"""Entidade Meta - objetivos de longo prazo com KPIs rastreáveis."""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class GoalStatus(str, Enum):
    """Estado da meta."""

    ACTIVE = "ativa"
    COMPLETED = "concluída"
    PAUSED = "pausada"
    ABANDONED = "abandonada"


class GoalType(str, Enum):
    """Tipo de meta para classificação."""

    FINANCIAL = "financeira"
    HEALTH = "saúde"
    EDUCATION = "educação"
    CAREER = "carreira"
    PERSONAL = "pessoal"
    RELATIONSHIP = "relacionamento"


class Goal(BaseModel):
    """Meta pessoal com progresso rastreável.

    Cada meta tem um valor alvo e um valor atual que pode ser atualizado
    incrementalmente. O sistema calcula progresso e projeta conclusão.
    """

    id: int | None = None
    name: str
    description: str = ""
    type: GoalType = GoalType.PERSONAL
    status: GoalStatus = GoalStatus.ACTIVE
    target_value: float = Field(default=100.0, description="Valor alvo (ex: R$ 100.000 ou 100%)")
    current_value: float = Field(default=0.0, description="Valor atual")
    unit: str = Field(default="%", description="Unidade de medida (%, R$, kg, dias)")
    start_date: date = Field(default_factory=date.today)
    deadline: date | None = None
    tags: list[str] = Field(default_factory=list)
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def progress_percent(self) -> float:
        """Progresso em percentual (0-100)."""
        if self.target_value == 0:
            return 100.0
        return min(100.0, (self.current_value / self.target_value) * 100)

    @property
    def is_completed(self) -> bool:
        return self.current_value >= self.target_value

    @property
    def remaining(self) -> float:
        return max(0, self.target_value - self.current_value)

    @property
    def days_remaining(self) -> int | None:
        if self.deadline is None:
            return None
        return max(0, (self.deadline - date.today()).days)

    @property
    def daily_rate_needed(self) -> float | None:
        """Quanto precisa avançar por dia para atingir a meta no prazo."""
        days = self.days_remaining
        if days is None or days == 0:
            return None
        return self.remaining / days

    def update_progress(self, value: float) -> None:
        """Atualiza o valor atual da meta."""
        self.current_value = value
        self.updated_at = datetime.now()
        if self.is_completed and self.status == GoalStatus.ACTIVE:
            self.status = GoalStatus.COMPLETED

    def increment(self, amount: float) -> None:
        """Incrementa o valor atual."""
        self.update_progress(self.current_value + amount)

    def to_storage_dict(self) -> dict:
        data = self.model_dump()
        data["start_date"] = self.start_date.isoformat()
        data["tags"] = ",".join(self.tags) if self.tags else ""
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        if self.deadline:
            data["deadline"] = self.deadline.isoformat()
        return data

    @classmethod
    def from_storage_dict(cls, data: dict) -> "Goal":
        if isinstance(data.get("tags"), str):
            data["tags"] = [t.strip() for t in data["tags"].split(",") if t.strip()]
        return cls(**data)
