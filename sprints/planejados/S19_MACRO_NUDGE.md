# Sprint S19: MacroIndicators e NudgeEngine

## Resumo Executivo
> Integração com indicadores macro BR (Selic, IPCA, CDI via API BCB) com cache 24h e graceful degradation. NudgeEngine com 7+ regras configuráveis: hidratação, medicamento, exercício, estudo, financeiro, pausa e meta.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| MacroIndicators | 1 | 0 | Pendente |
| Indicadores (Selic/IPCA/CDI) | 4 | 0 | Pendente |
| NudgeEngine | 1 | 0 | Pendente |
| Regras de nudge | 7+ | 0 | Pendente |
| Cache 24h | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/domain/services.py - MacroIndicators
- [ ] get_selic(), get_ipca(), get_cdi(), get_savings_yield()
- [ ] Cache de 24h para evitar chamadas repetidas à API BCB
- [ ] Graceful degradation: sem internet retorna último cache ou None
- [ ] src/bordo/domain/services.py - NudgeEngine
- [ ] check_all() -> list[Nudge]
- [ ] 7+ regras: hidratação, medicamento, exercício, estudo, financeiro, pausa coding, meta
- [ ] Emite NudgeTriggered via event bus
- [ ] CLI: bordo macro e bordo nudges
- [ ] tests/test_domain/test_nudge.py e test_macro.py

### Fora do Escopo
- Notificações push reais (ntfy.sh) - pós-v0.1.0
- Health Connect (pós-v0.1.0)
- Integração desktop (systemd, GNOME)

## Dependências
- Sprint S06 (FinancialEngine para regras financeiras)
- Sprint S04 (BordoEventBus para NudgeTriggered)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_domain/test_nudge.py tests/test_domain/test_macro.py -v` tudo verde
2. NudgeEngine com regra de hidratação ativada/silenciada
3. MacroIndicators retorna dados (mock da API BCB)
4. Graceful degradation sem internet funciona

## Notas Técnicas
- python-bcb e finbr para acesso à API SGS do Banco Central
- Cache em arquivo local (~/.config/bordo/cache/macro.json) para offline-first
- Nudge rules configuráveis via config.toml (thresholds, horários, categorias)
- NudgeEngine é independente: funciona sem FinancialEngine, GoalTracker ou IA

*"Somos o que repetidamente fazemos. A excelência, portanto, não é um ato, mas um hábito." - Aristóteles*
