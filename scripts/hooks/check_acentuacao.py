#!/usr/bin/env python3
"""Hook pre-commit: verifica acentuação PT-BR em arquivos Python e Markdown.

Detecta palavras comuns escritas sem acento e bloqueia o commit.
Busca case-sensitive (só detecta a versão sem acento).
"""

import re
import sys
from pathlib import Path

WORDS: dict[str, str] = {
    "funcao": "função",
    "funcoes": "funções",
    "validacao": "validação",
    "validacoes": "validações",
    "descricao": "descrição",
    "descricoes": "descrições",
    "comunicacao": "comunicação",
    "configuracao": "configuração",
    "configuracoes": "configurações",
    "informacao": "informação",
    "informacoes": "informações",
    "operacao": "operação",
    "operacoes": "operações",
    "transacao": "transação",
    "transacoes": "transações",
    "notificacao": "notificação",
    "notificacoes": "notificações",
    "integracao": "integração",
    "aplicacao": "aplicação",
    "conexao": "conexão",
    "excecao": "exceção",
    "excecoes": "exceções",
    "autorizacao": "autorização",
    "atualizacao": "atualização",
    "execucao": "execução",
    "versao": "versão",
    "padrao": "padrão",
    "padroes": "padrões",
    "condicao": "condição",
    "condicoes": "condições",
    "solucao": "solução",
    "frequencia": "frequência",
    "persistencia": "persistência",
    "referencia": "referência",
    "experiencia": "experiência",
    "dependencia": "dependência",
    "sequencia": "sequência",
    "projecao": "projeção",
    "refeicao": "refeição",
    "refeicoes": "refeições",
    "medicacao": "medicação",
    "hidratacao": "hidratação",
    "natacao": "natação",
    "educacao": "educação",
    "saude": "saúde",
    "unico": "único",
    "unica": "única",
    "necessario": "necessário",
    "necessaria": "necessária",
    "disponivel": "disponível",
    "impossivel": "impossível",
    "possivel": "possível",
}

ALLOWED_EXTENSIONS = {".py", ".md", ".toml", ".yaml", ".yml", ".txt", ".sh"}


def check_file(filepath: str) -> list[str]:
    """Verifica acentuação em um arquivo."""
    path = Path(filepath)

    if path.suffix not in ALLOWED_EXTENSIONS:
        return []

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    violations = []
    for line_num, line in enumerate(content.splitlines(), 1):
        for wrong, correct in WORDS.items():
            if re.search(rf"\b{wrong}\b", line):
                violations.append(f"  {filepath}:{line_num}: '{wrong}' -> '{correct}'")

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
        print("BLOQUEADO: Acentuação PT-BR incorreta:")
        for v in all_violations:
            print(v)
        print("\nCorrija a acentuação antes de commitar.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
