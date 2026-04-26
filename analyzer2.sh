#!/bin/bash

file=$1
errors=0

# --- VALIDAÇÃO ---
if [ -z "$file" ]; then
    echo "❌ Erro: Por favor, indica o nome do ficheiro de log."
    echo "Exemplo: ./analyzer2.sh 10000.log"
    exit 1
fi

if [ ! -f "$file" ]; then
    echo "❌ Erro: O ficheiro '$file' não foi encontrado nesta pasta."
    exit 1
fi

echo "A analisar o ficheiro com loop linha a linha..."

# Lê o ficheiro linha a linha usando um loop
while IFS= read -r line
do
    # Verifica se a linha contém " ERROR " (com espaços para evitar falsos positivos)
    if [[ "$line" == *" ERROR "* ]]; then
        ((errors++))
    fi
done < "$file"

echo ""
echo "============================"
echo "Relatório do Desafio 2 (Loop)"
echo "Total de erros encontrados: $errors"
echo "============================"
