# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR
# Ficheiro: importacao.py
# -----------------------------------------------------------------------------
# Este ficheiro trata da importação de bens a partir de ficheiros externos.
#
# Foi criado para permitir que o sistema carregue dados vindos de fora,
# por exemplo de uma pen USB, de outro computador ou de uma exportação.
#
# Nesta versão existem duas formas de importação:
#
# 1) Importação simples
#    O ficheiro tem de seguir exatamente a estrutura:
#    id;nome;categoria;estado;localizacao
#
# 2) Importação flexível
#    O ficheiro pode ter outros nomes de colunas.
#    O sistema mostra as colunas encontradas e pede ao utilizador para indicar
#    quais correspondem aos campos principais do inventário.
#
# Esta solução mantém a estrutura base do projeto:
# - cada bem continua a ter ID, nome, categoria, estado e localização
# - os dados continuam a ser guardados no inventario.txt
# - o sistema continua simples, baseado em listas, dicionários e ficheiros
#
# Objetivo pedagógico desta versão:
# ---------------------------------
# Esta versão mostra como o programa pode adaptar dados externos
# à estrutura interna do sistema.
#
# O ficheiro externo pode vir com colunas diferentes, mas o sistema
# obriga o utilizador a indicar quais colunas correspondem aos campos
# necessários para criar um bem válido.
#
# Assim, mesmo que o ficheiro venha de outro contexto, o sistema consegue
# transformar esses dados para a estrutura usada no inventário:
# id, nome, categoria, estado e localizacao.
# =============================================================================


# =============================================================================
# 1) IMPORTAÇÃO DE FUNÇÕES E DADOS DO FICHEIRO produtos.py
# -----------------------------------------------------------------------------
# Aqui reutilizamos funções e listas que já existem no projeto.
#
# linha_para_bem:
#   usada na importação simples para converter uma linha em bem.
#
# criar_bem:
#   usada na importação flexível para criar bens no formato interno do sistema.
#
# ESTADOS:
#   lista de estados possíveis, usada quando for necessário escolher
#   um estado padrão.
#
# TIPOS_BENS:
#   dicionário com tipos de bens conhecidos, usado para tentar descobrir
#   categoria e radical automaticamente.
#
# mostrar_opcoes:
#   função já existente para mostrar opções numeradas ao utilizador.
# =============================================================================
from produtos import (
    linha_para_bem,
    criar_bem,
    ESTADOS,
    TIPOS_BENS,
    mostrar_opcoes
)

from validacoes import validar_formato_id

# =============================================================================
# 2) FUNÇÃO _id_ja_existe(...)
# -----------------------------------------------------------------------------
# Esta função verifica se já existe um bem com determinado ID.
#
# O objetivo é evitar importar bens duplicados.
# =============================================================================
def _id_ja_existe(lista_bens, id_bem):
    """
    Verifica se já existe um bem com o ID indicado.

    Parâmetros:
        lista_bens (list):
            Lista atual de bens do inventário.

        id_bem (str):
            ID que queremos verificar.

    Devolve:
        bool:
            True se o ID já existir.
            False se o ID ainda não existir.
    """

    for bem in lista_bens:
        if bem["id"] == id_bem:
            return True

    return False


# =============================================================================
# 3) FUNÇÃO _linha_e_cabecalho(...)
# -----------------------------------------------------------------------------
# Alguns ficheiros podem ter uma primeira linha com os nomes das colunas.
#
# Exemplo:
# id;nome;categoria;estado;localizacao
#
# Esta função serve para detetar essa linha e ignorá-la durante a importação
# simples.
# =============================================================================
def _linha_e_cabecalho(linha):
    """
    Verifica se a linha parece ser um cabeçalho.

    Parâmetros:
        linha (str):
            Linha lida do ficheiro.

    Devolve:
        bool:
            True se parecer cabeçalho.
            False se não parecer cabeçalho.
    """

    linha = linha.strip().lower()

    # Aceitamos "localização" com acento e também "localizacao" sem acento.
    linha = linha.replace("localização", "localizacao")

    if linha == "id;nome;categoria;estado;localizacao":
        return True

    return False


# =============================================================================
# 4) FUNÇÃO importar_bens_de_ficheiro(...)
# -----------------------------------------------------------------------------
# Esta é a importação simples.
#
# Nesta opção, o ficheiro externo tem de seguir a mesma estrutura interna
# do sistema:
#
# id;nome;categoria;estado;localizacao
#
# Exemplo:
# COM0001;Computador;Equipamento Informático;Bom;Sala 1
#
# Esta função foi mantida porque é útil quando o ficheiro já vem preparado
# no formato correto.
# =============================================================================
def importar_bens_de_ficheiro(lista_bens):
    """
    Importa bens a partir de um ficheiro externo com estrutura fixa.

    Parâmetros:
        lista_bens (list):
            Lista atual de bens do inventário.

    Nota:
    -----
    A função altera a lista recebida, adicionando os bens importados.
    Depois, no main.py, deve ser chamada a função guardar_dados().
    """

    print("\n=== IMPORTAR BENS DE FICHEIRO EXTERNO ===")

    print("\nEsta é a importação simples.")
    print("O ficheiro deve ter a seguinte estrutura:")
    print("id;nome;categoria;estado;localizacao")

    print("\nExemplo:")
    print("COM0001;Computador;Equipamento Informático;Bom;Sala 1")

    caminho = input("\nIntroduza o caminho do ficheiro a importar: ").strip()

    # Removemos aspas, caso o utilizador copie o caminho com aspas.
    caminho = caminho.replace('"', "")

    if caminho == "":
        print("[INFO] Importação cancelada.")
        return

    total_linhas = 0
    bens_importados = 0
    bens_duplicados = 0
    linhas_invalidas = 0

    try:
        with open(caminho, "r", encoding="utf-8") as ficheiro:

            for linha in ficheiro:
                total_linhas += 1

                # Ignorar linhas vazias.
                if linha.strip() == "":
                    continue

                # Ignorar cabeçalho, se existir.
                if _linha_e_cabecalho(linha):
                    continue

                # Converter a linha num bem.
                bem = linha_para_bem(linha)

                # Se a linha estiver inválida, ignoramos.
                if bem is None:
                    linhas_invalidas += 1
                    print(f"[AVISO] Linha {total_linhas} inválida. Foi ignorada.")
                    continue

                # Verificar se o ID tem o formato correto.
                # Se não tiver, geramos automaticamente um novo ID válido.
                if not validar_formato_id(bem["id"]):
                    id_antigo = bem["id"]
                    novo_id = _gerar_id_automatico(lista_bens, bem["nome"])

                    print(f"[AVISO] O ID '{id_antigo}' não respeita o formato 3 letras + 4 números.")
                    print(f"[INFO] Foi gerado automaticamente o novo ID: {novo_id}")

                    bem["id"] = novo_id

                # Verificar se o ID já existe.
                if _id_ja_existe(lista_bens, bem["id"]):
                    bens_duplicados += 1
                    print(f"[AVISO] O bem {bem['id']} já existe. Foi ignorado.")
                    continue

                # Adicionar o bem ao inventário.
                lista_bens.append(bem)
                bens_importados += 1

        print("\n=== RESUMO DA IMPORTAÇÃO ===")
        print(f"Linhas lidas: {total_linhas}")
        print(f"Bens importados: {bens_importados}")
        print(f"Bens duplicados ignorados: {bens_duplicados}")
        print(f"Linhas inválidas ignoradas: {linhas_invalidas}")

        if bens_importados > 0:
            print("\n[OK] Importação concluída com sucesso.")
            print("[INFO] Os bens importados foram adicionados ao inventário.")
        else:
            print("\n[INFO] Nenhum novo bem foi importado.")

    except FileNotFoundError:
        print("[ERRO] Ficheiro não encontrado.")
        print("[INFO] Verifique se o caminho está correto.")

    except UnicodeDecodeError:
        print("[ERRO] Não foi possível ler o ficheiro com codificação UTF-8.")
        print("[INFO] Abra o ficheiro no Bloco de Notas e grave como UTF-8.")

    except Exception as erro:
        print("[ERRO] Ocorreu um erro durante a importação.")
        print(f"[INFO] Detalhe do erro: {erro}")


# =============================================================================
# 6) FUNÇÃO _separar_linha(...)
# -----------------------------------------------------------------------------
# Esta função recebe uma linha de texto e separa os campos.
#
# Nesta fase vamos aceitar ficheiros separados por:
# - ponto e vírgula ;
# - vírgula ,
#
# Exemplo com ;
# codigo;descricao;sala;situacao
#
# Exemplo com ,
# codigo,descricao,sala,situacao
# =============================================================================
def _separar_linha(linha, separador):
    """
    Separa uma linha de texto em várias partes.

    Parâmetros:
        linha (str):
            Linha lida do ficheiro.

        separador (str):
            Separador usado no ficheiro.
            Pode ser ";" ou ",".

    Devolve:
        list:
            Lista com os valores separados.
    """

    linha = linha.strip()
    partes = linha.split(separador)

    partes_limpas = []

    for parte in partes:
        partes_limpas.append(parte.strip())

    return partes_limpas


# =============================================================================
# 7) FUNÇÃO _detetar_separador(...)
# -----------------------------------------------------------------------------
# Esta função tenta perceber se o ficheiro usa ; ou , como separador.
# =============================================================================
def _detetar_separador(linha_cabecalho):
    """
    Tenta detetar o separador usado no ficheiro.

    Parâmetros:
        linha_cabecalho (str):
            Primeira linha útil do ficheiro.

    Devolve:
        str:
            ";" se encontrar ponto e vírgula.
            "," se encontrar vírgula.
            None se não conseguir detetar.
    """

    if ";" in linha_cabecalho:
        return ";"

    if "," in linha_cabecalho:
        return ","

    return None


# =============================================================================
# 8) FUNÇÃO _mostrar_colunas(...)
# -----------------------------------------------------------------------------
# Mostra as colunas encontradas no ficheiro externo.
# =============================================================================
def _mostrar_colunas(colunas):
    """
    Mostra as colunas encontradas no ficheiro externo.

    Parâmetros:
        colunas (list):
            Lista com os nomes das colunas.
    """

    print("\nColunas encontradas no ficheiro:")

    for i, coluna in enumerate(colunas, start=1):
        print(f"{i}. {coluna}")


# =============================================================================
# 9) FUNÇÃO _mostrar_ajuda_importacao_flexivel(...)
# -----------------------------------------------------------------------------
# Esta função mostra uma explicação inicial ao utilizador antes da importação.
#
# O objetivo é evitar que o utilizador se perca durante o processo.
# Como a importação flexível pode receber ficheiros com colunas diferentes,
# é importante explicar o que o sistema vai pedir.
# =============================================================================
def _mostrar_ajuda_importacao_flexivel():
    """
    Mostra uma explicação inicial sobre a importação flexível.
    """

    print("\n" + "=" * 60)
    print("AJUDA - IMPORTAÇÃO FLEXÍVEL")
    print("=" * 60)

    print("\nEsta opção serve para importar bens a partir de um ficheiro externo.")
    print("O ficheiro pode ter nomes de colunas diferentes dos usados no sistema.")

    print("\nExemplo de ficheiro externo:")
    print("codigo;descricao;sala;situacao")
    print("PC001;Computador HP;Sala TIC;Bom")

    print("\nO sistema vai mostrar as colunas encontradas e pedir que associe")
    print("essas colunas aos campos principais do inventário.")

    print("\nCampos usados internamente pelo sistema:")
    print("- ID")
    print("- Nome")
    print("- Categoria")
    print("- Estado")
    print("- Localização")

    print("\nRegras importantes:")
    print("- O NOME é obrigatório, porque sem nome não sabemos que bem é.")
    print("- O ID pode ser gerado automaticamente, se não existir no ficheiro.")
    print("- A categoria pode ser descoberta pelo nome ou ficar como 'Outro'.")
    print("- O estado pode ser escolhido como valor padrão para todos.")
    print("- A localização pode ser indicada como valor padrão para todos.")

    print("\nAs colunas que não forem necessárias serão ignoradas nesta versão.")
    print("Depois da importação, poderá alterar o estado ou a localização")
    print("dos bens através das opções normais do menu.")

    print("\nMais tarde, o sistema poderá evoluir para permitir alterar também")
    print("outros dados dos bens, dentro das opções disponíveis no projeto.")

    print("=" * 60)


# =============================================================================
# 10) FUNÇÃO _explicar_campo(...)
# -----------------------------------------------------------------------------
# Esta função explica ao utilizador para que serve cada campo do sistema.
#
# É usada durante o mapeamento das colunas, para o utilizador perceber
# melhor o que deve escolher.
# =============================================================================
def _explicar_campo(nome_campo):
    """
    Explica ao utilizador o significado de um campo do sistema.

    Parâmetros:
        nome_campo (str):
            Nome do campo que queremos explicar.
    """

    if nome_campo == "nome":
        print("Este campo identifica o bem.")
        print("Exemplo: Computador HP, Mesa Aluno, Projetor Epson.")
        print("Este campo é obrigatório.")

    elif nome_campo == "id":
        print("Este campo identifica o código único do bem.")
        print("Exemplo: COM0001, MSA0001, PRJ0001.")
        print("Se o ficheiro não tiver ID, o sistema pode gerar automaticamente.")

    elif nome_campo == "categoria":
        print("Este campo indica o tipo geral do bem.")
        print("Exemplo: Mobiliário, Equipamento Informático, Material Didático.")
        print("Se não existir, o sistema tenta descobrir pelo nome ou usa 'Outro'.")

    elif nome_campo == "estado":
        print("Este campo indica a condição atual do bem.")
        print("Exemplo: Novo, Bom, Danificado, Em Reparação.")
        print("Se não existir, será escolhido um estado padrão.")

    elif nome_campo == "localizacao":
        print("Este campo indica onde o bem está localizado.")
        print("Exemplo: Sala 1, Biblioteca, Laboratório, Armazém.")
        print("Se não existir, será pedida uma localização padrão.")


# =============================================================================
# 11) FUNÇÃO _escolher_coluna(...)
# -----------------------------------------------------------------------------
# Esta função pergunta ao utilizador qual coluna corresponde a um campo
# do sistema.
#
# Exemplo:
# O campo interno "nome" pode estar no ficheiro como:
# - nome
# - descricao
# - designacao
# - artigo
#
# Por isso, perguntamos ao utilizador.
# =============================================================================
def _escolher_coluna(colunas, nome_campo, obrigatorio):
    """
    Permite ao utilizador escolher uma coluna do ficheiro.

    Parâmetros:
        colunas (list):
            Lista com os nomes das colunas do ficheiro.

        nome_campo (str):
            Nome do campo interno do sistema.
            Exemplo: "nome", "estado", "localizacao"

        obrigatorio (bool):
            True se o campo for obrigatório.
            False se o campo puder ficar sem coluna.

    Devolve:
        int:
            Índice da coluna escolhida.

        None:
            Se o campo não tiver coluna associada.
    """

    while True:
        print("\n" + "-" * 50)
        print(f"Campo do sistema: {nome_campo}")
        print("-" * 50)

        # Explicamos ao utilizador o significado do campo.
        _explicar_campo(nome_campo)

        # Mostramos as colunas disponíveis no ficheiro.
        _mostrar_colunas(colunas)

        if obrigatorio:
            print("\nEste campo é obrigatório.")
            escolha = input(f"Escolha a coluna correspondente a '{nome_campo}': ").strip()
        else:
            print("\nSe o ficheiro não tiver esta coluna, escreva 0.")
            escolha = input(f"Escolha a coluna correspondente a '{nome_campo}': ").strip()

        if not obrigatorio and escolha == "0":
            return None

        if escolha.isdigit():
            indice = int(escolha) - 1

            if 0 <= indice < len(colunas):
                return indice

        print("[AVISO] Escolha inválida. Tente novamente.")


# =============================================================================
# 12) FUNÇÃO _descobrir_categoria_pelo_nome(...)
# -----------------------------------------------------------------------------
# Esta função tenta descobrir a categoria através do nome do bem.
#
# Exemplo:
# Se o nome for "Computador HP", o sistema percebe que contém "Computador"
# e pode usar a categoria de Computador.
#
# Se não conseguir descobrir, devolve "Outro".
# =============================================================================
def _descobrir_categoria_pelo_nome(nome_bem):
    """
    Tenta descobrir a categoria com base no nome do bem.

    Parâmetros:
        nome_bem (str):
            Nome do bem.

    Devolve:
        str:
            Categoria encontrada.
            Se não conseguir descobrir, devolve "Outro".
    """

    nome_minusculas = nome_bem.lower()

    for tipo_bem in TIPOS_BENS:
        tipo_minusculas = tipo_bem.lower()

        # Primeiro tentamos encontrar o nome completo do tipo de bem.
        if tipo_minusculas in nome_minusculas:
            return TIPOS_BENS[tipo_bem]["categoria"]

        # Depois tentamos encontrar apenas a primeira palavra.
        # Exemplo:
        # "Cadeira Azul" pode ser associada a "Cadeira Aluno".
        primeira_palavra = tipo_minusculas.split()[0]

        if primeira_palavra in nome_minusculas:
            return TIPOS_BENS[tipo_bem]["categoria"]

    return "Outro"


# =============================================================================
# 13) FUNÇÃO _obter_radical_pelo_nome(...)
# -----------------------------------------------------------------------------
# Esta função tenta obter um radical de 3 letras para gerar o ID.
#
# Primeiro tenta usar os tipos de bens conhecidos.
# Se não encontrar, usa as primeiras 3 letras do nome.
# =============================================================================
def _obter_radical_pelo_nome(nome_bem):
    """
    Obtém um radical de 3 letras para gerar o ID.

    Parâmetros:
        nome_bem (str):
            Nome do bem.

    Devolve:
        str:
            Radical com 3 letras.
    """

    nome_minusculas = nome_bem.lower()

    # Primeiro tentamos encontrar um tipo de bem conhecido.
    for tipo_bem in TIPOS_BENS:
        tipo_minusculas = tipo_bem.lower()

        if tipo_minusculas in nome_minusculas:
            return TIPOS_BENS[tipo_bem]["radical"]

        primeira_palavra = tipo_minusculas.split()[0]

        if primeira_palavra in nome_minusculas:
            return TIPOS_BENS[tipo_bem]["radical"]

    # Se não encontrarmos, usamos as primeiras 3 letras do nome.
    letras = ""

    for caractere in nome_bem.upper():
        if caractere.isalpha():
            letras += caractere

    if len(letras) >= 3:
        return letras[:3]

    # Se o nome for demasiado curto ou estranho, usamos um radical genérico.
    return "BEM"


# =============================================================================
# 14) FUNÇÃO _gerar_id_automatico(...)
# -----------------------------------------------------------------------------
# Esta função gera um novo ID usando:
# - radical de 3 letras
# - número com 4 dígitos
#
# Exemplo:
# COM0001
# COM0002
# MSA0001
# =============================================================================
def _gerar_id_automatico(lista_bens, nome_bem):
    """
    Gera automaticamente um ID para um bem importado.

    Parâmetros:
        lista_bens (list):
            Lista atual de bens do inventário.

        nome_bem (str):
            Nome do bem.

    Devolve:
        str:
            Novo ID gerado automaticamente.
    """

    radical = _obter_radical_pelo_nome(nome_bem)

    numeros_existentes = []

    for bem in lista_bens:
        id_atual = bem["id"]

        if id_atual.startswith(radical) and validar_formato_id(id_atual):
            parte_numerica = id_atual[len(radical):]


            if parte_numerica.isdigit():
                numeros_existentes.append(int(parte_numerica))

    if not numeros_existentes:
        return f"{radical}0001"

    proximo_numero = max(numeros_existentes) + 1

    return f"{radical}{str(proximo_numero).zfill(4)}"


# =============================================================================
# 15) FUNÇÃO importar_bens_flexivel(...)
# -----------------------------------------------------------------------------
# Esta função é a importação flexível da V3.
#
# Diferença para a importação simples:
# ------------------------------------
# Na importação simples, o ficheiro tinha de vir exatamente assim:
# id;nome;categoria;estado;localizacao
#
# Na importação flexível, o ficheiro pode ter outros nomes de colunas:
# codigo;descricao;sala;situacao
#
# O utilizador é que vai indicar ao sistema:
# - qual coluna é o nome
# - qual coluna é o ID, se existir
# - qual coluna é a categoria, se existir
# - qual coluna é o estado, se existir
# - qual coluna é a localização, se existir
#
# Se faltar alguma coluna, o sistema tenta resolver:
# - ID: gera automaticamente
# - categoria: tenta descobrir pelo nome ou usa "Outro"
# - estado: pede um estado padrão
# - localização: pede uma localização padrão
#
# As colunas extra são ignoradas nesta versão, porque o sistema atual ainda
# trabalha apenas com os 5 campos principais.
# =============================================================================
def importar_bens_flexivel(lista_bens):
    """
    Importa bens de forma flexível a partir de um ficheiro externo.

    Parâmetros:
        lista_bens (list):
            Lista atual de bens do inventário.

    Nota:
    -----
    Esta função altera a lista recebida, adicionando os bens importados.
    Depois, no main.py, deve ser chamada a função guardar_dados().
    """

    print("\n=== IMPORTAÇÃO FLEXÍVEL DE BENS ===")

    # Mostramos uma explicação inicial para orientar o utilizador.
    _mostrar_ajuda_importacao_flexivel()

    caminho = input("\nIntroduza o caminho do ficheiro a importar: ").strip()

    # Removemos aspas, caso o utilizador copie o caminho com aspas.
    caminho = caminho.replace('"', "")

    if caminho == "":
        print("[INFO] Importação cancelada.")
        return

    try:
        with open(caminho, "r", encoding="utf-8") as ficheiro:
            linhas = ficheiro.readlines()

        # Procurar a primeira linha não vazia.
        linha_cabecalho = ""

        for linha in linhas:
            if linha.strip() != "":
                linha_cabecalho = linha
                break

        if linha_cabecalho == "":
            print("[ERRO] O ficheiro está vazio.")
            return

        # Detetar se o ficheiro usa ; ou ,
        separador = _detetar_separador(linha_cabecalho)

        if separador is None:
            print("[ERRO] Não foi possível detetar o separador do ficheiro.")
            print("[INFO] Use ficheiros separados por ';' ou ','.")
            return

        # Obter os nomes das colunas.
        colunas = _separar_linha(linha_cabecalho, separador)

        print("\n[OK] Cabeçalho detetado com sucesso.")
        _mostrar_colunas(colunas)

        # ---------------------------------------------------------------------
        # MAPEAR COLUNAS
        # ---------------------------------------------------------------------
        print("\nAgora vamos associar as colunas do ficheiro aos campos do sistema.")
        print("Leia cada explicação e escolha o número da coluna correspondente.")

        # O nome é obrigatório, porque sem nome não sabemos que bem é.
        indice_nome = _escolher_coluna(colunas, "nome", True)

        # O ID pode não existir, porque conseguimos gerar automaticamente.
        indice_id = _escolher_coluna(colunas, "id", False)

        # A categoria pode não existir, porque conseguimos tentar descobrir.
        indice_categoria = _escolher_coluna(colunas, "categoria", False)

        # O estado pode não existir, mas nesse caso pedimos um estado padrão.
        indice_estado = _escolher_coluna(colunas, "estado", False)

        # A localização pode não existir, mas nesse caso pedimos uma localização padrão.
        indice_localizacao = _escolher_coluna(colunas, "localizacao", False)

        # ---------------------------------------------------------------------
        # VALORES PADRÃO PARA CAMPOS EM FALTA
        # ---------------------------------------------------------------------
        estado_padrao = ""

        if indice_estado is None:
            print("\nO ficheiro não tem coluna de estado.")
            print("Escolha o estado que será aplicado aos bens importados.")
            estado_padrao = mostrar_opcoes(ESTADOS, "Estado padrão")

        localizacao_padrao = ""

        if indice_localizacao is None:
            print("\nO ficheiro não tem coluna de localização.")
            print("Indique a localização que será aplicada aos bens importados.")
            print("Exemplo: Sala 1, Armazém, Biblioteca, Laboratório.")
            localizacao_padrao = input("Localização padrão: ").strip()

            if localizacao_padrao == "":
                localizacao_padrao = "Sem localização"

        # ---------------------------------------------------------------------
        # CONFIRMAR MAPEAMENTO
        # ---------------------------------------------------------------------
        print("\n=== MAPEAMENTO DEFINIDO ===")

        print(f"Nome        -> {colunas[indice_nome]}")

        if indice_id is None:
            print("ID          -> Gerado automaticamente no formato 3 letras + 4 números")
        else:
            print(f"ID          -> {colunas[indice_id]}")
            print("              Nota: se algum ID estiver fora do formato correto,")
            print("              será gerado automaticamente um novo ID válido.")

        if indice_categoria is None:
            print("Categoria   -> Descoberta pelo nome ou 'Outro'")
        else:
            print(f"Categoria   -> {colunas[indice_categoria]}")

        if indice_estado is None:
            print(f"Estado      -> Valor padrão: {estado_padrao}")
        else:
            print(f"Estado      -> {colunas[indice_estado]}")

        if indice_localizacao is None:
            print(f"Localização -> Valor padrão: {localizacao_padrao}")
        else:
            print(f"Localização -> {colunas[indice_localizacao]}")

        print("\nAs restantes colunas do ficheiro serão ignoradas nesta versão.")
        print("Depois da importação, poderá consultar os bens no inventário")
        print("e alterar estado ou localização através do menu principal.")

        confirmacao = input("\nConfirma este mapeamento? (S/N): ").strip().upper()

        if confirmacao != "S":
            print("[INFO] Importação cancelada pelo utilizador.")
            return

        # ---------------------------------------------------------------------
        # IMPORTAR LINHAS
        # ---------------------------------------------------------------------
        total_linhas = 0
        bens_importados = 0
        bens_duplicados = 0
        linhas_invalidas = 0

        # Variável para sabermos se já passámos o cabeçalho.
        cabecalho_ja_passou = False

        for linha in linhas:

            # Ignorar linhas vazias.
            if linha.strip() == "":
                continue

            # Ignorar a primeira linha útil, que é o cabeçalho.
            if not cabecalho_ja_passou:
                cabecalho_ja_passou = True
                continue

            total_linhas += 1

            valores = _separar_linha(linha, separador)

            # Se a linha tiver menos colunas do que o cabeçalho,
            # consideramos que está incompleta.
            if len(valores) < len(colunas):
                linhas_invalidas += 1
                print(f"[AVISO] Linha de dados {total_linhas} incompleta. Foi ignorada.")
                continue

            # -----------------------------------------------------------------
            # Obter nome
            # -----------------------------------------------------------------
            nome = valores[indice_nome].strip()

            if nome == "":
                linhas_invalidas += 1
                print(f"[AVISO] Linha de dados {total_linhas} sem nome. Foi ignorada.")
                continue

            # -----------------------------------------------------------------
            # Obter ou gerar ID
            # -----------------------------------------------------------------
            if indice_id is None:
                # Se o ficheiro não tiver coluna de ID,
                # o sistema gera automaticamente um ID válido.
                id_bem = _gerar_id_automatico(lista_bens, nome)

            else:
                # Se o ficheiro tiver coluna de ID,
                # vamos buscar esse valor.
                id_bem = valores[indice_id].strip().upper()

                # Se o ID vier vazio, geramos automaticamente.
                if id_bem == "":
                    id_bem = _gerar_id_automatico(lista_bens, nome)

                # Se o ID vier preenchido, mas fora do formato correto,
                # também geramos automaticamente um novo ID válido.
                elif not validar_formato_id(id_bem):
                    id_antigo = id_bem
                    id_bem = _gerar_id_automatico(lista_bens, nome)

                    print(f"[AVISO] O ID '{id_antigo}' não respeita o formato 3 letras + 4 números.")
                    print(f"[INFO] Para o bem '{nome}', foi gerado o novo ID: {id_bem}")

            # Verificar se o ID já existe.
            if _id_ja_existe(lista_bens, id_bem):
                bens_duplicados += 1
                print(f"[AVISO] O bem {id_bem} já existe. Foi ignorado.")
                continue

            # -----------------------------------------------------------------
            # Obter categoria
            # -----------------------------------------------------------------
            if indice_categoria is None:
                categoria = _descobrir_categoria_pelo_nome(nome)
            else:
                categoria = valores[indice_categoria].strip()

                if categoria == "":
                    categoria = _descobrir_categoria_pelo_nome(nome)

            # -----------------------------------------------------------------
            # Obter estado
            # -----------------------------------------------------------------
            if indice_estado is None:
                estado = estado_padrao
            else:
                estado = valores[indice_estado].strip()

                if estado == "":
                    estado = estado_padrao

            # -----------------------------------------------------------------
            # Obter localização
            # -----------------------------------------------------------------
            if indice_localizacao is None:
                localizacao = localizacao_padrao
            else:
                localizacao = valores[indice_localizacao].strip()

                if localizacao == "":
                    localizacao = localizacao_padrao

            # Criar o bem com a estrutura interna do sistema.
            novo_bem = criar_bem(
                id_bem=id_bem,
                nome=nome,
                categoria=categoria,
                estado=estado,
                localizacao=localizacao
            )

            # Adicionar à lista do inventário.
            lista_bens.append(novo_bem)
            bens_importados += 1

        # ---------------------------------------------------------------------
        # RESUMO FINAL
        # ---------------------------------------------------------------------
        print("\n=== RESUMO DA IMPORTAÇÃO FLEXÍVEL ===")
        print(f"Linhas de dados lidas: {total_linhas}")
        print(f"Bens importados: {bens_importados}")
        print(f"Bens duplicados ignorados: {bens_duplicados}")
        print(f"Linhas inválidas ignoradas: {linhas_invalidas}")

        if bens_importados > 0:
            print("\n[OK] Importação flexível concluída com sucesso.")
            print("[INFO] Os bens importados foram adicionados ao inventário.")
            print("[INFO] Pode agora consultar os bens na opção de listagem.")
            print("[INFO] Se necessário, pode alterar depois o estado ou a localização")
            print("       através das opções normais do menu.")
        else:
            print("\n[INFO] Nenhum novo bem foi importado.")

    except FileNotFoundError:
        print("[ERRO] Ficheiro não encontrado.")
        print("[INFO] Verifique se o caminho está correto.")

    except UnicodeDecodeError:
        print("[ERRO] Não foi possível ler o ficheiro com codificação UTF-8.")
        print("[INFO] Abra o ficheiro no Bloco de Notas e grave como UTF-8.")

    except Exception as erro:
        print("[ERRO] Ocorreu um erro durante a importação flexível.")
        print(f"[INFO] Detalhe do erro: {erro}")