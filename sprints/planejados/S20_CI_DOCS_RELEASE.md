# Sprint S20: CI, Documentação e Release

## Resumo Executivo
> Pipeline CI completo no GitHub Actions (lint + typecheck + tests + contracts), README atualizado com quickstart, documentação refletindo src/bordo/, limpeza do código legado em src/ e tag v0.1.0.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| CI pipeline verde | Sim | - | Pendente |
| Matrix Python | 3.10, 3.11, 3.12 | - | Pendente |
| Cobertura | > 80% | - | Pendente |
| Código legado removido | Sim | - | Pendente |
| Tag v0.1.0 | Sim | - | Pendente |

## Escopo

### Entregáveis
- [ ] .github/workflows/ci.yml atualizado: lint, typecheck, test, contracts, matrix Python
- [ ] Cache pip dependencies no CI
- [ ] README.md: quickstart standalone + quickstart Luna + diagrama + comandos CLI
- [ ] docs/ARQUITETURA.md refletindo src/bordo/
- [ ] docs/INTEGRACAO_LUNA.md com instruções reais
- [ ] docs/MIGRACAO.md explicando as 4 fases
- [ ] Remover código legado: src/domain/, src/adapters/, src/cli/, src/events/, src/ui/, src/mobile/
- [ ] Atualizar todos os imports nos testes
- [ ] Verificar anonimato (zero menções a IA)
- [ ] git tag v0.1.0

### Fora do Escopo
- Publicação no PyPI real (apenas PyPI test)
- Docker/containerização
- Documentação Sphinx/MkDocs (markdown é suficiente)

## Dependências
- Todas as sprints anteriores (S01-S19)

## Estimativa
- Complexidade: Média
- Duração estimada: 2 dias

## Critérios de Aceite
1. `ruff check src/bordo/` limpo
2. `mypy src/bordo/ --strict` limpo
3. `pytest tests/ -v --cov=src/bordo` tudo verde, cobertura > 80%
4. `grep -rniE "claude|anthropic|openai" src/bordo/ --include="*.py" | grep -viE "api|config"` vazio
5. `pip install -e ".[all]"` funciona
6. `bordo version` imprime 0.1.0
7. CI pipeline verde end-to-end

## Notas Técnicas
- Remover src/ legado só após confirmar que todos os testes passam com src/bordo/
- Badge de CI no README para visibilidade do status
- Anonimato obrigatório: nenhum arquivo pode mencionar nomes de IA
- Tag v0.1.0 marca o primeiro release funcional do Controle de Bordo como biblioteca

*"O código que não pode ser entendido não pode ser mantido." - Desconhecido*
