# Contribuindo com o Controle de Bordo

## Configuração do Ambiente

```bash
# 1. Clonar o repositório
git clone https://github.com/<USUARIO>/controle-de-bordo.git
cd controle-de-bordo

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -e ".[dev]"

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env conforme necessário

# 5. Verificar instalação
pytest tests/unit/
ruff check src/
```

## Estrutura do Projeto

```
src/
  domain/         -> Lógica pura (NUNCA importar de adapters/ui)
    entities/     -> Modelos Pydantic
    services/     -> Regras de negócio
    ports/        -> Interfaces (Protocol)
  adapters/       -> Implementações de ports
  ui/             -> Interface Flet
  events/         -> Event bus
  mobile/         -> Ponte Android
  cli/            -> Interface Typer
```

**Regra fundamental**: `domain/` nunca importa de `adapters/`, `ui/` ou `mobile/`.

## Convenções de Código

- **Python 3.10+** com type hints obrigatórios
- **Pydantic** para validação de dados
- **Acentuação PT-BR correta** em código, comments, docs e commits
- **Zero emojis** em qualquer lugar
- **Logging** via `logging` (nunca `print()`)
- **Paths** via `pathlib.Path` (nunca strings hardcoded)
- **Limite**: 800 linhas por arquivo

### Linting e formatação

```bash
# Verificar estilo
ruff check src/

# Formatar
ruff format src/

# Verificar tipos
mypy src/
```

## Testes

```bash
# Testes unitários
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Com cobertura
pytest --cov=src tests/
```

### Escrevendo testes

- Testes unitários em `tests/unit/` - sem dependências externas
- Testes de integração em `tests/integration/` - podem usar SQLite real
- Usar fixtures para storage mock
- Nomenclatura: `test_<modulo>_<comportamento>.py`

## Commits

Formato obrigatório em PT-BR:

```
tipo: descrição imperativa

# Tipos: feat, fix, refactor, docs, test, perf, chore
```

Exemplos:
```
feat: adicionar parser CSV do Nubank
fix: corrigir categorização de transações do iFood
refactor: extrair lógica de projeção para serviço dedicado
docs: documentar fluxo de importação OFX
test: cobrir cenários de conta atrasada
```

**Proibido em commits:**
- Emojis
- Menções a IA (Claude, GPT, Copilot, etc)
- `--force` sem autorização explícita

## Criando um novo Adapter

Para adicionar suporte a um novo banco:

1. Criar `src/adapters/importers/meu_banco.py`
2. Implementar o protocol `IBankImporter`
3. Adicionar testes em `tests/unit/test_meu_banco.py`
4. Documentar formato esperado em `docs/FINANCAS.md`

```python
from src.domain.ports.bank_importer import IBankImporter

class MeuBancoImporter:
    @property
    def bank_name(self) -> str:
        return "Meu Banco"

    @property
    def supported_formats(self) -> list[str]:
        return [".csv"]

    def parse(self, file_path: Path) -> list[Transaction]:
        # Implementar parser aqui
        ...

    def detect(self, file_path: Path) -> bool:
        # Verificar se o arquivo é deste banco
        ...
```

## Criando um novo Notifier

Para adicionar um novo canal de notificação:

1. Criar `src/adapters/notifiers/meu_notifier.py`
2. Implementar o protocol `INotifier`
3. Adicionar testes
4. Registrar no container de dependência

## Issues e PRs

- Issues em PT-BR com descrição clara do problema
- PRs com testes para toda funcionalidade nova
- Uma PR por funcionalidade (não misturar features)
- Rebase antes do merge (manter histórico limpo)

*"O segredo de progredir é começar." - Mark Twain*
