# Registry Map - Controle de Bordo

> Mapeamento completo de todos os arquivos do projeto.
> Total: 65 arquivos registrados

## O que é

O REGISTRY.csv é o catálogo central de todos os artefatos do projeto. Cada arquivo criado, editado ou removido deve estar registrado nele. Um hook bloqueante (`check_registry.sh`) impede a criação de arquivos não registrados.

## Estrutura do REGISTRY.csv

```csv
caminho,tipo,linhas,camada,status,tags,propósito
```

| Coluna | Descrição |
|--------|-----------|
| caminho | Caminho relativo à raiz do projeto |
| tipo | source, config, doc, script, teste |
| linhas | Contagem de linhas |
| camada | infra, domínio, orquestração, apresentação, teste, doc |
| status | active, orphan, deprecated, planned |
| tags | startup-critico, hub, referência, etc (separadas por ;) |
| propósito | Descrição em uma frase |

## Camadas

| Camada | Descrição |
|--------|-----------|
| infra | Configuração, persistência, cache, I/O, scripts |
| domínio | Lógica de negócio, entidades, serviços, ports |
| orquestração | Event bus, workflows, roteamento |
| apresentação | UI Flet, CLI Typer, widgets, páginas |
| teste | Testes E2E, fixtures, conftest |
| doc | Documentação, sprints, relatórios |

## Hook Bloqueante

O hook `.claude/hooks/check_registry.sh` roda após cada `Write` ou `Edit`. Se o arquivo não está no REGISTRY.csv, a operação é **bloqueada** com mensagem explicativa.

**Para adicionar um arquivo novo:**
1. Primeiro adicione a entrada no REGISTRY.csv
2. Depois crie/edite o arquivo

**Arquivos ignorados pelo hook:**
- `.venv/`, `.git/`, `__pycache__/`, `data/`, `.flet/`
- `.claude/plans/` (arquivos de plano temporários)
- `*.pyc`

## Distribuição por Camada

| Camada | Arquivos | Linhas |
|--------|----------|--------|
| infra | 20 | ~1.089 |
| domínio | 16 | ~1.609 |
| orquestração | 3 | ~211 |
| apresentação | 5 | ~332 |
| teste | 4 | ~299 |
| doc | 17 | ~2.487 |
| **Total** | **65** | **~6.027** |

*"O que não se mede não se gerencia." - William Edwards Deming*
