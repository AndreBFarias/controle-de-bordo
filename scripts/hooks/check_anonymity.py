#!/usr/bin/env python3
"""Hook pre-commit: bloqueia menções a IA em código e documentação.

Verifica arquivos staged e rejeita commit se encontrar referências
a ferramentas de IA (Claude, GPT, Copilot, Anthropic, OpenAI, etc).
Exceções: variáveis de ambiente, configs de API, este próprio arquivo.
"""

import re
import sys
from pathlib import Path

FORBIDDEN_PATTERNS = [
    r"\bclaude\b",
    r"\bgpt[-\s]?\d",
    r"\bcopilot\b",
    r"\bgemini\b",
    r"\banthropic\b",
    r"\bopenai\b",
    r"\bchatgpt\b",
    r"\bco-?authored[- ]by.*claude\b",
    r"\bco-?authored[- ]by.*anthropic\b",
]

ALLOWED_CONTEXTS = [
    r"api_key",
    r"API_KEY",
    r"provider",
    r"ANTHROPIC_API_KEY",
    r"OPENAI_API_KEY",
    r"anthropic_model",
    r"claude_provider",
    r"ollama_provider",
    r"claude-opus",
    r"claude-sonnet",
    r"claude-haiku",
]

EXCLUDED_FILES = {
    "scripts/hooks/check_anonymity.py",
    "scripts/hooks/check_registry.py",
    ".env.example",
    ".env",
    ".claude/settings.json",
    "CLAUDE.md",
    "docs/INTEGRACAO_LUNA.md",
    "docs/ARQUITETURA.md",
    "docs/CONTRIBUINDO.md",
    "docs/FINANCAS.md",
    "README.md",
    "REGISTRY.csv",
    "pyproject.toml",
    "requirements.txt",
    "requirements-ci.txt",
    "configs/default.toml",
    ".pre-commit-config.yaml",
    "src/domain/ports/ai_provider.py",
    "src/adapters/ai/__init__.py",
}

EXCLUDED_DIRS = {
    "sprints/",
    ".claude/",
}

EXCLUDED_PATTERNS = [
    "Arquitetura Modular",
    "Planejamento de Vida",
    "de Vida com IA",
]

EXCLUDED_EXTENSIONS = {".lock", ".db", ".pyc", ".png", ".jpg", ".gif"}


def check_file(filepath: str) -> list[str]:
    """Verifica um arquivo por menções proibidas."""
    path = Path(filepath)

    if path.suffix in EXCLUDED_EXTENSIONS:
        return []

    rel = str(path)
    if any(rel.endswith(exc) or rel == exc for exc in EXCLUDED_FILES):
        return []

    if any(rel.startswith(d) for d in EXCLUDED_DIRS):
        return []

    if any(p in rel for p in EXCLUDED_PATTERNS):
        return []

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    violations = []
    for line_num, line in enumerate(content.splitlines(), 1):
        line_lower = line.lower()

        if any(re.search(ctx, line, re.IGNORECASE) for ctx in ALLOWED_CONTEXTS):
            continue

        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, line_lower):
                violations.append(f"  {filepath}:{line_num}: {line.strip()[:80]}")
                break

    return violations


def main() -> int:
    files = sys.argv[1:]
    if not files:
        return 0

    all_violations = []
    for f in files:
        violations = check_file(f)
        all_violations.extend(violations)

    if all_violations:
        print("BLOQUEADO: Menções a IA encontradas:")
        for v in all_violations:
            print(v)
        print("\nRemova as referências antes de commitar.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
