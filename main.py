# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR
# Ficheiro: main.py
# -----------------------------------------------------------------------------
# Este é o ficheiro principal do programa.
#
# Ordem lógica do projeto:
# ------------------------
# 1) produtos.py
#    Define a estrutura dos bens, categorias, estados, localizações e tipos.
#
# 2) gestao.py
#    Contém a lógica de gestão do inventário:
#    - carregar dados
#    - guardar dados
#    - registar bens
#    - pesquisar bens
#    - listar bens
#    - alterar o estado de um bem
#    - alterar a localização de um bem
#
# 3) relatorios.py
#    Contém os relatórios simples da V2:
#    - relatório geral
#    - relatório por categoria
#    - relatório por estado
#    - relatório por localização
#    - exportação para TXT
#
# 4) main.py
#    Contém o menu principal apresentado ao utilizador.
#    Este ficheiro é o ponto de entrada do programa.
# =============================================================================


# =============================================================================
# 1) IMPORTAÇÃO DAS FUNÇÕES DO FICHEIRO gestao.py
# -----------------------------------------------------------------------------
# Aqui importamos apenas as funções necessárias para construir o menu.
# =============================================================================
from gestao import (
    carregar_dados,              # carrega os bens guardados no ficheiro
    guardar_dados,               # guarda os bens no ficheiro
    registar_bem,                # regista um novo bem
    pesquisar_bem,               # pesquisa bens por ID ou nome
    listar_inventario,           # lista todos os bens
    listar_por_localizacao,      # lista bens de uma localização
    alterar_estado_bem,          # altera o estado de um bem existente
    alterar_localizacao_bem,     # altera a localização de um bem existente
    remover_bem,                 # remove um bem existente
    obter_inventario             # devolve a lista de bens para os relatórios
)


# =============================================================================
# 2) IMPORTAÇÃO DAS FUNÇÕES DO FICHEIRO relatorios.py
# -----------------------------------------------------------------------------
# Estas funções foram criadas na V2 do projeto.
# Servem para gerar relatórios simples com base no inventário.
# =============================================================================
from relatorios import (
    relatorio_geral,              # mostra um resumo geral do inventário
    relatorio_por_categoria,      # mostra totais por categoria
    relatorio_por_estado,         # mostra totais por estado
    relatorio_por_localizacao,    # mostra totais por localização
    exportar_relatorio_txt        # exporta relatório geral para TXT
)

# =============================================================================
# 3) IMPORTAÇÃO DA FUNÇÃO DO FICHEIRO importacao.py
# -----------------------------------------------------------------------------
# Esta função foi criada para importar bens a partir de ficheiros externos.
# =============================================================================
from importacao import (
    importar_bens_de_ficheiro,
    importar_bens_flexivel
)

# =============================================================================
# 4) FUNÇÃO mostrar_menu()
# -----------------------------------------------------------------------------
# Esta função mostra o menu principal ao utilizador.
# Apenas apresenta as opções disponíveis.
# =============================================================================
def mostrar_menu():
    """
    Mostra o menu principal do sistema.

    Esta função apenas apresenta as opções disponíveis.
    A lógica de cada opção é tratada dentro da função main().
    """

    print("\n" + "=" * 50)
    print(" SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR")
    print("=" * 50)
    print("1. Registar novo bem")
    print("2. Pesquisar bem")
    print("3. Listar inventário completo")
    print("4. Listar bens por localização")
    print("5. Alterar estado de um bem")
    print("6. Alterar localização de um bem")
    print("7. Remover bem")
    print("8. Relatório geral")
    print("9. Relatório por categoria")
    print("10. Relatório por estado")
    print("11. Relatório por localização")
    print("12. Exportar relatório para TXT")
    print("13. Importar bens de ficheiro externo")
    print("14. Importar bens com mapeamento flexível")
    print("0. Guardar e sair")
    print("=" * 50)



# =============================================================================
# 5) FUNÇÃO main()
# -----------------------------------------------------------------------------
# Esta é a função principal do programa.
#
# Lógica:
# -------
# 1) Carrega os dados guardados no ficheiro
# 2) Mostra o menu em ciclo
# 3) Executa a opção escolhida pelo utilizador
# 4) Guarda os dados sempre que houver alterações
# 5) Sai quando o utilizador escolher a opção 0
# =============================================================================
def main():
    """
    Função principal do programa.
    """

    # -------------------------------------------------------------------------
    # PASSO 1 - Carregar dados existentes
    # -------------------------------------------------------------------------
    # Quando o programa arranca, tenta ler o ficheiro inventario.txt.
    # Se o ficheiro existir, os bens são carregados para a memória.
    # Se não existir, o programa começa com inventário vazio.
    carregar_dados()

    # -------------------------------------------------------------------------
    # PASSO 2 - Ciclo principal do menu
    # -------------------------------------------------------------------------
    # O menu fica a repetir até o utilizador escolher sair.
    while True:

        mostrar_menu()

        opcao = input("Escolha uma opção: ").strip()

        # ---------------------------------------------------------------------
        # OPÇÃO 1 - Registar novo bem
        # ---------------------------------------------------------------------
        if opcao == "1":
            registar_bem()

            # Como o inventário foi alterado, guardamos logo os dados.
            # Isto garante a persistência da informação.
            guardar_dados()

        # ---------------------------------------------------------------------
        # OPÇÃO 2 - Pesquisar bem
        # ---------------------------------------------------------------------
        elif opcao == "2":
            pesquisar_bem()

            # Pesquisar não altera dados.
            # Por isso, aqui não é necessário guardar.

        # ---------------------------------------------------------------------
        # OPÇÃO 3 - Listar inventário completo
        # ---------------------------------------------------------------------
        elif opcao == "3":
            listar_inventario()

            # Listar também não altera dados.
            # Por isso, não é necessário guardar.

        # ---------------------------------------------------------------------
        # OPÇÃO 4 - Listar bens por localização
        # ---------------------------------------------------------------------
        elif opcao == "4":
            listar_por_localizacao()

            # Esta opção apenas consulta dados.
            # Também não precisa de guardar.

        # ---------------------------------------------------------------------
        # OPÇÃO 5 - Alterar estado de um bem
        # ---------------------------------------------------------------------
        # Esta opção permite mudar o estado de um bem já registado.
        # Exemplo:
        #   Bom -> Danificado
        #   Danificado -> Em Reparação
        #
        # Como esta opção altera dados, chamamos guardar_dados()
        # logo a seguir, garantindo a persistência da alteração.
        elif opcao == "5":
            alterar_estado_bem()
            guardar_dados()

        # ---------------------------------------------------------------------
        # OPÇÃO 6 - Alterar localização de um bem
        # ---------------------------------------------------------------------
        # Esta opção permite mudar a localização de um bem.
        # Exemplo:
        #   Sala 1 -> Biblioteca
        #   Laboratório -> Armazém
        #
        # Como esta opção também altera dados, guardamos logo no ficheiro.
        elif opcao == "6":
            alterar_localizacao_bem()
            guardar_dados()

        # ---------------------------------------------------------------------
        # OPÇÃO 7 - Remover bem
        # ---------------------------------------------------------------------
        elif opcao == "7":
            remover_bem()
            guardar_dados()


        # ---------------------------------------------------------------------
        # OPÇÃO 8 - Relatório geral
        # ---------------------------------------------------------------------
        # Esta opção mostra um resumo geral do inventário:
        # - total de bens
        # - bens por categoria
        # - bens por estado
        # - bens por localização
        #
        # Como esta opção apenas consulta dados, não é necessário guardar.
        elif opcao == "8":
            lista_bens = obter_inventario()
            relatorio_geral(lista_bens)

        # ---------------------------------------------------------------------
        # OPÇÃO 9 - Relatório por categoria
        # ---------------------------------------------------------------------
        # Esta opção mostra quantos bens existem em cada categoria.
        # Exemplo:
        #   Mobiliário: 5
        #   Equipamento Informático: 3
        elif opcao == "9":
            lista_bens = obter_inventario()
            relatorio_por_categoria(lista_bens)

        # ---------------------------------------------------------------------
        # OPÇÃO 10 - Relatório por estado
        # ---------------------------------------------------------------------
        # Esta opção mostra quantos bens existem em cada estado.
        # Exemplo:
        #   Novo: 2
        #   Bom: 6
        #   Danificado: 1
        elif opcao == "10":
            lista_bens = obter_inventario()
            relatorio_por_estado(lista_bens)

        # ---------------------------------------------------------------------
        # OPÇÃO 11 - Relatório por localização
        # ---------------------------------------------------------------------
        # Esta opção mostra quantos bens existem em cada localização.
        # Exemplo:
        #   Sala 1: 4
        #   Biblioteca: 2
        #   Laboratório: 1
        elif opcao == "11":
            lista_bens = obter_inventario()
            relatorio_por_localizacao(lista_bens)

        # ---------------------------------------------------------------------
        # OPÇÃO 12 - Exportar relatório para TXT
        # ---------------------------------------------------------------------
        # Esta opção cria um ficheiro chamado relatorio_inventario.txt
        # com um resumo geral do inventário.
        #
        # Como apenas cria um relatório, não altera o inventário.
        elif opcao == "12":
            lista_bens = obter_inventario()
            exportar_relatorio_txt(lista_bens)

        # ---------------------------------------------------------------------
        # OPÇÃO 13 - Importar bens de ficheiro externo
        # ---------------------------------------------------------------------
        # Esta opção permite importar bens a partir de um ficheiro .txt ou .csv.
        #
        # O ficheiro deve seguir a estrutura:
        # id;nome;categoria;estado;localizacao
        #
        # Como esta opção pode adicionar novos bens ao inventário,
        # chamamos guardar_dados() no final.
        elif opcao == "13":
            lista_bens = obter_inventario()
            importar_bens_de_ficheiro(lista_bens)
            guardar_dados()

        # ---------------------------------------------------------------------
        # OPÇÃO 14 - Importar bens com mapeamento flexível
        # ---------------------------------------------------------------------
        # Esta opção permite importar ficheiros externos com colunas diferentes.
        #
        # O utilizador associa as colunas do ficheiro aos campos principais
        # do sistema:
        # - nome
        # - id
        # - categoria
        # - estado
        # - localização
        #
        # Se faltar algum campo, o sistema tenta completar:
        # - ID: gera automaticamente
        # - categoria: tenta descobrir pelo nome ou usa "Outro"
        # - estado: pede um valor padrão
        # - localização: pede um valor padrão
        #
        # Como esta opção pode adicionar novos bens ao inventário,
        # chamamos guardar_dados() no final.
        elif opcao == "14":
            lista_bens = obter_inventario()
            importar_bens_flexivel(lista_bens)
            guardar_dados()

        # ---------------------------------------------------------------------
        # OPÇÃO 0 - Guardar e sair
        # ---------------------------------------------------------------------
        elif opcao == "0":
            guardar_dados()
            print("\n[OK] Dados guardados com sucesso.")
            print("[INFO] Programa terminado.")
            break

        # ---------------------------------------------------------------------
        # OPÇÃO INVÁLIDA
        # ---------------------------------------------------------------------
        else:
            print("[AVISO] Opção inválida. Tente novamente.")


# =============================================================================
# 6) PONTO DE ENTRADA DO PROGRAMA
# -----------------------------------------------------------------------------
# Esta condição garante que o programa começa pela função main()
# quando executamos:
#
#     python main.py
#
# =============================================================================
if __name__ == "__main__":
    main()
