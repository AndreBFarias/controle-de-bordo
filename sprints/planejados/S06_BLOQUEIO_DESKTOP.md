# Sprint S06: Bloqueio Desktop

## Resumo Executivo
> Automação do desktop Pop!_OS: bloqueio de sites via /etc/hosts, modos de foco GNOME e serviços systemd para execução contínua.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| Bloqueador de sites | 1 serviço | 0 | Pendente |
| Modos de foco | 4 (Trabalho, Estudo, Escrita, Livre) | 0 | Pendente |
| Serviços systemd | 2 | 0 | Pendente |

## Escopo

### Entregáveis
- [ ] src/adapters/desktop/host_blocker.py - Manipulação de /etc/hosts
- [ ] src/adapters/desktop/gnome_focus.py - Modos de foco via gsettings
- [ ] src/adapters/desktop/dbus_monitor.py - Monitor de janelas ativas
- [ ] systemd/bordo-blocker.service
- [ ] systemd/bordo-monitor.service
- [ ] Integração com NudgeEngine para bloqueio condicional

### Fora do Escopo
- Compatibilidade com COSMIC (apenas GNOME 22.04)
- Monitoramento de produtividade com gráficos

## Dependências
- Sprint S00 (infra)
- Sprint S03 (NudgeEngine)

## Estimativa
- Complexidade: Média
- Duração estimada: 2-3 dias

## Critérios de Aceite
1. `sudo python -m src.adapters.desktop.host_blocker --enable trabalho` bloqueia sites
2. `bordo foco trabalho` ativa o modo de foco completo
3. Serviço systemd reinicia automaticamente no boot
4. Desbloqueio funciona ao mudar de modo

## Notas Técnicas
- /etc/hosts requer sudo - o serviço systemd roda como root
- gsettings funciona no GNOME 42+ (Pop!_OS 22.04)
- DBus via dasbus para monitoramento de janelas

*"Disciplina é escolher entre o que você quer agora e o que você mais quer." - Abraham Lincoln*
