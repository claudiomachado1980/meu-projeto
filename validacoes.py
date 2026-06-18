# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR
# Ficheiro: validacoes.py
# -----------------------------------------------------------------------------
# Este ficheiro contém funções de validação usadas pelo sistema.
#
# Porque criámos este ficheiro?
# -----------------------------
# Para separar as regras de validação da lógica principal.
#
# Exemplo:
# - o importacao.py trata de importar ficheiros
# - o gestao.py trata da gestão dos bens
# - o validacoes.py trata de verificar se os dados estão corretos
#
# Assim, se a regra do ID mudar no futuro, alteramos apenas aqui.
# =============================================================================


# =============================================================================
# 1) FUNÇÃO validar_formato_id(...)
# -----------------------------------------------------------------------------
# Esta função valida se um ID segue o formato definido no projeto:
#
# 3 letras + 4 números
#
# Exemplos válidos:
# COM0001
# MSA0001
# PRJ0001
#
# Exemplos inválidos:
# PCF001
# CADF001
# 123ABC1
# COM01
# =============================================================================
def validar_formato_id(id_bem):
    """
    Verifica se o ID tem o formato correto:
    3 letras + 4 números.

    Parâmetros:
        id_bem (str):
            ID do bem a validar.

    Devolve:
        bool:
            True se o ID estiver correto.
            False se o ID estiver incorreto.
    """

    id_bem = id_bem.strip().upper()

    # O ID tem de ter exatamente 7 caracteres.
    if len(id_bem) != 7:
        return False

    # As primeiras 3 posições devem ser letras.
    letras = id_bem[:3]

    for letra in letras:
        if not ("A" <= letra <= "Z"):
            return False

    # As últimas 4 posições devem ser números.
    numeros = id_bem[3:]

    if not numeros.isdigit():
        return False

    return True