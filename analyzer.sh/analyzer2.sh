#!/bin/bash

file=$1
errors=0

if [ ! -f "$file" ]; then
    echo "Erro: ficheiro não encontrado"
    exit 1
fi

echo "A analisar 10.000 linhas de forma otimizada..."

while read -r line
do
    # Usa a lógica interna do Bash [[ ]] em vez de chamar o grep externo
    if [[ "$line" =~ "401" || "$line" =~ "403" || "$line" =~ "404" || "$line" =~ "500" ]]; then
        ((errors++))
    fi
done < "$file"

echo ""
echo "============================"
echo "Relatório do Desafio 2 (Loop)"
echo "Total de erros encontrados: $errors"
echo "============================"
