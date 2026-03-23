# Sprint S00: Fundação

## Resumo Executivo
> Criação da infraestrutura base do projeto: repositório, arquitetura hexagonal, persistência SQLite e event bus.

## Status: CONCLUÍDO

## Data: 2026-03-22
## Duração real: Sessão única (~3h, junto com S01-S03)
## Iterações: 1

## Metas e KPIs

| KPI | Alvo | Resultado | Status |
|-----|------|-----------|--------|
| Estrutura hexagonal completa | 5 camadas | 5 camadas | Atingido |
| Ports definidos | 4 | 4 | Atingido |
| SQLite com WAL | 1 adapter | 1 adapter | Atingido |
| Event bus funcional | 1 | 1 (14 tipos de evento) | Superado |
| Testes E2E passando | 5+ | 11 | Superado |
| Documentação base | 3 docs | 6 docs + CLAUDE.md | Superado |

## Entregáveis

- [x] Estrutura de diretórios (domain/, adapters/, ui/, events/, mobile/, cli/)
- [x] pyproject.toml com dependências e tooling (ruff, mypy, pytest)
- [x] CLAUDE.md com regras do projeto
- [x] .gitignore, .env.example, LICENSE (GPL-3.0)
- [x] 4 ports: IStorage, INotifier, IAIProvider, IBankImporter
- [x] SQLiteAdapter com WAL mode, 7 tabelas, índices
- [x] EventBus pub/sub tipado com Pydantic
- [x] 14 tipos de evento (TransactionCreated, BillDue, etc)
- [x] install.sh idempotente
- [x] uninstall.sh com confirmações
- [x] .desktop para integração Linux
- [x] REGISTRY.csv com hook bloqueante
- [x] Hooks: bloqueio de agentes, verificação de acentuação, registro obrigatório

## Arquivos Criados

| Arquivo | Linhas | Camada |
|---------|--------|--------|
| src/domain/ports/storage.py | 52 | domínio |
| src/domain/ports/notifier.py | 37 | domínio |
| src/domain/ports/ai_provider.py | 35 | domínio |
| src/domain/ports/bank_importer.py | 48 | domínio |
| src/adapters/storage/sqlite_adapter.py | 286 | infra |
| src/events/bus.py | 99 | orquestração |
| src/events/events.py | 112 | orquestração |
| install.sh | 282 | infra |
| uninstall.sh | 192 | infra |
| REGISTRY.csv | ~90 | infra |
| .claude/hooks/check_registry.sh | 59 | infra |
| .claude/hooks/check_accentuation.sh | 92 | infra |

## Critérios de Aceite

1. [x] `python -c "from src.adapters.storage.sqlite_adapter import SQLiteAdapter"` funciona
2. [x] SQLite cria tabelas e opera em modo WAL
3. [x] Event bus emite e recebe eventos tipados
4. [x] install.sh executa sem erros
5. [x] Hooks bloqueiam agentes e verificam acentuação

## Notas Técnicas

- Removido `from __future__ import annotations` dos modelos Pydantic por incompatibilidade com campos chamados `date`
- Usado `Optional[X]` ao invés de `X | None` nos modelos Pydantic
- Forward references em classmethods usam strings (`-> "ClassName"`)

*"Dê-me uma alavanca longa o suficiente e um ponto de apoio, e moverei o mundo." - Arquimedes*
