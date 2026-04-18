#!/bin/bash
# Guarda o nome do ficheiro passado como argumento  

#!/bin/bash

file=$1

# DESAFIO 1 - Validação do ficheiro
if [ ! -f "$file" ]; then
    echo "Erro: ficheiro não encontrado"
    exit 1
fi

# O resto do código só corre se o ficheiro existir
echo "RELATÓRIO"
echo "Total linhas: $(wc -l < "$file")"
# ... resto dos teus comandos echo ...


# 1. Verifica se o nome do ficheiro foi escrito
if [ -z "$file" ]; then
    echo "❌ Erro: Por favor, indica o nome do ficheiro de log."
    echo "Exemplo: ./analyzer.sh 10000.log"
    exit 1
fi

# 2. Verifica se o ficheiro existe mesmo na pasta
if [ ! -f "$file" ]; then
    echo "❌ Erro: O ficheiro '$file' não foi encontrado nesta pasta."
    exit 1
fi

# --- RELATÓRIO EM PORTUGUÊS ---

echo "======================================"
echo "        RELATÓRIO DE ANÁLISE          "
echo "======================================"

echo "📊 Total de linhas: $(wc -l < "$file")"

# Filtra erros e esconde mensagens do sistema se falhar
erros=$(grep -E "401|403|404|500" "$file" 2>/dev/null | wc -l)
echo "⚠️ Total de erros encontrados: $erros"

ips=$(cut -d ' ' -f2 "$file" 2>/dev/null | sort | uniq | wc -l)
echo "🌐 IPs únicos detectados: $ips"

top_ip=$(cut -d ' ' -f2 "$file" 2>/dev/null | sort | uniq -c | sort -nr | head -1)
echo "🔝 IP com mais acessos: $top_ip"

downloads=$(grep "DOWNLOAD" "$file" 2>/dev/null | wc -l)
echo "📥 Total de downloads feitos: $downloads"

echo "======================================"

# Guarda o relatório num ficheiro na mesma pasta do log
./analyzer.sh "$file" > "$(dirname "$file")/relatorio_analise.txt"

echo "✅ Relatório guardado com sucesso em: $(dirname "$file")/relatorio_analise.txt"
