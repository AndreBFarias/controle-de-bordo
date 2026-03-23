#!/usr/bin/env bash
# ==============================================
# Hook bloqueante: verifica se arquivo criado/editado
# está registrado no REGISTRY.csv.
#
# Se o arquivo NÃO está no registry, BLOQUEIA a operação
# e exige que o desenvolvedor registre primeiro.
# ==============================================

FILE_PATH=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty' 2>/dev/null)

if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Normalizar caminho (remover prefixo do projeto se absoluto)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RELATIVE_PATH="${FILE_PATH#${PROJECT_DIR}/}"

# Se ainda é absoluto, não é do projeto - ignorar
if [[ "$RELATIVE_PATH" == /* ]]; then
    exit 0
fi

# Ignorar certos caminhos que não precisam de registro
case "$RELATIVE_PATH" in
    .venv/*|.git/*|__pycache__/*|*.pyc|.pytest_cache/*|.ruff_cache/*|data/*|.flet/*)
        exit 0
        ;;
    .claude/plans/*)
        exit 0
        ;;
esac

REGISTRY="${PROJECT_DIR}/REGISTRY.csv"

if [[ ! -f "$REGISTRY" ]]; then
    exit 0
fi

# Verificar se o caminho relativo existe no REGISTRY.csv
# Busca exata na primeira coluna (caminho)
if grep -q "^${RELATIVE_PATH}," "$REGISTRY" 2>/dev/null; then
    exit 0
fi

# Também verificar com ./ prefixo
if grep -q "^\./${RELATIVE_PATH}," "$REGISTRY" 2>/dev/null; then
    exit 0
fi

# Arquivo NÃO encontrado no registry - BLOQUEAR
cat <<BLOCK_JSON
{
    "continue": false,
    "stopReason": "REGISTRY BLOQUEANTE: O arquivo '${RELATIVE_PATH}' NÃO está registrado no REGISTRY.csv. Antes de criar/editar, adicione uma entrada no REGISTRY.csv com: caminho, tipo, linhas, camada, status, tags, propósito. Isso evita poluição e garante rastreabilidade de todos os artefatos do projeto."
}
BLOCK_JSON
