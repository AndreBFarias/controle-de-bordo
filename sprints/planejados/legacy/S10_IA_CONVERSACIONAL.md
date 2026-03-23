# Sprint S10: IA Conversacional

## Resumo Executivo
> Integração com Anthropic API como consultor financeiro inteligente sobre dados locais, com transição planejada para Ollama/Luna.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Adapter Anthropic | 1 | 0 | Pendente |
| Adapter Ollama | 1 | 0 | Pendente |
| Análise financeira por IA | 1 fluxo | 0 | Pendente |
| Sugestões personalizadas | Sim | Não | Pendente |

## Escopo

### Entregáveis
- [ ] src/adapters/ai/claude_provider.py - Adapter para Anthropic API
- [ ] src/adapters/ai/ollama_provider.py - Adapter para Ollama local
- [ ] Análise de padrões de gastos via LLM
- [ ] Sugestões personalizadas de economia
- [ ] CLI: `bordo ia analisar`, `bordo ia sugerir`
- [ ] Guardrails: prompt engineering para respostas financeiras seguras

### Fora do Escopo
- Conversação livre (foco em análise financeira)
- MCP server (integração Luna futura)
- Voz (Luna já resolve)

## Dependências
- Sprint S01 (dados financeiros para análise)
- Sprint S02 (indicadores macro para contexto)

## Estimativa
- Complexidade: Média
- Duração estimada: 2-3 dias

## Critérios de Aceite
1. `bordo ia analisar` gera resumo inteligente dos gastos do mês
2. `bordo ia sugerir` propõe ações concretas de economia
3. Troca entre Anthropic e Ollama via configuração (sem mudar código)
4. Funciona sem IA (graceful degradation)

## Notas Técnicas
- LLM recebe dados financeiros como contexto, nunca como prompt
- Respostas devem ser em PT-BR com acentuação correta
- Rate limiting para evitar custos excessivos com API paga
- RTX 3050 4GB limita Ollama a modelos 7B Q4

*"O computador nasceu para resolver problemas que não existiam antes." - Bill Gates*
