# Sprint S12: Sync Casal

## Resumo Executivo
> Sincronização de dados entre dois dispositivos para casais, via Syncthing P2P com resolução de conflitos por CRDTs.

## Status: PLANEJADO (FUTURO)

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Sync Syncthing funcional | 1 bridge | 0 | Pendente |
| CRDTs para conflitos | 1 engine | 0 | Pendente |
| Dados compartilhados | Orçamento, metas, agenda | 0 | Pendente |
| Dados privados isolados | Transações individuais | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] Configuração automática de Syncthing para SQLite
- [ ] Engine de CRDTs (Last-Write-Wins) para resolução de conflitos
- [ ] Separação de dados compartilhados vs. privados
- [ ] Tabela de orçamento compartilhado
- [ ] Tabela de metas comuns do casal
- [ ] Página Flet de visão compartilhada

### Fora do Escopo
- Supabase como backend (eliminado - local-first)
- Multi-usuário com autenticação (apenas 2 dispositivos pareados)

## Dependências
- Sprint S04 (Dashboard Flet)
- Sprint S07 (Syncthing bridge)

## Estimativa
- Complexidade: Alta
- Duração estimada: 3-4 dias

## Critérios de Aceite
1. Dois dispositivos sincronizam via Syncthing
2. Edição simultânea não causa perda de dados (CRDTs)
3. Transações pessoais permanecem privadas
4. Orçamento compartilhado reflete em ambos os dispositivos

*"Sozinhos podemos fazer tão pouco; juntos podemos fazer tanto." - Helen Keller*
