# Sprint S01: Scaffolding e pyproject.toml

## Resumo Executivo
> Estrutura de diretórios completa em src/bordo/, pyproject.toml com hatchling como build backend, configuração de pytest/mypy/ruff e pacote instalável via pip.

## Status: CONCLUÍDO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Estrutura src/bordo/ | 20 arquivos | 20 | Concluído |
| pip install -e ".[dev]" | Sem erros | OK | Concluído |
| import bordo | 0.1.0 | 0.1.0 | Concluído |
| mypy src/bordo/ | 0 erros | 0 | Concluído |
| ruff check src/bordo/ | 0 erros | 0 | Concluído |

## Escopo

### Entregáveis
- [x] src/bordo/__init__.py com __version__ = "0.1.0"
- [x] src/bordo/__main__.py para python -m bordo
- [x] src/bordo/domain/ com placeholders (entities, events, services, ports)
- [x] src/bordo/adapters/ com placeholders (sqlite_store, json_store, luna_bridge, nubank_csv, ofx_parser, flet_ui/)
- [x] src/bordo/migrations/ com placeholder (json_to_sqlite)
- [x] src/bordo/cli.py, plugin.py, config.py, bootstrap.py como placeholders
- [x] pyproject.toml reescrito com hatchling >= 1.26
- [x] CLAUDE.md atualizado referenciando review.md
- [x] Justfile adaptado ao novo layout
- [x] tests/test_domain/, test_adapters/, test_bridge/, test_migration/

### Fora do Escopo
- Lógica de negócio (Sprint S02+)
- Migração do código existente em src/ (sprints subsequentes)
- Testes funcionais (apenas coleta sem erros)

## Dependências
- Nenhuma (primeira sprint)

## Estimativa
- Complexidade: Baixa
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pip install -e ".[dev]"` instala sem erros
2. `python -c "import bordo; print(bordo.__version__)"` imprime `0.1.0`
3. `pytest --co -q` coleta sem erros
4. `mypy src/bordo/` passa limpo
5. `ruff check src/bordo/` passa limpo

## Notas Técnicas
- Hatchling escolhido sobre setuptools: suporte nativo PEP 660 (editable installs), build hooks para module.yaml futuro
- `packages = ["src/bordo"]` mapeia src/bordo/ para namespace `bordo` no sys.modules
- Dependencies core mínimas: pydantic>=2.0, aiosqlite>=0.20
- Código existente em src/ (layout antigo) permanece intocado

*"A simplicidade é a sofisticação suprema." - Leonardo da Vinci*
