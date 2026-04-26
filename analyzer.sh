#!/bin/bash

# Guarda o nome do ficheiro passado como argumento
file=$1

# --- VALIDAÇÃO ---

# 1. Verifica se o nome do ficheiro foi fornecido
if [ -z "$file" ]; then
    echo "❌ Erro: Por favor, indica o nome do ficheiro de log."
    echo "Exemplo: ./analyzer.sh 10000.log"
    exit 1
fi

# 2. Verifica se o ficheiro existe
if [ ! -f "$file" ]; then
    echo "❌ Erro: O ficheiro '$file' não foi encontrado nesta pasta."
    exit 1
fi

# --- RELATÓRIO EM PORTUGUÊS ---

echo "======================================"
echo "        RELATÓRIO DE ANÁLISE          "
echo "======================================"

echo "📊 Total de linhas: $(wc -l < "$file")"

# Conta erros: linhas que contêm a palavra ERROR (com código no final)
erros=$(grep -c " ERROR " "$file" 2>/dev/null)
echo "⚠️  Total de erros encontrados: $erros"

ips=$(awk '{print $2}' "$file" | sort | uniq | wc -l)
echo "🌐 IPs únicos detectados: $ips"

top_ip=$(awk '{print $2}' "$file" | sort | uniq -c | sort -nr | head -1)
echo "🔝 IP com mais acessos: $top_ip"

downloads=$(grep -c " DOWNLOAD " "$file" 2>/dev/null)
echo "📥 Total de downloads feitos: $downloads"

echo "======================================"

# --- GUARDAR RELATÓRIO NUM FICHEIRO ---
relatorio="$(dirname "$file")/relatorio_analise.txt"

{
    echo "======================================"
    echo "        RELATÓRIO DE ANÁLISE          "
    echo "======================================"
    echo "📊 Total de linhas: $(wc -l < "$file")"
    echo "⚠️  Total de erros encontrados: $erros"
    echo "🌐 IPs únicos detectados: $ips"
    echo "🔝 IP com mais acessos: $top_ip"
    echo "📥 Total de downloads feitos: $downloads"
    echo "======================================"
} > "$relatorio"

echo "✅ Relatório guardado com sucesso em: $relatorio"
