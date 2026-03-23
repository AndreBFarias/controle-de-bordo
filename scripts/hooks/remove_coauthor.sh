#!/usr/bin/env bash
# Executado como hook commit-msg.

COMMIT_MSG_FILE="$1"

if [[ -z "$COMMIT_MSG_FILE" ]] || [[ ! -f "$COMMIT_MSG_FILE" ]]; then
    exit 0
fi

    sed -i '/[Cc]o-[Aa]uthored-[Bb]y/d' "$COMMIT_MSG_FILE"
    # Remove linhas em branco extras no final
    sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' "$COMMIT_MSG_FILE"
fi

exit 0
