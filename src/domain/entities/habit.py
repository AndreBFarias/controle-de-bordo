"""Entidade Hábito - comportamentos rastreáveis com streak e frequência."""

from datetime import date, datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field


class HabitFrequency(str, Enum):
    """Frequência esperada do hábito."""

    DAILY = "diário"
    WEEKDAYS = "dias úteis"
    WEEKLY = "semanal"
    CUSTOM = "personalizado"


class Habit(BaseModel):
    """Hábito rastreável com sistema de streak.

    O streak conta dias consecutivos de cumprimento.
    Usado para inglês (Duolingo), exercícios, escrita, hidratação, etc.
    """

    id: int | None = None
    name: str
    description: str = ""
    frequency: HabitFrequency = HabitFrequency.DAILY
    target_per_day: int = Field(default=1, description="Vezes por dia para considerar cumprido")
    current_streak: int = Field(default=0, description="Dias consecutivos")
    best_streak: int = Field(default=0, description="Recorde de streak")
    total_completions: int = Field(default=0, description="Total de vezes completado")
    last_completed: date | None = None
    is_active: bool = True
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def completed_today(self) -> bool:
        return self.last_completed == date.today()

    @property
    def streak_broken(self) -> bool:
        """Verifica se o streak foi quebrado (não completou ontem)."""
        if self.last_completed is None:
            return False
        yesterday = date.today() - timedelta(days=1)
        return self.last_completed < yesterday

    def complete(self) -> None:
        """Registra conclusão do hábito para hoje."""
        today = date.today()
        if self.last_completed == today:
            return

        yesterday = today - timedelta(days=1)
        if self.last_completed == yesterday or self.last_completed is None:
            self.current_streak += 1
        else:
            self.current_streak = 1

        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak

        self.total_completions += 1
        self.last_completed = today

    def reset_streak(self) -> None:
        """Zera o streak atual (chamado quando quebra a sequência)."""
        self.current_streak = 0

    def to_storage_dict(self) -> dict:
        data = self.model_dump()
        data["tags"] = ",".join(self.tags) if self.tags else ""
        data["created_at"] = self.created_at.isoformat()
        if self.last_completed:
            data["last_completed"] = self.last_completed.isoformat()
        return data

    @classmethod
    def from_storage_dict(cls, data: dict) -> "Habit":
        if isinstance(data.get("tags"), str):
            data["tags"] = [t.strip() for t in data["tags"].split(",") if t.strip()]
        return cls(**data)
