"""Motor de nudges comportamentais - intervenções proativas baseadas em padrões."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Any

from src.domain.entities.habit import Habit
from src.domain.ports.storage import IStorage

logger = logging.getLogger(__name__)


class NudgeType:
    """Tipos de nudge disponíveis."""

    BILL_REMINDER = "lembrete_conta"
    HABIT_BROKEN = "hábito_quebrado"
    IMPULSE_WARNING = "alerta_impulso"
    GOAL_MILESTONE = "marco_meta"
    STUDY_REMINDER = "lembrete_estudo"
    HEALTH_CHECK = "verificação_saúde"
    SAVINGS_UPDATE = "atualização_economia"
    POSITIVE_REINFORCEMENT = "reforço_positivo"


class NudgeEngine:
    """Gera intervenções comportamentais baseadas no estado atual do usuário.

    Analisa dados financeiros, hábitos, saúde e metas para decidir
    qual nudge enviar e quando. Prioriza nudges positivos sobre negativos.
    """

    def __init__(self, storage: IStorage) -> None:
        self._storage = storage

    def check_all(self) -> list[dict[str, Any]]:
        """Executa todas as verificações e retorna nudges pendentes."""
        nudges: list[dict[str, Any]] = []

        nudges.extend(self._check_bills())
        nudges.extend(self._check_habits())
        nudges.extend(self._check_goals())
        nudges.extend(self._check_health())
        nudges.extend(self._check_study())

        nudges.sort(key=lambda n: {"urgente": 0, "alta": 1, "normal": 2, "baixa": 3}.get(n["prioridade"], 99))

        return nudges

    def _check_bills(self) -> list[dict[str, Any]]:
        """Verifica contas próximas do vencimento ou atrasadas."""
        nudges = []
        today = date.today()
        limit = today + timedelta(days=7)

        overdue = self._storage.execute_sql(
            "SELECT * FROM bills WHERE status = 'pendente' AND due_date < ?",
            (today.isoformat(),),
        )
        for bill in overdue:
            days = (today - date.fromisoformat(bill["due_date"])).days
            nudges.append(
                {
                    "tipo": NudgeType.BILL_REMINDER,
                    "prioridade": "urgente",
                    "título": f"Conta atrasada: {bill['name']}",
                    "mensagem": f"R$ {bill['amount']:.2f} venceu há {days} dia(s)",
                    "dados": bill,
                }
            )

        upcoming = self._storage.execute_sql(
            "SELECT * FROM bills WHERE status = 'pendente' AND due_date BETWEEN ? AND ?",
            (today.isoformat(), limit.isoformat()),
        )
        for bill in upcoming:
            days = (date.fromisoformat(bill["due_date"]) - today).days
            nudges.append(
                {
                    "tipo": NudgeType.BILL_REMINDER,
                    "prioridade": "alta" if days <= 2 else "normal",
                    "título": f"Conta próxima: {bill['name']}",
                    "mensagem": f"R$ {bill['amount']:.2f} vence em {days} dia(s)",
                    "dados": bill,
                }
            )

        return nudges

    def _check_habits(self) -> list[dict[str, Any]]:
        """Verifica hábitos com streak em risco ou conquistas."""
        nudges = []
        habits = self._storage.query("habits", filters={"is_active": 1})
        for habit_data in habits:
            habit = Habit.from_storage_dict(habit_data)

            if habit.streak_broken and habit.current_streak > 0:
                nudges.append(
                    {
                        "tipo": NudgeType.HABIT_BROKEN,
                        "prioridade": "alta",
                        "título": f"Streak em risco: {habit.name}",
                        "mensagem": f"Você tinha {habit.current_streak} dias consecutivos!",
                        "dados": habit_data,
                    }
                )

            if not habit.completed_today and habit.current_streak >= 7:
                nudges.append(
                    {
                        "tipo": NudgeType.HABIT_BROKEN,
                        "prioridade": "normal",
                        "título": f"Continue o streak: {habit.name}",
                        "mensagem": f"{habit.current_streak} dias consecutivos - não quebre agora!",
                        "dados": habit_data,
                    }
                )

            if habit.current_streak > 0 and habit.current_streak % 7 == 0 and habit.completed_today:
                nudges.append(
                    {
                        "tipo": NudgeType.POSITIVE_REINFORCEMENT,
                        "prioridade": "baixa",
                        "título": f"Parabéns! {habit.name}",
                        "mensagem": f"{habit.current_streak} dias consecutivos! Continue assim.",
                        "dados": habit_data,
                    }
                )

        return nudges

    def _check_goals(self) -> list[dict[str, Any]]:
        """Verifica marcos de metas atingidos."""
        nudges = []
        goals = self._storage.query("goals", filters={"status": "ativa"})

        for goal in goals:
            progress = 0.0
            if goal["target_value"] > 0:
                progress = (goal["current_value"] / goal["target_value"]) * 100

            milestones = [25, 50, 75, 90, 100]
            for milestone in milestones:
                prev_value = goal["target_value"] * (milestone - 5) / 100
                if (
                    goal["current_value"] >= goal["target_value"] * milestone / 100
                    and prev_value < goal["current_value"]
                ):
                    if milestone == 100:
                        nudges.append(
                            {
                                "tipo": NudgeType.GOAL_MILESTONE,
                                "prioridade": "normal",
                                "título": f"Meta concluída: {goal['name']}",
                                "mensagem": f"Você atingiu {goal['target_value']:.0f} {goal['unit']}!",
                                "dados": goal,
                            }
                        )
                    break

            if goal.get("deadline"):
                deadline = date.fromisoformat(goal["deadline"])
                days_left = (deadline - date.today()).days
                if 0 < days_left <= 7 and progress < 90:
                    nudges.append(
                        {
                            "tipo": NudgeType.GOAL_MILESTONE,
                            "prioridade": "alta",
                            "título": f"Prazo próximo: {goal['name']}",
                            "mensagem": f"{days_left} dias restantes, progresso em {progress:.0f}%",
                            "dados": goal,
                        }
                    )

        return nudges

    def _check_health(self) -> list[dict[str, Any]]:
        """Verifica métricas de saúde pendentes."""
        nudges = []
        today = date.today().isoformat()

        water_count = self._storage.count(
            "health_records",
            {
                "record_type": "hidratação",
                "date": today,
            },
        )

        if water_count == 0:
            hour = datetime.now().hour
            if hour >= 10:
                nudges.append(
                    {
                        "tipo": NudgeType.HEALTH_CHECK,
                        "prioridade": "normal",
                        "título": "Hidratação",
                        "mensagem": "Nenhum registro de água hoje. Beba água!",
                        "dados": {"copos_hoje": 0},
                    }
                )

        return nudges

    def _check_study(self) -> list[dict[str, Any]]:
        """Verifica se houve sessão de estudo recente."""
        nudges = []
        two_days_ago = (date.today() - timedelta(days=2)).isoformat()

        recent = self._storage.execute_sql(
            "SELECT COUNT(*) as cnt FROM study_sessions WHERE date >= ?",
            (two_days_ago,),
        )

        if recent and recent[0]["cnt"] == 0:
            nudges.append(
                {
                    "tipo": NudgeType.STUDY_REMINDER,
                    "prioridade": "normal",
                    "título": "Estudos parados",
                    "mensagem": "Nenhuma sessão de estudo nos últimos 2 dias.",
                    "dados": {},
                }
            )

        return nudges
