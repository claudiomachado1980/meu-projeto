#!/bin/bash

# ============================================================
#  AUTO_ANALYZER.SH — Script de Automação (Aula 5 — Desafio 6)
#  Corre automaticamente o analyzer e guarda o relatório
#  com a data no nome do ficheiro.
#
#  Uso: ./auto_analyzer.sh <ficheiro.log>
#  Exemplo: ./auto_analyzer.sh 10000.log
# ============================================================

file=$1

# Verifica se o ficheiro foi indicado
if [ -z "$file" ]; then
    echo "❌ Erro: Indica o ficheiro de log."
    echo "Uso: ./auto_analyzer.sh 10000.log"
    exit 1
fi

# Verifica se o ficheiro existe
if [ ! -f "$file" ]; then
    echo "❌ Erro: O ficheiro '$file' não foi encontrado."
    exit 1
fi

echo "⚙️  A iniciar análise automática de: $file"
echo "🕐 Data/Hora: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Chama o analyzer_final.sh em modo automático
./analyzer_final.sh "$file" --auto

echo ""
echo "✅ Automação concluída com sucesso!"
