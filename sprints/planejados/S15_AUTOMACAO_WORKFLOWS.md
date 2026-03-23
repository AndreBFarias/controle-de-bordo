# Sprint S15: Automação de Workflows

## Resumo Executivo
> Motor de agendamento interno (Chronos Engine) para rotinas periódicas, backup automático para GitHub e execução de workflows complexos sem cron externo.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Chronos Engine | 1 scheduler | 0 | Pendente |
| Backup automático | GitHub push | 0 | Pendente |
| Workflows configuráveis | 3+ | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] Chronos Engine: agendador interno baseado em asyncio
- [ ] Workflows: verificar contas todo dia, nudges diários, backup semanal
- [ ] Backup automático de dados para repositório GitHub privado
- [ ] Backup automático de arquivos de escrita (Markdown)
- [ ] Configuração de rotinas via default.toml

### Fora do Escopo
- Cron do sistema (self-contained, sem dependência externa)
- Interface gráfica de agendamento

## Dependências
- Sprint S03.5 (config_loader)
- Sprint S09 (Escrita / Watchdog)

## Estimativa
- Complexidade: Média-Alta
- Duração estimada: 2-3 dias

*"A automação aplicada a uma operação eficiente aumentará a eficiência." - Bill Gates*
