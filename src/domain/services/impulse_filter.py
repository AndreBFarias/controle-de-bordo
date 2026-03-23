"""Motor de fricção anti-impulso - economia comportamental aplicada."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any

from src.domain.entities.transaction import Transaction, TransactionCategory
from src.domain.ports.storage import IStorage

logger = logging.getLogger(__name__)


class FrictionLevel(str, Enum):
    """Níveis de intervenção contra compras impulsivas."""

    NONE = "nenhuma"
    SOFT = "suave"
    MEDIUM = "média"
    HARD = "forte"
    BLOCK = "bloqueio"


IMPULSE_CATEGORIES: set[TransactionCategory] = {
    TransactionCategory.LAZER,
    TransactionCategory.TECNOLOGIA,
    TransactionCategory.VESTUARIO,
    TransactionCategory.BELEZA,
}

ESSENTIAL_CATEGORIES: set[TransactionCategory] = {
    TransactionCategory.MORADIA,
    TransactionCategory.ALIMENTACAO,
    TransactionCategory.SAUDE,
    TransactionCategory.TRANSPORTE,
    TransactionCategory.EDUCACAO,
}


@dataclass
class ImpulseAnalysis:
    """Resultado da análise de uma potencial compra impulsiva."""

    friction_level: FrictionLevel
    is_impulse: bool
    reasons: list[str]
    goal_impact: str
    suggestion: str
    delay_hours: int = 0


class ImpulseFilter:
    """Filtro comportamental contra compras por impulso.

    Baseado em economia comportamental (Thaler & Sunstein):
    - Regra das 24 horas para compras não essenciais
    - Análise de necessidade vs. desejo
    - Enquadramento de perda (aversão à perda)
    - Fricção digital deliberada
    """

    def __init__(
        self,
        storage: IStorage,
        monthly_budget: float = 0,
        impulse_threshold: float = 50.0,
    ) -> None:
        self._storage = storage
        self._monthly_budget = monthly_budget
        self._impulse_threshold = impulse_threshold

    def analyze(self, transaction: Transaction) -> ImpulseAnalysis:
        """Analisa uma transação e determina o nível de fricção necessário."""
        reasons: list[str] = []
        friction = FrictionLevel.NONE
        delay = 0

        if transaction.category in ESSENTIAL_CATEGORIES:
            return ImpulseAnalysis(
                friction_level=FrictionLevel.NONE,
                is_impulse=False,
                reasons=["Categoria essencial"],
                goal_impact="",
                suggestion="",
            )

        if transaction.category in IMPULSE_CATEGORIES:
            reasons.append(f"Categoria de risco: {transaction.category.value}")
            friction = FrictionLevel.SOFT

        amount = abs(transaction.amount)
        if amount >= self._impulse_threshold:
            reasons.append(f"Valor acima do limiar de impulso (R$ {self._impulse_threshold:.2f})")
            friction = FrictionLevel.MEDIUM
            delay = 24

        monthly_spent = self._get_monthly_spent_in_category(transaction.category)
        if self._monthly_budget > 0:
            budget_used = (monthly_spent + amount) / self._monthly_budget
            if budget_used > 0.8:
                reasons.append(f"Orçamento mensal em {budget_used:.0%}")
                friction = FrictionLevel.HARD
                delay = 48

        goal_impact = self._calculate_goal_impact(amount)

        suggestion = self._generate_suggestion(friction, amount, goal_impact)

        is_impulse = friction.value not in (FrictionLevel.NONE.value, FrictionLevel.SOFT.value)

        return ImpulseAnalysis(
            friction_level=friction,
            is_impulse=is_impulse,
            reasons=reasons,
            goal_impact=goal_impact,
            suggestion=suggestion,
            delay_hours=delay,
        )

    def _get_monthly_spent_in_category(self, category: TransactionCategory) -> float:
        """Calcula total gasto na categoria no mês atual."""
        first_day = date.today().replace(day=1)
        rows = self._storage.execute_sql(
            """
            SELECT COALESCE(SUM(ABS(amount)), 0) as total
            FROM transactions
            WHERE category = ? AND type = 'despesa' AND date >= ?
            """,
            (category.value, first_day.isoformat()),
        )
        return float(rows[0]["total"]) if rows else 0.0

    def _calculate_goal_impact(self, amount: float) -> str:
        """Calcula impacto de um gasto nas metas financeiras ativas."""
        goals = self._storage.query("goals", filters={"type": "financeira", "status": "ativa"})
        if not goals:
            return ""

        impacts = []
        for goal in goals:
            remaining = goal["target_value"] - goal["current_value"]
            if remaining > 0:
                impact_percent = (amount / remaining) * 100
                if impact_percent >= 1:
                    impacts.append(f"{goal['name']}: -{impact_percent:.1f}% do restante")

        return "; ".join(impacts) if impacts else ""

    def _generate_suggestion(self, friction: FrictionLevel, amount: float, goal_impact: str) -> str:
        """Gera sugestão personalizada baseada no nível de fricção."""
        if friction == FrictionLevel.NONE:
            return ""

        if friction == FrictionLevel.SOFT:
            return "Considere se este gasto está alinhado com suas metas."

        if friction == FrictionLevel.MEDIUM:
            suggestion = f"Espere 24h antes de decidir. R$ {amount:.2f} investidos renderiam mais."
            if goal_impact:
                suggestion += f" Impacto nas metas: {goal_impact}"
            return suggestion

        if friction in (FrictionLevel.HARD, FrictionLevel.BLOCK):
            return (
                f"Orçamento crítico. Este gasto de R$ {amount:.2f} compromete suas metas. "
                f"Descreva em 3 frases por que é necessário AGORA."
            )

        return ""

    def get_monthly_impulse_summary(self) -> dict[str, Any]:
        """Resumo de compras impulsivas do mês."""
        first_day = date.today().replace(day=1)
        rows = self._storage.execute_sql(
            """
            SELECT COUNT(*) as count, COALESCE(SUM(ABS(amount)), 0) as total
            FROM transactions
            WHERE is_impulse = 1 AND date >= ?
            """,
            (first_day.isoformat(),),
        )
        row = rows[0] if rows else {"count": 0, "total": 0}
        return {
            "compras_impulso": row["count"],
            "total_impulso": float(row["total"]),
            "economia_potencial": float(row["total"]),
        }
