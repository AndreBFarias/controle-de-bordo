#!/usr/bin/env bash
# Verifica acentuação PT-BR em arquivos modificados pelo Claude.
# Detecta palavras comuns escritas sem acento e alerta.

FILE_PATH=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty' 2>/dev/null)

if [[ -z "$FILE_PATH" ]] || [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Apenas verificar arquivos de texto relevantes
case "$FILE_PATH" in
    *.py|*.md|*.toml|*.yaml|*.yml|*.txt|*.sh)
        ;;
    *)
        exit 0
        ;;
esac

ERRORS=""

# Palavras que DEVEM ter acento (padrão: sem acento -> com acento)
declare -A WORDS=(
    ["funcao"]="função"
    ["funcoes"]="funções"
    ["validacao"]="validação"
    ["validacoes"]="validações"
    ["descricao"]="descrição"
    ["descricoes"]="descrições"
    ["comunicacao"]="comunicação"
    ["configuracao"]="configuração"
    ["configuracoes"]="configurações"
    ["informacao"]="informação"
    ["informacoes"]="informações"
    ["operacao"]="operação"
    ["operacoes"]="operações"
    ["transacao"]="transação"
    ["transacoes"]="transações"
    ["notificacao"]="notificação"
    ["notificacoes"]="notificações"
    ["integracao"]="integração"
    ["aplicacao"]="aplicação"
    ["conexao"]="conexão"
    ["excecao"]="exceção"
    ["excecoes"]="exceções"
    ["autorizacao"]="autorização"
    ["atualizacao"]="atualização"
    ["execucao"]="execução"
    ["versao"]="versão"
    ["padrao"]="padrão"
    ["padroes"]="padrões"
    ["condicao"]="condição"
    ["condicoes"]="condições"
    ["solucao"]="solução"
    ["frequencia"]="frequência"
    ["persistencia"]="persistência"
    ["referencia"]="referência"
    ["experiencia"]="experiência"
    ["dependencia"]="dependência"
    ["sequencia"]="sequência"
    ["projecao"]="projeção"
    ["refeicao"]="refeição"
    ["refeicoes"]="refeições"
    ["medicacao"]="medicação"
    ["hidratacao"]="hidratação"
    ["natacao"]="natação"
    ["educacao"]="educação"
    ["saude"]="saúde"
    ["unico"]="único"
    ["unica"]="única"
    ["necessario"]="necessário"
    ["necessaria"]="necessária"
    ["disponivel"]="disponível"
    ["impossivel"]="impossível"
    ["possivel"]="possível"
)

for wrong in "${!WORDS[@]}"; do
    correct="${WORDS[$wrong]}"
    # Busca case-sensitive, apenas palavras inteiras (sem acento = erro)
    if grep -qw "$wrong" "$FILE_PATH" 2>/dev/null; then
        LINE=$(grep -nw "$wrong" "$FILE_PATH" | head -1)
        ERRORS="${ERRORS}\n  '$wrong' -> '${correct}' (linha ${LINE%%:*})"
    fi
done

if [[ -n "$ERRORS" ]]; then
    echo "{\"systemMessage\": \"Acentuacao PT-BR: encontradas palavras sem acento em ${FILE_PATH}:${ERRORS}\"}"
    exit 0
fi

exit 0
