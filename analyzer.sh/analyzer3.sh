#!/bin/bash

file=$1

# Validação: Verifica se o ficheiro foi passado e se existe
if [ ! -f "$file" ]; then
    echo "Erro: Ficheiro '$file' não encontrado."
    exit 1
fi

while true
do
    clear
    echo "======= MENU DE ANÁLISE ======="
    echo "1 - Total de linhas"
    echo "2 - Total de erros"
    echo "3 - IPs únicos"
    echo "4 - Top IP"
    echo "5 - Downloads"
    echo "6 - Sair"
    echo "7 - Gerar relatório para ficheiro"
    echo "==============================="
    echo -n "Escolha uma opção: "
    read option

    case $option in
        1)
            echo "📊 Total de linhas: $(wc -l < "$file")"
            ;;
        2)
            # Desafio 2: Contagem com loop para ser mais rigoroso
            count=0
            while read -r line; do
                if echo "$line" | grep -qE "ERROR|401|403|404|500"; then
                    ((count++))
                fi
            done < "$file"
            echo "⚠️ Total de erros: $count"
            ;;
        3)
            echo "🌐 IPs únicos: $(cut -d ' ' -f2 "$file" | sort | uniq | wc -l)"
            ;;
        4)
            echo "🔝 Top IP: $(cut -d ' ' -f2 "$file" | sort | uniq -c | sort -nr | head -1)"
            ;;
        5)
            echo "📥 Downloads: $(grep "DOWNLOAD" "$file" | wc -l)"
            ;;
        6)
            echo "👋 A sair..."
            break
            ;;
        7)
            # --- DESAFIO 5: Formatação exata da imagem ---
            echo "📄 A gerar o ficheiro 'relatorio.txt'..."
            
            # Cálculo das variáveis para o ficheiro
            linhas=$(wc -l < "$file")
            erros=$(grep -E "ERROR|401|403|404|500" "$file" | wc -l)
            ips=$(cut -d ' ' -f2 "$file" | sort | uniq | wc -l)
            top_ip=$(cut -d ' ' -f2 "$file" | sort | uniq -c | sort -nr | head -1)
            downloads=$(grep "DOWNLOAD" "$file" | wc -l)

            # Escrita no ficheiro com o formato da imagem
            {
                echo "RELATÓRIO"
                echo "Total linhas: $linhas"
                echo "Total erros: $erros"
                echo "IPs únicos: $ips"
                echo "Top IP: $top_ip"
                echo "Downloads: $downloads"
            } > relatorio.txt
            
            echo "✅ Relatório gravado com sucesso!"
            ;;
        *)
            echo "❌ Opção inválida!"
            ;;
    esac

    # A TUA PAUSA (Mantida exatamente como pediste)
    if [ "$option" != "6" ]; then
        echo ""
        read -p "Pressione [Enter] para continuar..." temp
    fi
done

