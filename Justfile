set shell := ["bash", "-c"]

venv := ".venv/bin/"

# Listar comandos disponíveis
help:
    @just --list --unsorted

# Instalação completa
setup:
    ./install.sh

# Instalar em modo editável com deps de dev
install-dev:
    pip install -e ".[dev]"

# Executar testes
test:
    {{venv}}python -m pytest tests/ -v --tb=short

# Executar testes com cobertura
test-cov:
    {{venv}}python -m pytest tests/ --cov=bordo --cov-report=term-missing

# Linting
lint:
    {{venv}}ruff check src/bordo/

# Formatação
format:
    {{venv}}ruff format src/bordo/

# Verificação de tipos
types:
    {{venv}}mypy src/bordo/

# Pipeline CI completo (lint + types + test)
ci: lint types test

# Executar pre-commit em todos os arquivos
pre:
    pre-commit run --all-files

# Executar CLI
cli *ARGS:
    {{venv}}python -m bordo {{ARGS}}

# Verificar versão
version:
    {{venv}}python -c "import bordo; print(bordo.__version__)"

# Contar linhas de código
loc:
    @find src/bordo -name "*.py" -not -path "*/__pycache__/*" | xargs wc -l | tail -1
    @echo "Arquivos Python: $(find src/bordo -name '*.py' -not -path '*/__pycache__/*' | wc -l)"
    @echo "Registry: $(tail -n +2 REGISTRY.csv | wc -l) entradas"
