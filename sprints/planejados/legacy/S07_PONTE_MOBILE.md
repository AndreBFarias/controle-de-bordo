# Sprint S07: Ponte Mobile

## Resumo Executivo
> Comunicação bidirecional com Android via ADB wireless, Tasker/Shizuku para automação e ntfy.sh para notificações push gratuitas.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| ADB bridge funcional | 1 | 0 | Pendente |
| Perfis Tasker gerados | 4+ | 0 | Pendente |
| Notificador ntfy.sh | 1 | 0 | Pendente |
| Scripts Shizuku | 3+ | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/mobile/adb_bridge.py - Comunicação ADB over TCP/IP
- [ ] src/mobile/shizuku_commands.py - Scripts de suspensão/bloqueio de apps
- [ ] src/mobile/tasker_profiles.py - Gerador de perfis Tasker
- [ ] src/mobile/app_monitor.py - Monitor de apps via ADB
- [ ] src/adapters/notifiers/ntfy_notifier.py - Push notifications via ntfy.sh
- [ ] src/adapters/notifiers/desktop_notifier.py - notify-send para Linux
- [ ] tasker/README.md - Instruções de importação dos perfis

### Fora do Escopo
- App Flet no celular (Sprint S08)
- Detecção de apps via Accessibility API (bloqueada no Android 17)

## Dependências
- Sprint S00 (infra)
- Sprint S03 (NudgeEngine para disparar alertas)
- Sprint S04.5 (notificadores ntfy.sh para push mobile)

## Estimativa
- Complexidade: Alta
- Duração estimada: 3-4 dias

## Critérios de Aceite
1. `bordo mobile conectar <ip>` estabelece conexão ADB
2. `bordo mobile suspender com.instagram.android` suspende o app
3. Notificação ntfy.sh chega no celular em < 5 segundos
4. Perfis Tasker exportados importam sem erro

*"A tecnologia é melhor quando aproxima as pessoas." - Matt Mullenweg*
