# Sprint S02: Indicadores Macroeconômicos

## Resumo Executivo
> Integração com dados do Banco Central do Brasil via finbr e python-bcb para Selic, IPCA e CDI, com projeções de economia para metas financeiras.

## Status: CONCLUÍDO

## Data: 2026-03-22
## Duração real: Sessão única (~3h, junto com S00/S01/S03)
## Iterações: 1

## Metas e KPIs

| KPI | Alvo | Resultado | Status |
|-----|------|-----------|--------|
| Indicadores integrados | 3 (Selic, IPCA, CDI) | 3 | Atingido |
| Projeção de economia | 1 função | project_savings completa | Atingido |
| Graceful degradation | Funcionar offline | Retorna None se libs indisponíveis | Atingido |
| CLI macro | 2 comandos | resumo + projeção | Atingido |

## Entregáveis

- [x] MacroIndicators com get_selic(), get_ipca(), get_cdi()
- [x] project_savings() com juros compostos e taxa variável
- [x] get_summary() com todos os indicadores
- [x] Fallback: finbr -> python-bcb -> None (graceful degradation)
- [x] CLI: `bordo macro resumo`, `bordo macro projecao`

## Arquivos Criados

| Arquivo | Linhas | Camada |
|---------|--------|--------|
| src/domain/services/macro_indicators.py | 131 | domínio |

## Critérios de Aceite

1. [x] Projeção funciona com taxa manual (sem internet)
2. [x] `bordo macro projecao 4000 24` retorna projeção válida
3. [x] Teste E2E valida cálculo de juros compostos

## Notas Técnicas

- finbr e python-bcb são opcionais - o sistema funciona sem eles
- A Selic é usada como taxa padrão quando nenhuma é especificada
- Cálculo usa juros compostos mensais: `(1 + taxa_anual/100)^(1/12) - 1`

*"O juro composto é a oitava maravilha do mundo. Quem entende, ganha. Quem não entende, paga." - Albert Einstein (atribuído)*
