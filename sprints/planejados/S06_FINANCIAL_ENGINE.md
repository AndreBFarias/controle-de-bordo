# Sprint S06: FinancialEngine e Importadores

## Resumo Executivo
> Motor financeiro com categorização automática por palavras-chave, cálculo de balanços e tendências. Importadores CSV Nubank e OFX genérico satisfazendo IBankImporter.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| FinancialEngine | 1 | 0 | Pendente |
| Importadores IBankImporter | 2 | 0 | Pendente |
| Categorias automáticas | 8+ | 0 | Pendente |
| Fixture CSV Nubank | 1 | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/domain/services.py - FinancialEngine com DI (IStorage, IEventBus)
- [ ] add_transaction() com categorização automática por palavras-chave
- [ ] get_balance(period) - saldo por período
- [ ] get_summary(month, year) - receitas, despesas, saldo, top categorias
- [ ] get_spending_trend(months) - média por categoria nos últimos N meses
- [ ] Emite TransactionCreated via event bus
- [ ] src/bordo/adapters/nubank_csv.py satisfazendo IBankImporter
- [ ] src/bordo/adapters/ofx_parser.py satisfazendo IBankImporter
- [ ] Dicionário de categorização com 8+ categorias (alimentação, transporte, moradia, etc.)
- [ ] tests/fixtures/nubank_sample.csv com dados fictícios
- [ ] tests/test_domain/test_financial.py e tests/test_adapters/test_importers.py

### Fora do Escopo
- ImpulseFilter (Sprint S07)
- GoalTracker (Sprint S07)
- Gráficos e visualização (Sprint S18)

## Dependências
- Sprint S02 (entidades Transaction)
- Sprint S04 (BordoEventBus)
- Sprint S05 (SQLiteStore)

## Estimativa
- Complexidade: Alta
- Duração estimada: 2 dias

## Critérios de Aceite
1. `pytest tests/test_domain/test_financial.py tests/test_adapters/test_importers.py -v` tudo verde
2. Importar CSV fixture e validar totais corretos
3. Categorização automática correta para 10+ descrições
4. get_balance e get_summary retornam valores corretos

## Notas Técnicas
- Categorização por regex/keywords em dicionário configurável (não hardcoded)
- CSV Nubank: colunas Data, Valor, Identificador, Descrição
- OFX: formato SGML usado por bancos BR (Itaú, BB, Bradesco)
- FinancialEngine recebe dependências via construtor (padrão hexagonal)

*"O que não se mede não se melhora." - Peter Drucker*
