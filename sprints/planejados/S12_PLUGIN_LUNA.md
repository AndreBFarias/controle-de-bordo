# Sprint S12: Plugin Luna Completo

## Resumo Executivo
> BordoLunaPlugin satisfazendo IModule da Luna com lifecycle on_load/on_enable/on_disable, module.yaml e discovery via entry points. O Bordo se torna módulo instalável na Luna com pip install.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| BordoLunaPlugin | 1 | 0 | Pendente |
| module.yaml | 1 | 0 | Pendente |
| Entry point discovery | Sim | - | Pendente |
| Lifecycle completo | 3 métodos | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/plugin.py - BordoLunaPlugin com manifest, on_load, on_enable, on_disable
- [ ] on_load: cria config, SQLiteStore, serviços via create_luna_plugin()
- [ ] on_enable: cria EventBusBridge, bridge.connect()
- [ ] on_disable: bridge.disconnect(), cleanup
- [ ] module.yaml na raiz com id, luna_version, skills, commands, events, widgets, settings
- [ ] tests/test_bridge/test_luna_plugin.py com mocks (sem importar código Luna real)

### Fora do Escopo
- Widgets Textual (Sprint S17)
- Migração de dados (Sprint S13)
- Testes com Luna real (Sprint S15)

## Dependências
- Sprint S09 (config e bootstrap com create_luna_plugin)
- Sprint S11 (EventBusBridge)

## Estimativa
- Complexidade: Alta
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_bridge/test_luna_plugin.py -v` tudo verde
2. `pip install -e ".[luna]"` instala sem erros
3. Plugin inicializa com ModuleContext mock
4. Entry point discovery via importlib.metadata simulado funciona

## Notas Técnicas
- Luna descobre módulos via importlib.metadata.entry_points(group="luna.modules")
- module.yaml: manifesto estático lido por Luna para metadata sem importar código
- Mocks para ModuleContext, EventBus Luna e Manifest nos testes (zero dependência da Luna)
- plugin.py só é importado quando o Bordo detecta contexto Luna (import condicional)

*"Um bom módulo é aquele que pode ser explicado em uma frase." - John Ousterhout*
