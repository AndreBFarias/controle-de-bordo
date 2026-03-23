# Sprint S11: Saúde

## Resumo Executivo
> Importação de dados de saúde via Health Connect (substitui Google Fit deprecated), com tracking de HRV, exercícios e ajuste adaptativo de rotina.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Importação Health Connect | 1 adapter | 0 | Pendente |
| Métricas de saúde | 5+ tipos | 0 | Pendente |
| Ajuste adaptativo | 1 algoritmo | 0 | Pendente |
| Página Flet saúde | 1 | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/adapters/importers/health_connect.py - Import via ADB pull
- [ ] Métricas: passos, sono, frequência cardíaca, HRV, exercícios
- [ ] Algoritmo de ajuste: HRV baixo -> sugerir atividade leve
- [ ] src/ui/pages/health.py - Página de saúde com gráficos
- [ ] CLI: `bordo saude resumo`, `bordo saude importar`
- [ ] Integração com NudgeEngine (alertas de saúde)

### Fora do Escopo
- Google Fit API (deprecated)
- Monitoramento em tempo real de wearable
- OpenCV para detecção de fadiga

## Dependências
- Sprint S04 (Dashboard Flet)
- Sprint S07 (Ponte Mobile para ADB pull)

## Estimativa
- Complexidade: Alta
- Duração estimada: 3-4 dias

## Critérios de Aceite
1. Health Connect export importa dados de saúde corretamente
2. Dashboard mostra métricas de saúde com tendências
3. HRV baixo dispara nudge de atividade leve
4. Funciona com dados manuais (sem wearable)

## Notas Técnicas
- Health Connect armazena dados no dispositivo (alinhado com local-first)
- Export via ADB: `adb pull /data/data/com.google.android.apps.healthdata/`
- Alternativa: export manual via app Health Connect
- Google Fit API foi descontinuada em 2026

*"Cuide do seu corpo. É o único lugar que você tem para viver." - Jim Rohn*
