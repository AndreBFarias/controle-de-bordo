# Controle de Bordo - Índice de Sprints

> Atualizado em: 2026-03-22 (pós-auditoria + DevOps)
> Total: 22 sprints (4 concluídos, 18 planejados) cobrindo 100% das features dos documentos

## Status Geral

| Fase | Sprints | Status |
|------|---------|--------|
| Fase 0: Fundação | S00-S03 | CONCLUÍDA |
| Fase 0.5: Consolidação | S03.5 + DevOps | PLANEJADA |
| Fase 1: Interface e Experiência | S04, S04.5, S05a, S05b | PLANEJADA |
| Fase 1.5: Inteligência | S10 | PLANEJADA (antecipada) |
| Fase 2: Automação | S06, S07, S07.5 | PLANEJADA |
| Fase 3: Expansão | S08, S09, S11 | PLANEJADA |
| Fase 4: Integração | S12, S13 | FUTURA |

## Sprints por Ordem de Execução

### Fase 0: Fundação (CONCLUÍDA)

| # | Sprint | Status | Duração real | Entregáveis |
|---|--------|--------|-------------|-------------|
| S00 | [Fundação](concluidos/S00_FUNDACAO.md) | CONCLUÍDO | Sessão única (~3h) | Repo, arq. hexagonal, SQLite, event bus, CLI |
| S01 | [Finanças Core](concluidos/S01_FINANCAS_CORE.md) | CONCLUÍDO | Sessão única (~3h) | Entidades, CSV/OFX, categorização |
| S02 | [Indicadores Macro](concluidos/S02_INDICADORES_MACRO.md) | CONCLUÍDO | Sessão única (~3h) | finbr, Selic, IPCA, CDI, projeções |
| S03 | [Motor Anti-Impulso](concluidos/S03_MOTOR_ANTI_IMPULSO.md) | CONCLUÍDO | Sessão única (~3h) | Fricção digital, nudges |

> Nota: S00-S03 foram executados em uma sessão intensiva. A divisão é lógica para rastreabilidade.

### Fase 0.5: Consolidação (PLANEJADA - pós-auditoria)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S03.5 | [Configuração e Onboarding](planejados/S03.5_CONFIGURACAO_ONBOARDING.md) | PLANEJADO | TOML loader, wizard setup, EventBus integrado |

### Fase 1: Interface e Experiência (PLANEJADA)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S04 | [Dashboard Flet](planejados/S04_DASHBOARD_FLET.md) | PLANEJADO | UI visual desktop/mobile |
| S04.5 | [Notificadores](planejados/S04.5_NOTIFICADORES.md) | PLANEJADO | ntfy.sh + notify-send |
| S05a | [Metas + Vínculo Financeiro](planejados/S05a_METAS_VINCULO.md) | PLANEJADO | Metas com vínculo a transações |
| S05b | [Hábitos + Gamificação](planejados/S05b_HABITOS_GAMIFICACAO.md) | PLANEJADO | Streaks, conquistas |

### Fase 1.5: Inteligência (PLANEJADA - antecipada da Fase 3)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S10 | [IA Conversacional](planejados/S10_IA_CONVERSACIONAL.md) | PLANEJADO | Anthropic API + Ollama adapter |

> Antecipada porque o usuário declarou intenção de usar IA desde o início.

### Fase 2: Automação (PLANEJADA)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S06 | [Bloqueio Desktop](planejados/S06_BLOQUEIO_DESKTOP.md) | PLANEJADO | /etc/hosts, GNOME, systemd |
| S07 | [Ponte Mobile](planejados/S07_PONTE_MOBILE.md) | PLANEJADO | ADB, Tasker, Shizuku |
| S07.5 | [Qualidade e Cobertura](planejados/S07.5_QUALIDADE_COBERTURA.md) | PLANEJADO | 30+ testes, 70% cobertura |

### Fase 3: Expansão (PLANEJADA)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S08 | [App Mobile Flet](planejados/S08_APP_MOBILE_FLET.md) | PLANEJADO | Dashboard como APK |
| S09 | [Estudos e Escrita](planejados/S09_ESTUDOS_ESCRITA.md) | PLANEJADO | Trackers, Watchdog |
| S11 | [Saúde](planejados/S11_SAUDE.md) | PLANEJADO | Health Connect, HRV |

### Fase 4: Integração (FUTURA)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S12 | [Sync Casal](planejados/S12_SYNC_CASAL.md) | FUTURO | Syncthing, CRDTs |
| S13 | [Integração Luna](planejados/S13_INTEGRACAO_LUNA.md) | FUTURO | Módulo IModule |

### Fase 5: Vida Completa (FUTURA)

| # | Sprint | Status | Foco |
|---|--------|--------|------|
| S14 | [Orçamento Inteligente](planejados/S14_ORCAMENTO_INTELIGENTE.md) | FUTURO | Baldes, desvio automático, bloqueio condicional |
| S15 | [Automação de Workflows](planejados/S15_AUTOMACAO_WORKFLOWS.md) | FUTURO | Chronos Engine, backup, cron interno |
| S16 | [Vida Doméstica](planejados/S16_VIDA_DOMESTICA.md) | FUTURO | Cardápio, cuidado pessoal, CalDAV |

## Relatórios Executivos

| Relatório | Fase | Status |
|-----------|------|--------|
| [Fase 0 - Fundação](relatorios/RELATORIO_FASE_0_FUNDACAO.md) | S00-S03 | DISPONÍVEL |
| [Template](relatorios/TEMPLATE_RELATORIO.md) | - | REFERÊNCIA |

## Grafo de Dependências (pós-auditoria)

```
S00 ── S01 ── S02 ── S03        (Fase 0: fundação)
                      │
                      S03.5      (Fase 0.5: consolidação)
                      │
              ┌───────┤
              │       │
              S04 ── S04.5       (Fase 1: interface)
              │       │
              ├── S05a ── S05b
              │
              S10                (Fase 1.5: inteligência)
              │
              ├── S06
              │         │
              ├── S07 ──┤        (Fase 2: automação)
              │         │
              │       S07.5
              │
              ├── S08
              ├── S09            (Fase 3: expansão)
              ├── S11
              │
              └── S12 ── S13     (Fase 4: integração)
                          │
                    ┌─────┤
                    S14   S15      (Fase 5: vida completa)
                    │     │
                    └──S16─┘
```

## Histórico de Mudanças

### DevOps (2026-03-22)
- Git + GitHub + CI/CD + pre-commit + Justfile
- Mapeamento de 100% das features dos 3 documentos
- **S14 criada**: Orçamento Inteligente (baldes, desvio, bloqueio condicional)
- **S15 criada**: Automação de Workflows (Chronos Engine, backup)
- **S16 criada**: Vida Doméstica (cardápio, cuidado pessoal, CalDAV)

### Auditoria (2026-03-22)
- Fase 0.5 (S03.5) - Consolidação
- S05 dividida em S05a + S05b
- S04.5 - Notificadores
- S07.5 - Qualidade
- S10 antecipada para Fase 1.5
- S08 rebaixada para Fase 3

*"Planeje o trabalho e trabalhe o plano." - Napoleon Hill*
