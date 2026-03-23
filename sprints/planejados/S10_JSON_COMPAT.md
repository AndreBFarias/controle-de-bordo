# Sprint S10: JSON Adapter Compatível com life_manager

## Resumo Executivo
> Adaptador JSON que satisfaz IStorage no formato exato do life_manager da Luna (um arquivo por tabela, IDs incrementais, UTF-8 com indent=2). Ponte de compatibilidade para leitura de dados existentes sem migração.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| JsonStore satisfaz IStorage | Sim | - | Pendente |
| Formato compatível life_manager | Sim | - | Pendente |
| File lock thread-safe | Sim | - | Pendente |
| Fixtures Luna | 1 diretório | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/bordo/adapters/json_store.py satisfazendo IStorage
- [ ] Um arquivo JSON por tabela (transactions.json, goals.json, etc.)
- [ ] Formato life_manager: lista de dicts com campo "id" inteiro
- [ ] Encoding UTF-8 com ensure_ascii=False e indent=2
- [ ] _next_id() gera IDs incrementais (max existente + 1)
- [ ] Thread-safe via file lock (fcntl)
- [ ] Arquivo inexistente retorna lista vazia sem crashear
- [ ] tests/fixtures/luna_life_manager/ com JSONs de exemplo
- [ ] tests/test_adapters/test_json_compat.py

### Fora do Escopo
- Migração JSON -> SQLite (Sprint S13)
- DualWriteRepository (Sprint S13)
- Performance com arquivos grandes (suficiente para uso pessoal)

## Dependências
- Sprint S03 (IStorage Protocol definido)

## Estimativa
- Complexidade: Média
- Duração estimada: 1 dia

## Critérios de Aceite
1. `pytest tests/test_adapters/test_json_compat.py -v` tudo verde
2. CRUD completo funciona
3. Formato de saída idêntico ao life_manager (json.load() puro)
4. IDs incrementais corretos

## Notas Técnicas
- Este adapter é a ponte de compatibilidade: o Bordo lê dados existentes do life_manager sem migração
- Formato life_manager: [{"id": 1, "campo": "valor"}, ...] com datas ISO e UTF-8
- File lock via fcntl.flock() para prevenir corrupção em acesso concorrente
- Independente do S05 (SQLite) - pode rodar em paralelo com ele

*"Compatibilidade é respeito pelo trabalho anterior." - Desconhecido*
