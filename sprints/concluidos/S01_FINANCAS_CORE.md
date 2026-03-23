# Sprint S01: Finanças Core

## Resumo Executivo
> Motor financeiro completo: entidades, importação de extratos bancários (CSV Nubank + OFX genérico) e categorização automática por palavras-chave.

## Status: CONCLUÍDO

## Data: 2026-03-22
## Duração real: Sessão única (~3h, junto com S00/S02/S03)
## Iterações: 1

## Metas e KPIs

| KPI | Alvo | Resultado | Status |
|-----|------|-----------|--------|
| Entidades de domínio | 6 | 6 | Atingido |
| Importadores bancários | 2 | 2 (Nubank CSV + OFX) | Atingido |
| Categorias automáticas | 10+ | 13 categorias | Superado |
| Resumo financeiro | 1 serviço | FinancialEngine completo | Atingido |
| CLI financeira | 3 comandos | 5 comandos | Superado |

## Entregáveis

- [x] Entidade Transaction (tipo, categoria, banco, tags, impulso)
- [x] Entidade Bill (vencimento, recorrência, status, lembrete)
- [x] Entidade Goal (progresso, KPIs, projeção)
- [x] Entidade Habit (streak, frequência, completions)
- [x] Entidade HealthRecord (hidratação, refeição, exercício, peso)
- [x] Entidade StudySession (plataforma, duração, progresso)
- [x] Parser CSV Nubank com detecção automática
- [x] Parser OFX genérico (Itaú, BB, Bradesco, Inter)
- [x] FinancialEngine: categorização, resumo, contas, despesas por categoria
- [x] CLI: `bordo financas resumo`, `bordo financas importar`, `bordo financas categorias`
- [x] CLI: `bordo contas listar`, `bordo contas adicionar`, `bordo contas pagar`
- [x] configs/categories.toml com mapeamento de palavras-chave

## Arquivos Criados

| Arquivo | Linhas | Camada |
|---------|--------|--------|
| src/domain/entities/transaction.py | 89 | domínio |
| src/domain/entities/bill.py | 79 | domínio |
| src/domain/entities/goal.py | 107 | domínio |
| src/domain/entities/habit.py | 86 | domínio |
| src/domain/entities/health_record.py | 82 | domínio |
| src/domain/entities/study_session.py | 57 | domínio |
| src/adapters/importers/nubank_csv.py | 106 | infra |
| src/adapters/importers/ofx_parser.py | 115 | infra |
| src/domain/services/financial_engine.py | 227 | domínio |
| src/cli/main.py | 332 | apresentação |
| configs/categories.toml | 86 | domínio |

## Critérios de Aceite

1. [x] Importação de CSV Nubank gera transações categorizadas
2. [x] Resumo financeiro calcula receitas, despesas e saldo corretamente
3. [x] Contas a pagar monitoram vencimento e detectam atraso
4. [x] Testes E2E validam fluxo completo de importação

## Notas Técnicas

- Categorização usa busca case-insensitive por substrings na descrição
- "salario" (sem acento) foi adicionado como keyword porque extratos bancários não usam acentuação
- OFX parser usa `ofxparse` como dependência, com fallback de encoding latin-1

*"O dinheiro é um bom servo e um mau senhor." - Francis Bacon*
