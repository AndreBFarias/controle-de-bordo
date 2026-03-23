# Sprint S11: EventBusBridge Bidirecional

## Resumo Executivo
> Componente mais crítico da integração Luna: EventBusBridge com EventRegistry, conversão bidirecional BaseModel<->dict, guard contra reentrância e GenericEvent como fallback. 100% de cobertura exigida.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| EventRegistry | 1 | 0 | Pendente |
| EventBusBridge | 1 | 0 | Pendente |
| Guard reentrância | Sim | - | Pendente |
| Cobertura luna_bridge.py | 100% | - | Pendente |
| Teste stress 1000 eventos | 0 loops | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/adapters/luna_bridge.py - EventRegistry
- [ ] register(name, event_type) e auto_register(event_type) com prefixo "bordo."
- [ ] EventBusBridge(luna_bus, bordo_bus, registry)
- [ ] connect() e disconnect()
- [ ] _bridging: bool guard contra loop infinito
- [ ] Luna->Bordo: (str, dict) -> model_validate() -> BaseModel
- [ ] Bordo->Luna: BaseModel -> model_dump() -> (str, dict)
- [ ] GenericEvent(BaseModel) como fallback para eventos não mapeados
- [ ] Eventos desconhecidos logados mas não crasheiam
- [ ] tests/test_bridge/test_event_bridge.py

### Fora do Escopo
- Plugin Luna completo (Sprint S12)
- Módulo module.yaml (Sprint S12)

## Dependências
- Sprint S04 (BordoEventBus)

## Estimativa
- Complexidade: Alta
- Duração estimada: 2 dias

## Critérios de Aceite
1. `pytest tests/test_bridge/test_event_bridge.py -v` tudo verde
2. `pytest tests/test_bridge/ --cov=src/bordo/adapters/luna_bridge --cov-report=term` 100% cobertura
3. 1000 eventos em sequência: cada um chega exatamente 1 vez (zero loops)
4. connect() e disconnect() funcionam corretamente

## Notas Técnicas
- Conversão via model_dump() (Pydantic->dict) e model_validate() (dict->Pydantic), O(microsegundos) graças ao core Rust do Pydantic v2
- Prefixo "bordo." evita colisão com 130+ sprints de eventos Luna
- Guard _bridging = True durante processamento: se evento voltar pelo outro bus, é ignorado
- GenericEvent com campo data: dict para eventos Luna sem tipo mapeado no Bordo
- Componente mais crítico porque falha aqui = integração inteira quebra

*"A interface entre dois sistemas é sempre o ponto mais frágil." - Fred Brooks*
