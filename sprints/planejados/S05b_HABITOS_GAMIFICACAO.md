# Sprint S05b: Hábitos + Gamificação

## Resumo Executivo
> Interface Flet para tracking de hábitos com sistema de streak visual, conquistas por milestones e mecanismos de reforço positivo.

## Status: PLANEJADO

## Origem: Auditoria de 2026-03-22

Sprint S05 original dividida. S05b foca exclusivamente em hábitos e gamificação.

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Página Flet de hábitos | 1 | 0 | Pendente |
| Streak visual | Componente | 0 | Pendente |
| Conquistas (milestones) | 3+ níveis | 0 | Pendente |
| Registro com um toque | Sim | Não | Pendente |

## Escopo

### Entregáveis
- [ ] src/ui/pages/habits.py - Página de hábitos com cards
- [ ] src/ui/components/streak_counter.py - Contador visual de streak
- [ ] Sistema de conquistas: 7, 30, 100, 365 dias consecutivos
- [ ] Registro rápido: toque único para completar hábito do dia
- [ ] EventBus: HabitCompleted dispara notificação de conquista
- [ ] Teste E2E: streak cresce e conquista é desbloqueada

### Fora do Escopo
- Integração com Duolingo API (registro manual)
- Metas financeiras (Sprint S05a)

## Dependências
- Sprint S04 (Dashboard Flet)
- Sprint S05a (pode ser paralela)

## Estimativa
- Complexidade: Média
- Duração estimada: 2 dias

## Critérios de Aceite
1. Hábitos aparecem como cards com streak em destaque
2. Completar hábito atualiza streak e best_streak
3. Milestone de 7 dias gera notificação de conquista
4. Streak quebrado gera alerta visual

*"A motivação é o que faz você começar. O hábito é o que faz você continuar." - Jim Ryun*
