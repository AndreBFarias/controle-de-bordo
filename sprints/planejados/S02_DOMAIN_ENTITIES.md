# Sprint S02: Domain Entities com Pydantic

## Resumo Executivo
> Implementação das 6 entidades de domínio Pydantic v2 e eventos tipados BaseModel em src/bordo/domain/, com serialização roundtrip testada.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Entidades Pydantic | 6 | 0 | Pendente |
| Eventos tipados | 9+ | 0 | Pendente |
| Testes roundtrip | 6+ | 0 | Pendente |
| mypy --strict entities | 0 erros | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/domain/entities.py - Transaction, Bill, Goal, Habit, HealthRecord, StudySession
- [ ] Enums: TransactionType, TransactionCategory, BillStatus, GoalCategory, HabitFrequency
- [ ] Cada entidade com id: int | None = None, created_at com default datetime.now()
- [ ] src/bordo/domain/events.py - TransactionCreated, TransactionDeleted, BillPaid, BillDue, GoalUpdated, GoalMilestone, HabitCompleted, HabitStreakBroken, NudgeTriggered
- [ ] tests/test_domain/test_entities.py - roundtrip model_validate(entity.model_dump())
- [ ] Validação de campos obrigatórios e enums

### Fora do Escopo
- Persistência (Sprint S05)
- Lógica de negócio (Sprint S06-S07)
- Ports e interfaces (Sprint S03)

## Dependências
- Sprint S01 (scaffolding e pyproject.toml)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_domain/test_entities.py -v` tudo verde
2. `mypy src/bordo/domain/entities.py --strict` passa limpo
3. Cada entidade sobrevive `model_validate(entity.model_dump())` sem perda de dados

## Notas Técnicas
- Pydantic v2 com core Rust: model_dump/model_validate em microsegundos
- Eventos herdam de BaseModel para serialização automática no EventBusBridge (S11)
- Prefixo "bordo." nos nomes de eventos previne colisão com eventos Luna
- Entidades devem ser independentes de framework (zero imports de SQLite, Flet, etc.)

*"As coisas simples devem ser simples, as complexas devem ser possíveis." - Alan Kay*
