"""Porta de notificação - interface para envio de alertas ao usuário."""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable


class NotificationPriority(Enum):
    """Níveis de prioridade para notificações."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@runtime_checkable
class INotifier(Protocol):
    """Contrato para adaptadores de notificação.

    Implementações: ntfy.sh (push mobile), notify-send (desktop), som, etc.
    """

    def send(
        self,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        tags: list[str] | None = None,
    ) -> bool:
        """Envia uma notificação. Retorna True se enviou com sucesso."""
        ...

    def is_available(self) -> bool:
        """Verifica se o notificador está disponível."""
        ...
