# Controle de Bordo - Roadmap de Produto

> Visão estratégica e cronograma macro do projeto.
> Versão: 0.1.0 | Data: 2026-03-22

## Visão do Produto

Ser o primeiro Life Operating System open source maduro em Python, focado no contexto brasileiro, com gestão financeira integrada a hábitos, saúde e automação de dispositivos. Local-first, gratuito, sem dependência de cloud.

## Público-Alvo

- Desenvolvedores brasileiros que querem controle total sobre seus dados
- Casais com rotina intensa que precisam de automação de decisões
- Pessoas que querem disciplina financeira automatizada (anti-impulso)
- Comunidade open source brasileira

## Fases do Projeto

### Fase 0: Fundação (CONCLUÍDA - Semanas 1-2)

**Objetivo**: Infraestrutura técnica sólida e motor financeiro funcional.

| Entregável | Status |
|------------|--------|
| Arquitetura hexagonal completa | Concluído |
| SQLite + WAL para persistência | Concluído |
| 6 entidades de domínio (Pydantic) | Concluído |
| 4 ports (interfaces) | Concluído |
| 5 serviços de domínio | Concluído |
| Event bus tipado | Concluído |
| Importação CSV Nubank + OFX | Concluído |
| Indicadores macro (Selic, IPCA, CDI) | Concluído |
| Motor anti-impulso | Concluído |
| CLI Typer completa | Concluído |
| 11 testes E2E passando | Concluído |
| Documentação completa (6 docs) | Concluído |
| install.sh / uninstall.sh | Concluído |
| Registry-map com hook bloqueante | Concluído |

### Fase 0.5: Consolidação (2026-03-23 a 2026-03-24) - NOVA

**Objetivo**: Corrigir lacunas da auditoria e preparar onboarding.

- S03.5: config_loader integrado, wizard de setup, EventBus nos serviços, logging

### Fase 1: Interface e Experiência (2026-03-25 a 2026-04-05)

**Objetivo**: Tornar o sistema visual e acessível.

- S04: Dashboard Flet com métricas financeiras e de metas
- S04.5: Notificadores (ntfy.sh + desktop)
- S05a: Metas com vínculo automático a transações financeiras
- S05b: Hábitos com streaks visuais e gamificação

### Fase 1.5: Inteligência (2026-04-06 a 2026-04-09) - ANTECIPADA

**Objetivo**: Integrar IA desde cedo (declaração do usuário).

- S10: Anthropic API + Ollama adapter para análise financeira

### Fase 2: Automação (2026-04-10 a 2026-04-22)

**Objetivo**: Automatizar o ambiente desktop e mobile.

- S06: Bloqueio de sites via /etc/hosts + systemd
- S07: Ponte ADB, Tasker, Shizuku, modos de foco GNOME
- S07.5: Sprint de qualidade (30+ testes, 70% cobertura)

### Fase 3: Expansão (2026-04-23 a 2026-05-07)

**Objetivo**: Cobrir todas as áreas da vida.

- S08: App Flet empacotado como APK
- S09: Tracker de estudos e escrita (Watchdog)
- S11: Health Connect para dados de saúde
- HRV e ajuste adaptativo de rotina

### Fase 4: Integração (Semanas 11+)

**Objetivo**: Unificar com o ecossistema Luna.

- Sincronização de casal via Syncthing + CRDTs
- Empacotamento como módulo Luna (IModule)
- Migração de dados do life_manager
- Coexistência Luna + Bordo standalone

## Métricas de Sucesso

| Métrica | Fase 0 | Fase 1 | Fase 2 | Fase 3 | Fase 4 |
|---------|--------|--------|--------|--------|--------|
| Arquivos Python | 42 | ~60 | ~80 | ~100 | ~110 |
| Testes E2E | 11 | ~25 | ~40 | ~55 | ~65 |
| Cobertura (%) | - | 60% | 70% | 80% | 85% |
| Entidades | 6 | 6 | 6 | 8 | 8 |
| Bancos suportados | 2 | 2 | 2 | 4 | 4 |
| Plataformas | CLI | CLI+Desktop | CLI+Desktop+Mobile | CLI+Desktop+Mobile | CLI+Desktop+Mobile+Luna |

## Riscos e Mitigações

| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|-----------|
| Flet não atingir 1.0 estável | Média | Alto | Manter CLI funcional como fallback |
| Android 17+ restringir Shizuku | Baixa | Médio | ADB via rede como alternativa |
| finbr/python-bcb descontinuados | Baixa | Médio | Acesso direto à API SGS do BCB |
| Escopo crescer demais | Alta | Alto | Respeitar sprints, não misturar features |

## Diferencial Competitivo

| Característica | Controle de Bordo | Apps de mercado |
|----------------|-------------------|-----------------|
| Código | Open source (GPL-3.0) | Proprietário |
| Dados | Local (SQLite, seu PC) | Cloud (servidor deles) |
| Custo | Gratuito | Assinatura mensal |
| Indicadores BR | Selic, IPCA, CDI direto do BCB | Genéricos ou inexistentes |
| Anti-impulso | Economia comportamental | Alertas simples |
| Automação | Desktop + Mobile integrados | Só mobile |
| Personalização | 100% código Python | Interface limitada |
| Privacidade | Zero telemetria | Coleta de dados |

*"A melhor maneira de prever o futuro é inventá-lo." - Alan Kay*
