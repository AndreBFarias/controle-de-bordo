# Sprint S05: SQLite Adapter com WAL

## Resumo Executivo
> Implementação do SQLiteStore satisfazendo IStorage com WAL mode, PRAGMA user_version para controle de schema, backup atômico via Connection.backup() e tabelas para as 6 entidades.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| SQLiteStore implementado | 1 | 0 | Pendente |
| Satisfaz IStorage | Sim | - | Pendente |
| journal_mode = WAL | Sim | - | Pendente |
| Tabelas criadas | 6 | 0 | Pendente |
| Backup funcional | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/adapters/sqlite_store.py satisfazendo IStorage
- [ ] PRAGMA journal_mode=WAL, synchronous=NORMAL, foreign_keys=ON
- [ ] PRAGMA user_version para controle incremental de schema (sem Alembic)
- [ ] Schema migration automática ao conectar (verifica user_version, aplica DDL)
- [ ] Tabelas: transactions, bills, goals, habits, health_records, study_sessions
- [ ] backup() via sqlite3.Connection.backup()
- [ ] Context manager para transações com rollback
- [ ] check_same_thread=False para WAL
- [ ] tests/test_adapters/test_sqlite.py

### Fora do Escopo
- JSON adapter (Sprint S10)
- Alembic ou migrações externas (user_version é suficiente)
- Async (aiosqlite será usado quando necessário, por ora síncrono)

## Dependências
- Sprint S03 (IStorage Protocol definido)

## Estimativa
- Complexidade: Alta
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_adapters/test_sqlite.py -v` tudo verde
2. `mypy src/bordo/adapters/sqlite_store.py --strict` passa
3. PRAGMA journal_mode retorna 'wal'
4. Dados persistem entre conexões
5. backup() cria arquivo funcional
6. Schema migration idempotente

## Notas Técnicas
- WAL mode permite leituras concorrentes durante escritas (TUI Luna + CLI Bordo simultâneos)
- user_version sobre Alembic: projeto pessoal com SQLite local, Alembic é overkill
- synchronous=NORMAL: compromisso entre segurança e performance (aceitável com WAL)
- Connection.backup() é atômico e thread-safe (Python 3.7+)

*"Perfeição é atingida não quando não há mais nada a adicionar, mas quando não há mais nada a remover." - Antoine de Saint-Exupéry*
