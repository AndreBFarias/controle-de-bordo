# Integração Luna × Controle de Bordo: análise técnica e plano de sprints

O Controle de Bordo pode funcionar como biblioteca standalone e como módulo Luna sem duplicação de código, usando **entry points Python, um event bus bridge bidirecional com EventRegistry e uma migração faseada de JSON para SQLite**. O caminho mais seguro exige resolver infraestrutura de packaging primeiro, depois domínio, depois integração — nessa ordem. A análise identifica cinco gaps técnicos críticos e propõe 20 sprints de 1–2 dias cada para um mês de trabalho full-time, onde cada sprint entrega um artefato testável via `pytest`.

O principal risco deste projeto não é complexidade algorítmica — é acoplamento prematuro. A Luna tem 130+ sprints de código maduro com convenções próprias (event bus `(str, dict)`, JSON storage, module.yaml discovery). O Bordo quer usar Pydantic tipado, SQLite WAL e arquitetura hexagonal. **Forçar um projeto a adotar as convenções do outro vai quebrar ambos.** A solução é tratar a fronteira entre eles como uma API pública: contratos explícitos via `typing.Protocol`, serialização explícita na ponte de eventos, e zero imports cruzados entre domínios.

---

## A arquitetura-alvo resolve cinco incompatibilidades fundamentais

O diagrama mental que deve guiar cada decisão é este: o Bordo é uma **biblioteca Python independente** que expõe um `plugin.py` opcional. A Luna consome esse plugin via entry points. Nunca o contrário.

**Gap 1 — Event bus incompatível.** Luna emite `(event: str, data: dict)`. O Bordo deve emitir `BaseModel` tipado internamente. A solução é um `EventBusBridge` com `EventRegistry` que converte bidirecionalmente usando `model_dump()` e `model_validate()` do Pydantic v2 (implementado em Rust, microsegundos por conversão). O bridge mora no pacote do Bordo dentro de `adapters/luna_bridge.py` e só é importado quando o Bordo detecta que está rodando como módulo Luna. Um guard de reentrância (`_bridging: bool`) impede loops infinitos.

**Gap 2 — Storage divergente.** O life_manager da Luna usa `json.load/json.dump` em arquivos separados (`~/.luna/data/contas.json`, etc.). O Bordo usa SQLite + WAL. A migração segue quatro fases: JSON_ONLY → DUAL_WRITE → DUAL_READ_SQL → SQLITE_ONLY. Um `DualWriteRepository` grava em ambos simultaneamente durante a fase 2 e 3, com validação de integridade via checksums SHA-256. A chave é que o rollback é trivial — basta voltar o `StorageMode` para `JSON_ONLY` e os arquivos originais continuam intactos como backup.

**Gap 3 — Module discovery.** Luna carrega módulos de `src/modules/` e `~/.luna/modules/` via `module.yaml`. O Bordo precisa gerar um `module.yaml` compatível E se registrar via `[project.entry-points."luna.modules"]` no `pyproject.toml`. Isso permite que a Luna descubra o Bordo automaticamente com `importlib.metadata.entry_points(group="luna.modules")` após um simples `pip install controle-de-bordo[luna]`.

**Gap 4 — Duplicação funcional.** O life_manager já tem contas, finanças, metas, peso, água, refeições, remédios. O Bordo quer reimplementar com infraestrutura melhor. A solução correta é: o Bordo se torna o novo backend desses dados. O life_manager delega para o Bordo via Protocol interfaces, e seus widgets Textual continuam funcionando conectados à mesma camada de serviço — agora alimentada por SQLite em vez de JSON.

**Gap 5 — Packaging.** O `pyproject.toml` do Bordo precisa usar **hatchling** como build backend (melhor suporte a plugins e configurabilidade em 2025-2026), src-layout, optional dependencies para CLI (`[cli]`) e para Luna (`[luna]`), e entry points tanto para `[project.scripts]` (CLI standalone) quanto para `[project.entry-points."luna.modules"]` (plugin).

---

## O pyproject.toml que governa tudo

A estrutura de diretórios alvo e o packaging determinam como todo o resto se encaixa:

```
controle-de-bordo/
├── pyproject.toml
├── CLAUDE.md                    # Governança para Claude Code
├── src/
│   └── bordo/
│       ├── __init__.py          # API pública: entidades, serviços, ports
│       ├── __main__.py          # python -m bordo
│       ├── cli.py               # Typer CLI (dep opcional)
│       ├── plugin.py            # Adapter Luna (dep opcional)
│       ├── config.py            # Config dual-mode (standalone vs plugin)
│       ├── bootstrap.py         # Composition roots
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── entities.py      # Transaction, Goal, Habit, etc. (Pydantic)
│       │   ├── events.py        # Eventos tipados (BaseModel)
│       │   ├── services.py      # FinancialEngine, GoalTracker, etc.
│       │   └── ports.py         # IStorage, INotifier, IEventBus (Protocol)
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── sqlite_store.py  # SQLite + WAL
│       │   ├── json_store.py    # Compat com life_manager JSON
│       │   ├── luna_bridge.py   # EventBusBridge
│       │   ├── nubank_csv.py    # Importador CSV Nubank
│       │   ├── ofx_parser.py    # Importador OFX
│       │   └── flet_ui/         # Interface Flet
│       └── migrations/
│           ├── __init__.py
│           └── json_to_sqlite.py
├── module.yaml                  # Manifesto para Luna
└── tests/
    ├── test_domain/
    ├── test_adapters/
    ├── test_bridge/
    └── test_migration/
```

O `pyproject.toml` essencial:

```toml
[build-system]
requires = ["hatchling >= 1.26"]
build-backend = "hatchling.build"

[project]
name = "controle-de-bordo"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pydantic>=2.0", "aiosqlite>=0.20"]

[project.optional-dependencies]
cli = ["typer>=0.12", "rich>=13.0"]
luna = []  # Sem deps extras — Luna injeta seus próprios adapters
flet = ["flet>=0.80"]
dev = ["pytest>=8.0", "pytest-asyncio", "mypy>=1.8"]
all = ["controle-de-bordo[cli,flet]"]

[project.scripts]
bordo = "bordo.cli:app"

[project.entry-points."luna.modules"]
controle-de-bordo = "bordo.plugin:BordoLunaPlugin"

[tool.hatch.build.targets.wheel]
packages = ["src/bordo"]
```

A decisão de usar **hatchling** sobre setuptools é deliberada: suporte nativo a PEP 660 (editable installs), build hooks para gerar `module.yaml`, e 6.5% de market share crescente com excelente documentação. O `extras_require` com `[luna]` vazio é intencional — quando rodando como plugin Luna, quem provê os adapters de infra (event bus, storage host) é a própria Luna via dependency injection.

---

## O event bus bridge em detalhe técnico

O componente mais crítico da integração é o `EventBusBridge`. Ele precisa ser **bidirecional**, **tolerante a falhas**, e **sem loops**:

```python
# bordo/adapters/luna_bridge.py
class EventRegistry:
    """Mapa bidirecional: nome_string  Type[BaseModel]"""
    def register(self, name: str, event_type: Type[BaseModel]) -> None: ...
    def auto_register(self, event_type: Type[BaseModel]) -> None:
        # TransactionCreated → "bordo.transaction_created"
        name = f"bordo.{camel_to_snake(event_type.__name__)}"
        self.register(name, event_type)

class EventBusBridge:
    def __init__(self, luna_bus, bordo_bus, registry):
        self._luna = luna_bus      # emit(str, dict) / on(str, cb)
        self._bordo = bordo_bus    # emit(BaseModel) / on(Type, cb)
        self._registry = registry
        self._bridging = False     # Guard contra reentrância

    def connect(self):
        for name, etype in self._registry:
            self._bordo.on(etype, self._make_typed_handler(name))
            self._luna.on(name, self._make_dict_handler(etype))
```

A conversão usa **`model_dump()`** (Pydantic → dict, para Luna consumir) e **`model_validate()`** (dict → Pydantic, para Bordo consumir). Ambas são operações O(μs) graças ao core Rust do Pydantic v2. O prefixo `bordo.` nos nomes de eventos evita colisões com eventos nativos da Luna.

---

## Migração JSON → SQLite em quatro fases com rollback garantido

A migração nunca deve ser big-bang. O padrão de **dual-write progressivo** garante que a qualquer momento o desenvolvedor pode voltar atrás:

**Fase 1 (JSON_ONLY):** Estado atual. Dados vivem em `~/.luna/data/*.json`. Nenhuma mudança.

**Fase 2 (DUAL_WRITE):** Toda escrita vai para JSON E SQLite. Leitura continua do JSON. Isso permite validar que o SQLite está recebendo dados corretos sem afetar a aplicação. Duração recomendada: 3-5 dias de uso real.

**Fase 3 (DUAL_READ_SQL):** Escrita continua dual. Leitura muda para SQLite. O JSON vira backup implícito. Se algo quebrar, basta voltar para Fase 2.

**Fase 4 (SQLITE_ONLY):** JSON files são arquivados (não deletados). O `DualWriteRepository` é substituído pelo `SQLiteStore` direto. Performance melhora pois elimina I/O duplo.

A implementação usa um `StorageMode` enum e um `DualWriteRepository` que encapsula ambos os backends atrás da mesma `IStorage` Protocol. O SQLite é configurado com **WAL mode** (`PRAGMA journal_mode=WAL`), que permite leituras concorrentes durante escritas — essencial para quando a TUI da Luna e o CLI do Bordo acessam os mesmos dados simultaneamente.

Antes de qualquer migração, um backup atômico é criado usando `sqlite3.Connection.backup()` (Python 3.7+) para o banco existente e `shutil.copytree()` para os JSONs, com checksums SHA-256 em um `manifest.json` para validação posterior.

---

## Arquitetura de UI: Textual e Flet coexistem via ViewModel compartilhado

Textual (TUI da Luna) e Flet (GUI planejada do Bordo) **não podem rodar na mesma janela** — Textual renderiza escape codes no terminal, Flet usa Flutter engine em janela nativa. Mas podem compartilhar 100% da lógica de negócio via um **ViewModel UI-agnóstico**.

O padrão é: `bordo/domain/services.py` contém lógica pura. `bordo/viewmodels.py` expõe estado como `Observable[T]` com `.subscribe(callback)`. A TUI Textual e a GUI Flet cada uma implementam seus próprios bindings ao ViewModel. O entry point do Bordo aceita `--ui tui` ou `--ui flet` para escolher frontend.

Para o contexto Luna, os widgets Textual do life_manager podem ser migrados para consumir o ViewModel do Bordo em vez de ler JSON diretamente. O padrão de **widget slots** da Luna (Containers com IDs como `#plugin-slot-main`) permite que o Bordo registre seus widgets via `WidgetRegistry` — descobertos por entry points ou por module.yaml.

---

## Plano de sprints: 20 sprints em 4 semanas

O plano segue a ordem: **Infraestrutura → Domínio → Standalone → Integração → UI → Polish**. Cada sprint tem 1-2 dias e entrega um artefato testável. Os comandos de teste estão incluídos para execução direta via Claude Code.

### Semana 1 — Fundação (S01–S05)

**S01 · Scaffolding e pyproject.toml (dia 1)**
Criar estrutura de diretórios completa, `pyproject.toml` com hatchling, `CLAUDE.md` com regras de estilo e comandos. Configurar `pytest`, `mypy`, e `ruff`. Verificar: `pip install -e ".[dev]"` funciona, `pytest` roda sem erros, `mypy src/` passa limpo.
- Arquivo: `pyproject.toml`, `src/bordo/__init__.py`, `CLAUDE.md`
- Teste: `pip install -e ".[dev]" && pytest --co -q` lista 0 erros
- Critério de pronto: `python -c "import bordo; print(bordo.__version__)"` imprime `0.1.0`

**S02 · Domain entities com Pydantic (dia 2)**
Implementar as 6 entidades em `domain/entities.py`: `Transaction`, `Bill`, `Goal`, `Habit`, `HealthRecord`, `StudySession`. Cada uma com `model_dump()` e `model_validate()` testados. Incluir `domain/events.py` com eventos tipados: `TransactionCreated`, `GoalUpdated`, `HabitCompleted`, etc.
- Teste: `pytest tests/test_domain/test_entities.py` — serialização roundtrip para cada entidade
- Critério: cada entidade sobrevive `model_validate(entity.model_dump())` sem perda de dados

**S03 · Ports e protocols (dia 3)**
Definir em `domain/ports.py` os contratos: `IStorage`, `INotifier`, `IAIProvider`, `IBankImporter`, `IEventBus`. Todos como `typing.Protocol` com `@runtime_checkable`. Incluir testes que verificam que classes stub satisfazem cada Protocol.
- Teste: `pytest tests/test_domain/test_ports.py` — `isinstance(StubStorage(), IStorage)` retorna `True`
- Critério: `mypy --strict src/bordo/domain/` passa sem erros

**S04 · Event bus interno tipado (dia 4)**
Implementar `BordoEventBus` em `domain/event_bus.py` com interface `emit(event: BaseModel)` / `on(event_type: Type[BaseModel], callback)`. Síncrono, sem threading (Luna é single-thread por módulo). Incluir suporte a wildcard handler para debug.
- Teste: `pytest tests/test_domain/test_event_bus.py` — emit+receive, múltiplos handlers, sem crosstalk
- Critério: 100% coverage no event bus

**S05 · SQLite adapter com WAL (dia 5)**
Implementar `adapters/sqlite_store.py` que satisfaz `IStorage`. Configurar WAL, synchronous=NORMAL, foreign_keys=ON. Usar `PRAGMA user_version` para controle de schema. Incluir método `backup()` usando `sqlite3.Connection.backup()`.
- Teste: `pytest tests/test_adapters/test_sqlite.py` — CRUD completo, WAL ativo, backup funciona
- Critério: `PRAGMA journal_mode` retorna `wal`, dados persistem entre conexões

### Semana 2 — Serviços e standalone (S06–S10)

**S06 · FinancialEngine + importadores (dias 6-7)**
Implementar `domain/services.py::FinancialEngine` com lógica de categorização de transações. Implementar `adapters/nubank_csv.py` e `adapters/ofx_parser.py` satisfazendo `IBankImporter`. O motor recebe transações normalizadas e calcula balanços, médias e tendências.
- Teste: `pytest tests/test_domain/test_financial.py` — importação de CSV fixture, cálculo de balanço correto
- Critério: importar CSV Nubank real (fixture anonimizada) e validar totais

**S07 · ImpulseFilter e GoalTracker (dia 8)**
Implementar motor anti-impulso: regra de 24h, custo-de-oportunidade (quanto uma compra atrasa a meta do apartamento), e score de fricção. GoalTracker monitora KPIs (economia, streak Duolingo, sessões de estudo, peso).
- Teste: `pytest tests/test_domain/test_impulse.py` — cenários de compra aprovada/bloqueada
- Critério: compra de R$500 com meta de apartamento ativa retorna score de impacto

**S08 · CLI Typer completo (dia 9)**
Implementar `cli.py` com comandos: `bordo import <csv>`, `bordo balance`, `bordo goals`, `bordo impulse-check <valor> <categoria>`, `bordo habits`. Usar `bootstrap.py` para composition root standalone (injeta SQLiteStore).
- Teste: `pytest tests/test_cli.py` usando `typer.testing.CliRunner`
- Critério: `bordo import fixtures/nubank.csv && bordo balance` mostra saldo correto

**S09 · Config dual-mode e bootstrap (dia 10)**
Implementar `config.py` com `BordoConfig` (dataclass) que carrega de `~/.config/bordo/config.toml` (standalone) ou recebe dict do host (plugin). `bootstrap.py` com dois composition roots: `create_standalone()` e `create_luna_plugin(host_context)`. Detecção automática de modo via `importlib.metadata`.
- Teste: `pytest tests/test_config.py` — config standalone carrega TOML, config plugin aceita dict
- Critério: `detect_mode()` retorna `"standalone"` quando Luna não está instalada

**S10 · JSON adapter compat (dia 11)**
Implementar `adapters/json_store.py` que satisfaz `IStorage` mas lê/escreve no formato exato do life_manager da Luna (`json.load/json.dump`, um arquivo por entidade). Isso permite que o Bordo leia dados existentes do life_manager sem migração.
- Teste: `pytest tests/test_adapters/test_json_compat.py` — fixtures com formato real do life_manager
- Critério: dados salvos pelo json_store são legíveis pelo life_manager original e vice-versa

### Semana 3 — Integração Luna (S11–S15)

**S11 · EventBusBridge bidirecional (dias 12-13)**
Implementar `adapters/luna_bridge.py` com `EventRegistry`, `EventBusBridge`, guard de reentrância, e logging de eventos não-registrados. Registrar todos os eventos do Bordo com prefixo `bordo.`. Incluir `GenericEvent(BaseModel)` como fallback para eventos Luna sem tipo.
- Teste: `pytest tests/test_bridge/test_event_bridge.py` — Luna→Bordo, Bordo→Luna, sem loop infinito, eventos desconhecidos não crasham
- Critério: 100% coverage no bridge, zero loops em teste de stress com 1000 eventos

**S12 · Plugin Luna completo (dia 14)**
Implementar `plugin.py::BordoLunaPlugin` que satisfaz o `IModule` protocol da Luna. Incluir `module.yaml` com metadata, dependências, e slot registration. O plugin usa `create_luna_plugin()` do bootstrap, recebe `ModuleContext` da Luna, e wira o EventBusBridge.
- Teste: `pytest tests/test_bridge/test_luna_plugin.py` — plugin inicializa com ModuleContext mock, registra handlers no event bus Luna mock
- Critério: `pip install -e ".[luna]"` + simular discovery via entry points funciona

**S13 · Migração JSON→SQLite faseada (dias 15-16)**
Implementar `migrations/json_to_sqlite.py` com `MigrationManager`, `DataMigrator`, `DualWriteRepository`, e os 4 `StorageMode`. Incluir CLI command `bordo migrate --phase dual-write|dual-read-sql|sqlite-only|rollback`. Backup automático antes de cada mudança de fase.
- Teste: `pytest tests/test_migration/` — idempotência (rodar 2x = mesmo resultado), integridade (SHA-256 match), rollback funciona
- Critério: migrar fixture de 1000 registros JSON, validar contagem e checksums no SQLite, voltar para JSON e verificar integridade

**S14 · Contract tests compartilhados (dia 17)**
Criar `tests/contracts/` com test base classes que validam os Protocol contracts. Rodar contra implementações Luna mock E contra implementações Bordo reais. Configurar `mypy --strict` no CI para detectar violações de Protocol estaticamente.
- Teste: `pytest tests/contracts/` — todas implementações passam contract tests
- Critério: `mypy --strict src/` passa sem erros de Protocol

**S15 · Integração end-to-end Luna (dia 18)**
Teste de integração completo: Luna inicializa → descobre Bordo via entry points → carrega plugin → bridge conecta event buses → transação importada no Bordo aparece como evento na Luna → life_manager TUI widget mostra dados do SQLite via Bordo.
- Teste: `pytest tests/test_integration/test_e2e_luna.py` — fluxo completo com Luna test harness
- Critério: evento emitido no Bordo chega na Luna E vice-versa em menos de 10ms

### Semana 4 — UI e polish (S16–S20)

**S16 · ViewModels UI-agnósticos (dia 19)**
Implementar `viewmodels.py` com `Observable[T]`, `FinanceViewModel`, `GoalsViewModel`, `HabitsViewModel`. Cada ViewModel expõe estado como observáveis e métodos de ação async. Zero imports de Textual ou Flet.
- Teste: `pytest tests/test_viewmodels.py` — subscribe recebe notificação após mudança de estado
- Critério: nenhum import de framework UI em `viewmodels.py`

**S17 · Widgets Textual para Luna (dia 20)**
Implementar widgets Textual em `adapters/textual_widgets/` que consomem ViewModels: `FinanceDashboard`, `GoalProgress`, `HabitTracker`. Registrar no `WidgetRegistry` da Luna via plugin. Usar Container slots para posicionamento.
- Teste: `pytest tests/test_adapters/test_textual.py` usando `textual.testing.App`
- Critério: widget renderiza dados do ViewModel corretamente em app Textual de teste

**S18 · Interface Flet standalone (dias 21-22)**
Implementar `adapters/flet_ui/` com views Flet que consomem os mesmos ViewModels: dashboard financeiro, metas, hábitos. Entry point: `bordo --ui flet` lança janela Flet.
- Teste: smoke test manual + teste de ViewModel binding unitário
- Critério: `bordo --ui flet` abre janela com dados reais do SQLite

**S19 · MacroIndicators e NudgeEngine (dia 23)**
Implementar integração com indicadores macro (Selic, IPCA via API BCB/`python-bcb`). NudgeEngine gera lembretes contextuais baseados em regras: hidratação, medicamentos, pausa para exercício, gating estudo→jogo.
- Teste: `pytest tests/test_domain/test_nudge.py` — cenários de nudge ativado/silenciado
- Critério: NudgeEngine com 5+ regras configuráveis, MacroIndicators com dados reais da API BCB

**S20 · CI, documentação e release (dia 24-25)**
Configurar GitHub Actions com: lint (ruff), type check (mypy --strict), testes unitários, testes de integração, testes de contrato. Escrever README com quickstart standalone e quickstart Luna. Criar `bordo --version` e tag v0.1.0.
- Teste: CI pipeline verde end-to-end
- Critério: `pip install controle-de-bordo[all]` funciona do PyPI test, CI 100% verde

---

## Ordem de dependência e caminho crítico

O caminho crítico é: **S01 → S02 → S03 → S04 → S05 → S08 (standalone funcional)**. A partir de S08, o Bordo já funciona sozinho como CLI. A integração Luna (S11-S15) depende de S04 (event bus) e S10 (JSON compat) estarem prontos. O UI (S16-S18) depende de S06-S07 (serviços) estarem prontos.

Sprints que podem ser feitos em paralelo (se o dev quiser alternar por fadiga):
- S06 e S07 são independentes entre si
- S10 pode ser feito em paralelo com S06-S08
- S16 pode começar assim que S06-S07 terminarem
- S19 é independente de S11-S15

**Regra de ouro para cada sprint:** começar implementando o teste primeiro (TDD), depois a implementação. O Claude Code CLI executa melhor quando recebe `pytest tests/test_X.py` como critério de sucesso explícito.

---

## Decisões técnicas que evitam retrabalho futuro

**Hatchling sobre setuptools.** O setuptools domina 79% do mercado mas por inércia. Hatchling tem suporte superior a PEP 660 (editable installs obrigatórios desde pip 25.0), build hooks nativos, e configuração mais limpa. Para um projeto greenfield em 2026, é a escolha que minimiza dívida técnica.

**Protocols sobre ABCs.** O Bordo define contratos como `typing.Protocol` (PEP 544), não como `abc.ABC`. Isso significa que a Luna não precisa herdar de nada do Bordo — basta implementar os métodos corretos (structural subtyping). Isso elimina acoplamento de importação entre os dois projetos.

**`PRAGMA user_version` sobre Alembic.** Para um projeto pessoal com SQLite local, Alembic é overkill. O `user_version` do SQLite é um inteiro atômico que rastreia versão de schema. O `sqlite_store.py` verifica na conexão e aplica migrations incrementais. Simples, zero dependências extras, impossível de corromper.

**Observable pattern caseiro sobre biblioteca.** As alternativas (py-mvvm, GSO, RxPY) adicionam dependências e complexidade. Um `Observable[T]` com 30 linhas de código é suficiente para sincronizar estado entre ViewModels e UIs. Se escalar, migrar para algo como `reactivex` é trivial porque a interface é a mesma.

**Prefixo `bordo.` em eventos.** Todos os eventos que cruzam o bridge levam prefixo: `bordo.transaction_created`, `bordo.goal_updated`. Isso previne colisão de nomes com os 130+ sprints de eventos já existentes na Luna. A Luna mantém seu namespace intacto.

---

## O que pode dar errado e como mitigar

O risco número um é **scope creep** — o Bordo planeja integração com Android (Shizuku), Google Fit, Pluggy API, sync de casal via CRDTs. Nenhuma dessas features deve entrar no primeiro mês. As 20 sprints cobrem o núcleo: finanças, metas, hábitos, integração Luna, duas UIs. Tudo o mais é pós-v0.1.0.

O risco número dois é **o life_manager da Luna ser mais acoplado do que o esperado.** Se os widgets do life_manager fazem `json.load()` diretamente (em vez de passar por uma abstração), a migração vai exigir refatorar código Luna — o que é arriscado em um projeto com 2500+ arquivos. A sprint S10 (JSON compat adapter) mitiga isso: o Bordo finge ser JSON files para o life_manager enquanto a migração acontece por baixo.

O risco número três é **Flet ainda ser pré-1.0.** A API do Flet está mudando (declarativa com `@ft.component` no 1.0 beta). A sprint S18 deve usar a API imperativa atual (estável) e isolar todo código Flet em `adapters/flet_ui/`. Se o Flet quebrar numa atualização, só essa pasta precisa mudar — os ViewModels ficam intactos.

## Conclusão

A integração exige disciplina arquitetural mais do que talento técnico. O Bordo deve nascer como **biblioteca-primeiro, aplicação-segundo** — expondo `domain/` e `ports.py` como API pública limpa. A Luna consome via entry points e Protocol contracts, sem imports diretos. O event bus bridge e a migração faseada são os dois componentes mais complexos, mas com os contract tests e a estratégia de dual-write, ambos são reversíveis a qualquer momento. O mês de férias é suficiente se o desenvolvedor resistir à tentação de adicionar features antes da infraestrutura estar sólida — as primeiras 5 sprints são fundação pura, sem funcionalidade visível, e são as mais importantes de todas.
