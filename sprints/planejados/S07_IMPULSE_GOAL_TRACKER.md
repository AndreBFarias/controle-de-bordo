# Sprint S07: ImpulseFilter e GoalTracker

## Resumo Executivo
> Motor anti-impulso com regra de 24h, custo-de-oportunidade e score de fricção. GoalTracker com projeções, vínculo a transações e alertas de milestone via event bus.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| ImpulseFilter | 1 | 0 | Pendente |
| Regras de impulso | 4+ | 0 | Pendente |
| GoalTracker | 1 | 0 | Pendente |
| Milestone alerts | 4 (25/50/75/100%) | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/domain/services.py - ImpulseFilter
- [ ] check_purchase(amount, category, description) -> ImpulseResult
- [ ] ImpulseResult: approved, score (0-100), reasons, opportunity_cost
- [ ] Regra 24h: compras acima de threshold requerem espera
- [ ] Custo-oportunidade: "atrasa meta [X] em N dias"
- [ ] Limite mensal por categoria
- [ ] src/bordo/domain/services.py - GoalTracker
- [ ] add_goal(), update_progress(), get_goals()
- [ ] calculate_projection() - data estimada de conclusão
- [ ] get_milestone_alerts() - notifica em 25%, 50%, 75%, 100%
- [ ] Emite GoalUpdated e GoalMilestone via event bus
- [ ] tests/test_domain/test_impulse.py e tests/test_domain/test_goals.py

### Fora do Escopo
- Interface visual (Sprint S18)
- Bloqueio de sites/apps (Sprint legada)
- Gamificação de hábitos (separado)

## Dependências
- Sprint S02 (entidades Goal, Transaction)
- Sprint S04 (BordoEventBus)
- Sprint S05 (SQLiteStore)

## Estimativa
- Complexidade: Alta
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_domain/test_impulse.py tests/test_domain/test_goals.py -v` tudo verde
2. Compra de R$500 com meta ativa retorna score de impacto
3. Compra abaixo do threshold é aprovada automaticamente
4. Milestone emitido ao cruzar 50%

## Notas Técnicas
- ImpulseFilter inspirado em economia comportamental (nudge theory)
- Score 0-100: 0=aprovado sem ressalvas, 100=bloqueio total
- Projeção de meta: linear simples (valor restante / média mensal de progresso)
- GoalTracker desacoplado do FinancialEngine via event bus

*"Entre o estímulo e a resposta existe um espaço. Nesse espaço reside a liberdade de escolha." - Viktor Frankl*
