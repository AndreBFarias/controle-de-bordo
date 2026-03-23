"""Entidade Sessão de Estudo - rastreamento de cursos e aprendizado."""

import datetime as dt
from enum import Enum

from pydantic import BaseModel, Field


class StudyPlatform(str, Enum):
    """Plataforma de estudo."""

    ALURA = "alura"
    COURSERA = "coursera"
    OPEN_ENGLISH = "open english"
    DUOLINGO = "duolingo"
    YOUTUBE = "youtube"
    BOOK = "livro"
    OTHER = "outro"


class StudySession(BaseModel):
    """Sessão de estudo individual.

    Registra tempo gasto, plataforma, tópico e progresso.
    Integra com tracker de hábitos para manter streaks de estudo.
    """

    id: int | None = None
    session_date: dt.date = Field(default_factory=dt.date.today)
    platform: StudyPlatform = StudyPlatform.OTHER
    course_name: str = ""
    topic: str = ""
    duration_minutes: int = Field(ge=0, description="Duração em minutos")
    progress_percent: float | None = Field(default=None, ge=0, le=100, description="Progresso no curso (0-100)")
    notes: str = ""
    language: str = Field(default="", description="Idioma estudado (se aplicável)")
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)

    @property
    def duration_hours(self) -> float:
        return self.duration_minutes / 60.0

    def to_storage_dict(self) -> dict:
        data = self.model_dump()
        data["date"] = self.session_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data.pop("session_date", None)
        return data

    @classmethod
    def from_storage_dict(cls, data: dict) -> "StudySession":
        if "date" in data and "session_date" not in data:
            data["session_date"] = data.pop("date")
        return cls(**data)
