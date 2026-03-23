"""Porta de IA - interface para provedores de inteligência artificial."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IAIProvider(Protocol):
    """Contrato para adaptadores de IA.

    Abstrai a diferença entre provedores cloud (Anthropic API) e locais (Ollama).
    O domínio pede análise/geração de texto sem saber quem processa.
    """

    def analyze(self, prompt: str, context: str | None = None) -> str:
        """Envia um prompt e retorna a resposta do modelo.

        Args:
            prompt: Instrução principal.
            context: Dados contextuais (extrato bancário, métricas, etc).

        Returns:
            Texto gerado pelo modelo.
        """
        ...

    def is_available(self) -> bool:
        """Verifica se o provedor está acessível."""
        ...

    @property
    def provider_name(self) -> str:
        """Nome do provedor (para logging)."""
        ...
