#!/bin/bash

file=$1

# --- VALIDAÇÃO ---
if [ -z "$file" ]; then
    echo "❌ Erro: Por favor, indica o nome do ficheiro de log."
    echo "Exemplo: ./analyzer3.sh 10000.log"
    exit 1
fi

if [ ! -f "$file" ]; then
    echo "❌ Erro: Ficheiro '$file' não encontrado."
    exit 1
fi

# --- MENU INTERATIVO ---
while true
do
    clear
    echo "======= MENU DE ANÁLISE ======="
    echo "1 - Total de linhas"
    echo "2 - Total de erros"
    echo "3 - IPs únicos"
    echo "4 - Top IP"
    echo "5 - Downloads"
    echo "6 - Gerar relatório para ficheiro"
    echo "7 - Sair"
    echo "==============================="
    echo -n "Escolha uma opção: "
    read option

    case $option in
        1)
            echo "📊 Total de linhas: $(wc -l < "$file")"
            ;;
        2)
            # Contagem com loop para ser rigoroso (evita falsos positivos)
            count=0
            while IFS= read -r line; do
                if [[ "$line" == *" ERROR "* ]]; then
                    ((count++))
                fi
            done < "$file"
            echo "⚠️  Total de erros: $count"
            ;;
        3)
            echo "🌐 IPs únicos: $(awk '{print $2}' "$file" | sort | uniq | wc -l)"
            ;;
        4)
            echo "🔝 Top IP: $(awk '{print $2}' "$file" | sort | uniq -c | sort -nr | head -1)"
            ;;
        5)
            echo "📥 Downloads: $(grep -c " DOWNLOAD " "$file")"
            ;;
        6)
            echo "📄 A gerar o ficheiro 'relatorio.txt'..."

            # Cálculo das variáveis
            linhas=$(wc -l < "$file")
            
            erros=0
            while IFS= read -r line; do
                if [[ "$line" == *" ERROR "* ]]; then
                    ((erros++))
                fi
            done < "$file"

            ips=$(awk '{print $2}' "$file" | sort | uniq | wc -l)
            top_ip=$(awk '{print $2}' "$file" | sort | uniq -c | sort -nr | head -1)
            downloads=$(grep -c " DOWNLOAD " "$file")

            # Escrita no ficheiro com formato consistente
            {
                echo "RELATÓRIO FINAL"
                echo "----------------------------"
                echo "Total linhas: $linhas"
                echo "Total erros: $erros"
                echo "IPs únicos: $ips"
                echo "Top IP: $top_ip"
                echo "Downloads: $downloads"
                echo "----------------------------"
            } > relatorio.txt

            echo "✅ Relatório gravado com sucesso em relatorio.txt!"
            ;;
        7)
            echo "👋 A sair..."
            break
            ;;
        *)
            echo "❌ Opção inválida!"
            ;;
    esac

    echo ""
    read -p "Pressione [Enter] para continuar..." temp
done
