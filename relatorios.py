# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR
# Ficheiro: relatorios.py
# -----------------------------------------------------------------------------
# Este ficheiro foi criado na V2 do projeto.
#
# Objetivo deste ficheiro:
# ------------------------
# Criar relatórios simples com base nos bens registados no inventário.
#
# Porque é que criámos um ficheiro separado?
# ------------------------------------------
# Para manter o projeto organizado:
#
# - produtos.py
#   Define a estrutura dos bens.
#
# - gestao.py
#   Trata da gestão do inventário.
#
# - main.py
#   Mostra o menu principal ao utilizador.
#
# - relatorios.py
#   Trata apenas dos relatórios.
#
# Assim, cada ficheiro tem uma responsabilidade própria.
# =============================================================================


# =============================================================================
# 1) FUNÇÃO contar_por_campo(...)
# -----------------------------------------------------------------------------
# Esta função é uma função auxiliar.
#
# Ela serve para contar quantos bens existem agrupados por um determinado campo.
#
# Exemplos:
# ---------
# Se o campo for "categoria", conta quantos bens existem por categoria.
# Se o campo for "estado", conta quantos bens existem por estado.
# Se o campo for "localizacao", conta quantos bens existem por localização.
# =============================================================================
import os

def contar_por_campo(lista_bens, campo):
    """
    Conta quantos bens existem para cada valor de um determinado campo.

    Parâmetros:
        lista_bens (list):
            Lista com todos os bens do inventário.

        campo (str):
            Nome do campo que queremos contar.
            Exemplos: "categoria", "estado", "localizacao"

    Devolve:
        dict:
            Dicionário com as contagens encontradas.
            Exemplo:
            {
                "Mobiliário": 5,
                "Equipamento Informático": 3
            }
    """

    # Dicionário onde vamos guardar as contagens.
    contagens = {}

    # Percorremos todos os bens da lista.
    for bem in lista_bens:

        # Vamos buscar o valor do campo pretendido.
        # Usamos get() para evitar erro caso algum campo não exista.
        valor = bem.get(campo, "Sem informação")

        # Se o valor estiver vazio, usamos um texto padrão.
        if valor == "":
            valor = "Sem informação"

        # Se este valor já existir no dicionário, somamos 1.
        if valor in contagens:
            contagens[valor] += 1

        # Se ainda não existir, começamos a contagem em 1.
        else:
            contagens[valor] = 1

    # No final devolvemos o dicionário com as contagens.
    return contagens


# =============================================================================
# 2) FUNÇÃO mostrar_contagens(...)
# -----------------------------------------------------------------------------
# Esta função recebe um título e um dicionário de contagens.
# Depois mostra essa informação no terminal de forma organizada.
# =============================================================================
def mostrar_contagens(titulo, contagens):
    """
    Mostra no terminal as contagens de um relatório.

    Parâmetros:
        titulo (str):
            Título do relatório.

        contagens (dict):
            Dicionário com os dados a apresentar.
    """

    print("\n" + "=" * 50)
    print(titulo)
    print("=" * 50)

    # Se não existirem dados, mostramos uma mensagem informativa.
    if not contagens:
        print("[INFO] Não existem dados para apresentar.")

    # Caso existam dados, mostramos cada linha do relatório.
    else:
        for descricao, quantidade in contagens.items():
            print(f"{descricao}: {quantidade}")

    print("=" * 50)


# =============================================================================
# 3) FUNÇÃO relatorio_geral(...)
# -----------------------------------------------------------------------------
# Esta função mostra um resumo geral do inventário.
#
# O relatório apresenta:
# - total de bens registados
# - resumo por categoria
# - resumo por estado
# - resumo por localização
# =============================================================================
def relatorio_geral(lista_bens):
    """
    Mostra um relatório geral do inventário.

    Parâmetros:
        lista_bens (list):
            Lista com todos os bens registados.
    """

    print("\n" + "=" * 50)
    print("RELATÓRIO GERAL DO INVENTÁRIO")
    print("=" * 50)

    # Calculamos o total de bens registados.
    total_bens = len(lista_bens)

    print(f"Total de bens registados: {total_bens}")

    # Se não houver bens, não vale a pena continuar.
    if total_bens == 0:
        print("[INFO] O inventário está vazio.")
        print("=" * 50)
        return

    # -------------------------------------------------------------------------
    # Resumo por categoria
    # -------------------------------------------------------------------------
    print("\nResumo por categoria:")
    contagens_categoria = contar_por_campo(lista_bens, "categoria")

    for categoria, quantidade in contagens_categoria.items():
        print(f"- {categoria}: {quantidade}")

    # -------------------------------------------------------------------------
    # Resumo por estado
    # -------------------------------------------------------------------------
    print("\nResumo por estado:")
    contagens_estado = contar_por_campo(lista_bens, "estado")

    for estado, quantidade in contagens_estado.items():
        print(f"- {estado}: {quantidade}")

    # -------------------------------------------------------------------------
    # Resumo por localização
    # -------------------------------------------------------------------------
    print("\nResumo por localização:")
    contagens_localizacao = contar_por_campo(lista_bens, "localizacao")

    for localizacao, quantidade in contagens_localizacao.items():
        print(f"- {localizacao}: {quantidade}")

    print("=" * 50)


# =============================================================================
# 4) FUNÇÃO relatorio_por_categoria(...)
# -----------------------------------------------------------------------------
# Esta função mostra apenas o relatório por categoria.
# =============================================================================
def relatorio_por_categoria(lista_bens):
    """
    Mostra quantos bens existem por categoria.

    Parâmetros:
        lista_bens (list):
            Lista com todos os bens registados.
    """

    contagens = contar_por_campo(lista_bens, "categoria")
    mostrar_contagens("RELATÓRIO POR CATEGORIA", contagens)


# =============================================================================
# 5) FUNÇÃO relatorio_por_estado(...)
# -----------------------------------------------------------------------------
# Esta função mostra apenas o relatório por estado.
# =============================================================================
def relatorio_por_estado(lista_bens):
    """
    Mostra quantos bens existem por estado.

    Parâmetros:
        lista_bens (list):
            Lista com todos os bens registados.
    """

    contagens = contar_por_campo(lista_bens, "estado")
    mostrar_contagens("RELATÓRIO POR ESTADO", contagens)


# =============================================================================
# 6) FUNÇÃO relatorio_por_localizacao(...)
# -----------------------------------------------------------------------------
# Esta função mostra apenas o relatório por localização.
# =============================================================================
def relatorio_por_localizacao(lista_bens):
    """
    Mostra quantos bens existem por localização.

    Parâmetros:
        lista_bens (list):
            Lista com todos os bens registados.
    """

    contagens = contar_por_campo(lista_bens, "localizacao")
    mostrar_contagens("RELATÓRIO POR LOCALIZAÇÃO", contagens)


# =============================================================================
# 7) FUNÇÃO exportar_relatorio_txt(...)
# -----------------------------------------------------------------------------
# Esta função exporta um relatório geral para um ficheiro de texto.
#
# Nesta fase, vamos exportar para TXT porque é simples e adequado ao nível
# atual do projeto.
#
# Mais tarde, numa versão futura, podemos evoluir para:
# - CSV
# - Excel
# - PDF
# =============================================================================
def exportar_relatorio_txt(lista_bens):
    """
    Exporta um relatório geral do inventário para um ficheiro TXT.

    Parâmetros:
        lista_bens (list):
            Lista com todos os bens registados.
    """
    # Criamos a pasta dos relatórios, caso ainda não exista.
    os.makedirs("relatorios_exportados", exist_ok=True)

    # Nome do ficheiro que será criado.
    nome_ficheiro = "relatorios_exportados/relatorio_inventario.txt"

    # Calculamos as contagens necessárias.
    total_bens = len(lista_bens)
    contagens_categoria = contar_por_campo(lista_bens, "categoria")
    contagens_estado = contar_por_campo(lista_bens, "estado")
    contagens_localizacao = contar_por_campo(lista_bens, "localizacao")

    # Abrimos o ficheiro em modo escrita.
    with open(nome_ficheiro, "w", encoding="utf-8") as ficheiro:

        ficheiro.write("RELATÓRIO GERAL DO INVENTÁRIO\n")
        ficheiro.write("=" * 50 + "\n\n")

        ficheiro.write(f"Total de bens registados: {total_bens}\n\n")

        # ---------------------------------------------------------------------
        # Escrever resumo por categoria
        # ---------------------------------------------------------------------
        ficheiro.write("Resumo por categoria:\n")

        if not contagens_categoria:
            ficheiro.write("- Sem dados para apresentar\n")
        else:
            for categoria, quantidade in contagens_categoria.items():
                ficheiro.write(f"- {categoria}: {quantidade}\n")

        # ---------------------------------------------------------------------
        # Escrever resumo por estado
        # ---------------------------------------------------------------------
        ficheiro.write("\nResumo por estado:\n")

        if not contagens_estado:
            ficheiro.write("- Sem dados para apresentar\n")
        else:
            for estado, quantidade in contagens_estado.items():
                ficheiro.write(f"- {estado}: {quantidade}\n")

        # ---------------------------------------------------------------------
        # Escrever resumo por localização
        # ---------------------------------------------------------------------
        ficheiro.write("\nResumo por localização:\n")

        if not contagens_localizacao:
            ficheiro.write("- Sem dados para apresentar\n")
        else:
            for localizacao, quantidade in contagens_localizacao.items():
                ficheiro.write(f"- {localizacao}: {quantidade}\n")

    print(f"\n[OK] Relatório exportado com sucesso para '{nome_ficheiro}'.")