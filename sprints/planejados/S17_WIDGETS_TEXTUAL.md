# Sprint S17: Widgets Textual para Luna

## Resumo Executivo
> Widgets Textual consumindo ViewModels para integração visual na TUI da Luna: FinanceDashboard, GoalProgress, HabitTracker, HealthSummary. Registrados via WidgetRegistry e module.yaml.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Widgets Textual | 4 | 0 | Pendente |
| Consome ViewModels | Sim | - | Pendente |
| Subscribe/Unsubscribe | Sim | - | Pendente |
| module.yaml atualizado | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/adapters/textual_widgets/__init__.py
- [ ] finance_dashboard.py - saldo, receitas, despesas, top categorias
- [ ] goal_progress.py - barras de progresso, projeção de conclusão
- [ ] habit_tracker.py - lista com streak visual
- [ ] health_summary.py - água, refeições, peso do dia
- [ ] Cada widget: recebe ViewModel, subscribe em compose(), unsubscribe em on_unmount()
- [ ] module.yaml atualizado com widgets e slots
- [ ] tests/test_adapters/test_textual_widgets.py

### Fora do Escopo
- Interface Flet (Sprint S18)
- Gráficos avançados (matplotlib)
- Customização de temas Luna

## Dependências
- Sprint S16 (ViewModels)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_adapters/test_textual_widgets.py -v` tudo verde
2. Widget renderiza sem crash com dados mock
3. Widget atualiza quando ViewModel muda

## Notas Técnicas
- Textual renderiza escape codes no terminal (TUI da Luna)
- Widget slots da Luna: Containers com IDs como #plugin-slot-main
- Widgets descobertos por entry points ou module.yaml
- Cada widget é independente e pode ser registrado individualmente

*"A interface com o usuário é a última oportunidade de errar." - Desconhecido*
