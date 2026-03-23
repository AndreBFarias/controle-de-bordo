# Controle de Bordo

**Life Operating System open source, local-first, focado no contexto brasileiro.**

Gestão integrada de finanças pessoais, hábitos, saúde, estudos, escrita e automação de dispositivos. Seus dados ficam no seu computador. Sem cloud, sem assinatura, sem telemetria.

---

## O que é

O Controle de Bordo é um sistema operacional de vida pessoal que funciona como um copiloto digital. Ele integra:

- **Finanças**: Importação de extratos (CSV/OFX), categorização automática, indicadores do BCB (Selic, IPCA, CDI), prevenção de compras impulsivas
- **Metas**: Tracker com KPIs, projeções de prazo, progresso visual
- **Hábitos**: Sistema de streak, frequência configurável, gamificação
- **Saúde**: Hidratação, refeições, exercícios, medicamentos, peso
- **Estudos**: Tracker de cursos (Alura, Coursera, Duolingo), tempo dedicado
- **Escrita**: Monitoramento de progresso em projetos de escrita
- **Automação Desktop**: Bloqueio de distrações, modos de foco (Pop!_OS/GNOME)
- **Automação Mobile**: Controle de apps, notificações push (Android)

## Filosofia

- **Local-first**: SQLite no seu computador. Nenhum dado sai da sua rede
- **Open source**: GPL-3.0. Audite, modifique, contribua
- **Gratuito**: Zero custo, zero assinatura, zero freemium
- **Brasileiro**: Indicadores do BCB, parsers para bancos nacionais, documentação em PT-BR
- **Sem IA obrigatória**: Funciona 100% sem IA. O provedor de IA é opcional e intercambiável

## Instalação

```bash
# Clonar
git clone https://github.com/<USUARIO>/controle-de-bordo.git
cd controle-de-bordo

# Ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar
pip install -e .

# Configurar
cp .env.example .env

# Executar (UI)
flet run src/ui/app.py

# Executar (CLI)
bordo financas resumo
```

### Requisitos

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Python | 3.10 | 3.12+ |
| RAM | 4GB | 8GB+ |
| GPU | - | NVIDIA 4GB+ (para IA local) |
| Sistema | Linux | Pop!_OS/Ubuntu |
| Android | 10+ | 13+ (para Shizuku) |

### Extras opcionais

```bash
# IA via Anthropic API
pip install -e ".[ai-cloud]"

# IA local via Ollama
pip install -e ".[ai-local]"

# Automação desktop (Pop!_OS/GNOME)
pip install -e ".[desktop]"

# Desenvolvimento
pip install -e ".[dev]"
```

## Uso

### CLI

```bash
# Resumo financeiro do mês
bordo financas resumo

# Importar extrato do Nubank
bordo financas importar ~/Downloads/extrato-nubank.csv

# Ver contas a pagar
bordo contas listar

# Indicadores macroeconômicos
bordo macro resumo

# Registrar hábito
bordo habito completar "Duolingo"

# Ver metas
bordo metas listar
```

### Interface Visual (Flet)

```bash
flet run src/ui/app.py
```

## Arquitetura

Arquitetura hexagonal (Ports & Adapters) com domínio isolado:

```
domain/    -> Lógica pura, zero dependência externa
adapters/  -> SQLite, importers CSV/OFX, ntfy.sh, Anthropic/Ollama
ui/        -> Dashboard Flet (desktop + mobile)
events/    -> Event bus pub/sub tipado
mobile/    -> Ponte Android (ADB, Tasker, Shizuku)
```

Detalhes completos em [docs/ARQUITETURA.md](docs/ARQUITETURA.md).

## Documentação

| Documento | Conteúdo |
|-----------|----------|
| [ARQUITETURA.md](docs/ARQUITETURA.md) | Visão geral, diagrama de camadas, stack técnica |
| [FINANCAS.md](docs/FINANCAS.md) | Módulo financeiro, importação, anti-impulso, indicadores |
| [MOBILE.md](docs/MOBILE.md) | Integração Android, Tasker, Shizuku, ntfy.sh |
| [DESKTOP.md](docs/DESKTOP.md) | Automação Pop!_OS, bloqueio de sites, modos de foco |
| [INTEGRACAO_LUNA.md](docs/INTEGRACAO_LUNA.md) | Plano de integração com a Luna |
| [CONTRIBUINDO.md](docs/CONTRIBUINDO.md) | Setup de dev, convenções, como contribuir |

## Integração com Luna

O Controle de Bordo será integrado como módulo da [Luna](https://github.com/<USUARIO>/Luna), assistente de IA local multimodal. O motor de regras (`domain/`) será importável como biblioteca Python, e um adapter traduzirá a interface IModule da Luna.

## Licença

GPL-3.0 - veja [LICENSE](LICENSE).

---

*"O preço da liberdade é a eterna vigilância." - Thomas Jefferson*
