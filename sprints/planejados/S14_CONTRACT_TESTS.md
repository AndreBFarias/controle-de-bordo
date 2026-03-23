# Sprint S14: Contract Tests Compartilhados

## Resumo Executivo
> Test base classes que validam Protocol contracts para IStorage, IEventBus e IBankImporter. Rodam contra todas as implementações concretas. mypy --strict habilitado no CI.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Contract test classes | 3 | 0 | Pendente |
| Implementações testadas | SQLite + JSON + EventBus + importadores | 0 | Pendente |
| mypy --strict src/bordo/ | 0 erros | - | Pendente |
| CI atualizado | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] tests/contracts/test_storage_contract.py - StorageContractTest base
- [ ] Testes: insert, get_by_id, update, delete, query, count, backup
- [ ] Rodar contra SQLiteStore E JsonStore
- [ ] tests/contracts/test_event_bus_contract.py - EventBusContractTest base
- [ ] Rodar contra BordoEventBus
- [ ] tests/contracts/test_importer_contract.py - ImporterContractTest base
- [ ] Rodar contra NubankCSV e OFXParser
- [ ] Configurar mypy --strict no pyproject.toml
- [ ] Atualizar .github/workflows/ci.yml: ruff + mypy --strict + pytest + contracts

### Fora do Escopo
- Testes de integração Luna (Sprint S15)
- Testes de UI (Sprint S17-S18)

## Dependências
- Sprint S05 (SQLiteStore)
- Sprint S10 (JsonStore)
- Sprint S04 (BordoEventBus)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/contracts/ -v` todos os contracts passam para todas as implementações
2. `mypy src/bordo/ --strict` passa limpo
3. CI pipeline atualizado e verde

## Notas Técnicas
- Padrão: classe base com métodos de teste, subclasses concretas definem fixture com implementação
- Contract tests garantem que trocar SQLite por JSON (ou vice-versa) não quebra nada
- mypy --strict detecta violações de Protocol estaticamente em tempo de build
- Mesmos contracts podem ser usados pela Luna para validar seus próprios adapters

*"Teste o contrato, não a implementação." - Desconhecido*
