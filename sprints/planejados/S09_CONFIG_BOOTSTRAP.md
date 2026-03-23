# Sprint S09: Config Dual-Mode e Bootstrap

## Resumo Executivo
> Sistema de configuração que opera em dois modos: standalone (TOML em ~/.config/bordo/) e plugin Luna (dict injetado pelo host). Detecção automática de modo via importlib.metadata.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| BordoConfig | 1 | 0 | Pendente |
| Modo standalone (TOML) | Sim | - | Pendente |
| Modo plugin (dict) | Sim | - | Pendente |
| detect_mode() | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/config.py - BordoConfig (dataclass ou BaseSettings)
- [ ] db_path, config_dir, currency, impulse_threshold, impulse_cooldown_hours, log_level
- [ ] Carregamento standalone: lê ~/.config/bordo/config.toml, cria default se inexistente
- [ ] Carregamento plugin: recebe dict do ModuleContext Luna
- [ ] detect_mode() -> "standalone" | "luna"
- [ ] src/bordo/bootstrap.py atualizado: create_standalone(config) e create_luna_plugin(host_context)
- [ ] tests/test_config.py

### Fora do Escopo
- Plugin Luna completo (Sprint S12)
- Wizard interativo de setup (pós-v0.1.0)

## Dependências
- Sprint S05 (SQLiteStore para bootstrap)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_config.py -v` tudo verde
2. Config standalone carrega TOML e cria default
3. Config plugin aceita dict
4. detect_mode() retorna "standalone" quando Luna não instalada

## Notas Técnicas
- TOML nativo no Python 3.11+ (tomllib), fallback para tomli no 3.10
- detect_mode() usa importlib.metadata para verificar se Luna está instalada
- BordoConfig é imutável após criação (frozen dataclass ou model_config frozen)
- XDG compliance: ~/.config/bordo/config.toml, ~/.local/share/bordo/bordo.db

*"A configuração é o destino." - Abraham Lincoln (adaptado)*
