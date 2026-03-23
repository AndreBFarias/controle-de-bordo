# Sprint S03: Ports e Protocols

## Resumo Executivo
> Definição dos contratos de domínio como typing.Protocol com @runtime_checkable: IStorage, INotifier, IAIProvider, IBankImporter, IEventBus. Structural subtyping sem herança forçada.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Protocols definidos | 5 | 0 | Pendente |
| Testes isinstance | 5+ | 0 | Pendente |
| mypy --strict domain/ | 0 erros | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/domain/ports.py com 5 Protocols @runtime_checkable
- [ ] IStorage: initialize, insert, update, delete, get_by_id, query, count, backup
- [ ] INotifier: notify(title, message, urgency)
- [ ] IAIProvider: analyze(prompt, context), categorize(description)
- [ ] IBankImporter: import_file(path) -> list[Transaction], supported_formats()
- [ ] IEventBus: emit(event), on(event_type, callback), off(event_type, callback)
- [ ] tests/test_domain/test_ports.py com stubs que satisfazem e violam cada Protocol

### Fora do Escopo
- Implementações concretas (SQLiteStore em S05, JsonStore em S10)
- Event bus real (Sprint S04)

## Dependências
- Sprint S01 (scaffolding)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_domain/test_ports.py -v` tudo verde
2. `mypy src/bordo/domain/ --strict` passa limpo
3. `isinstance(StubStorage(), IStorage)` retorna True
4. Classe incompleta falha no isinstance

## Notas Técnicas
- Protocol (PEP 544) sobre ABCs: Luna não precisa herdar do Bordo, basta implementar os métodos (structural subtyping)
- @runtime_checkable permite isinstance() em tempo de execução para validação
- IStorage usa CRUD genérico com tabela como string para flexibilidade entre SQLite e JSON
- IBankImporter retorna list[Transaction] normalizado independente do banco

*"Programa para uma interface, não para uma implementação." - Gang of Four*
