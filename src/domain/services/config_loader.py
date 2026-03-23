"""Carregamento e aplicação de configuração TOML."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("configs/default.toml")
USER_CONFIG_PATH = Path("configs/user.toml")


def _load_toml(path: Path) -> dict[str, Any]:
    """Carrega arquivo TOML com fallback para Python < 3.11."""
    if not path.exists():
        return {}

    try:
        if sys.version_info >= (3, 11):
            import tomllib

            with open(path, "rb") as f:
                return tomllib.load(f)
        else:
            import tomli

            with open(path, "rb") as f:
                return tomli.load(f)
    except Exception as exc:
        logger.error("Falha ao carregar %s: %s", path, exc)
        return {}


def load_config(
    default_path: Path | None = None,
    user_path: Path | None = None,
) -> dict[str, Any]:
    """Carrega configuração com merge: default <- user (user sobrescreve default).

    Args:
        default_path: Caminho para default.toml (padrão: configs/default.toml)
        user_path: Caminho para user.toml (padrão: configs/user.toml)

    Returns:
        Dicionário de configuração mesclado.
    """
    default_path = default_path or DEFAULT_CONFIG_PATH
    user_path = user_path or USER_CONFIG_PATH

    config = _load_toml(default_path)
    user_config = _load_toml(user_path)

    _deep_merge(config, user_config)

    logger.info("Configuração carregada (default: %s, user: %s)", default_path.exists(), user_path.exists())
    return config


def _deep_merge(base: dict, override: dict) -> None:
    """Merge recursivo: override sobrescreve base, preservando chaves ausentes."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def get_financial_config(config: dict[str, Any]) -> dict[str, Any]:
    """Extrai configuração financeira do config global."""
    return config.get("financas", {})


def get_impulse_threshold(config: dict[str, Any]) -> float:
    """Retorna limiar de impulso configurado."""
    return float(config.get("financas", {}).get("impulse_threshold", 50.0))


def get_monthly_budget(config: dict[str, Any]) -> float:
    """Retorna orçamento mensal configurado."""
    return float(config.get("financas", {}).get("monthly_budget", 0.0))


def get_bill_reminder_days(config: dict[str, Any]) -> int:
    """Retorna dias de antecedência para lembrete de contas."""
    return int(config.get("financas", {}).get("bill_reminder_days", 3))
