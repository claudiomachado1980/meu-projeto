# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR
# Ficheiro: gestao.py
# -----------------------------------------------------------------------------
# Este ficheiro trata da lógica principal do sistema.
#
# Ordem de construção deste ficheiro:
# -----------------------------------
# 1) Primeiro implementamos a leitura e escrita do ficheiro de dados
# 2) Depois criamos funções auxiliares internas
# 3) Só depois implementamos as funções principais do sistema
#
# Porque é que esta ordem faz sentido?
# ------------------------------------
# Porque antes de registar, pesquisar ou listar bens, o sistema tem de saber:
# - carregar os dados do ficheiro
# - guardar os dados no ficheiro
# - encontrar bens pelo ID
# - gerar novos IDs automaticamente
#
# Só depois disso faz sentido construir as operações principais.
# =============================================================================


# =============================================================================
# 1) IMPORTAÇÃO DE FUNÇÕES E DADOS DO FICHEIRO produtos.py
# -----------------------------------------------------------------------------
# Aqui vamos buscar:
# - a função para criar bens
# - a função que converte bem -> linha
# - a função que converte linha -> bem
# - a função para mostrar um bem
# - a função para mostrar opções ao utilizador
# - os tipos de bens iniciais
# - as funções para obter categoria e radical automaticamente
# - as listas de estados e localizações
# =============================================================================
from produtos import (
    criar_bem,
    bem_para_linha,
    linha_para_bem,
    mostrar_bem,
    mostrar_opcoes,
    nomes_tipos_bens,
    obter_categoria_do_bem,
    obter_radical_do_bem,
    ESTADOS,
    LOCALIZACOES
)


# =============================================================================
# 2) NOME DO FICHEIRO DE DADOS
# -----------------------------------------------------------------------------
# Este é o ficheiro onde o inventário será guardado de forma permanente.
# Nesta V1, vamos usar um ficheiro de texto simples.
# =============================================================================
FICHEIRO_DADOS = "inventario.txt"


# =============================================================================
# 3) INVENTÁRIO EM MEMÓRIA
# -----------------------------------------------------------------------------
# Esta lista guarda todos os bens enquanto o programa está a correr.
# Quando o sistema arranca:
# - lê o ficheiro
# - carrega os bens para esta lista
#
# Depois, ao guardar:
# - pega nesta lista
# - escreve tudo no ficheiro
# =============================================================================
inventario = []


# =============================================================================
# 4) FUNÇÕES DE LEITURA E ESCRITA DE FICHEIRO
# =============================================================================

def carregar_dados():
    """
    Lê o ficheiro inventario.txt e carrega os bens para a lista 'inventario'.

    O que esta função faz:
    ----------------------
    1. Limpa a lista atual em memória
    2. Tenta abrir o ficheiro em modo leitura
    3. Lê linha a linha
    4. Converte cada linha num dicionário de bem
    5. Guarda cada bem válido na lista 'inventario'

    Se o ficheiro não existir:
    --------------------------
    O sistema não dá erro fatal.
    Apenas arranca com inventário vazio.
    """
    global inventario

    # Antes de carregar os dados, limpamos a lista em memória.
    # Isto evita duplicações caso a função seja chamada mais do que uma vez.
    inventario = []

    try:
        # Abrimos o ficheiro em modo leitura.
        with open(FICHEIRO_DADOS, "r", encoding="utf-8") as ficheiro:

            # Lemos o ficheiro linha a linha.
            for linha in ficheiro:
                bem = linha_para_bem(linha)

                # Só adicionamos à lista se a linha for válida.
                if bem is not None:
                    inventario.append(bem)

        print(f"[OK] {len(inventario)} bem(ns) carregado(s) do ficheiro.")

    except FileNotFoundError:
        print("[INFO] Ficheiro de dados não encontrado.")
        print("[INFO] O sistema vai iniciar com inventário vazio.")


def guardar_dados():
    """
    Guarda todos os bens da lista 'inventario' no ficheiro inventario.txt.

    O que esta função faz:
    ----------------------
    1. Abre o ficheiro em modo escrita ('w')
    2. Reescreve todo o conteúdo do ficheiro
    3. Guarda cada bem numa linha

    Nota:
    -----
    Como usamos 'w', o ficheiro é reescrito de novo com o estado atual.
    """
    # Abrimos o ficheiro em modo escrita.
    with open(FICHEIRO_DADOS, "w", encoding="utf-8") as ficheiro:

        # Percorremos todos os bens em memória.
        for bem in inventario:
            linha = bem_para_linha(bem)
            ficheiro.write(linha)


# =============================================================================
# 5) FUNÇÕES AUXILIARES INTERNAS
# -----------------------------------------------------------------------------
# Estas funções ajudam o sistema internamente.
# Não são chamadas diretamente pelo utilizador no menu.
# =============================================================================

def obter_inventario():
    """
    Devolve a lista de bens atualmente carregados em memória.

    Esta função foi criada para permitir que outros módulos,
    como o ficheiro relatorios.py, consigam consultar o inventário
    sem mexer diretamente na variável global 'inventario'.

    Na V2, esta função será usada para gerar relatórios.
    """

    return inventario


def _encontrar_bem_por_id(id_bem):
    """
    Procura um bem pelo ID.

    Parâmetros:
        id_bem (str):
            ID do bem a procurar.

    Devolve:
        dict:
            Se encontrar o bem.

        None:
            Se não encontrar.
    """
    # Percorremos todos os bens do inventário.
    for bem in inventario:

        # Se o ID corresponder, devolvemos logo esse bem.
        if bem["id"] == id_bem:
            return bem

    # Se chegarmos ao fim sem encontrar, devolvemos None.
    return None


def _gerar_novo_id(radical):
    """
    Gera automaticamente um novo ID para um determinado tipo de bem.

    Exemplo:
    --------
    Se o radical for 'MSA' e já existirem:
        MSA0001
        MSA0002

    então o próximo será:
        MSA0003

    Parâmetros:
        radical (str):
            Radical do tipo de bem.

    Devolve:
        str:
            Novo ID gerado automaticamente.
    """
    # Lista para guardar apenas os números já usados com este radical.
    numeros_existentes = []

    # Percorremos todos os bens já existentes no inventário.
    for bem in inventario:
        id_atual = bem["id"]

        # Verificamos se este ID começa com o radical pretendido.
        if id_atual.startswith(radical):

            # Extraímos apenas a parte numérica do ID.
            parte_numerica = id_atual[len(radical):]

            # Confirmamos que essa parte é composta só por números.
            if parte_numerica.isdigit():
                numeros_existentes.append(int(parte_numerica))

    # Se ainda não existir nenhum bem com esse radical,
    # começamos a numeração em 0001.
    if not numeros_existentes:
        return f"{radical}0001"

    # Caso já existam IDs com este radical:
    # - encontramos o maior número
    # - somamos 1
    proximo_numero = max(numeros_existentes) + 1

    # Devolvemos o novo ID com 4 dígitos.
    return f"{radical}{str(proximo_numero).zfill(4)}"


# =============================================================================
# 6) FUNÇÕES PRINCIPAIS DO SISTEMA
# =============================================================================

def registar_bem():
    """
    Regista um novo bem no sistema.

    Lógica desta função:
    --------------------
    1. O utilizador escolhe o nome/tipo do bem
    2. O sistema obtém automaticamente a categoria
    3. O sistema obtém automaticamente o radical
    4. O sistema gera automaticamente o novo ID
    5. O utilizador escolhe o estado
    6. O utilizador escolhe a localização
    7. O bem é criado e adicionado ao inventário
    """
    print("\n=== REGISTAR NOVO BEM ===")

    # -------------------------------------------------------------------------
    # PASSO 1 - Escolher o nome/tipo do bem
    # -------------------------------------------------------------------------
    lista_nomes_bens = nomes_tipos_bens()
    nome_bem = mostrar_opcoes(lista_nomes_bens, "Escolha o tipo de bem")

    # -------------------------------------------------------------------------
    # PASSO 2 - Obter automaticamente a categoria do bem
    # -------------------------------------------------------------------------
    categoria = obter_categoria_do_bem(nome_bem)

    # -------------------------------------------------------------------------
    # PASSO 3 - Obter automaticamente o radical do ID
    # -------------------------------------------------------------------------
    radical = obter_radical_do_bem(nome_bem)

    # -------------------------------------------------------------------------
    # PASSO 4 - Gerar automaticamente o novo ID
    # -------------------------------------------------------------------------
    novo_id = _gerar_novo_id(radical)

    # -------------------------------------------------------------------------
    # PASSO 5 - Escolher o estado do bem
    # -------------------------------------------------------------------------
    estado = mostrar_opcoes(ESTADOS, "Escolha o estado do bem")

    # -------------------------------------------------------------------------
    # PASSO 6 - Escolher a localização do bem
    # -------------------------------------------------------------------------
    localizacao = mostrar_opcoes(LOCALIZACOES, "Escolha a localização do bem")

    # -------------------------------------------------------------------------
    # PASSO 7 - Criar o dicionário do bem
    # -------------------------------------------------------------------------
    novo_bem = criar_bem(
        id_bem=novo_id,
        nome=nome_bem,
        categoria=categoria,
        estado=estado,
        localizacao=localizacao
    )

    # -------------------------------------------------------------------------
    # PASSO 8 - Adicionar o novo bem à lista em memória
    # -------------------------------------------------------------------------
    inventario.append(novo_bem)

    # -------------------------------------------------------------------------
    # PASSO 9 - Mostrar confirmação ao utilizador
    # -------------------------------------------------------------------------
    print("\n[OK] Bem registado com sucesso!")
    print("[INFO] Dados do novo bem:")
    mostrar_bem(novo_bem)


def pesquisar_bem():
    """
    Permite pesquisar bens pelo ID ou pelo nome.

    Lógica:
    -------
    O utilizador introduz um texto.
    O sistema vai procurar:
    - se esse texto aparece no ID
    - ou se aparece no nome

    A pesquisa ao nome não distingue maiúsculas/minúsculas.
    """
    print("\n=== PESQUISAR BEM ===")

    # Se o inventário estiver vazio, não vale a pena continuar.
    if not inventario:
        print("[INFO] O inventário está vazio.")
        return

    # Pedimos ao utilizador o termo de pesquisa.
    termo = input("Introduza o ID ou nome do bem a pesquisar: ").strip()

    # Se o utilizador não escrever nada, avisamos e terminamos a função.
    if not termo:
        print("[AVISO] Não introduziu nenhum termo de pesquisa.")
        return

    # Criamos uma versão em minúsculas do termo,
    # para facilitar comparações sem distinguir maiúsculas/minúsculas.
    termo_minusculas = termo.lower()

    # Lista onde vamos guardar todos os resultados encontrados.
    resultados = []

    # Percorremos todos os bens do inventário.
    for bem in inventario:
        if termo_minusculas in bem["id"].lower() or termo_minusculas in bem["nome"].lower():
            resultados.append(bem)

    # Mostrar o resultado final da pesquisa.
    if not resultados:
        print("[INFO] Nenhum bem encontrado.")
    else:
        print(f"\n[OK] Foram encontrados {len(resultados)} resultado(s):")
        for bem in resultados:
            mostrar_bem(bem)


def listar_inventario():
    """
    Mostra no ecrã todos os bens do inventário.
    """
    print("\n=== INVENTÁRIO COMPLETO ===")

    # Se o inventário estiver vazio, mostramos uma mensagem informativa.
    if not inventario:
        print("[INFO] O inventário está vazio.")
        return

    # Mostramos o total de bens registados.
    print(f"[INFO] Total de bens registados: {len(inventario)}\n")

    # Mostramos cada bem.
    for bem in inventario:
        mostrar_bem(bem)


def listar_por_localizacao():
    """
    Mostra os bens existentes numa determinada localização.

    Lógica:
    -------
    1. O utilizador escolhe uma localização
    2. O sistema filtra os bens dessa localização
    3. O sistema apresenta os resultados
    """
    print("\n=== LISTAR BENS POR LOCALIZAÇÃO ===")

    # Se o inventário estiver vazio, não há nada para listar.
    if not inventario:
        print("[INFO] O inventário está vazio.")
        return

    # O utilizador escolhe a localização que pretende consultar.
    local_escolhido = mostrar_opcoes(LOCALIZACOES, "Escolha a localização")

    # Lista onde vamos guardar os bens encontrados nesse local.
    bens_no_local = []

    # Percorremos o inventário e guardamos apenas os bens do local escolhido.
    for bem in inventario:
        if bem["localizacao"] == local_escolhido:
            bens_no_local.append(bem)

    # Mostramos o resultado final.
    if not bens_no_local:
        print(f"[INFO] Não existem bens registados em '{local_escolhido}'.")
    else:
        print(f"\n[OK] Existem {len(bens_no_local)} bem(ns) em '{local_escolhido}':")
        for bem in bens_no_local:
            mostrar_bem(bem)


def alterar_estado_bem():
    """
    Altera o estado de um bem já existente.

    Lógica:
    -------
    1. O utilizador introduz o ID do bem
    2. O sistema procura esse bem no inventário
    3. Se encontrar, mostra os dados atuais
    4. O utilizador escolhe o novo estado
    5. O estado do bem é atualizado

    Nota:
    -----
    Esta função altera apenas os dados em memória.
    A gravação no ficheiro será feita no main.py com guardar_dados().
    """

    print("\n=== ALTERAR ESTADO DE UM BEM ===")

    # Se o inventário estiver vazio, não há bens para alterar.
    if not inventario:
        print("[INFO] O inventário está vazio.")
        return

    # Pedimos o ID do bem.
    id_bem = input("Introduza o ID do bem: ").strip().upper()

    # Procuramos o bem usando a função auxiliar interna.
    bem = _encontrar_bem_por_id(id_bem)

    # Se não encontrar, avisamos o utilizador.
    if bem is None:
        print("[AVISO] Bem não encontrado.")
        return

    # Mostramos o bem encontrado antes da alteração.
    print("\n[INFO] Bem encontrado:")
    mostrar_bem(bem)

    # O utilizador escolhe o novo estado.
    novo_estado = mostrar_opcoes(ESTADOS, "Escolha o novo estado do bem")

    # Atualizamos o campo estado.
    bem["estado"] = novo_estado

    print("\n[OK] Estado atualizado com sucesso!")
    mostrar_bem(bem)


def alterar_localizacao_bem():
    """
    Altera a localização de um bem já existente.

    Lógica:
    -------
    1. O utilizador introduz o ID do bem
    2. O sistema procura esse bem no inventário
    3. Se encontrar, mostra os dados atuais
    4. O utilizador escolhe a nova localização
    5. A localização do bem é atualizada

    Nota:
    -----
    Esta função altera apenas os dados em memória.
    A gravação no ficheiro será feita no main.py com guardar_dados().
    """

    print("\n=== ALTERAR LOCALIZAÇÃO DE UM BEM ===")

    # Se o inventário estiver vazio, não há bens para alterar.
    if not inventario:
        print("[INFO] O inventário está vazio.")
        return

    # Pedimos o ID do bem.
    id_bem = input("Introduza o ID do bem: ").strip().upper()

    # Procuramos o bem usando a função auxiliar interna.
    bem = _encontrar_bem_por_id(id_bem)

    # Se não encontrar, avisamos o utilizador.
    if bem is None:
        print("[AVISO] Bem não encontrado.")
        return

    # Mostramos o bem encontrado antes da alteração.
    print("\n[INFO] Bem encontrado:")
    mostrar_bem(bem)

    # O utilizador escolhe a nova localização.
    nova_localizacao = mostrar_opcoes(LOCALIZACOES, "Escolha a nova localização do bem")

    # Atualizamos o campo localização.
    bem["localizacao"] = nova_localizacao

    print("\n[OK] Localização atualizada com sucesso!")
    mostrar_bem(bem)            



def remover_bem():
    """
    Remove um bem existente do inventário.

    Esta função foi criada depois das funções de registo, pesquisa,
    listagem e alteração, porque só faz sentido remover um bem
    depois de ele já existir no sistema.

    Lógica:
    -------
    1. Verifica se existem bens no inventário
    2. Pede ao utilizador o ID do bem
    3. Procura esse bem no inventário
    4. Se encontrar, mostra os dados do bem
    5. Pede confirmação antes de remover
    6. Remove o bem da lista em memória

    Nota:
    -----
    Esta função altera apenas os dados em memória.
    A gravação no ficheiro inventario.txt será feita no main.py
    com a função guardar_dados().
    """

    print("\n=== REMOVER BEM ===")

    # Se o inventário estiver vazio, não há bens para remover.
    if not inventario:
        print("[INFO] O inventário está vazio.")
        return

    # Pedimos o ID do bem que o utilizador pretende remover.
    id_bem = input("Introduza o ID do bem a remover: ").strip().upper()

    # Procuramos o bem através da função auxiliar interna.
    bem = _encontrar_bem_por_id(id_bem)

    # Se o bem não existir, avisamos o utilizador.
    if bem is None:
        print("[AVISO] Bem não encontrado.")
        return

    # Mostramos o bem antes de remover.
    # Isto ajuda o utilizador a confirmar que é mesmo este bem.
    print("\n[INFO] Bem encontrado:")
    mostrar_bem(bem)

    # Pedimos confirmação antes de apagar.
    confirmacao = input("Tem a certeza que pretende remover este bem? (S/N): ").strip().upper()

    # Só removemos se o utilizador confirmar com S.
    if confirmacao == "S":
        inventario.remove(bem)
        print("[OK] Bem removido com sucesso.")
    else:
        print("[INFO] Remoção cancelada.")