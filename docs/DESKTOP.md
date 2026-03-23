# Automação Desktop - Controle de Bordo

> **Status**: Arquitetura planejada - implementação na Sprint S06.
> Os componentes descritos abaixo ainda não foram codificados.

## Visão Geral

Integração profunda com Pop!_OS 22.04 (GNOME) para bloqueio de distrações, modos de foco e monitoramento de produtividade. Funciona via DBus, gsettings e manipulação de /etc/hosts.

## Componentes

### 1. Bloqueador de Sites (`src/adapters/desktop/host_blocker.py`)

Manipula `/etc/hosts` para bloquear sites distrativos em nível de sistema.

**Funcionamento:**
```
# Adiciona ao /etc/hosts:
127.0.0.1 www.instagram.com
127.0.0.1 www.tiktok.com
127.0.0.1 www.shopee.com.br
127.0.0.1 www.amazon.com.br
# ... etc
```

**Requisitos:**
- Permissão de escrita em /etc/hosts (requer sudo)
- Serviço systemd para aplicar regras no boot
- Desbloqueio condicional (ex: após completar meta de estudo)

**Listas de bloqueio por modo:**
| Modo | Sites bloqueados |
|------|-----------------|
| Trabalho | Redes sociais, entretenimento, compras |
| Estudo | Redes sociais, entretenimento |
| Escrita | Tudo exceto editor e referências |
| Livre | Nenhum |

### 2. Modos de Foco (`src/adapters/desktop/gnome_focus.py`)

Configura o ambiente GNOME automaticamente via gsettings e DBus.

**Modos disponíveis:**

| Modo | Ações automáticas |
|------|------------------|
| **Trabalho** | Bloquear sites, silenciar notificações, tiling focado |
| **Estudo** | Bloquear sites, abrir Duolingo/Alura, timer visível |
| **Escrita** | Tela limpa, editor maximizado, sem notificações |
| **Exercício** | Sem tela, apenas alertas de tempo |
| **Livre** | Desbloquear tudo, notificações ativas |

**Implementação via gsettings:**
```bash
# Silenciar notificações
gsettings set org.gnome.desktop.notifications show-banners false

# Modo Não Perturbe
gsettings set org.gnome.desktop.notifications show-in-lock-screen false

# Tiling automático (Pop Shell)
# Via dbus-send para reorganizar janelas
```

### 3. Monitor de Janelas (`src/adapters/desktop/dbus_monitor.py`)

Monitora apps em foco via DBus para métricas de produtividade.

**Dados coletados:**
- Tempo por aplicativo (para gráfico de produtividade)
- Detecção de troca frequente de contexto (sinal de distração)
- Alerta quando app de compras/rede social está em foco durante horário de trabalho

### 4. Serviços Systemd

**bordo-blocker.service** - Bloqueador de sites automático:
```ini
[Unit]
Description=Controle de Bordo - Bloqueador de Sites
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m src.adapters.desktop.host_blocker --daemon
Restart=always

[Install]
WantedBy=multi-user.target
```

**bordo-monitor.service** - Monitor de produtividade:
```ini
[Unit]
Description=Controle de Bordo - Monitor de Produtividade
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m src.adapters.desktop.dbus_monitor --daemon
Restart=always
Environment=DISPLAY=:1

[Install]
WantedBy=graphical-session.target
```

## Fluxo de Automação

```
1. Usuário inicia sessão de trabalho (manual ou horário)
2. Sistema ativa modo "Trabalho":
   - Bloqueia sites via /etc/hosts
   - Silencia notificações GNOME
   - Reorganiza janelas (IDE + Terminal + Teams)
3. Monitor rastreia apps em foco
4. Se detectar distração:
   - Nudge suave (notificação)
   - Se persistir: nudge forte
5. Ao completar sessão:
   - Desbloqueia sites gradualmente
   - Relatório de produtividade
```

## Compatibilidade

| Ambiente | Status | Notas |
|----------|--------|-------|
| Pop!_OS 22.04 (GNOME) | Suportado | Ambiente principal de desenvolvimento |
| Ubuntu 22.04+ (GNOME) | Compatível | gsettings e DBus idênticos |
| Pop!_OS 24.04 (COSMIC) | Parcial | DBus funciona, gsettings pode variar |
| Outros Linux (GNOME) | Compatível | Mesma base GNOME |
| Outros DE (KDE, XFCE) | Limitado | Apenas /etc/hosts e notificações genéricas |

*"Disciplina é a ponte entre metas e realizações." - Jim Rohn*
