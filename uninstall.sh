#!/bin/bash
# ==============================================
# CONTROLE DE BORDO - Desinstalação
# ==============================================
# Remove componentes instalados pelo install.sh.
# Nunca remove código-fonte.
# Confirmação antes de cada ação destrutiva.
# ==============================================

set -e

# ----------------------------------------------
# CORES
# ----------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ----------------------------------------------
# VARIÁVEIS
# ----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
DATA_DIR="${SCRIPT_DIR}/data"
ENV_FILE="${SCRIPT_DIR}/.env"
DESKTOP_FILE="controle-de-bordo.desktop"
DESKTOP_DST="${HOME}/.local/share/applications/${DESKTOP_FILE}"

# ----------------------------------------------
# FUNÇÕES
# ----------------------------------------------
print_header() {
    echo ""
    echo -e "${YELLOW}"
    echo "  ╔════════════════════════════════════════════════╗"
    echo "  ║                                                ║"
    echo "  ║        CONTROLE DE BORDO                       ║"
    echo "  ║        Desinstalação                           ║"
    echo "  ║                                                ║"
    echo "  ╚════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

confirm() {
    local message=$1
    echo -en "${YELLOW}${message} [s/N]: ${NC}"
    read -r response
    [[ "$response" =~ ^[sS]$ ]]
}

print_removed() {
    echo -e "  ${GREEN}REMOVIDO${NC} $1"
}

print_kept() {
    echo -e "  ${CYAN}MANTIDO${NC} $1"
}

print_not_found() {
    echo -e "  ${CYAN}---${NC} $1 (não encontrado)"
}

# ----------------------------------------------
# REMOÇÕES
# ----------------------------------------------
remove_venv() {
    echo -e "${BOLD}1. Ambiente virtual (.venv/)${NC}"
    if [[ -d "$VENV_DIR" ]]; then
        if confirm "   Remover ambiente virtual?"; then
            rm -rf "$VENV_DIR"
            print_removed ".venv/"
        else
            print_kept ".venv/"
        fi
    else
        print_not_found ".venv/"
    fi
    echo ""
}

remove_desktop() {
    echo -e "${BOLD}2. Lançador de aplicação (.desktop)${NC}"
    if [[ -f "$DESKTOP_DST" ]]; then
        if confirm "   Remover lançador do desktop?"; then
            rm -f "$DESKTOP_DST"
            if command -v update-desktop-database &>/dev/null; then
                update-desktop-database "$(dirname "$DESKTOP_DST")" 2>/dev/null || true
            fi
            print_removed "$DESKTOP_DST"
        else
            print_kept "$DESKTOP_DST"
        fi
    else
        print_not_found "Lançador .desktop"
    fi
    echo ""
}

remove_data() {
    echo -e "${BOLD}3. Dados pessoais (data/)${NC}"
    if [[ -d "$DATA_DIR" ]]; then
        echo -e "  ${RED}ATENÇÃO: Esta ação remove seu banco de dados e todos os dados financeiros!${NC}"
        if confirm "   Remover dados pessoais (data/bordo.db)?"; then
            rm -rf "$DATA_DIR"
            print_removed "data/"
        else
            print_kept "data/"
        fi
    else
        print_not_found "data/"
    fi
    echo ""
}

remove_env() {
    echo -e "${BOLD}4. Configurações (.env)${NC}"
    if [[ -f "$ENV_FILE" ]]; then
        if confirm "   Remover arquivo de configuração (.env)?"; then
            rm -f "$ENV_FILE"
            print_removed ".env"
        else
            print_kept ".env"
        fi
    else
        print_not_found ".env"
    fi
    echo ""
}

remove_cache() {
    echo -e "${BOLD}5. Caches e temporários${NC}"
    local removed=0

    for cache_dir in ".pytest_cache" ".ruff_cache" ".mypy_cache" "__pycache__" ".flet"; do
        if find "$SCRIPT_DIR" -name "$cache_dir" -type d 2>/dev/null | grep -q .; then
            find "$SCRIPT_DIR" -name "$cache_dir" -type d -exec rm -rf {} + 2>/dev/null || true
            print_removed "$cache_dir"
            removed=$((removed + 1))
        fi
    done

    find "$SCRIPT_DIR" -name "*.pyc" -delete 2>/dev/null || true

    if [[ $removed -eq 0 ]]; then
        print_not_found "Caches"
    fi
    echo ""
}

# ----------------------------------------------
# MAIN
# ----------------------------------------------
main() {
    cd "$SCRIPT_DIR"
    print_header

    echo -e "${BOLD}O que será removido:${NC}"
    echo "  - Ambiente virtual (.venv/)"
    echo "  - Lançador do desktop (.desktop)"
    echo "  - Dados pessoais (data/) [com confirmação]"
    echo "  - Configurações (.env) [com confirmação]"
    echo "  - Caches e temporários"
    echo ""
    echo -e "${CYAN}O código-fonte NUNCA é removido.${NC}"
    echo ""

    if ! confirm "Iniciar desinstalação?"; then
        echo ""
        echo "Desinstalação cancelada."
        exit 0
    fi

    echo ""
    remove_venv
    remove_desktop
    remove_data
    remove_env
    remove_cache

    echo -e "${GREEN}${BOLD}Desinstalação concluída.${NC}"
    echo ""
    echo "Para reinstalar: ./install.sh"
    echo ""
}

main "$@"

# "Quem abre uma escola, fecha uma prisão." - Victor Hugo
