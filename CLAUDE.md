# Controle de Bordo - Regras do Projeto

## Modelo Obrigatório

**USAR EXCLUSIVAMENTE Opus 4.6 (claude-opus-4-6).** Nunca delegar tarefas para modelos inferiores (Sonnet, Haiku). Subagentes estão PROIBIDOS - todo trabalho deve ser feito diretamente, sem agentes paralelos.

## Acentuação

**ACENTUAÇÃO PT-BR CORRETA É OBRIGATÓRIA** em TODAS as respostas, código, commits, docs, comentários e strings. Isso inclui: á, é, í, ó, ú, â, ê, ô, ã, õ, à, ç. NUNCA escreva "funcao", "validacao", "descricao" - o correto é "função", "validação", "descrição". Sem exceção.

## Arquitetura

**Hexagonal (Ports & Adapters)**. O domínio (`src/domain/`) NUNCA importa de `src/adapters/`, `src/ui/` ou `src/mobile/`. Comunicação via interfaces em `src/domain/ports/`.

```
domain/          -> Lógica pura, zero dependência externa
  entities/      -> Modelos Pydantic (Transaction, Bill, Goal, Habit, etc)
  services/      -> Regras de negócio (financial_engine, impulse_filter, etc)
  ports/         -> Interfaces (IStorage, INotifier, IAIProvider, IBankImporter)
adapters/        -> Implementações concretas dos ports
  storage/       -> SQLite + WAL
  importers/     -> CSV Nubank, OFX genérico
  notifiers/     -> ntfy.sh, notify-send
  ai/            -> Anthropic API, Ollama
  desktop/       -> /etc/hosts blocker, GNOME gsettings
ui/              -> Interface Flet (desktop + mobile)
events/          -> Event bus pub/sub tipado
mobile/          -> Ponte Android (ADB, Tasker, Shizuku)
cli/             -> Interface Typer
```

## Comandos

```bash
# Testes (SEMPRE E2E unificados, nunca unitários isolados)
pytest tests/e2e/
pytest --cov=src tests/e2e/

# Linting
ruff check src/
ruff format src/

# Tipagem
mypy src/

# Executar UI
flet run src/ui/app.py

# CLI
python -m src.cli.main financas resumo
```

## Convenções

- Python 3.10+, type hints obrigatórios
- Pydantic para validação de dados
- SQLite em modo WAL para persistência
- Logging via `logging` (NUNCA `print()`)
- Paths relativos via `pathlib.Path`
- Acentuação PT-BR correta em TUDO (código, docs, commits, comentários)
- Zero emojis
- Zero menções a IA em commits ou código
- Commits em PT-BR: `tipo: descrição imperativa`
- Licença: GPL-3.0

## Decisões Arquiteturais

1. **Local-first**: SQLite é a fonte da verdade. Zero dependência de cloud
2. **AI-agnostic**: Port `ai_provider.py` abstrai provedores. Trocar = trocar adapter
3. **Luna-ready**: Estrutura domain/ + ports/ será empacotada como módulo Luna no futuro
4. **Graceful degradation**: Funciona sem IA, sem internet, sem celular
5. **Open Finance impossível**: BCB exige autorização institucional. Usar CSV/OFX
6. **Google Fit deprecated**: Usar Health Connect
7. **Indicadores BR**: finbr + python-bcb para Selic, IPCA, CDI

## Git e Branching

```bash
# Branches
main   <- protegida, só aceita PR com CI verde
dev    <- trabalho diário
feature/xxx <- funcionalidades novas
fix/xxx     <- correções

# Fluxo
git checkout dev
git checkout -b feature/minha-feature
# ... desenvolver ...
just ci  # validar ANTES de commitar
git add <arquivos>
git commit -m "feat: descrição imperativa em PT-BR"
git push -u origin feature/minha-feature
# Abrir PR: feature → dev (CI obrigatória)
# Depois: dev → main (Quality Gates obrigatórios)
```

**Regras:**
- NUNCA push direto na main
- NUNCA `--force` sem autorização
- NUNCA `--no-verify` nos hooks
- Commits em PT-BR: `tipo: descrição imperativa`
- Pre-commit valida: anonimidade, acentuação, registry, ruff

## Limites

- 800 linhas por arquivo (exceções: config, testes)
- Se ultrapassar: extrair para módulos separados
