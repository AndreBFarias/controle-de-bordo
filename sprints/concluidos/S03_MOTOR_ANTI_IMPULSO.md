# Sprint S03: Motor Anti-Impulso

## Resumo Executivo
> Sistema de fricção digital contra compras impulsivas baseado em economia comportamental. Classifica transações por nível de risco, calcula impacto nas metas e gera nudges proativos.

## Status: CONCLUÍDO

## Data: 2026-03-22
## Duração real: Sessão única (~3h, junto com S00/S01/S02)
## Iterações: 1

## Metas e KPIs

| KPI | Alvo | Resultado | Status |
|-----|------|-----------|--------|
| Níveis de fricção | 4+ | 5 (nenhuma, suave, média, forte, bloqueio) | Superado |
| Motor de nudges | 1 serviço | NudgeEngine com 5 verificações | Superado |
| Vieses comportamentais combatidos | 3 | 3 (presente, perda, contabilidade mental) | Atingido |
| Testes de impulso | 2+ | 3 testes E2E | Superado |

## Entregáveis

- [x] ImpulseFilter com 5 níveis de fricção
- [x] Análise de impacto nas metas financeiras
- [x] Categorias de risco vs. essenciais configuráveis
- [x] NudgeEngine com verificação de contas, hábitos, metas, saúde, estudos
- [x] CLI: `bordo nudges` (verifica todos os nudges pendentes)
- [x] configs/default.toml com parâmetros de impulso configuráveis
- [x] Teste E2E validando classificação de transações

## Arquivos Criados

| Arquivo | Linhas | Camada |
|---------|--------|--------|
| src/domain/services/impulse_filter.py | 190 | domínio |
| src/domain/services/nudge_engine.py | 207 | domínio |
| src/domain/services/goal_tracker.py | 110 | domínio |
| configs/default.toml | 86 | infra |

## Lógica de Fricção

```
Transação detectada
  → Categoria essencial? → NENHUMA (passa livre)
  → Categoria de risco?
    → Valor < limiar → SUAVE (lembrete de metas)
    → Valor >= limiar → MÉDIA (esperar 24h)
    → Orçamento > 80% → FORTE (justificativa obrigatória)
    → Orçamento estourado → BLOQUEIO
```

## Critérios de Aceite

1. [x] Supermercado passa sem fricção (essencial)
2. [x] Jogo de R$ 89 no Steam ativa fricção média (24h delay)
3. [x] Nudges detectam contas atrasadas como urgentes
4. [x] Event bus emite ImpulseAlert quando compra é detectada
5. [x] Testes E2E validam todos os cenários

## Notas Técnicas

- Limiar de impulso padrão: R$ 50,00 (configurável via default.toml)
- Categorias de risco: lazer, tecnologia, vestuário, beleza
- Categorias essenciais: moradia, alimentação, saúde, transporte, educação
- O cálculo de impacto nas metas verifica todas as metas financeiras ativas

*"Entre o estímulo e a resposta, há um espaço. Nesse espaço reside o poder de escolher." - Viktor Frankl*
