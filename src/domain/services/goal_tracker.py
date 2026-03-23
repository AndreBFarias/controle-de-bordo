"""Tracker de metas - acompanhamento de progresso com projeções."""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from src.domain.entities.goal import Goal, GoalStatus, GoalType
from src.domain.ports.storage import IStorage

logger = logging.getLogger(__name__)


class GoalTracker:
    """Gerencia metas pessoais com cálculo de progresso e projeções."""

    def __init__(self, storage: IStorage) -> None:
        self._storage = storage

    def create_goal(
        self,
        name: str,
        target_value: float,
        unit: str = "%",
        goal_type: str | GoalType = "pessoal",
        deadline: date | None = None,
        **kwargs: Any,
    ) -> Goal:
        """Cria uma nova meta."""
        goal = Goal(
            name=name,
            target_value=target_value,
            unit=unit,
            type=GoalType(goal_type) if isinstance(goal_type, str) else goal_type,
            deadline=deadline,
            **kwargs,
        )
        data = goal.to_storage_dict()
        data.pop("id", None)
        goal_id = self._storage.insert("goals", data)
        goal.id = goal_id
        logger.info("Meta criada: %s (alvo: %.2f %s)", name, target_value, unit)
        return goal

    def update_progress(self, goal_id: int, new_value: float) -> Goal | None:
        """Atualiza o progresso de uma meta."""
        row = self._storage.get_by_id("goals", goal_id)
        if not row:
            return None

        goal = Goal.from_storage_dict(row)
        goal.update_progress(new_value)

        self._storage.update(
            "goals",
            goal_id,
            {
                "current_value": goal.current_value,
                "status": goal.status.value,
                "updated_at": datetime.now().isoformat(),
            },
        )

        logger.info("Meta '%s' atualizada: %.1f%%", goal.name, goal.progress_percent)
        return goal

    def increment_progress(self, goal_id: int, amount: float) -> Goal | None:
        """Incrementa o progresso de uma meta."""
        row = self._storage.get_by_id("goals", goal_id)
        if not row:
            return None

        goal = Goal.from_storage_dict(row)
        goal.increment(amount)

        self._storage.update(
            "goals",
            goal_id,
            {
                "current_value": goal.current_value,
                "status": goal.status.value,
                "updated_at": datetime.now().isoformat(),
            },
        )
        return goal

    def get_active_goals(self) -> list[Goal]:
        """Retorna todas as metas ativas."""
        rows = self._storage.query("goals", filters={"status": GoalStatus.ACTIVE.value})
        return [Goal.from_storage_dict(r) for r in rows]

    def get_goal_summary(self) -> list[dict[str, Any]]:
        """Resumo de todas as metas ativas com projeções."""
        goals = self.get_active_goals()
        summaries = []

        for goal in goals:
            summary: dict[str, Any] = {
                "id": goal.id,
                "nome": goal.name,
                "tipo": goal.type.value,
                "progresso": f"{goal.progress_percent:.1f}%",
                "atual": f"{goal.current_value:.2f} {goal.unit}",
                "alvo": f"{goal.target_value:.2f} {goal.unit}",
                "restante": f"{goal.remaining:.2f} {goal.unit}",
            }

            if goal.deadline:
                summary["prazo"] = goal.deadline.isoformat()
                summary["dias_restantes"] = goal.days_remaining
                rate = goal.daily_rate_needed
                if rate is not None:
                    summary["ritmo_diário"] = f"{rate:.2f} {goal.unit}/dia"

            summaries.append(summary)

        return summaries
