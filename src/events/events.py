"""Definições de eventos do sistema - tipados com Pydantic."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Evento base do sistema."""

    timestamp: datetime = Field(default_factory=datetime.now)
    source: str = ""


class TransactionCreated(BaseEvent):
    """Emitido quando uma transação é registrada."""

    transaction_id: int
    amount: float
    category: str
    is_impulse: bool = False


class BillDue(BaseEvent):
    """Emitido quando uma conta está próxima do vencimento."""

    bill_id: int
    bill_name: str
    amount: float
    days_until_due: int


class BillOverdue(BaseEvent):
    """Emitido quando uma conta está atrasada."""

    bill_id: int
    bill_name: str
    amount: float
    days_overdue: int


class GoalUpdated(BaseEvent):
    """Emitido quando o progresso de uma meta é atualizado."""

    goal_id: int
    goal_name: str
    progress_percent: float
    is_completed: bool = False


class HabitCompleted(BaseEvent):
    """Emitido quando um hábito é completado no dia."""

    habit_id: int
    habit_name: str
    current_streak: int


class HabitStreakBroken(BaseEvent):
    """Emitido quando o streak de um hábito é quebrado."""

    habit_id: int
    habit_name: str
    lost_streak: int


class ImpulseAlert(BaseEvent):
    """Emitido quando uma compra por impulso é detectada."""

    transaction_id: int
    amount: float
    category: str
    goal_impact: str = ""


class NudgeTrigger(BaseEvent):
    """Emitido quando o sistema decide enviar um nudge comportamental."""

    nudge_type: str
    message: str
    severity: str = "normal"


class HealthRecordCreated(BaseEvent):
    """Emitido quando um registro de saúde é criado."""

    record_type: str
    value: float


class StudySessionLogged(BaseEvent):
    """Emitido quando uma sessão de estudo é registrada."""

    platform: str
    duration_minutes: int
    language: str = ""


class FocusModeChanged(BaseEvent):
    """Emitido quando o modo de foco é alterado no desktop."""

    mode: str
    active: bool


class AppBlocked(BaseEvent):
    """Emitido quando um app é bloqueado no Android."""

    package_name: str
    reason: str
