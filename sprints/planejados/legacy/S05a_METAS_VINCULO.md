# Sprint S05a: Metas + Vínculo Financeiro

## Resumo Executivo
> Interface Flet para metas com KPIs visuais e vínculo automático entre transações financeiras e progresso de metas (ex: cada economia incrementa a meta "Apartamento").

## Status: PLANEJADO

## Origem: Auditoria de 2026-03-22

Sprint S05 original (Metas e Hábitos) foi dividida em S05a (Metas) e S05b (Hábitos) por serem domínios distintos com complexidade suficiente para sprints separadas.

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Página Flet de metas | 1 | 0 | Pendente |
| Vínculo transação -> meta | 1 regra | 0 | Pendente |
| Projeção visual | Gráfico | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/ui/pages/goals.py - Página de metas com barras de progresso
- [ ] Regra: economia (receita - despesa) incrementa meta financeira ativa
- [ ] Projeção visual: "no ritmo atual, meta atingida em X meses"
- [ ] CLI: `bordo metas atualizar <id> <valor>` com feedback visual
- [ ] Teste E2E: transação importada -> meta financeira incrementada

### Fora do Escopo
- Hábitos e streaks (Sprint S05b)
- Gamificação (Sprint S05b)

## Dependências
- Sprint S04 (Dashboard Flet)

## Estimativa
- Complexidade: Média
- Duração estimada: 2 dias

## Critérios de Aceite
1. Página de metas mostra progresso real do SQLite
2. Transação de receita incrementa meta financeira ativa
3. Projeção mostra data estimada de conclusão
4. Teste E2E valida vínculo transação -> meta

*"Uma meta sem um plano é apenas um desejo." - Antoine de Saint-Exupéry*
