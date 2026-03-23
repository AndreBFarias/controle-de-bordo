# Controle de Bordo - Roadmap de Produto

> Visão estratégica e cronograma macro do projeto.
> Versão: 0.1.0 | Data: 2026-03-23 | Plano: review.md (20 sprints)

## Visão do Produto

Ser o primeiro Life Operating System open source maduro em Python, focado no contexto brasileiro, com gestão financeira integrada a hábitos, saúde e automação de dispositivos. Local-first, gratuito, sem dependência de cloud. Funciona standalone e como módulo Luna.

## Público-Alvo

- Desenvolvedores brasileiros que querem controle total sobre seus dados
- Casais com rotina intensa que precisam de automação de decisões
- Pessoas que querem disciplina financeira automatizada (anti-impulso)
- Comunidade open source brasileira

## Arquitetura-Alvo

O Bordo é uma **biblioteca Python independente** que expõe um `plugin.py` opcional. A Luna consome via entry points. Nunca o contrário.

```
src/bordo/
  domain/           -> Lógica pura, zero dependência externa
    entities.py     -> 6 entidades Pydantic v2
    events.py       -> Eventos tipados BaseModel
    services.py     -> FinancialEngine, GoalTracker, ImpulseFilter, NudgeEngine
    ports.py        -> Protocols (IStorage, INotifier, IEventBus)
  adapters/         -> Implementações concretas
    sqlite_store.py -> SQLite + WAL
    json_store.py   -> Compat life_manager Luna
    luna_bridge.py  -> EventBusBridge bidirecional
    flet_ui/        -> Interface Flet
  migrations/       -> JSON -> SQLite faseada
```

## Fases do Projeto (4 semanas)

### Semana 1: Fundação (S01-S05)

**Objetivo**: Pacote instalável com domínio tipado, event bus e persistência SQLite.

| Sprint | Entregável | Status |
|--------|-----------|--------|
| S01 | Scaffolding, hatchling, src/bordo/ | Concluído |
| S02 | 6 entidades Pydantic + eventos tipados | Planejado |
| S03 | 5 Protocols @runtime_checkable | Planejado |
| S04 | BordoEventBus síncrono | Planejado |
| S05 | SQLiteStore com WAL e backup | Planejado |

### Semana 2: Serviços e Standalone (S06-S10)

**Objetivo**: Bordo funcional como CLI standalone com motor financeiro e anti-impulso.

| Sprint | Entregável | Status |
|--------|-----------|--------|
| S06 | FinancialEngine + CSV Nubank + OFX | Planejado |
| S07 | ImpulseFilter + GoalTracker | Planejado |
| S08 | CLI Typer com 10+ comandos | Planejado |
| S09 | Config TOML dual-mode | Planejado |
| S10 | JsonStore compatível life_manager | Planejado |

**Marco**: `bordo import nubank.csv && bordo balance` funciona.

### Semana 3: Integração Luna (S11-S15)

**Objetivo**: Bordo como módulo Luna via entry points, com migração de dados.

| Sprint | Entregável | Status |
|--------|-----------|--------|
| S11 | EventBusBridge bidirecional | Planejado |
| S12 | BordoLunaPlugin + module.yaml | Planejado |
| S13 | Migração JSON->SQLite em 4 fases | Planejado |
| S14 | Contract tests + mypy --strict | Planejado |
| S15 | 5 cenários E2E de integração | Planejado |

**Marco**: `pip install controle-de-bordo[luna]` e Luna descobre o Bordo automaticamente.

### Semana 4: UI e Polish (S16-S20)

**Objetivo**: Interface visual, indicadores macro e release v0.1.0.

| Sprint | Entregável | Status |
|--------|-----------|--------|
| S16 | Observable[T] + 4 ViewModels | Planejado |
| S17 | 4 widgets Textual para Luna | Planejado |
| S18 | 4 páginas Flet standalone | Planejado |
| S19 | MacroIndicators + NudgeEngine | Planejado |
| S20 | CI, docs, limpeza, tag v0.1.0 | Planejado |

**Marco**: `bordo ui` abre dashboard Flet com dados reais.

## Métricas de Sucesso

| Métrica | Semana 1 | Semana 2 | Semana 3 | Semana 4 |
|---------|----------|----------|----------|----------|
| Arquivos Python | ~25 | ~40 | ~55 | ~70 |
| Testes | 0 | ~25 | ~45 | ~65 |
| Cobertura (%) | - | 60% | 75% | 80%+ |
| Entidades | 6 | 6 | 6 | 6 |
| Protocols | 5 | 5 | 5 | 5 |
| Plataformas | Pacote | CLI | CLI+Luna | CLI+Luna+Flet |

## Riscos e Mitigações

| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|-----------|
| Scope creep (Android, CRDT, etc.) | Alta | Alto | Pós-v0.1.0 estritamente |
| life_manager mais acoplado que esperado | Média | Médio | JsonStore como ponte (S10) |
| Flet pré-1.0 com API instável | Média | Médio | Código isolado em adapters/flet_ui/ |
| Complexidade do EventBusBridge | Média | Alto | 100% cobertura, guard reentrância |
| mypy --strict revelar muitos erros | Baixa | Baixo | Habilitar gradualmente (S14) |

## Decisões Técnicas Fundamentais

| Decisão | Motivo |
|---------|--------|
| Hatchling sobre setuptools | PEP 660 nativo, build hooks, configuração limpa |
| Protocols sobre ABCs | Structural subtyping sem herança forçada |
| user_version sobre Alembic | Projeto pessoal com SQLite, Alembic é overkill |
| Observable caseiro sobre RxPY | 30 linhas, zero dependências |
| Prefixo "bordo." em eventos | Previne colisão com 130+ eventos Luna |

## Pós-v0.1.0

Features adiadas intencionalmente para após o release:
- Integração Android (Shizuku, Tasker)
- Sync de casal (CRDTs, Syncthing)
- Health Connect
- Bloqueio desktop (/etc/hosts, GNOME)
- IA conversacional (Anthropic API, Ollama)
- Orçamento inteligente (baldes)
- App mobile (Flet APK)

## Diferencial Competitivo

| Característica | Controle de Bordo | Apps de mercado |
|----------------|-------------------|-----------------|
| Código | Open source (GPL-3.0) | Proprietário |
| Dados | Local (SQLite, seu PC) | Cloud (servidor deles) |
| Custo | Gratuito | Assinatura mensal |
| Indicadores BR | Selic, IPCA, CDI direto do BCB | Genéricos ou inexistentes |
| Anti-impulso | Economia comportamental | Alertas simples |
| Integração | Módulo Luna plugável | Ecossistema fechado |
| Privacidade | Zero telemetria | Coleta de dados |

*"A melhor maneira de prever o futuro é inventá-lo." - Alan Kay*
