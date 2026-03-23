"""Entidade Registro de Saúde - hidratação, refeições, exercícios, medicamentos."""

import datetime as dt
from enum import Enum

from pydantic import BaseModel, Field


class HealthRecordType(str, Enum):
    """Tipo de registro de saúde."""

    HYDRATION = "hidratação"
    MEAL = "refeição"
    EXERCISE = "exercício"
    WEIGHT = "peso"
    SLEEP = "sono"
    MEDICATION = "medicamento"
    HEART_RATE = "frequência cardíaca"
    MOOD = "humor"


class MealType(str, Enum):
    """Tipo de refeição."""

    BREAKFAST = "café da manhã"
    LUNCH = "almoço"
    DINNER = "jantar"
    SNACK = "lanche"


class ExerciseType(str, Enum):
    """Tipo de exercício."""

    SWIMMING = "natação"
    WALKING = "caminhada"
    RUNNING = "corrida"
    GYM = "academia"
    YOGA = "yoga"
    CYCLING = "ciclismo"
    OTHER = "outro"


class HealthRecord(BaseModel):
    """Registro genérico de saúde.

    Formato flexível que acomoda diferentes tipos de dados de saúde.
    O campo `value` tem semântica diferente conforme o `record_type`:
    - hidratação: número de copos
    - peso: quilos
    - exercício: minutos
    - sono: horas
    - frequência cardíaca: BPM
    - humor: escala 1-10
    """

    id: int | None = None
    record_type: HealthRecordType
    record_date: dt.date = Field(default_factory=dt.date.today)
    record_time: dt.time | None = None
    value: float = Field(description="Valor numérico (semântica depende do tipo)")
    unit: str = ""
    subtype: str = Field(default="", description="Subtipo (ex: tipo de refeição ou exercício)")
    description: str = ""
    duration_minutes: int | None = None
    notes: str = ""
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)

    def to_storage_dict(self) -> dict:
        data = self.model_dump()
        data["date"] = self.record_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        if self.record_time:
            data["record_time"] = self.record_time.isoformat()
        data.pop("record_date", None)
        return data

    @classmethod
    def from_storage_dict(cls, data: dict) -> "HealthRecord":
        if "date" in data and "record_date" not in data:
            data["record_date"] = data.pop("date")
        return cls(**data)
