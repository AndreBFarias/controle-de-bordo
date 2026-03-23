# Sprint S13: Integração Luna

## Resumo Executivo
> Empacotamento do Controle de Bordo como módulo Luna (IModule), permitindo que a assistente de IA local opere sobre os dados e serviços do sistema.

## Status: PLANEJADO (FUTURO)

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Módulo IModule funcional | 1 | 0 | Pendente |
| module.yaml completo | 1 | 0 | Pendente |
| Skills Luna | 3+ | 0 | Pendente |
| Migração do life_manager | 1 script | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] Adapter `LunaModuleAdapter` implementando IModule
- [ ] module.yaml com skills, commands, widgets, events
- [ ] BordoFinancialSkill para Luna
- [ ] BordoImpulseSkill para Luna
- [ ] BordoMacroSkill para Luna
- [ ] Script de migração JSON (life_manager) -> SQLite (Bordo)
- [ ] Widget Textual para dashboard no terminal Luna

### Fora do Escopo
- Substituição total do life_manager (coexistência)
- MCP server (sprint posterior se necessário)

## Dependências
- Todos os sprints anteriores (S00-S11)
- Luna v5.5.0+ (compatibilidade de IModule)

## Estimativa
- Complexidade: Alta
- Duração estimada: 4-5 dias

## Critérios de Aceite
1. `pip install controle-de-bordo` importável como biblioteca
2. Luna carrega o módulo via module.yaml
3. `minhas contas` na Luna retorna dados do Controle de Bordo
4. Life_manager e Bordo coexistem sem conflito
5. Migração de dados preserva todos os registros

## Notas Técnicas
- Luna usa Textual para TUI; Bordo usa Flet para GUI - ambas interfaces coexistem
- O domain/ do Bordo é o "motor" importável
- Luna Event Bus (`src/core/event_bus.py`) é compatível com o bus do Bordo
- Entidades do Bordo (Pydantic) podem ser serializadas para o formato Luna

*"A união faz a força." - Esopo*
