"""Event Bus - sistema pub/sub tipado para comunicação desacoplada entre módulos."""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EventBus:
    """Barramento de eventos pub/sub.

    Permite que módulos se comuniquem sem acoplamento direto.
    Quando uma transação é registrada, o módulo financeiro publica
    TransactionCreated; o módulo de nudges escuta e decide se intervém.

    Suporta persistência opcional via SQLite para auditoria.
    """

    def __init__(self, persist_fn: Callable[[str, str, str], None] | None = None) -> None:
        self._listeners: dict[str, list[Callable]] = defaultdict(list)
        self._enabled: bool = True
        self._persist_fn = persist_fn

    def on(self, event_type: str, callback: Callable[[BaseModel], None]) -> None:
        """Registra um listener para um tipo de evento.

        Args:
            event_type: Nome do tipo de evento (ex: 'TransactionCreated').
            callback: Função chamada quando o evento é emitido.
        """
        self._listeners[event_type].append(callback)
        logger.debug("Listener registrado para %s", event_type)

    def off(self, event_type: str, callback: Callable) -> None:
        """Remove um listener específico."""
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(callback)
            except ValueError:
                pass

    def emit(self, event: BaseModel, source: str = "") -> None:
        """Publica um evento para todos os listeners registrados.

        Args:
            event: Instância do evento (Pydantic BaseModel).
            source: Identificador do módulo que emitiu.
        """
        if not self._enabled:
            return

        event_type = type(event).__name__

        if self._persist_fn:
            try:
                self._persist_fn(
                    event_type,
                    event.model_dump_json(),
                    source,
                )
            except Exception as exc:
                logger.error("Falha ao persistir evento %s: %s", event_type, exc)

        listeners = self._listeners.get(event_type, [])
        for callback in listeners:
            try:
                callback(event)
            except Exception as exc:
                logger.error("Erro no handler de %s: %s", event_type, exc)

        logger.debug("Evento %s emitido (%d listeners)", event_type, len(listeners))

    def clear(self, event_type: str | None = None) -> None:
        """Remove listeners. Se event_type=None, remove todos."""
        if event_type:
            self._listeners[event_type] = []
        else:
            self._listeners.clear()

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    @property
    def listener_count(self) -> int:
        return sum(len(v) for v in self._listeners.values())

    def list_events(self) -> list[str]:
        """Lista tipos de eventos com listeners registrados."""
        return list(self._listeners.keys())
