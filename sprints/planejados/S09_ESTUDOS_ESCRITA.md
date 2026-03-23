# Sprint S09: Estudos e Escrita

## Resumo Executivo
> Trackers de sessões de estudo (Alura, Coursera, Duolingo) e progresso de escrita (Watchdog monitorando diretório Markdown).

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Tracker de estudos | 1 serviço | 0 | Pendente |
| Tracker de escrita | 1 serviço | 0 | Pendente |
| Integração Watchdog | 1 monitor | 0 | Pendente |
| Plataformas suportadas | 5+ | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] Serviço de tracking de sessões de estudo
- [ ] Registro manual de lições/cursos completados
- [ ] Monitor Watchdog para diretório de escrita (Markdown)
- [ ] Contagem de palavras diária/semanal/mensal
- [ ] CLI: `bordo estudo registrar`, `bordo escrita status`
- [ ] Integração com hábitos (streak de estudo)
- [ ] Página Flet de estudos e escrita

### Fora do Escopo
- Scraping automático de plataformas (frágil, viola ToS)
- OCR de screenshots de progresso

## Dependências
- Sprint S01 (entidade StudySession)
- Sprint S04 (Dashboard Flet)

## Estimativa
- Complexidade: Média
- Duração estimada: 2-3 dias

## Critérios de Aceite
1. `bordo estudo registrar alura 45` registra 45min na Alura
2. Watchdog detecta edição em `~/Escrita/` e atualiza contagem
3. Dashboard mostra progresso de estudo e escrita
4. Streak de estudo integra com hábitos

*"A educação é a arma mais poderosa que você pode usar para mudar o mundo." - Nelson Mandela*
