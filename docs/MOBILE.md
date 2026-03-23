# Integração Mobile - Controle de Bordo

> **Status**: Arquitetura planejada - implementação nas Sprints S07 (ponte) e S08 (app Flet).
> Os componentes descritos abaixo ainda não foram codificados.

## Visão Geral

A ponte mobile conecta o sistema desktop ao Android sem root, utilizando Tasker + Shizuku para automação e ntfy.sh para notificações push. O app Flet fornece um dashboard visual no celular.

## Componentes

### 1. ADB Bridge (`src/mobile/adb_bridge.py`)

Comunicação com o Android via ADB over TCP/IP.

**Configuração inicial** (feita uma vez pelo usuário):
```bash
# No celular: Ativar Depuração USB
# Conectar via USB e autorizar
adb tcpip 5555
adb connect <IP_DO_CELULAR>:5555
# Desconectar o USB - agora funciona via Wi-Fi
```

**Capacidades:**
- Listar apps em execução
- Suspender/retomar apps (Shizuku necessário)
- Bloquear rede de apps específicos
- Enviar inputs de toque
- Capturar screenshots

### 2. Shizuku (`src/mobile/shizuku_commands.py`)

Execução de comandos ADB com privilégios elevados sem root.

**Comandos úteis para o sistema:**
```bash
# Suspender app de compras
pm suspend com.shopee.br

# Bloquear rede do app
cmd connectivity set-package-networking-enabled 0 com.instagram.android

# Retomar app
pm unsuspend com.shopee.br
```

**Restrições do Android 17:**
- API de Acessibilidade bloqueada para apps não-acessíveis
- Shizuku + ADB continua funcionando para suspensão e bloqueio de rede
- Detecção de "usuário abrindo app de compras" limitada a monitoramento de processos

### 3. Tasker Profiles (`src/mobile/tasker_profiles.py`)

Gerador de perfis Tasker para importação no Android.

**Perfis gerados:**
| Perfil | Gatilho | Ação |
|--------|---------|------|
| Bloqueio de foco | Horário de trabalho | Suspender apps distrativos |
| Alerta de compra | Notificação do Nubank | Parsear valor e enviar ao sistema |
| Lembrete de hábito | Horário configurado | Push via ntfy.sh |
| Bloqueio noturno | 23:00-06:00 | Suspender redes sociais |

### 4. Notificações Push (`src/adapters/notifiers/ntfy_notifier.py`)

ntfy.sh como serviço de notificações push gratuito e self-hosted.

**Configuração:**
```bash
# Usando o servidor público (gratuito)
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=controle-de-bordo-<seu-hash>

# Ou self-hosted (mais privado)
docker run -p 80:80 binwiederhier/ntfy serve
```

**Tipos de notificação:**
| Tipo | Prioridade | Exemplo |
|------|-----------|---------|
| Conta atrasada | Urgente | "Conta de luz venceu há 2 dias - R$ 180,00" |
| Conta próxima | Alta | "Internet vence em 3 dias - R$ 120,00" |
| Hábito pendente | Normal | "Duolingo: 0 lições hoje. Streak: 42 dias" |
| Meta atingida | Normal | "Parabéns! Meta de natação semanal concluída" |
| Impulso detectado | Alta | "Compra de R$ 350 em Tecnologia. Meta apartamento: -0.4%" |

### 5. App Mobile Flet (`src/ui/`)

Dashboard Flet empacotado como APK para acesso direto no celular.

**Funcionalidades:**
- Visualização de saldo e metas
- Registro rápido de transações
- Tracker de hábitos com streak
- Alertas e notificações in-app
- Sincronizado via Syncthing (SQLite compartilhado)

**Build:**
```bash
# Instalar Flet CLI
pip install flet

# Build APK
flet build apk src/ui/app.py
```

## Fluxo de Dados

```
Desktop (Pop!_OS)                    Mobile (Android)
     │                                    │
     │  ←── Syncthing (SQLite P2P) ──→   │
     │                                    │
     │  ──── ntfy.sh (push) ──────────→  │
     │                                    │
     │  ←── ADB bridge (comandos) ────   │
     │                                    │
     │  ←── Tasker (notificações) ────   │
```

## Segurança

- ADB bridge funciona apenas na rede local (Wi-Fi)
- ntfy.sh com tópico secreto (hash único por instalação)
- SQLite é o mesmo arquivo sincronizado - sem API exposta
- Shizuku requer autorização explícita do usuário

*"A liberdade é a posse plena da razão." - Cícero*
