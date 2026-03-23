# Sprint S16: ViewModels UI-Agnósticos

## Resumo Executivo
> Observable[T] genérico (~30 linhas) e ViewModels para finanças, metas, hábitos e saúde. Zero imports de Textual ou Flet. Camada de apresentação compartilhada entre TUI e GUI.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Observable[T] | 1 | 0 | Pendente |
| ViewModels | 4 | 0 | Pendente |
| Imports Textual/Flet | 0 | - | Pendente |
| Testes subscribe/notify | 4+ | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/viewmodels.py
- [ ] Observable[T]: value getter, set(), subscribe(callback), unsubscribe()
- [ ] FinanceViewModel: balance, monthly_summary, recent_transactions, refresh(), import_file()
- [ ] GoalsViewModel: goals, add_goal(), update_progress(), refresh()
- [ ] HabitsViewModel: habits, complete_habit(), refresh()
- [ ] HealthViewModel: today, log_water(), log_meal(), log_weight(), refresh()
- [ ] ZERO imports de Textual ou Flet
- [ ] tests/test_viewmodels.py

### Fora do Escopo
- Widgets Textual (Sprint S17)
- Páginas Flet (Sprint S18)
- Binding reativo avançado (RxPY) - Observable caseiro é suficiente

## Dependências
- Sprint S06 (FinancialEngine)
- Sprint S07 (GoalTracker, ImpulseFilter)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_viewmodels.py -v` tudo verde
2. `grep -rn "textual\|flet" src/bordo/viewmodels.py` retorna vazio
3. Observable notifica após set(), não notifica após unsubscribe()
4. FinanceViewModel.refresh() atualiza balance

## Notas Técnicas
- Observable caseiro (~30 linhas) sobre biblioteca externa: zero dependências, interface simples
- Padrão MVVM: ViewModel expõe estado como Observable, UI apenas se inscreve
- Se escalar, migração para reactivex é trivial (mesma interface subscribe/unsubscribe)
- ViewModels são testáveis sem framework UI (unit test puro)

*"Separe o que muda do que permanece." - Erich Gamma*
