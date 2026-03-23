# Sprint S13: Migração JSON para SQLite Faseada

## Resumo Executivo
> Migração progressiva em 4 fases (JSON_ONLY -> DUAL_WRITE -> DUAL_READ_SQL -> SQLITE_ONLY) com DualWriteRepository, backup atômico, validação de integridade SHA-256 e rollback garantido a qualquer momento.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| StorageMode enum | 4 fases | 0 | Pendente |
| DualWriteRepository | 1 | 0 | Pendente |
| MigrationManager | 1 | 0 | Pendente |
| Rollback funcional | Sim | - | Pendente |
| Idempotência | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/migrations/json_to_sqlite.py
- [ ] StorageMode enum: JSON_ONLY, DUAL_WRITE, DUAL_READ_SQL, SQLITE_ONLY
- [ ] DualWriteRepository satisfazendo IStorage com comportamento por fase
- [ ] MigrationManager: get_current_phase, advance_phase, rollback, validate_integrity
- [ ] DataMigrator: migrate_json_to_sqlite() -> MigrationReport
- [ ] Backup atômico: shutil.copytree para JSON, Connection.backup para SQLite
- [ ] Validação de integridade via contagem e checksums SHA-256
- [ ] CLI: bordo migrate --phase, --validate, --rollback
- [ ] tests/test_migration/ com cenários completos

### Fora do Escopo
- Migração automática sem intervenção do usuário
- Migração de schemas entre versões de SQLite (user_version já cobre)

## Dependências
- Sprint S05 (SQLiteStore)
- Sprint S10 (JsonStore)

## Estimativa
- Complexidade: Alta
- Duração estimada: 2 dias

## Critérios de Aceite
1. `pytest tests/test_migration/ -v` tudo verde
2. Migrar 100+ registros JSON -> SQLite com contagens corretas
3. Idempotência: rodar 2x = mesmo resultado
4. Rollback: avançar para DUAL_WRITE, voltar para JSON_ONLY funciona
5. Checksums SHA-256 batem entre JSON e SQLite

## Notas Técnicas
- Dual-write progressivo garante rollback trivial a qualquer momento
- Fase 2 (DUAL_WRITE) recomendada por 3-5 dias de uso real antes de avançar
- JSON files nunca são deletados, apenas arquivados na fase 4
- manifest.json com checksums para auditoria posterior
- DualWriteRepository é transparente: código de negócio não sabe que existem dois backends

*"Toda migração bem-sucedida é uma migração que pode ser revertida." - Desconhecido*
