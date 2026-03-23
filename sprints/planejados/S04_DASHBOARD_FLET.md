# Sprint S04: Dashboard Flet

## Resumo Executivo
> Interface visual desktop e mobile usando Flet (Material Design 3), com dashboard de métricas financeiras, metas e alertas.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Páginas Flet | 5+ | 0 | Pendente |
| Componentes reutilizáveis | 4+ | 0 | Pendente |
| Tema claro/escuro | Sim | Não | Pendente |
| Responsivo desktop/mobile | Sim | Não | Pendente |

## Escopo

### Entregáveis
- [ ] src/ui/app.py - Ponto de entrada Flet com navegação
- [ ] src/ui/theme.py - Tema com paleta de cores, claro/escuro
- [ ] src/ui/pages/dashboard.py - Página principal com cards de métricas
- [ ] src/ui/pages/finances.py - Gestão financeira (resumo, transações, importar)
- [ ] src/ui/pages/goals.py - Metas com barras de progresso
- [ ] src/ui/pages/settings.py - Configurações do sistema
- [ ] src/ui/components/metric_card.py - Card de métrica reutilizável
- [ ] src/ui/components/progress_ring.py - Anel de progresso circular
- [ ] src/ui/components/alert_banner.py - Banner de alerta/nudge
- [ ] src/ui/components/transaction_list.py - Lista de transações scrollável

### Fora do Escopo
- Gráficos avançados (matplotlib) - Sprint posterior
- App mobile empacotado (APK) - Sprint S08
- Tema customizado por entidade Luna - Integração futura

## Dependências
- Sprint S00 (SQLite adapter)
- Sprint S01 (FinancialEngine, entidades)
- Sprint S03 (NudgeEngine)

## Arquivos Impactados

| Arquivo | Ação | Descrição |
|---------|------|-----------|
| src/ui/app.py | Criar | Ponto de entrada com NavigationBar |
| src/ui/theme.py | Criar | Paleta de cores e temas |
| src/ui/pages/*.py | Criar | 4 páginas principais |
| src/ui/components/*.py | Criar | 4 componentes reutilizáveis |

## Estimativa
- Complexidade: Alta
- Duração estimada: 3-4 dias

## Critérios de Aceite
1. `flet run src/ui/app.py` abre dashboard funcional
2. Navegação entre páginas funciona
3. Dashboard mostra saldo, metas, alertas com dados reais do SQLite
4. Tema escuro/claro alterna corretamente
5. Layout responsivo em janela pequena (simulando mobile)

*"Design não é apenas como parece. Design é como funciona." - Steve Jobs*
