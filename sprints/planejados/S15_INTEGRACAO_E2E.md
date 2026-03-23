# Sprint S15: Integração End-to-End Luna

## Resumo Executivo
> Teste de integração completo: discovery via entry points -> plugin load -> bridge connect -> fluxo financeiro bidirecional -> migração durante uso -> graceful degradation sem Luna.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Cenários E2E | 5 | 0 | Pendente |
| Latência evento bridge | < 10ms | - | Pendente |
| Graceful degradation | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] tests/test_integration/test_e2e_luna.py
- [ ] Cenário 1: Discovery -> Load -> Enable (entry points mock)
- [ ] Cenário 2: Fluxo financeiro completo (import CSV -> TransactionCreated chega na Luna)
- [ ] Cenário 3: Luna -> Bordo (evento dict -> evento tipado)
- [ ] Cenário 4: Migração durante uso (JSON_ONLY -> DUAL_WRITE -> SQLITE_ONLY)
- [ ] Cenário 5: Graceful degradation (sem Luna real -> funciona via CLI)

### Fora do Escopo
- Testes com Luna real instalada (requer Luna v5.5.0+)
- Performance benchmarks (suficiente < 10ms)

## Dependências
- Sprint S11 (EventBusBridge)
- Sprint S12 (Plugin Luna)
- Sprint S13 (Migração)

## Estimativa
- Complexidade: Alta
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_integration/ -v` tudo verde
2. Evento emitido no Bordo chega na Luna e vice-versa em < 10ms
3. Migração durante uso não perde dados
4. Bordo funciona normalmente com bridge desconectado

## Notas Técnicas
- Todos os testes usam mocks para Luna (ModuleContext, EventBus)
- Cenário 4 é o mais complexo: state machine de migração durante operação
- Graceful degradation é requisito fundamental: Bordo funciona 100% sem Luna
- Latência < 10ms garantida pela conversão Pydantic v2 em Rust

*"O teste de integração é onde a teoria encontra a realidade." - Desconhecido*
