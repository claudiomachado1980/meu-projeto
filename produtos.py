# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR
# Ficheiro: produtos.py
# -----------------------------------------------------------------------------
# Este ficheiro é o ponto de partida do projeto.
#
# Porque é que começámos por aqui?
# --------------------------------
# Antes de criar menus, relatórios ou movimentações, precisamos primeiro de
# definir o que é um "bem" dentro do sistema.
#
# Neste ficheiro vamos guardar:
# - as categorias iniciais
# - os estados iniciais
# - as localizações iniciais
# - os tipos de bens iniciais
# - os radicais dos IDs
# - as funções base para:
#     * criar um bem
#     * transformar um bem numa linha de ficheiro
#     * transformar uma linha de ficheiro num bem
#     * mostrar um bem no ecrã
#     * mostrar listas de opções ao utilizador
#
# Este ficheiro serve, portanto, como base estrutural do projeto.
# =============================================================================


# =============================================================================
# 1) CATEGORIAS INICIAIS DA VERSÃO 1
# -----------------------------------------------------------------------------
# Estas categorias foram definidas para a V1 do projeto.
# Mais tarde, numa versão futura, podem vir a ser editáveis ou expandíveis.
# =============================================================================
CATEGORIAS = [
    "Mobiliário",
    "Equipamento Informático",
    "Equipamento Laboratorial",
    "Material Didático",
    "Material Administrativo",
    "Outro"
]


# =============================================================================
# 2) ESTADOS INICIAIS DA VERSÃO 1
# -----------------------------------------------------------------------------
# O estado representa a condição atual de cada bem.
# Exemplo:
# - um computador pode estar "Bom"
# - um projetor pode estar "Em Reparação"
# =============================================================================
ESTADOS = [
    "Novo",
    "Bom",
    "Danificado",
    "Em Reparação",
    "Inutilizado"
]


# =============================================================================
# 3) LOCALIZAÇÕES INICIAIS DA VERSÃO 1
# -----------------------------------------------------------------------------
# Como o primeiro contexto do projeto é a escola, as localizações iniciais
# refletem espaços escolares.
#
# Nota:
# No futuro, estas localizações poderão ser editáveis, mas para já ficam
# definidas aqui para simplificar a versão 1.
# =============================================================================
LOCALIZACOES = [
    "Sala 1",
    "Sala 2",
    "Sala 3",
    "Sala 4",
    "Sala 5",
    "Sala 6",
    "Sala 7",
    "Sala 8",
    "Sala 9",
    "Sala 10",
    "Laboratório",
    "Biblioteca",
    "Secretaria",
    "Sala de Professores",
    "Armazém",
    "Direção",
    "Refeitório"
]


# =============================================================================
# 4) TIPOS DE BENS INICIAIS
# -----------------------------------------------------------------------------
# Aqui definimos alguns tipos de bens já conhecidos pelo sistema.
#
# Porque é que isto é útil?
# -------------------------
# Quando o utilizador quiser registar um novo bem, o sistema já sabe:
# - qual é a categoria desse bem
# - qual é o radical a usar no ID
#
# Exemplo:
# "Mesa Aluno" -> categoria "Mobiliário" e radical "MSA"
# "Computador" -> categoria "Equipamento Informático" e radical "COM"
#
# Isto evita que o utilizador tenha de escrever sempre:
# - a categoria manualmente
# - o ID manualmente
#
# Ou seja, o sistema fica mais prático e com menos erros.
# =============================================================================
TIPOS_BENS = {
    "Mesa Aluno": {
        "categoria": "Mobiliário",
        "radical": "MSA"
    },
    "Mesa Professor": {
        "categoria": "Mobiliário",
        "radical": "MSP"
    },
    "Cadeira Aluno": {
        "categoria": "Mobiliário",
        "radical": "CAA"
    },
    "Cadeira Professor": {
        "categoria": "Mobiliário",
        "radical": "CAP"
    },
    "Quadro Branco": {
        "categoria": "Material Didático",
        "radical": "QBR"
    },
    "Computador": {
        "categoria": "Equipamento Informático",
        "radical": "COM"
    },
    "Projetor": {
        "categoria": "Equipamento Informático",
        "radical": "PRJ"
    },
    "Armário": {
        "categoria": "Material Administrativo",
        "radical": "ARM"
    },
    "Livro": {
        "categoria": "Material Didático",
        "radical": "LIV"
    },
    "Microscópio": {
        "categoria": "Equipamento Laboratorial",
        "radical": "MIC"
    },
    "Impressora": {
        "categoria": "Equipamento Informático",
        "radical": "IMP"
    },
    "Outro": {
        "categoria": "Outro",
        "radical": "OUT"
    }
}


# =============================================================================
# 5) FUNÇÃO criar_bem(...)
# -----------------------------------------------------------------------------
# Esta função cria a estrutura base de um bem.
#
# Nesta V1, cada bem tem 5 campos:
# - id
# - nome
# - categoria
# - estado
# - localizacao
#
# Nota importante:
# ----------------
# Nesta versão 1 NÃO vamos usar:
# - quantidade
# - valor / preço
#
# Porque queremos trabalhar cada bem de forma individual.
# Ou seja:
# 1 linha no ficheiro = 1 bem
# =============================================================================
def criar_bem(id_bem, nome, categoria, estado, localizacao):
    """
    Cria e devolve um dicionário com os dados de um bem.

    Parâmetros:
        id_bem (str):
            ID único do bem.
            Exemplo: "MSA0001"

        nome (str):
            Nome do bem.
            Exemplo: "Mesa Aluno"

        categoria (str):
            Categoria do bem.
            Exemplo: "Mobiliário"

        estado (str):
            Estado atual do bem.
            Exemplo: "Bom"

        localizacao (str):
            Localização atual do bem.
            Exemplo: "Sala 1"

    Devolve:
        dict:
            Um dicionário com todos os campos do bem.
    """

    # Criamos e devolvemos um dicionário.
    # Este dicionário vai ser a estrutura base usada em todo o projeto.
    return {
        "id": id_bem.strip().upper(),          # remove espaços e coloca em maiúsculas
        "nome": nome.strip(),                  # remove espaços extra no início/fim
        "categoria": categoria.strip(),        # remove espaços extra
        "estado": estado.strip(),              # remove espaços extra
        "localizacao": localizacao.strip()     # remove espaços extra
    }


# =============================================================================
# 6) FUNÇÃO bem_para_linha(...)
# -----------------------------------------------------------------------------
# Esta função converte um bem (dicionário) numa linha de texto.
#
# Porque é que isto é necessário?
# -------------------------------
# Porque os dados vão ser guardados num ficheiro de texto.
# Então precisamos de transformar o dicionário numa linha simples, com os
# campos separados por ';'
#
# Exemplo de linha:
# MSA0001;Mesa Aluno;Mobiliário;Bom;Sala 1
# =============================================================================
def bem_para_linha(bem):
    """
    Converte um dicionário de bem numa linha de texto.

    Parâmetros:
        bem (dict):
            Dicionário com os dados do bem.

    Devolve:
        str:
            Linha formatada para guardar no ficheiro.
    """

    # Usamos f-strings para juntar todos os campos numa única linha.
    # No final acrescentamos '\n' para garantir mudança de linha no ficheiro.
    return (
        f"{bem['id']};"
        f"{bem['nome']};"
        f"{bem['categoria']};"
        f"{bem['estado']};"
        f"{bem['localizacao']}\n"
    )


# =============================================================================
# 7) FUNÇÃO linha_para_bem(...)
# -----------------------------------------------------------------------------
# Esta função faz o processo inverso da anterior.
#
# Ou seja:
# recebe uma linha do ficheiro e transforma essa linha num dicionário.
#
# Isto é importante quando o sistema arranca e precisa de ler o ficheiro
# inventario.txt para carregar os bens para a memória.
# =============================================================================
def linha_para_bem(linha):
    """
    Recebe uma linha do ficheiro e converte essa linha num dicionário de bem.

    Parâmetros:
        linha (str):
            Linha lida do ficheiro.

    Devolve:
        dict:
            Dicionário do bem, se a linha estiver correta.

        None:
            Se a linha estiver vazia ou com formato inválido.
    """

    # Retira espaços em branco e quebras de linha no início/fim
    linha = linha.strip()

    # Se a linha estiver vazia, não há nada para processar
    if not linha:
        return None

    # Divide a linha pelos ';'
    partes = linha.split(";")

    # Nesta V1 esperamos exatamente 5 campos
    # Se não tiver 5, a linha é considerada inválida
    if len(partes) != 5:
        return None

    # Guardamos cada parte numa variável separada
    id_bem = partes[0].strip()
    nome = partes[1].strip()
    categoria = partes[2].strip()
    estado = partes[3].strip()
    localizacao = partes[4].strip()

    # Validação mínima:
    # se o ID ou o nome vierem vazios, ignoramos a linha
    if not id_bem or not nome:
        return None

    # Se estiver tudo bem, criamos e devolvemos o dicionário do bem
    return criar_bem(id_bem, nome, categoria, estado, localizacao)


# =============================================================================
# 8) FUNÇÃO mostrar_bem(...)
# -----------------------------------------------------------------------------
# Esta função serve para mostrar um bem no ecrã de forma organizada.
#
# Vai ser usada em várias partes do sistema:
# - pesquisa
# - listagem
# - confirmação de registo
# - confirmação de transferência
# =============================================================================
def mostrar_bem(bem):
    """
    Mostra os dados de um bem no ecrã.

    Parâmetros:
        bem (dict):
            Dicionário do bem a apresentar.
    """

    # Linha visual para separar melhor a informação no terminal
    print("-" * 45)

    # Apresentação dos campos do bem
    print(f"ID          : {bem['id']}")
    print(f"Nome        : {bem['nome']}")
    print(f"Categoria   : {bem['categoria']}")
    print(f"Estado      : {bem['estado']}")
    print(f"Localização : {bem['localizacao']}")

    # Linha visual de fecho
    print("-" * 45)


# =============================================================================
# 9) FUNÇÃO mostrar_opcoes(...)
# -----------------------------------------------------------------------------
# Esta função mostra uma lista numerada de opções ao utilizador
# e devolve a opção escolhida.
#
# Exemplo de uso:
# - escolher categoria
# - escolher estado
# - escolher localização
# - escolher tipo de bem
# =============================================================================
def mostrar_opcoes(lista, titulo):
    """
    Mostra uma lista de opções numeradas e devolve o valor escolhido.

    Parâmetros:
        lista (list):
            Lista com as opções disponíveis.

        titulo (str):
            Título da lista apresentado no ecrã.

    Devolve:
        str:
            O valor escolhido pelo utilizador.
    """

    # Mostrar o título da secção
    print(f"\n--- {titulo} ---")

    # Mostrar a lista numerada
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item}")

    # Ciclo para garantir que o utilizador só sai quando escolher uma opção válida
    while True:
        escolha = input(f"Escolha uma opção (1 a {len(lista)}): ").strip()

        # Verifica se o utilizador escreveu um número
        if escolha.isdigit():
            indice = int(escolha) - 1

            # Verifica se esse número corresponde a uma posição válida da lista
            if 0 <= indice < len(lista):
                return lista[indice]

        # Se chegar aqui, a opção era inválida
        print("[AVISO] Opção inválida. Tente novamente.")


# =============================================================================
# 10) FUNÇÃO nomes_tipos_bens(...)
# -----------------------------------------------------------------------------
# Esta função devolve apenas os nomes dos tipos de bens iniciais.
#
# Exemplo de resultado:
# - Mesa Aluno
# - Computador
# - Projetor
#
# Vai ser usada no registo de novos bens.
# =============================================================================
def nomes_tipos_bens():
    """
    Devolve uma lista com os nomes dos tipos de bens disponíveis.

    Devolve:
        list:
            Lista de nomes de bens.
    """

    # O método keys() devolve as chaves do dicionário.
    # Depois convertemos para lista.
    return list(TIPOS_BENS.keys())


# =============================================================================
# 11) FUNÇÃO obter_categoria_do_bem(...)
# -----------------------------------------------------------------------------
# Esta função recebe o nome do bem e devolve automaticamente a categoria.
#
# Exemplo:
# "Mesa Aluno" -> "Mobiliário"
# "Computador" -> "Equipamento Informático"
#
# Isto evita que o utilizador tenha de escolher a categoria manualmente
# sempre que regista um bem conhecido.
# =============================================================================
def obter_categoria_do_bem(nome_bem):
    """
    Devolve a categoria associada ao nome do bem.

    Parâmetros:
        nome_bem (str):
            Nome do bem.

    Devolve:
        str:
            Categoria do bem.
            Se não existir na tabela, devolve "Outro".
    """

    # Verifica se o nome do bem existe no dicionário TIPOS_BENS
    if nome_bem in TIPOS_BENS:
        return TIPOS_BENS[nome_bem]["categoria"]

    # Se não existir, devolve a categoria genérica "Outro"
    return "Outro"


# =============================================================================
# 12) FUNÇÃO obter_radical_do_bem(...)
# -----------------------------------------------------------------------------
# Esta função recebe o nome do bem e devolve automaticamente o radical do ID.
#
# Exemplo:
# "Mesa Aluno" -> "MSA"
# "Projetor"   -> "PRJ"
#
# Isto vai permitir ao gestao.py gerar IDs automáticos como:
# - MSA0001
# - PRJ0001
# =============================================================================
def obter_radical_do_bem(nome_bem):
    """
    Devolve o radical associado ao nome do bem.

    Parâmetros:
        nome_bem (str):
            Nome do bem.

    Devolve:
        str:
            Radical do bem.
            Se não existir na tabela, devolve "OUT".
    """

    # Verifica se o nome do bem existe no dicionário TIPOS_BENS
    if nome_bem in TIPOS_BENS:
        return TIPOS_BENS[nome_bem]["radical"]

    # Se não existir, devolve o radical genérico "OUT"
    return "OUT"