# Controle de Bordo - Índice de Sprints

> Atualizado em: 2026-03-23 (plano de 20 sprints via review.md)
> Total: 20 sprints em 4 semanas, 1 concluída, 19 planejadas

## Status Geral

| Fase | Sprints | Semana | Status |
|------|---------|--------|--------|
| Fundação | S01-S05 | 1 | S01 concluída, S02-S05 planejadas |
| Serviços e Standalone | S06-S10 | 2 | Planejadas |
| Integração Luna | S11-S15 | 3 | Planejadas |
| UI e Polish | S16-S20 | 4 | Planejadas |

## Sprints por Ordem de Execução

### Semana 1 - Fundação (S01-S05)

| # | Sprint | Status | Duração | Entregáveis |
|---|--------|--------|---------|-------------|
| S01 | [Scaffolding e pyproject.toml](planejados/S01_SCAFFOLDING_PYPROJECT.md) | CONCLUIDO | 1 dia | src/bordo/, hatchling, pytest/mypy/ruff |
| S02 | [Domain Entities](planejados/S02_DOMAIN_ENTITIES.md) | PLANEJADO | 1 dia | 6 entidades Pydantic, 9+ eventos tipados |
| S03 | [Ports e Protocols](planejados/S03_PORTS_PROTOCOLS.md) | PLANEJADO | 1 dia | 5 Protocols @runtime_checkable |
| S04 | [Event Bus Tipado](planejados/S04_EVENT_BUS_TIPADO.md) | PLANEJADO | 1 dia | BordoEventBus síncrono, wildcard handler |
| S05 | [SQLite WAL](planejados/S05_SQLITE_WAL.md) | PLANEJADO | 1 dia | SQLiteStore, WAL, user_version, backup |

### Semana 2 - Serviços e Standalone (S06-S10)

| # | Sprint | Status | Duração | Entregáveis |
|---|--------|--------|---------|-------------|
| S06 | [FinancialEngine](planejados/S06_FINANCIAL_ENGINE.md) | PLANEJADO | 2 dias | Motor financeiro, CSV Nubank, OFX |
| S07 | [ImpulseFilter e GoalTracker](planejados/S07_IMPULSE_GOAL_TRACKER.md) | PLANEJADO | 1 dia | Anti-impulso, metas, milestones |
| S08 | [CLI Typer](planejados/S08_CLI_TYPER.md) | PLANEJADO | 1 dia | 10+ comandos, bootstrap standalone |
| S09 | [Config e Bootstrap](planejados/S09_CONFIG_BOOTSTRAP.md) | PLANEJADO | 1 dia | TOML, dual-mode, detect_mode |
| S10 | [JSON Compat](planejados/S10_JSON_COMPAT.md) | PLANEJADO | 1 dia | JsonStore formato life_manager |

### Semana 3 - Integração Luna (S11-S15)

| # | Sprint | Status | Duração | Entregáveis |
|---|--------|--------|---------|-------------|
| S11 | [EventBusBridge](planejados/S11_EVENT_BUS_BRIDGE.md) | PLANEJADO | 2 dias | Bridge bidirecional, EventRegistry |
| S12 | [Plugin Luna](planejados/S12_PLUGIN_LUNA.md) | PLANEJADO | 1 dia | BordoLunaPlugin, module.yaml |
| S13 | [Migração JSON->SQLite](planejados/S13_MIGRACAO_JSON_SQLITE.md) | PLANEJADO | 2 dias | 4 fases, DualWrite, rollback |
| S14 | [Contract Tests](planejados/S14_CONTRACT_TESTS.md) | PLANEJADO | 1 dia | Test base classes, mypy --strict |
| S15 | [Integração E2E](planejados/S15_INTEGRACAO_E2E.md) | PLANEJADO | 1 dia | 5 cenários E2E, graceful degradation |

### Semana 4 - UI e Polish (S16-S20)

| # | Sprint | Status | Duração | Entregáveis |
|---|--------|--------|---------|-------------|
| S16 | [ViewModels](planejados/S16_VIEWMODELS.md) | PLANEJADO | 1 dia | Observable[T], 4 ViewModels |
| S17 | [Widgets Textual](planejados/S17_WIDGETS_TEXTUAL.md) | PLANEJADO | 1 dia | 4 widgets TUI para Luna |
| S18 | [Flet UI](planejados/S18_FLET_UI.md) | PLANEJADO | 2 dias | 4 páginas, tema escuro, responsivo |
| S19 | [Macro e Nudge](planejados/S19_MACRO_NUDGE.md) | PLANEJADO | 1 dia | Selic/IPCA/CDI, 7+ regras nudge |
| S20 | [CI, Docs e Release](planejados/S20_CI_DOCS_RELEASE.md) | PLANEJADO | 2 dias | Pipeline CI, docs, tag v0.1.0 |

## Grafo de Dependências

```
S01 ── S02 ── S06 ── S08 (standalone funcional)
 │      │      │
 │      └──────┤
 │             │
 ├── S03 ── S04 ── S11 ── S12 ── S15
 │      │              │
 │      └── S05 ── S06 │
 │           │     │   │
 │           └── S09   S13
 │                     │
 └── S10 ───────── S13 ── S14
                          │
S06 + S07 ── S16 ── S17
              │
              └── S18

S06 + S04 ── S19

Todas ── S20
```

## Caminho Crítico

**S01 -> S02 -> S03 -> S04 -> S05 -> S06 -> S08** (standalone funcional na Semana 2)

A partir de S08, o Bordo funciona sozinho como CLI. Integração Luna (S11-S15) e UI (S16-S18) são paralelas.

## Sprints Legadas (plano anterior)

Sprints do plano original (S00-S16) foram movidas para [legacy/](planejados/legacy/). As sprints concluídas S00-S03 permanecem em [concluídos/](concluidos/).

| Sprint | Status | Localização |
|--------|--------|-------------|
| S00 Fundação | Concluído | [concluidos/S00_FUNDACAO.md](concluidos/S00_FUNDACAO.md) |
| S01 Finanças Core | Concluído | [concluidos/S01_FINANCAS_CORE.md](concluidos/S01_FINANCAS_CORE.md) |
| S02 Indicadores Macro | Concluído | [concluidos/S02_INDICADORES_MACRO.md](concluidos/S02_INDICADORES_MACRO.md) |
| S03 Motor Anti-Impulso | Concluído | [concluidos/S03_MOTOR_ANTI_IMPULSO.md](concluidos/S03_MOTOR_ANTI_IMPULSO.md) |
| S03.5-S16 (antigos) | Legado | [planejados/legacy/](planejados/legacy/) |

## Relatórios

| Relatório | Fase | Status |
|-----------|------|--------|
| [Fase 0 - Fundação](relatorios/RELATORIO_FASE_0_FUNDACAO.md) | S00-S03 (antigo) | Disponível |
| [Template](relatorios/TEMPLATE_RELATORIO.md) | - | Referência |

*"Planeje o trabalho e trabalhe o plano." - Napoleon Hill*
