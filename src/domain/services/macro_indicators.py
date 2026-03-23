"""Indicadores macroeconômicos brasileiros via finbr e python-bcb."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MacroIndicators:
    """Acesso a indicadores do Banco Central do Brasil.

    Utiliza finbr e python-bcb para obter Selic, IPCA, CDI e outros
    indicadores relevantes para planejamento financeiro pessoal.
    Graceful degradation: retorna None se as libs não estiverem disponíveis.
    """

    def __init__(self) -> None:
        self._finbr_available = False
        self._bcb_available = False
        self._check_availability()

    def _check_availability(self) -> None:
        import importlib.util

        self._finbr_available = importlib.util.find_spec("finbr") is not None
        if not self._finbr_available:
            logger.warning("finbr não disponível - indicadores limitados")

        self._bcb_available = importlib.util.find_spec("bcb") is not None
        if not self._bcb_available:
            logger.warning("python-bcb não disponível - indicadores limitados")

    def get_selic(self) -> float | None:
        """Retorna a taxa Selic atual (% a.a.)."""
        if self._finbr_available:
            try:
                import finbr

                selic = finbr.selic()
                if hasattr(selic, "iloc"):
                    return float(selic.iloc[-1])
                return float(selic)
            except Exception as exc:
                logger.error("Falha ao obter Selic via finbr: %s", exc)

        if self._bcb_available:
            try:
                from bcb import sgs

                df = sgs.get({"selic": 432}, last=1)
                return float(df.iloc[-1]["selic"])
            except Exception as exc:
                logger.error("Falha ao obter Selic via python-bcb: %s", exc)

        return None

    def get_ipca(self, months: int = 12) -> float | None:
        """Retorna IPCA acumulado nos últimos N meses (%)."""
        if self._finbr_available:
            try:
                import finbr

                ipca = finbr.ipca()
                if hasattr(ipca, "tail"):
                    recent = ipca.tail(months)
                    accumulated = 1.0
                    for val in recent.values:
                        accumulated *= 1 + float(val) / 100
                    return round((accumulated - 1) * 100, 2)
            except Exception as exc:
                logger.error("Falha ao obter IPCA via finbr: %s", exc)

        return None

    def get_cdi(self) -> float | None:
        """Retorna a taxa CDI atual (% a.a.)."""
        if self._finbr_available:
            try:
                import finbr

                cdi = finbr.cdi()
                if hasattr(cdi, "iloc"):
                    return float(cdi.iloc[-1])
                return float(cdi)
            except Exception as exc:
                logger.error("Falha ao obter CDI via finbr: %s", exc)

        return None

    def project_savings(
        self,
        monthly_deposit: float,
        months: int,
        annual_rate: float | None = None,
    ) -> dict[str, Any]:
        """Projeta economia futura com juros compostos.

        Se annual_rate não for fornecida, usa a Selic atual.
        """
        if annual_rate is None:
            annual_rate = self.get_selic() or 12.25

        monthly_rate = (1 + annual_rate / 100) ** (1 / 12) - 1

        total = 0.0
        for _ in range(months):
            total = (total + monthly_deposit) * (1 + monthly_rate)

        total_deposited = monthly_deposit * months
        total_interest = total - total_deposited

        return {
            "total_projetado": round(total, 2),
            "total_depositado": round(total_deposited, 2),
            "rendimento": round(total_interest, 2),
            "taxa_anual": annual_rate,
            "taxa_mensal": round(monthly_rate * 100, 4),
            "meses": months,
            "depósito_mensal": monthly_deposit,
        }

    def get_summary(self) -> dict[str, Any]:
        """Resumo de todos os indicadores disponíveis."""
        return {
            "selic": self.get_selic(),
            "ipca_12m": self.get_ipca(12),
            "cdi": self.get_cdi(),
            "fonte": "Banco Central do Brasil (BCB)",
            "disponível": self._finbr_available or self._bcb_available,
        }
