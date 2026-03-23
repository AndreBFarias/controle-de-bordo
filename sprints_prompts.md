# Controle de Bordo — 20 Prompts para Claude Code CLI

> Copie e cole cada prompt no terminal do Claude Code.
> Sempre espere o plano (`/plan`) antes de aprovar a execução.
> Após cada sprint, rode os comandos de verificação listados.

---

## S01 · Scaffolding e pyproject.toml

```
Leia o arquivo review.md na raiz do projeto. Ele contém a análise técnica completa e o plano de 20 sprints para o Controle de Bordo.

Sua tarefa é executar a Sprint S01 (Scaffolding e pyproject.toml).

Siga EXATAMENTE a estrutura de diretórios e o pyproject.toml descrito no review.md. O código existente em src/ NÃO deve ser movido nem deletado — ele será migrado nas sprints seguintes.

Entregáveis:
1. Estrutura de diretórios src/bordo/ completa com __init__.py em cada pacote
2. Todos os módulos placeholder com docstring mínima (sem lógica)
3. pyproject.toml reescrito com hatchling como build backend
4. CLAUDE.md atualizado referenciando review.md
5. pytest, mypy, ruff configurados para o novo layout
6. Estrutura tests/test_domain/, test_adapters/, test_bridge/, test_migration/

Critério de pronto:
  pip install -e ".[dev]"
  python -c "import bordo; print(bordo.__version__)"  # imprime 0.1.0
  pytest --co -q  # 0 erros de coleta
  mypy src/bordo/  # passa limpo
  ruff check src/bordo/  # passa limpo

Use /plan antes de começar.
```

---

## S02 · Domain entities com Pydantic

```
Leia review.md. Execute a Sprint S02 (Domain entities com Pydantic).

Implementar em src/bordo/domain/entities.py as 6 entidades Pydantic:
- Transaction (date, description, amount, type, category, bank)
- Bill (name, amount, due_date, category, paid, paid_at)
- Goal (name, target_value, current_value, deadline, category)
- Habit (name, frequency, streak, last_completed, category)
- HealthRecord (date, weight, water_cups, meals, medications, notes)
- StudySession (date, subject, duration_minutes, platform, notes)

Cada entidade deve ter:
- Tipos Python corretos com type hints
- Enums onde fizer sentido (TransactionType, TransactionCategory, BillStatus, etc.)
- Método to_storage_dict() e from_storage_dict() (ou usar model_dump/model_validate)
- Campo id: int | None = None (gerado pelo storage)
- Campo created_at com default datetime.now()

Implementar em src/bordo/domain/events.py os eventos tipados (BaseModel):
- TransactionCreated, TransactionDeleted
- BillPaid, BillDue
- GoalUpdated, GoalMilestone
- HabitCompleted, HabitStreakBroken
- NudgeTriggered

Criar testes em tests/test_domain/test_entities.py:
- Serialização roundtrip (model_validate(entity.model_dump())) para cada entidade
- Validação de campos obrigatórios
- Enums aceitos e rejeitados

Critério de pronto:
  pytest tests/test_domain/test_entities.py -v  # tudo verde
  mypy src/bordo/domain/entities.py --strict  # passa limpo

Use /plan antes de começar.
```

---

## S03 · Ports e protocols

```
Leia review.md. Execute a Sprint S03 (Ports e protocols).

Implementar em src/bordo/domain/ports.py os contratos com typing.Protocol e @runtime_checkable:

1. IStorage — CRUD genérico:
   - initialize() -> None
   - insert(table: str, data: dict) -> int
   - update(table: str, record_id: int, data: dict) -> bool
   - delete(table: str, record_id: int) -> bool
   - get_by_id(table: str, record_id: int) -> dict | None
   - query(table: str, filters: dict | None, order_by: str | None, limit: int | None) -> list[dict]
   - count(table: str, filters: dict | None) -> int
   - backup(path: Path) -> None

2. INotifier:
   - notify(title: str, message: str, urgency: str) -> bool

3. IAIProvider:
   - analyze(prompt: str, context: str) -> str
   - categorize(description: str) -> str

4. IBankImporter:
   - import_file(path: Path) -> list[Transaction]
   - supported_formats() -> list[str]

5. IEventBus:
   - emit(event: BaseModel) -> None
   - on(event_type: type[BaseModel], callback: Callable) -> None
   - off(event_type: type[BaseModel], callback: Callable) -> None

Criar testes em tests/test_domain/test_ports.py:
- Classes stub mínimas que implementam cada Protocol
- isinstance(StubStorage(), IStorage) retorna True para cada um
- Classe que NÃO implementa um método -> isinstance retorna False

Critério de pronto:
  pytest tests/test_domain/test_ports.py -v  # tudo verde
  mypy src/bordo/domain/ --strict  # passa limpo

Use /plan antes de começar.
```

---

## S04 · Event bus interno tipado

```
Leia review.md. Execute a Sprint S04 (Event bus interno tipado).

Implementar BordoEventBus em src/bordo/domain/event_bus.py que satisfaz IEventBus:
- emit(event: BaseModel) — publica evento para todos os handlers do tipo
- on(event_type: Type[BaseModel], callback) — registra handler
- off(event_type: Type[BaseModel], callback) — remove handler
- Síncrono (sem threading)
- Logging de eventos emitidos e handlers chamados
- Handler de wildcard para debug (recebe TODOS os eventos)
- Tratamento de exceção: handler que falha NÃO impede outros handlers de rodar

Criar testes em tests/test_domain/test_event_bus.py:
- emit + receive funciona
- Múltiplos handlers para mesmo tipo
- Handler de um tipo NÃO recebe evento de outro tipo
- Handler que levanta exceção não impede outros
- off() remove handler corretamente
- Wildcard handler recebe todos os eventos
- emit sem handlers registrados não falha

Critério de pronto:
  pytest tests/test_domain/test_event_bus.py -v  # tudo verde
  pytest tests/test_domain/test_event_bus.py --cov=src/bordo/domain/event_bus --cov-report=term  # 100% coverage

Use /plan antes de começar.
```

---

## S05 · SQLite adapter com WAL

```
Leia review.md. Execute a Sprint S05 (SQLite adapter com WAL).

Implementar SQLiteStore em src/bordo/adapters/sqlite_store.py que satisfaz IStorage:
- Conexão com PRAGMA journal_mode=WAL, synchronous=NORMAL, foreign_keys=ON
- PRAGMA user_version para controle de schema (sem Alembic)
- Schema migration automática: ao conectar, verifica user_version e aplica DDL incremental
- Tabelas para todas as 6 entidades (transactions, bills, goals, habits, health_records, study_sessions)
- Método backup() usando sqlite3.Connection.backup()
- Context manager para transações
- Thread-safe (check_same_thread=False para WAL)

Criar testes em tests/test_adapters/test_sqlite.py:
- CRUD completo para cada tabela
- PRAGMA journal_mode retorna 'wal'
- Schema migration: abrir com version 0 cria tabelas, abrir de novo não recria
- backup() cria arquivo funcional
- Dados persistem entre conexões
- Transação com rollback funciona

Critério de pronto:
  pytest tests/test_adapters/test_sqlite.py -v  # tudo verde
  mypy src/bordo/adapters/sqlite_store.py --strict  # passa

Use /plan antes de começar.
```

---

## S06 · FinancialEngine + importadores

```
Leia review.md. Execute a Sprint S06 (FinancialEngine + importadores).

Implementar em src/bordo/domain/services.py a classe FinancialEngine:
- add_transaction() com categorização automática por palavras-chave
- get_balance(period) — saldo por período
- get_summary(month, year) — receitas, despesas, saldo, top categorias
- get_spending_trend(months) — média de gastos por categoria nos últimos N meses
- Recebe IStorage e IEventBus via construtor (dependency injection)
- Emite TransactionCreated via event bus ao adicionar transação

Implementar importadores que satisfazem IBankImporter:
- src/bordo/adapters/nubank_csv.py — parseia CSV do Nubank
- src/bordo/adapters/ofx_parser.py — parseia OFX genérico

Categorização automática em um dicionário de regras:
- ALIMENTACAO: ifood, restaurante, padaria, mercado, supermercado...
- TRANSPORTE: uber, 99, combustivel, estacionamento...
- MORADIA: aluguel, condominio, energia, agua, internet...
- (pelo menos 8 categorias)

Criar tests/test_domain/test_financial.py e tests/test_adapters/test_importers.py:
- Importar CSV fixture anonimizado e validar totais
- Categorização automática correta para 10+ descrições
- get_balance retorna valor correto após N transações
- get_summary agrupa corretamente por categoria

Criar tests/fixtures/nubank_sample.csv com dados fictícios (10-20 linhas).

Critério de pronto:
  pytest tests/test_domain/test_financial.py tests/test_adapters/test_importers.py -v  # tudo verde

Use /plan antes de começar.
```

---

## S07 · ImpulseFilter e GoalTracker

```
Leia review.md. Execute a Sprint S07 (ImpulseFilter e GoalTracker).

Implementar em src/bordo/domain/services.py:

ImpulseFilter:
- check_purchase(amount, category, description) -> ImpulseResult
- ImpulseResult com: approved (bool), score (0-100), reasons (list[str]), opportunity_cost (str)
- Regras configuráveis:
  * Regra 24h: compras acima de X requerem espera
  * Custo-oportunidade: "essa compra atrasa sua meta [apartamento] em N dias"
  * Categoria proibida: bloquear categorias em certos horários
  * Limite mensal por categoria
- Recebe IStorage para consultar metas e histórico

GoalTracker:
- add_goal(), update_progress(), get_goals()
- calculate_projection(goal) — data estimada de conclusão baseada em ritmo atual
- link_transactions(goal) — vincular transações a metas financeiras
- get_milestone_alerts() — notificar quando atingir 25%, 50%, 75%, 100%
- Emite GoalUpdated e GoalMilestone via event bus

Criar tests/test_domain/test_impulse.py e tests/test_domain/test_goals.py:
- Compra de R$500 com meta ativa retorna score de impacto
- Compra abaixo do threshold é aprovada automaticamente
- GoalTracker calcula projeção correta
- Milestone emitido ao cruzar 50%

Critério de pronto:
  pytest tests/test_domain/test_impulse.py tests/test_domain/test_goals.py -v  # tudo verde

Use /plan antes de começar.
```

---

## S08 · CLI Typer completo

```
Leia review.md. Execute a Sprint S08 (CLI Typer completo).

Implementar src/bordo/cli.py com Typer:

Comandos:
- bordo import <arquivo> — importa CSV/OFX e mostra resumo
- bordo balance [--month M] [--year Y] — saldo do período
- bordo summary [--month M] — resumo financeiro com categorias
- bordo impulse-check <valor> <categoria> — verifica compra contra metas
- bordo goals — lista metas com progresso
- bordo goal add <nome> <valor-alvo> <prazo> — adiciona meta
- bordo habits — lista hábitos com streaks
- bordo habit done <nome> — marca hábito como feito
- bordo health — resumo de saúde
- bordo version — versão do bordo

Implementar src/bordo/bootstrap.py:
- create_standalone() -> dict com todas as dependências injetadas
  (SQLiteStore, BordoEventBus, FinancialEngine, ImpulseFilter, GoalTracker)
- Caminho do DB: ~/.config/bordo/bordo.db (respeitar XDG)
- Criar diretório se não existir

Implementar src/bordo/__main__.py para suportar python -m bordo.

Criar tests/test_cli.py usando typer.testing.CliRunner:
- bordo version retorna 0.1.0
- bordo import com fixture CSV funciona
- bordo balance após import mostra saldo correto
- bordo impulse-check retorna resultado formatado

Critério de pronto:
  pytest tests/test_cli.py -v  # tudo verde
  pip install -e ".[cli]"
  bordo version  # imprime 0.1.0

Use /plan antes de começar.
```

---

## S09 · Config dual-mode e bootstrap

```
Leia review.md. Execute a Sprint S09 (Config dual-mode e bootstrap).

Implementar src/bordo/config.py:

BordoConfig (dataclass ou Pydantic BaseSettings):
- db_path: Path (default ~/.config/bordo/bordo.db)
- config_dir: Path (default ~/.config/bordo/)
- currency: str (default "BRL")
- impulse_threshold: float (default 100.0)
- impulse_cooldown_hours: int (default 24)
- log_level: str (default "INFO")

Carregamento:
- Standalone: lê de ~/.config/bordo/config.toml (cria default se não existir)
- Plugin Luna: recebe dict do ModuleContext da Luna
- detect_mode() -> "standalone" | "luna" (checa se bordo.plugin está em contexto Luna)

Atualizar src/bordo/bootstrap.py:
- create_standalone(config: BordoConfig | None = None) — usa config ou carrega default
- create_luna_plugin(host_context: dict) — recebe contexto Luna e cria dependências

Criar tests/test_config.py:
- Config standalone carrega TOML
- Config com valores custom via TOML
- Config plugin aceita dict
- detect_mode retorna "standalone" quando Luna não instalada
- Config default cria arquivo TOML se não existir

Critério de pronto:
  pytest tests/test_config.py -v  # tudo verde

Use /plan antes de começar.
```

---

## S10 · JSON adapter compatível com life_manager

```
Leia review.md. Execute a Sprint S10 (JSON adapter compatível com life_manager Luna).

Implementar src/bordo/adapters/json_store.py que satisfaz IStorage:
- Lê/escreve no formato EXATO do life_manager da Luna
- Um arquivo JSON por "tabela" (contas.json, transactions.json, goals.json, etc.)
- Estrutura de dados compatível com LifeStorage da Luna:
  * Lista de dicts com campo "id" inteiro
  * Datas como strings ISO
  * Encoding UTF-8 com ensure_ascii=False e indent=2
- _next_id() gera IDs incrementais (max existente + 1)
- Thread-safe via file lock (fcntl ou portalocker)

Este adapter permite que o Bordo LEIA dados existentes do life_manager da Luna sem nenhuma migração. É a ponte de compatibilidade.

Criar tests/test_adapters/test_json_compat.py:
- CRUD completo funciona
- Formato de saída é idêntico ao do life_manager Luna (comparar JSON byte a byte)
- Dados salvos pelo json_store são legíveis por json.load() puro
- Arquivo inexistente retorna lista/dict vazio (não crasheia)
- IDs são gerados corretamente

Criar tests/fixtures/luna_life_manager/ com JSONs de exemplo no formato Luna.

Critério de pronto:
  pytest tests/test_adapters/test_json_compat.py -v  # tudo verde

Use /plan antes de começar.
```

---

## S11 · EventBusBridge bidirecional

```
Leia review.md. Execute a Sprint S11 (EventBusBridge bidirecional).

Este é o componente MAIS CRÍTICO da integração. Leia a seção "O event bus bridge em detalhe técnico" do review.md com atenção.

Implementar em src/bordo/adapters/luna_bridge.py:

EventRegistry:
- register(name: str, event_type: Type[BaseModel]) — mapeia string  tipo
- auto_register(event_type: Type[BaseModel]) — gera nome automático com prefixo "bordo."
  (TransactionCreated → "bordo.transaction_created")
- get_type(name: str) -> Type[BaseModel] | None
- get_name(event_type: Type[BaseModel]) -> str | None
- Registrar TODOS os eventos de domain/events.py automaticamente

EventBusBridge:
- __init__(luna_bus, bordo_bus, registry)
- connect() — registra handlers nos dois buses
- disconnect() — remove handlers
- _bridging: bool — guard contra reentrância (loop infinito)
- Luna→Bordo: recebe (str, dict), converte para BaseModel via model_validate(), emite no bordo_bus
- Bordo→Luna: recebe BaseModel, converte para dict via model_dump(), emite no luna_bus com nome string
- Eventos desconhecidos são logados mas NÃO crasheiam
- GenericEvent(BaseModel) como fallback para eventos Luna sem tipo mapeado

Criar tests/test_bridge/test_event_bridge.py:
- Bordo emite TransactionCreated → chega na Luna como dict com key "bordo.transaction_created"
- Luna emite ("bordo.goal_updated", {...}) → chega no Bordo como GoalUpdated tipado
- Sem loop infinito: emitir 1000 eventos em sequência, contar que cada um chega EXATAMENTE 1 vez
- Evento desconhecido logado mas não crasheia
- connect() e disconnect() funcionam
- GenericEvent fallback funciona

Critério de pronto:
  pytest tests/test_bridge/test_event_bridge.py -v  # tudo verde
  pytest tests/test_bridge/ --cov=src/bordo/adapters/luna_bridge --cov-report=term  # 100%

Use /plan antes de começar.
```

---

## S12 · Plugin Luna completo

```
Leia review.md. Execute a Sprint S12 (Plugin Luna completo).

Implementar src/bordo/plugin.py — BordoLunaPlugin que satisfaz o IModule protocol da Luna:

class BordoLunaPlugin:
    @property
    def manifest(self) -> Manifest: ...  # lê module.yaml
    def on_load(self, ctx: ModuleContext) -> None: ...
    def on_enable(self, ctx: ModuleContext) -> None: ...
    def on_disable(self, ctx: ModuleContext) -> None: ...

on_load:
- Recebe ModuleContext da Luna
- Cria BordoConfig a partir de ctx.get_setting()
- Inicializa SQLiteStore com ctx.data_dir / "bordo.db"
- Cria BordoEventBus e todos os serviços via create_luna_plugin()

on_enable:
- Cria EventBusBridge entre Luna event bus e Bordo event bus
- bridge.connect()
- Registra handlers para eventos Luna relevantes (entity:changed, code:session_start, etc.)

on_disable:
- bridge.disconnect()
- Cleanup

Criar module.yaml na raiz do projeto conforme a seção do review.md:
- id: "controle_de_bordo"
- luna_version: ">=5.5.0"
- skills, commands, events, widgets, settings

Criar tests/test_bridge/test_luna_plugin.py:
- Plugin inicializa com ModuleContext mock
- on_load cria storage e serviços
- on_enable conecta bridge
- on_disable desconecta limpo
- Entry point discovery funciona: importlib.metadata simulado

NÃO importar código real da Luna nos testes — criar mocks para ModuleContext, EventBus Luna, e Manifest.

Critério de pronto:
  pytest tests/test_bridge/test_luna_plugin.py -v  # tudo verde
  pip install -e ".[luna]"  # instala sem erro

Use /plan antes de começar.
```

---

## S13 · Migração JSON→SQLite faseada

```
Leia review.md. Execute a Sprint S13 (Migração JSON→SQLite faseada).

Leia a seção "Migração JSON → SQLite em quatro fases com rollback garantido" do review.md.

Implementar em src/bordo/migrations/json_to_sqlite.py:

StorageMode (Enum):
- JSON_ONLY, DUAL_WRITE, DUAL_READ_SQL, SQLITE_ONLY

DualWriteRepository (satisfaz IStorage):
- Encapsula JsonStore e SQLiteStore
- Comportamento muda conforme StorageMode:
  * JSON_ONLY: lê e escreve só JSON
  * DUAL_WRITE: escreve em ambos, lê do JSON
  * DUAL_READ_SQL: escreve em ambos, lê do SQLite
  * SQLITE_ONLY: lê e escreve só SQLite

MigrationManager:
- get_current_phase() -> StorageMode
- advance_phase() — avança para próxima fase com backup automático antes
- rollback() — volta para fase anterior
- validate_integrity() -> bool — compara contagens e checksums entre JSON e SQLite
- backup_all() — backup atômico de JSON (shutil.copytree) e SQLite (Connection.backup)

DataMigrator:
- migrate_json_to_sqlite(json_dir: Path, sqlite_path: Path) -> MigrationReport
- MigrationReport com: total_records, migrated, skipped, errors, checksums

Adicionar comando CLI: bordo migrate --phase <fase> e bordo migrate --validate e bordo migrate --rollback

Criar tests/test_migration/:
- Migrar 100+ registros JSON → SQLite, validar contagens
- Idempotência: rodar migração 2x = mesmo resultado
- Rollback funciona: avançar para DUAL_WRITE, rollback para JSON_ONLY
- Integridade: checksums batem entre JSON e SQLite
- DualWriteRepository em cada modo se comporta corretamente

Critério de pronto:
  pytest tests/test_migration/ -v  # tudo verde

Use /plan antes de começar.
```

---

## S14 · Contract tests compartilhados

```
Leia review.md. Execute a Sprint S14 (Contract tests compartilhados).

Criar tests/contracts/ com test base classes que validam os Protocol contracts:

tests/contracts/test_storage_contract.py:
- Classe base StorageContractTest com todos os testes que QUALQUER IStorage deve passar
- Testes: insert retorna int, get_by_id encontra registro, update modifica, delete remove, query filtra, count conta, backup cria arquivo
- Rodar contra SQLiteStore E JsonStore — ambos devem passar 100%

tests/contracts/test_event_bus_contract.py:
- Classe base EventBusContractTest
- Testes: emit+on funciona, off remove, handler isolado por tipo, exceção em handler não propaga
- Rodar contra BordoEventBus

tests/contracts/test_importer_contract.py:
- Classe base ImporterContractTest
- Testes: import_file retorna list[Transaction], supported_formats retorna list[str]
- Rodar contra NubankCSV e OFXParser

Padrão: cada contract test é uma classe com métodos de teste. Subclasses concretas só definem um fixture que cria a implementação.

Configurar mypy --strict no CI (pyproject.toml [tool.mypy]).

Criar/atualizar .github/workflows/ci.yml:
- ruff check + ruff format --check
- mypy --strict src/bordo/
- pytest tests/ -v --cov=src/bordo

Critério de pronto:
  pytest tests/contracts/ -v  # TODOS os contracts passam para TODAS as implementações
  mypy src/bordo/ --strict  # passa limpo

Use /plan antes de começar.
```

---

## S15 · Integração end-to-end Luna

```
Leia review.md. Execute a Sprint S15 (Integração end-to-end Luna).

Criar tests/test_integration/test_e2e_luna.py — teste de integração completo:

Cenário 1: Discovery → Load → Enable
- Simular Luna discovery via entry points (mock importlib.metadata)
- Instanciar BordoLunaPlugin
- Chamar on_load com ModuleContext mock
- Chamar on_enable
- Verificar que bridge está conectado

Cenário 2: Fluxo financeiro completo
- Importar CSV via FinancialEngine
- Verificar que TransactionCreated chega na "Luna" (mock bus) como dict
- Verificar que dados estão no SQLite
- Chamar get_summary e validar números

Cenário 3: Fluxo Luna → Bordo
- Simular Luna emitindo "life:bill_due" com dict
- Verificar que chega no Bordo como evento tipado (ou GenericEvent)

Cenário 4: Migração durante uso
- Iniciar em JSON_ONLY
- Adicionar dados
- Avançar para DUAL_WRITE
- Adicionar mais dados
- Verificar que ambos storages têm tudo
- Avançar para SQLITE_ONLY
- Verificar leitura correta

Cenário 5: Graceful degradation
- Plugin inicializa sem Luna real instalada → detecta standalone → funciona via CLI
- Bridge desconectado → Bordo continua funcionando normalmente sem emitir para Luna

Critério de pronto:
  pytest tests/test_integration/ -v  # tudo verde

Use /plan antes de começar.
```

---

## S16 · ViewModels UI-agnósticos

```
Leia review.md. Execute a Sprint S16 (ViewModels UI-agnósticos).

Implementar src/bordo/viewmodels.py:

Observable[T]:
- Classe genérica ~30 linhas
- .value: T (getter)
- .set(new_value: T) — atualiza e notifica
- .subscribe(callback: Callable[[T], None]) — registra listener
- .unsubscribe(callback) — remove listener

FinanceViewModel:
- balance: Observable[float]
- monthly_summary: Observable[dict]
- recent_transactions: Observable[list[Transaction]]
- refresh() — recarrega do storage
- import_file(path: Path) — importa e atualiza observables

GoalsViewModel:
- goals: Observable[list[Goal]]
- add_goal(...), update_progress(...), refresh()

HabitsViewModel:
- habits: Observable[list[Habit]]
- complete_habit(name: str), refresh()

HealthViewModel:
- today: Observable[HealthRecord]
- log_water(), log_meal(), log_weight(), refresh()

REGRA: ZERO imports de Textual ou Flet em viewmodels.py. Só domain e ports.

Criar tests/test_viewmodels.py:
- Observable notifica subscriber após set()
- Observable NÃO notifica após unsubscribe()
- FinanceViewModel.refresh() atualiza balance
- Múltiplos subscribers recebem notificação

Critério de pronto:
  pytest tests/test_viewmodels.py -v  # tudo verde
  grep -rn "textual\|flet" src/bordo/viewmodels.py  # retorna VAZIO

Use /plan antes de começar.
```

---

## S17 · Widgets Textual para Luna

```
Leia review.md. Execute a Sprint S17 (Widgets Textual para Luna).

Implementar src/bordo/adapters/textual_widgets/:

__init__.py
finance_dashboard.py — FinanceDashboardWidget(Static):
  - Mostra saldo, receitas, despesas do mês
  - Top 5 categorias de gasto
  - Consome FinanceViewModel

goal_progress.py — GoalProgressWidget(Static):
  - Barra de progresso para cada meta
  - Projeção de data de conclusão
  - Consome GoalsViewModel

habit_tracker.py — HabitTrackerWidget(Static):
  - Lista de hábitos com streak visual
  - Consome HabitsViewModel

health_summary.py — HealthSummaryWidget(Static):
  - Água, refeições, peso do dia
  - Consome HealthViewModel

Cada widget:
- Recebe ViewModel no construtor
- Se inscreve nos Observables no compose()
- Atualiza UI no callback
- Desinscreve no on_unmount()

Atualizar module.yaml com widgets e seus slots.

Criar tests/test_adapters/test_textual_widgets.py:
- Cada widget renderiza sem crash com dados mock
- Widget atualiza quando ViewModel muda

Critério de pronto:
  pytest tests/test_adapters/test_textual_widgets.py -v  # tudo verde

Use /plan antes de começar.
```

---

## S18 · Interface Flet standalone

```
Leia review.md. Execute a Sprint S18 (Interface Flet standalone).

Implementar src/bordo/adapters/flet_ui/:

__init__.py
app.py — entry point Flet:
  - Navegação com tabs: Finanças, Metas, Hábitos, Saúde
  - Tema escuro por default (dark mode)
  - Responsivo (desktop e mobile)

pages/finance_page.py:
  - Cards com saldo, receitas, despesas
  - Tabela de transações recentes
  - Botão importar CSV
  - Consome FinanceViewModel

pages/goals_page.py:
  - Cards de meta com progress bar
  - Formulário para adicionar meta
  - Consome GoalsViewModel

pages/habits_page.py:
  - Lista com checkbox e streak counter
  - Consome HabitsViewModel

pages/health_page.py:
  - Botões rápidos: +1 copo água, registrar refeição, registrar peso
  - Resumo do dia
  - Consome HealthViewModel

Atualizar bootstrap.py:
- create_standalone() aceita --ui flet ou --ui cli

Atualizar cli.py:
- bordo ui — lança interface Flet (flet.app(target=main))

Critério de pronto:
  pip install -e ".[flet]"
  bordo ui  # abre janela Flet funcional
  # Teste manual: importar CSV, ver saldo, adicionar meta

Use /plan antes de começar.
```

---

## S19 · MacroIndicators e NudgeEngine

```
Leia review.md. Execute a Sprint S19 (MacroIndicators e NudgeEngine).

Implementar em src/bordo/domain/services.py:

MacroIndicators:
- get_selic() -> float — taxa Selic atual (API BCB ou python-bcb)
- get_ipca() -> float — IPCA acumulado 12m
- get_cdi() -> float — CDI anual
- get_savings_yield() -> float — rendimento poupança
- cache de 24h para evitar chamadas repetidas
- Graceful degradation: se sem internet, retorna último valor cacheado ou None

NudgeEngine:
- Recebe IStorage, IEventBus, BordoConfig
- check_all() -> list[Nudge] — verifica todas as regras e retorna nudges pendentes
- Nudge(title, message, urgency, category, rule_name)
- Regras configuráveis:
  * Hidratação: se water_cups < meta às 14h, lembrar
  * Medicamento: se horário do remédio passou e não registrou
  * Exercício: se N dias sem registrar treino
  * Estudo: se streak Duolingo/Alura em risco
  * Financeiro: se gasto mensal em categoria X > threshold
  * Pausa: se sessão de coding > 2h contínua
  * Meta: se ritmo atual não alcança meta no prazo
- Emite NudgeTriggered via event bus

Adicionar ao CLI: bordo macro — mostra Selic, IPCA, CDI
Adicionar ao CLI: bordo nudges — mostra nudges pendentes

Criar tests/test_domain/test_nudge.py e test_macro.py:
- NudgeEngine com regra de hidratação ativada/silenciada
- MacroIndicators retorna dados (mock da API BCB)
- Graceful degradation sem internet

Critério de pronto:
  pytest tests/test_domain/test_nudge.py tests/test_domain/test_macro.py -v  # tudo verde

Use /plan antes de começar.
```

---

## S20 · CI, documentação e release

```
Leia review.md. Execute a Sprint S20 (CI, documentação e release).

1. GitHub Actions (.github/workflows/ci.yml):
   - Job lint: ruff check + ruff format --check
   - Job typecheck: mypy --strict src/bordo/
   - Job test: pytest tests/ -v --cov=src/bordo --cov-report=xml
   - Job contracts: pytest tests/contracts/ -v
   - Matrix Python 3.10, 3.11, 3.12
   - Cache pip dependencies
   - Badge no README

2. README.md atualizado:
   - Quickstart standalone (pip install, bordo import, bordo balance)
   - Quickstart Luna (pip install controle-de-bordo[luna], ativar módulo)
   - Diagrama de arquitetura (texto ASCII ou mermaid)
   - Lista de comandos CLI
   - Seção de contribuição

3. docs/ atualizado:
   - ARQUITETURA.md refletindo nova estrutura src/bordo/
   - INTEGRACAO_LUNA.md com instruções reais (não só plano)
   - MIGRACAO.md explicando as 4 fases

4. Limpeza final:
   - Remover código antigo em src/domain/, src/adapters/, src/cli/, src/events/, src/ui/, src/mobile/ que foi migrado para src/bordo/
   - Atualizar todos os imports nos testes
   - Verificar que NENHUM arquivo menciona nomes de IA ou pessoas (regra de anonimato)

5. Tag e versão:
   - Atualizar __version__ para "0.1.0" (confirmar)
   - git tag v0.1.0

Critério de pronto:
  ruff check src/bordo/  # limpo
  mypy src/bordo/ --strict  # limpo
  pytest tests/ -v --cov=src/bordo  # tudo verde, cobertura > 80%
  grep -rniE "claude|anthropic|openai" src/bordo/ --include="*.py" | grep -viE "api|config"  # VAZIO
  pip install -e ".[all]"  # funciona
  bordo version  # 0.1.0
  bordo ui  # abre Flet

Use /plan antes de começar.
```

---

## Dicas gerais

- **Sempre peça `/plan` antes.** Isso te dá controle sobre o que vai ser feito.
- **Se uma sprint falhar nos testes**, diga: `Os testes falharam. Aqui está a saída: [cola o erro]. Corrija.`
- **Se quiser continuar de onde parou**, diga: `Leia review.md. Estou na Sprint SXX. O estado atual é: [descreva]. Continue.`
- **Commite após cada sprint verde**: `git add . && git commit -m "feat: SXX — descrição"`
- **Se o plano parecer errado**, escolha opção 3 e diga o que mudar antes de aprovar.
