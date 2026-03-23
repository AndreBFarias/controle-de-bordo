# Sprint S04: Event Bus Interno Tipado

## Resumo Executivo
> Implementação do BordoEventBus síncrono com interface emit(BaseModel)/on(Type, callback), wildcard handler para debug e tolerância a falhas em handlers individuais.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| BordoEventBus implementado | 1 | 0 | Pendente |
| Satisfaz IEventBus | Sim | - | Pendente |
| Cobertura event_bus.py | 100% | - | Pendente |
| Testes | 7+ | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/domain/event_bus.py - BordoEventBus satisfazendo IEventBus
- [ ] emit(event: BaseModel) publica para handlers do tipo
- [ ] on(event_type, callback) registra handler
- [ ] off(event_type, callback) remove handler
- [ ] Wildcard handler para debug (recebe todos os eventos)
- [ ] Handler que falha não impede outros de rodar (try/except + logging)
- [ ] Síncrono, sem threading (Luna é single-thread por módulo)
- [ ] tests/test_domain/test_event_bus.py com 7+ cenários

### Fora do Escopo
- EventBusBridge Luna (Sprint S11)
- Threading e async (desnecessário para o modelo Luna)

## Dependências
- Sprint S03 (IEventBus Protocol definido)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_domain/test_event_bus.py -v` tudo verde
2. `pytest tests/test_domain/test_event_bus.py --cov=src/bordo/domain/event_bus --cov-report=term` 100% cobertura
3. emit + receive funciona, sem crosstalk entre tipos, off() remove, wildcard recebe tudo

## Notas Técnicas
- Síncrono por design: Luna é single-thread por módulo, threading adicionaria complexidade sem benefício
- Wildcard handler útil para debug e logging de todos os eventos
- Exceção em handler isolada via try/except: log do erro, continua para próximo handler
- Base para o EventBusBridge bidirecional da Sprint S11

*"Não se comunique pela memória compartilhada; compartilhe memória pela comunicação." - Rob Pike*
