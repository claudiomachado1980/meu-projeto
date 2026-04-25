#!/bin/bash

# ============================================================
#  ANALYZER FINAL — Analisador de Logs de Sistema
#  Autor  : [O teu nome]
#  Versão : 3.0
#  Descrição: Script completo para análise de ficheiros de log
# ============================================================

# ─── VARIÁVEIS GLOBAIS ──────────────────────────────────────
file=""
filter_data=""   # conteúdo do ficheiro (pode ser filtrado)

# ─── CORES para output mais bonito ──────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'  # No Color (reset)

# ============================================================
# SECÇÃO 1 — VALIDAÇÃO DE ARGUMENTOS
# ============================================================

# Verifica se foi passado pelo menos um argumento (nome do ficheiro)
if [ -z "$1" ]; then
    echo -e "${RED}❌ Erro: Nenhum ficheiro foi indicado.${NC}"
    echo "Uso correto: ./analyzer_final.sh <ficheiro.log> [user=<utilizador>] [action=<AÇÃO>]"
    echo "Exemplos:"
    echo "  ./analyzer_final.sh 10000.log"
    echo "  ./analyzer_final.sh 10000.log user=user13"
    echo "  ./analyzer_final.sh 10000.log action=DOWNLOAD"
    exit 1
fi

file="$1"

# Verifica se o ficheiro existe
if [ ! -f "$file" ]; then
    echo -e "${RED}❌ Erro: O ficheiro '$file' não foi encontrado.${NC}"
    exit 1
fi

# ─── FILTROS OPCIONAIS (Aula 5 — Desafios 2 e 3) ────────────
# Suporta: user=user13  ou  action=DOWNLOAD
user_filter=""
action_filter=""

for arg in "$@"; do
    if [[ "$arg" == user=* ]]; then
        user_filter="${arg#user=}"
    elif [[ "$arg" == action=* ]]; then
        action_filter="${arg#action=}"
    fi
done

# Aplica filtros ao conteúdo do ficheiro
# Se ambos os filtros estiverem ativos, aplica os dois
if [ -n "$user_filter" ] && [ -n "$action_filter" ]; then
    filter_data=$(grep " $user_filter " "$file" | grep " $action_filter ")
    echo -e "${CYAN}🔍 Filtros ativos: utilizador='$user_filter' | ação='$action_filter'${NC}"
elif [ -n "$user_filter" ]; then
    filter_data=$(grep " $user_filter " "$file")
    echo -e "${CYAN}🔍 Filtro ativo: utilizador='$user_filter'${NC}"
elif [ -n "$action_filter" ]; then
    filter_data=$(grep " $action_filter " "$file")
    echo -e "${CYAN}🔍 Filtro ativo: ação='$action_filter'${NC}"
else
    filter_data=$(cat "$file")
fi


# ============================================================
# SECÇÃO 2 — FUNÇÕES (Aula 5 — Desafio 1)
# Cada funcionalidade está numa função separada e reutilizável
# ============================================================

# Retorna o total de linhas no conjunto de dados atual
total_linhas() {
    echo "$filter_data" | grep -c .
}

# Conta erros usando loop linha a linha (Aula 4 — Desafio 2)
total_erros() {
    local count=0
    while IFS= read -r line; do
        if [[ "$line" == *" ERROR "* ]]; then
            ((count++))
        fi
    done <<< "$filter_data"
    echo "$count"
}

# Conta IPs únicos
ips_unicos() {
    echo "$filter_data" | awk '{print $2}' | sort | uniq | wc -l
}

# Conta downloads
total_downloads() {
    echo "$filter_data" | grep -c " DOWNLOAD "
}

# Conta uploads
total_uploads() {
    echo "$filter_data" | grep -c " UPLOAD "
}

# Conta erros com código 500
erros_500() {
    echo "$filter_data" | grep -c " 500$"
}

# IP com mais acessos (top 1)
top_ip() {
    echo "$filter_data" | awk '{print $2}' | sort | uniq -c | sort -nr | head -1 | awk '{print $2, "("$1" acessos)"}'
}

# Top 5 IPs com mais acessos (Aula 5 — Desafio 5)
top5_ips() {
    echo "$filter_data" | awk '{print $2}' | sort | uniq -c | sort -nr | head -5 | \
    awk '{printf "  %s acessos  →  %s\n", $1, $2}'
}

# Utilizador mais ativo
utilizador_mais_ativo() {
    echo "$filter_data" | awk '{print $3}' | sort | uniq -c | sort -nr | head -1 | \
    awk '{print $2, "("$1" ações)"}'
}

# Recurso mais acedido
recurso_mais_acedido() {
    echo "$filter_data" | awk '{print $5}' | sort | uniq -c | sort -nr | head -1 | \
    awk '{print $2, "("$1" vezes)"}'
}

# Utilizador que fez mais downloads
user_mais_downloads() {
    echo "$filter_data" | grep " DOWNLOAD " | awk '{print $3}' | sort | uniq -c | sort -nr | head -1 | \
    awk '{print $2, "("$1" downloads)"}'
}

# IP que gerou mais erros 500
ip_mais_erros500() {
    echo "$filter_data" | grep " 500$" | awk '{print $2}' | sort | uniq -c | sort -nr | head -1 | \
    awk '{print $2, "("$1" erros 500)"}'
}

# Recurso que gera mais erros
recurso_mais_erros() {
    echo "$filter_data" | grep " ERROR " | awk '{print $5}' | sort | uniq -c | sort -nr | head -1 | \
    awk '{print $2, "("$1" erros)"}'
}

# Utilizadores únicos
utilizadores_unicos() {
    echo "$filter_data" | awk '{print $3}' | sort | uniq | wc -l
}


# ============================================================
# SECÇÃO 3 — GERAÇÃO DE RELATÓRIO (Aula 4 — Desafio 5)
# ============================================================

gerar_relatorio() {
    # Nome do ficheiro de relatório inclui data (Aula 5 — Desafio 6)
    local data_hoje
    data_hoje=$(date +%Y-%m-%d)
    local relatorio="relatorio_${data_hoje}.txt"

    echo -e "${YELLOW}📄 A gerar relatório...${NC}"

    {
        echo "=============================================="
        echo "         RELATÓRIO FINAL DE ANÁLISE          "
        echo "=============================================="
        echo "Ficheiro analisado : $file"
        echo "Data de geração    : $(date '+%Y-%m-%d %H:%M:%S')"
        if [ -n "$user_filter" ];   then echo "Filtro utilizador  : $user_filter"; fi
        if [ -n "$action_filter" ]; then echo "Filtro ação        : $action_filter"; fi
        echo "----------------------------------------------"
        echo ""
        echo "--- ESTATÍSTICAS GERAIS ---"
        echo "Total de linhas        : $(total_linhas)"
        echo "Total de erros         : $(total_erros)"
        echo "IPs únicos             : $(ips_unicos)"
        echo "Utilizadores únicos    : $(utilizadores_unicos)"
        echo ""
        echo "--- ATIVIDADE ---"
        echo "Downloads              : $(total_downloads)"
        echo "Uploads                : $(total_uploads)"
        echo "Erros 500              : $(erros_500)"
        echo ""
        echo "--- TOPS ---"
        echo "Top IP                 : $(top_ip)"
        echo "Utilizador mais ativo  : $(utilizador_mais_ativo)"
        echo "Recurso mais acedido   : $(recurso_mais_acedido)"
        echo "Utilizador c/ mais DL  : $(user_mais_downloads)"
        echo "IP com mais erros 500  : $(ip_mais_erros500)"
        echo "Recurso com mais erros : $(recurso_mais_erros)"
        echo ""
        echo "--- TOP 5 IPs ---"
        top5_ips
        echo ""
        echo "=============================================="
    } > "$relatorio"

    echo -e "${GREEN}✅ Relatório guardado em: ${BOLD}$relatorio${NC}"
}


# ============================================================
# SECÇÃO 4 — MENU INTERATIVO (Aula 4 — Desafios 3 e 4)
# ============================================================

mostrar_menu() {
    clear
    echo -e "${BOLD}${CYAN}"
    echo "  ╔══════════════════════════════════════╗"
    echo "  ║      ANALISADOR DE LOGS — v3.0       ║"
    echo "  ╚══════════════════════════════════════╝${NC}"
    echo -e "  Ficheiro: ${YELLOW}$file${NC}"
    if [ -n "$user_filter" ];   then echo -e "  Filtro utilizador: ${YELLOW}$user_filter${NC}"; fi
    if [ -n "$action_filter" ]; then echo -e "  Filtro ação: ${YELLOW}$action_filter${NC}"; fi
    echo ""
    echo "  ┌─────────────────────────────────────┐"
    echo "  │  1 - Total de linhas                │"
    echo "  │  2 - Total de erros                 │"
    echo "  │  3 - IPs únicos                     │"
    echo "  │  4 - Top IP (mais acessos)           │"
    echo "  │  5 - Downloads                      │"
    echo "  │  6 - Uploads                        │"
    echo "  │  7 - Erros 500                      │"
    echo "  │  8 - Utilizador mais ativo          │"
    echo "  │  9 - Recurso mais acedido           │"
    echo "  │  10 - Top 5 IPs                     │"
    echo "  │  11 - Utilizador com mais downloads │"
    echo "  │  12 - IP com mais erros 500         │"
    echo "  │  13 - Recurso que gera mais erros   │"
    echo "  │  14 - Relatório completo no terminal│"
    echo "  │  15 - Guardar relatório em ficheiro │"
    echo "  │  0  - Sair                          │"
    echo "  └─────────────────────────────────────┘"
    echo ""
    echo -n "  Escolhe uma opção: "
}

executar_opcao() {
    local opcao="$1"
    echo ""
    case $opcao in
        1)  echo -e "  📊 ${BOLD}Total de linhas:${NC} $(total_linhas)" ;;
        2)  echo -e "  ⚠️  ${BOLD}Total de erros:${NC} $(total_erros)" ;;
        3)  echo -e "  🌐 ${BOLD}IPs únicos:${NC} $(ips_unicos)" ;;
        4)  echo -e "  🔝 ${BOLD}Top IP:${NC} $(top_ip)" ;;
        5)  echo -e "  📥 ${BOLD}Downloads:${NC} $(total_downloads)" ;;
        6)  echo -e "  📤 ${BOLD}Uploads:${NC} $(total_uploads)" ;;
        7)  echo -e "  🔴 ${BOLD}Erros 500:${NC} $(erros_500)" ;;
        8)  echo -e "  🏆 ${BOLD}Utilizador mais ativo:${NC} $(utilizador_mais_ativo)" ;;
        9)  echo -e "  📂 ${BOLD}Recurso mais acedido:${NC} $(recurso_mais_acedido)" ;;
        10)
            echo -e "  🏅 ${BOLD}Top 5 IPs com mais acessos:${NC}"
            top5_ips
            ;;
        11) echo -e "  💾 ${BOLD}Utilizador com mais downloads:${NC} $(user_mais_downloads)" ;;
        12) echo -e "  🚨 ${BOLD}IP com mais erros 500:${NC} $(ip_mais_erros500)" ;;
        13) echo -e "  ⛔ ${BOLD}Recurso que gera mais erros:${NC} $(recurso_mais_erros)" ;;
        14)
            echo -e "${BOLD}${CYAN}"
            echo "  ══════════════════════════════════════════"
            echo "           RELATÓRIO COMPLETO               "
            echo "  ══════════════════════════════════════════${NC}"
            echo -e "  Total de linhas        : ${YELLOW}$(total_linhas)${NC}"
            echo -e "  Total de erros         : ${RED}$(total_erros)${NC}"
            echo -e "  IPs únicos             : $(ips_unicos)"
            echo -e "  Utilizadores únicos    : $(utilizadores_unicos)"
            echo -e "  Downloads              : $(total_downloads)"
            echo -e "  Uploads                : $(total_uploads)"
            echo -e "  Erros 500              : ${RED}$(erros_500)${NC}"
            echo -e "  Top IP                 : ${YELLOW}$(top_ip)${NC}"
            echo -e "  Utilizador mais ativo  : ${YELLOW}$(utilizador_mais_ativo)${NC}"
            echo -e "  Recurso mais acedido   : $(recurso_mais_acedido)"
            echo -e "  Utilizador c/ mais DL  : $(user_mais_downloads)"
            echo -e "  IP c/ mais erros 500   : ${RED}$(ip_mais_erros500)${NC}"
            echo -e "  Recurso c/ mais erros  : $(recurso_mais_erros)"
            echo ""
            echo -e "  ${BOLD}Top 5 IPs:${NC}"
            top5_ips
            echo -e "${CYAN}  ══════════════════════════════════════════${NC}"
            ;;
        15) gerar_relatorio ;;
        0)
            echo -e "${GREEN}  👋 A sair... Até logo!${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}  ❌ Opção inválida! Escolhe um número entre 0 e 15.${NC}"
            ;;
    esac
    echo ""
    read -rp "  Prima [Enter] para continuar..." _temp
}


# ============================================================
# SECÇÃO 5 — AUTOMAÇÃO (Aula 5 — Desafio 6)
# Se chamado com o argumento --auto, corre automaticamente
# e guarda o relatório sem interação do utilizador
# Exemplo: ./analyzer_final.sh 10000.log --auto
# ============================================================

for arg in "$@"; do
    if [[ "$arg" == "--auto" ]]; then
        echo -e "${CYAN}⚙️  Modo automático ativado...${NC}"
        gerar_relatorio
        echo -e "${GREEN}✅ Análise automática concluída!${NC}"
        exit 0
    fi
done


# ============================================================
# SECÇÃO 6 — LOOP PRINCIPAL DO MENU (Aula 4 — Desafio 4)
# O menu repete até o utilizador escolher sair (opção 0)
# ============================================================

while true; do
    mostrar_menu
    read -r opcao
    executar_opcao "$opcao"
done
