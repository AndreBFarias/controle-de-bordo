# Sprint S18: Interface Flet Standalone

## Resumo Executivo
> Interface visual Flet com navegação por tabs (Finanças, Metas, Hábitos, Saúde), tema escuro, responsiva, consumindo os mesmos ViewModels dos widgets Textual. Entry point: bordo ui.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Páginas Flet | 4 | 0 | Pendente |
| App entry point | 1 | 0 | Pendente |
| Tema escuro | Sim | - | Pendente |
| Responsivo | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/adapters/flet_ui/app.py - entry point com navegação tabs
- [ ] src/bordo/adapters/flet_ui/pages/finance_page.py - cards, tabela, botão importar
- [ ] src/bordo/adapters/flet_ui/pages/goals_page.py - cards com progress bar, formulário
- [ ] src/bordo/adapters/flet_ui/pages/habits_page.py - checkbox, streak counter
- [ ] src/bordo/adapters/flet_ui/pages/health_page.py - botões rápidos, resumo do dia
- [ ] CLI: bordo ui lança janela Flet
- [ ] Tema escuro por default (Material Design 3)

### Fora do Escopo
- App mobile empacotado (APK) - pós-v0.1.0
- Gráficos matplotlib
- Sincronização em tempo real entre TUI e Flet

## Dependências
- Sprint S16 (ViewModels)

## Estimativa
- Complexidade: Alta
- Duração estimada: 2 dias

## Critérios de Aceite
1. `pip install -e ".[flet]"` instala sem erros
2. `bordo ui` abre janela Flet funcional
3. Navegação entre 4 tabs funciona
4. Dados reais do SQLite aparecem na interface

## Notas Técnicas
- Flet usa Flutter engine em janela nativa (não terminal)
- API imperativa atual (estável), não declarativa @ft.component (beta)
- Todo código Flet isolado em adapters/flet_ui/ - se API mudar, só essa pasta é afetada
- ViewModels compartilhados com Textual: mesma lógica, duas representações visuais

*"Design não é apenas como parece. Design é como funciona." - Steve Jobs*
