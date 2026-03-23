set shell := ["bash", "-c"]

venv := ".venv/bin/"

# Listar comandos disponíveis
help:
    @just --list --unsorted

# Instalação completa
setup:
    ./install.sh

# Executar testes E2E
test:
    {{venv}}python -m pytest tests/e2e/ -v --tb=short

# Executar testes com cobertura
test-cov:
    {{venv}}python -m pytest tests/e2e/ --cov=src --cov-report=term-missing

# Linting
lint:
    {{venv}}ruff check src/

# Formatação
format:
    {{venv}}ruff format src/

# Verificação de tipos
types:
    {{venv}}mypy src/

# Pipeline CI completo (lint + types + test)
ci: lint types test

# Executar pre-commit em todos os arquivos
pre:
    pre-commit run --all-files

# Executar UI Flet
run:
    {{venv}}flet run src/ui/app.py

# Executar CLI
cli *ARGS:
    {{venv}}python -m src.cli.main {{ARGS}}

# Status rápido
status:
    {{venv}}python -m src.cli.main status

# Resumo financeiro
financas:
    {{venv}}python -m src.cli.main financas resumo

# Indicadores macro
macro:
    {{venv}}python -m src.cli.main macro resumo

# Nudges pendentes
nudges:
    {{venv}}python -m src.cli.main nudges

# Contar linhas de código
loc:
    @find src -name "*.py" -not -path "*/__pycache__/*" | xargs wc -l | tail -1
    @echo "Arquivos Python: $(find src -name '*.py' -not -path '*/__pycache__/*' | wc -l)"
    @echo "Testes E2E: $(grep -c 'def test_' tests/e2e/*.py 2>/dev/null || echo 0)"
    @echo "Registry: $(tail -n +2 REGISTRY.csv | wc -l) entradas"
