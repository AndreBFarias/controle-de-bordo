#!/bin/bash
# ==============================================
# CONTROLE DE BORDO - Instalação Completa
# ==============================================
# Script idempotente: pode ser executado múltiplas
# vezes sem causar erros ou duplicar instalações.
# ==============================================

set -e

# ----------------------------------------------
# CORES
# ----------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ----------------------------------------------
# VARIÁVEIS
# ----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
DATA_DIR="${SCRIPT_DIR}/data"
DB_PATH="${DATA_DIR}/bordo.db"
ENV_FILE="${SCRIPT_DIR}/.env"
DESKTOP_FILE="controle-de-bordo.desktop"
DESKTOP_SRC="${SCRIPT_DIR}/assets/${DESKTOP_FILE}"
DESKTOP_DST="${HOME}/.local/share/applications/${DESKTOP_FILE}"
PYTHON_MIN_MAJOR=3
PYTHON_MIN_MINOR=10
TOTAL_STEPS=7

# ----------------------------------------------
# FUNÇÕES UTILITÁRIAS
# ----------------------------------------------
print_header() {
    echo ""
    echo -e "${CYAN}"
    echo "  ╔════════════════════════════════════════════════╗"
    echo "  ║                                                ║"
    echo "  ║        CONTROLE DE BORDO                       ║"
    echo "  ║        Life Operating System                   ║"
    echo "  ║                                                ║"
    echo "  ║        Local-first. Open source. Brasileiro.   ║"
    echo "  ║                                                ║"
    echo "  ╚════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

print_step() {
    local step=$1
    local message=$2
    echo -e "${CYAN}[${step}/${TOTAL_STEPS}]${NC} ${message}"
}

print_success() {
    echo -e "  ${GREEN}OK${NC} $1"
}

print_skip() {
    echo -e "  ${YELLOW}SKIP${NC} $1"
}

print_error() {
    echo -e "  ${RED}ERRO${NC} $1"
}

print_warn() {
    echo -e "  ${YELLOW}AVISO${NC} $1"
}

# ----------------------------------------------
# VERIFICAÇÕES
# ----------------------------------------------
check_python() {
    print_step 1 "Verificando Python..."

    if ! command -v python3 &>/dev/null; then
        print_error "Python 3 não encontrado."
        echo "  Instale com: sudo apt install python3 python3-venv python3-pip"
        exit 1
    fi

    local version
    version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)

    if [[ "$major" -lt "$PYTHON_MIN_MAJOR" ]] || { [[ "$major" -eq "$PYTHON_MIN_MAJOR" ]] && [[ "$minor" -lt "$PYTHON_MIN_MINOR" ]]; }; then
        print_error "Python ${PYTHON_MIN_MAJOR}.${PYTHON_MIN_MINOR}+ necessário (encontrado: ${version})"
        exit 1
    fi

    print_success "Python ${version}"

    if ! python3 -c "import venv" &>/dev/null; then
        print_error "Módulo venv não encontrado."
        echo "  Instale com: sudo apt install python3-venv"
        exit 1
    fi
    print_success "Módulo venv disponível"
}

# ----------------------------------------------
# CRIAÇÃO DO VENV
# ----------------------------------------------
setup_venv() {
    print_step 2 "Configurando ambiente virtual..."

    if [[ -d "$VENV_DIR" ]] && [[ -f "$VENV_DIR/bin/activate" ]]; then
        print_skip "Ambiente virtual já existe em .venv/"
    else
        python3 -m venv "$VENV_DIR"
        print_success "Ambiente virtual criado em .venv/"
    fi

    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    print_success "Ambiente ativado"
}

# ----------------------------------------------
# INSTALAÇÃO DE DEPENDÊNCIAS
# ----------------------------------------------
install_deps() {
    print_step 3 "Instalando dependências..."

    pip install --upgrade pip --quiet 2>/dev/null
    print_success "pip atualizado"

    if [[ -f "${SCRIPT_DIR}/pyproject.toml" ]]; then
        pip install -e "." --quiet 2>/dev/null
        print_success "Dependências principais instaladas"
    elif [[ -f "${SCRIPT_DIR}/requirements.txt" ]]; then
        pip install -r "${SCRIPT_DIR}/requirements.txt" --quiet 2>/dev/null
        print_success "Dependências (requirements.txt) instaladas"
    else
        print_error "Nenhum arquivo de dependências encontrado"
        exit 1
    fi

    # Dependências de desenvolvimento (opcional)
    if pip install -e ".[dev]" --quiet 2>/dev/null; then
        print_success "Dependências de desenvolvimento instaladas"
    else
        print_warn "Dependências de dev não instaladas (opcional)"
    fi
}

# ----------------------------------------------
# INICIALIZAÇÃO DO BANCO DE DADOS
# ----------------------------------------------
setup_database() {
    print_step 4 "Inicializando banco de dados..."

    mkdir -p "$DATA_DIR"

    if [[ -f "$DB_PATH" ]]; then
        print_skip "Banco de dados já existe em data/bordo.db"
    else
        python3 -c "
from src.adapters.storage.sqlite_adapter import SQLiteAdapter
storage = SQLiteAdapter('${DB_PATH}')
storage.initialize()
storage.close()
print('  Banco inicializado com sucesso')
"
        print_success "SQLite criado em data/bordo.db (modo WAL)"
    fi
}

# ----------------------------------------------
# CONFIGURAÇÃO (.env)
# ----------------------------------------------
setup_env() {
    print_step 5 "Configurando variáveis de ambiente..."

    if [[ -f "$ENV_FILE" ]]; then
        print_skip "Arquivo .env já existe"
    else
        if [[ -f "${SCRIPT_DIR}/.env.example" ]]; then
            cp "${SCRIPT_DIR}/.env.example" "$ENV_FILE"
            print_success "Arquivo .env criado a partir de .env.example"
            print_warn "Edite .env para configurar suas chaves de API (opcional)"
        else
            print_warn "Arquivo .env.example não encontrado"
        fi
    fi
}

# ----------------------------------------------
# ARQUIVO .DESKTOP
# ----------------------------------------------
setup_desktop() {
    print_step 6 "Configurando integração com desktop..."

    if [[ ! -f "$DESKTOP_SRC" ]]; then
        print_warn "Arquivo .desktop não encontrado em assets/"
        return
    fi

    mkdir -p "$(dirname "$DESKTOP_DST")"

    # Gera .desktop com caminho absoluto
    sed "s|{{INSTALL_DIR}}|${SCRIPT_DIR}|g" "$DESKTOP_SRC" > "$DESKTOP_DST"

    if command -v update-desktop-database &>/dev/null; then
        update-desktop-database "$(dirname "$DESKTOP_DST")" 2>/dev/null || true
    fi

    print_success "Lançador instalado em ~/.local/share/applications/"
}

# ----------------------------------------------
# VERIFICAÇÃO FINAL
# ----------------------------------------------
verify_install() {
    print_step 7 "Verificando instalação..."

    local errors=0

    if python3 -c "from src.adapters.storage.sqlite_adapter import SQLiteAdapter" 2>/dev/null; then
        print_success "Imports do projeto funcionando"
    else
        print_error "Falha nos imports"
        errors=$((errors + 1))
    fi

    if [[ -f "$DB_PATH" ]]; then
        print_success "Banco de dados acessível"
    else
        print_error "Banco de dados não encontrado"
        errors=$((errors + 1))
    fi

    if command -v bordo &>/dev/null; then
        print_success "Comando 'bordo' disponível no PATH"
    else
        print_warn "Comando 'bordo' não no PATH (use: source .venv/bin/activate)"
    fi

    echo ""
    if [[ $errors -eq 0 ]]; then
        echo -e "${GREEN}${BOLD}Instalação concluída com sucesso!${NC}"
    else
        echo -e "${RED}${BOLD}Instalação com ${errors} erro(s). Verifique acima.${NC}"
        exit 1
    fi

    echo ""
    echo -e "${BOLD}Para começar:${NC}"
    echo "  source .venv/bin/activate"
    echo "  bordo status"
    echo "  bordo financas resumo"
    echo "  flet run src/ui/app.py"
    echo ""
}

# ----------------------------------------------
# MAIN
# ----------------------------------------------
main() {
    cd "$SCRIPT_DIR"
    print_header
    check_python
    setup_venv
    install_deps
    setup_database
    setup_env
    setup_desktop
    verify_install
}

main "$@"

# "A liberdade é o direito de fazer tudo o que as leis permitem." - Montesquieu
