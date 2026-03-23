#!/usr/bin/env python3
"""Hook pre-commit: verifica se arquivos novos estão no REGISTRY.csv.

Bloqueia commits que adicionem arquivos não registrados.
Exceções: .venv/, .git/, __pycache__/, data/, .flet/, .pytest_cache/
"""

import csv
import sys
from pathlib import Path

REGISTRY_PATH = Path("REGISTRY.csv")

IGNORED_PREFIXES = (
    ".venv/",
    ".git/",
    "__pycache__/",
    "data/",
    ".flet/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".mypy_cache/",
    ".claude/plans/",
)

IGNORED_SUFFIXES = (".pyc",)


def load_registry() -> set[str]:
    """Carrega caminhos do REGISTRY.csv."""
    if not REGISTRY_PATH.exists():
        return set()

    paths = set()
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            caminho = row.get("caminho", "").strip()
            if caminho:
                paths.add(caminho)
    return paths


def main() -> int:
    files = sys.argv[1:]
    if not files:
        return 0

    registry = load_registry()
    violations = []

    for filepath in files:
        if filepath == "REGISTRY.csv":
            continue

        if any(filepath.startswith(p) for p in IGNORED_PREFIXES):
            continue

        if any(filepath.endswith(s) for s in IGNORED_SUFFIXES):
            continue

        if filepath not in registry:
            violations.append(f"  {filepath}")

    if violations:
        print("BLOQUEADO: Arquivos não registrados no REGISTRY.csv:")
        for v in violations:
            print(v)
        print("\nAdicione as entradas no REGISTRY.csv antes de commitar.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
