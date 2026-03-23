# Sprint S08: CLI Typer Completo

## Resumo Executivo
> CLI com Typer expondo todos os serviços: import, balance, summary, impulse-check, goals, habits, health, version. Bootstrap com composition root standalone e SQLiteStore em ~/.config/bordo/.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Comandos CLI | 10+ | 0 | Pendente |
| bootstrap.py funcional | 1 | 0 | Pendente |
| __main__.py funcional | 1 | 0 | Pendente |
| Testes CliRunner | 4+ | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/cli.py com Typer: import, balance, summary, impulse-check, goals, goal add, habits, habit done, health, version
- [ ] src/bordo/bootstrap.py - create_standalone() com DI completa (SQLiteStore, BordoEventBus, FinancialEngine, ImpulseFilter, GoalTracker)
- [ ] DB path: ~/.config/bordo/bordo.db (XDG compliant)
- [ ] src/bordo/__main__.py delegando para CLI
- [ ] tests/test_cli.py com typer.testing.CliRunner

### Fora do Escopo
- Interface Flet (Sprint S18)
- Comandos de migração (Sprint S13)
- Config TOML avançada (Sprint S09)

## Dependências
- Sprint S06 (FinancialEngine)
- Sprint S07 (ImpulseFilter, GoalTracker)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_cli.py -v` tudo verde
2. `pip install -e ".[cli]"` instala sem erros
3. `bordo version` imprime 0.1.0
4. `bordo import fixtures/nubank.csv && bordo balance` mostra saldo correto

## Notas Técnicas
- Typer é wrapper sobre Click com type hints e autocompletion
- CliRunner permite testar CLI sem subprocesso (stdout capturado)
- ~/.config/bordo/ segue XDG Base Directory Specification
- bootstrap.py é o composition root: único local que instancia dependências concretas

*"Faça a coisa mais simples que possa funcionar." - Kent Beck*
