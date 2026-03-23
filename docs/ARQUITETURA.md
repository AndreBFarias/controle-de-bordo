# Arquitetura do Controle de Bordo

## Visão Geral

O Controle de Bordo é um Life Operating System local-first, open source (GPL-3.0), construído em Python com arquitetura hexagonal. O sistema gerencia finanças pessoais, hábitos, saúde, estudos, escrita e automação de dispositivos, com foco no contexto brasileiro.

## Princípios Fundamentais

1. **Local-first**: SQLite é a fonte da verdade. Zero dependência de cloud
2. **Hexagonal**: Domínio isolado de infraestrutura via Ports & Adapters
3. **AI-agnostic**: Port abstrai provedores de IA. Trocar = trocar adapter
4. **Luna-ready**: Projetado para integração futura como módulo Luna
5. **Graceful degradation**: Funciona sem IA, sem internet, sem celular

## Diagrama de Camadas

```
                    ┌─────────────────────────┐
                    │       Interface          │
                    │   Flet (Desktop/Mobile)  │
                    │   Typer CLI              │
                    └────────────┬────────────┘
                                 │
                    ┌────────────────────────┐
                    │     Event Bus (Pub/Sub)  │
                    │     Eventos tipados      │
                    │     Pydantic models      │
                    └────────────┬────────────┘
                                 │
    ┌────────────────────────────────────────────────────────┐
    │                    DOMÍNIO                               │
    │  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
    │  │Entidades │  │  Serviços    │  │     Ports         │  │
    │  │Transaction│  │FinancialEng │  │ IStorage          │  │
    │  │Bill      │  │ImpulseFilter│  │ INotifier         │  │
    │  │Goal      │  │GoalTracker  │  │ IAIProvider       │  │
    │  │Habit     │  │MacroIndicat.│  │ IBankImporter     │  │
    │  │Health    │  │NudgeEngine  │  │                   │  │
    │  │Study     │  │             │  │                   │  │
    │  └──────────┘  └──────────────┘  └───────────────────┘  │
    └────────────────────────────┬────────────────────────────┘
                                 │
    ┌────────────────────────────────────────────────────────┐
    │                  ADAPTADORES                             │
    │  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
    │  │Storage  │ │Importers │ │Notifiers │ │AI Providers│  │
    │  │ SQLite  │ │ CSV Nub. │ │ ntfy.sh  │ │ Anthropic  │  │
    │  │ +WAL    │ │ OFX gen. │ │ desktop  │ │ Ollama     │  │
    │  └─────────┘ └──────────┘ └──────────┘ └────────────┘  │
    │  ┌─────────────────┐  ┌──────────────────────────────┐  │
    │  │Desktop          │  │Mobile                        │  │
    │  │ /etc/hosts      │  │ ADB bridge                   │  │
    │  │ GNOME gsettings │  │ Tasker/Shizuku profiles      │  │
    │  │ DBus monitor    │  │ ntfy.sh push                 │  │
    │  └─────────────────┘  └──────────────────────────────┘  │
    └─────────────────────────────────────────────────────────┘
```

## Regra de Ouro: Direção das Dependências

```
domain/ NUNCA importa de adapters/, ui/ ou mobile/
adapters/ importa APENAS de domain/ports/ e domain/entities/
ui/ importa de domain/services/ e domain/entities/
```

## Stack Técnica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| UI | Flet | Cross-platform Python, Material Design 3 |
| CLI | Typer + Rich | Ergonomia, validação, ajuda automática |
| Persistência | SQLite + WAL | ACID, local-first, zero infra |
| Validação | Pydantic | Type safety, serialização |
| Indicadores BR | finbr + python-bcb | Selic, IPCA, CDI direto do BCB |
| IA (fase 1) | Anthropic SDK | Raciocínio superior para MVP |
| IA (fase 2) | Ollama | Privacidade total, integração Luna |
| Push | ntfy.sh | Self-hosted, open source, gratuito |
| Sync | Syncthing | P2P, battle-tested, zero cloud |
| Desktop | dasbus + gsettings | Integração GNOME nativa |
| Mobile | ADB + Tasker + Shizuku | Automação Android sem root |

## Decisões Arquiteturais Documentadas

### Open Finance é impossível para open source

O Open Finance Brasil exige autorização do BCB como instituição participante. Intermediários (Pluggy, Belvo) são B2B pagos com contrato mínimo de 12 meses. Solução: importação CSV/OFX manual.

### Google Fit API está deprecated

A API REST do Google Fit foi descontinuada em 2026. Novos registros bloqueados desde maio/2024. Substituição: Health Connect (dados no dispositivo, alinhado com local-first).

### Por que Flet e não GTK4/Libadwaita/KivyMD

- GTK4/Libadwaita: Específico do GNOME, quebraria com COSMIC
- KivyMD: Performance ruim no Android, crashes em Adreno
- Flet: Python puro, motor Flutter, desktop + mobile + web, Material Design 3

### Por que não usar bubus como Event Bus

Luna já tem um event bus próprio funcional. Para o standalone, um bus simples tipado com Pydantic é suficiente. bubus seria over-engineering para a fase atual.

## Integração Futura com Luna

O módulo `life_manager` da Luna (v5.4.0) já implementa funcionalidades básicas de finanças, saúde e metas. A integração seguirá o padrão IModule da Luna:

1. `domain/` vira o "motor" importável
2. Um adapter `LunaModuleAdapter` implementa `IModule`
3. O `module.yaml` registra skills, commands, widgets e events
4. A UI Flet continua como app standalone separado

*"A simplicidade é o último grau de sofisticação." - Leonardo da Vinci*
