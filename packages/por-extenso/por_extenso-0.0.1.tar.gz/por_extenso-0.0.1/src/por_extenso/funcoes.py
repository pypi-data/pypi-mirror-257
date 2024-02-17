"""Funções para converter números em extenso."""

DICIONARIO_CARDINAIS = {
    0: "zero",
    1: "um",
    2: "dois",
    3: "três",
    4: "quatro",
    5: "cinco",
    6: "seis",
    7: "sete",
    8: "oito",
    9: "nove",
    10: "dez",
    11: "onze",
    12: "doze",
    13: "treze",
    14: "quatorze",
    15: "quinze",
    16: "dezesseis",
    17: "dezessete",
    18: "dezoito",
    19: "dezenove",
    20: "vinte",
    30: "trinta",
    40: "quarenta",
    50: "cinquenta",
    60: "sessenta",
    70: "setenta",
    80: "oitenta",
    90: "noventa",
    100: "cento",
    200: "duzentos",
    300: "trezentos",
    400: "quatrocentos",
    500: "quinhentos",
    600: "seiscentos",
    700: "setecentos",
    800: "oitocentos",
    900: "novecentos",
    1_000: "mil",
    1_000_000: "milhão",
    1_000_000_000: "bilhão",
    1_000_000_000_000: "trilhão",
}

DICIONARIO_MOEDAS = {
    "real": "R$",
    "dólar": "US$",
    "euro": "€",
    "libra": "£",
    "iene": "¥",
    "peso": "ARS$",
}

MOEDAS_PLURAIS = {
    "real": "reais",
    "dólar": "dólares",
    "euro": "euros",
    "libra": "libras",
    "iene": "ienes",
    "peso": "pesos",
}


def trata_numero(numero):
    """
    Trata o número para ser convertido recebe string, inteiro ou float e retorna tupla com inteiro e fração
    """
    if isinstance(numero, float):
        numero_split = str(numero).split(".")
    elif isinstance(numero, int):
        numero_split = [str(numero), "00"]
    elif numero.count(",") == 1:
        numero_split = numero.split(",")
    elif numero.count(".") == 1:
        numero_split = numero.split(".")
    else:
        numero_split = [numero, "00"]

    numero_split[0] = "".join(char for char in numero_split[0] if char.isdigit())
    return tuple(numero_split)


def trata_centena(numero):
    """
    Transcreve um número de 100 a 999 em algarismos para um string representando
    o número por extenso.
    """
    centena = DICIONARIO_CARDINAIS[int(numero[0]) * 100]
    dezena = DICIONARIO_CARDINAIS[int(numero[1]) * 10]
    unidade = DICIONARIO_CARDINAIS[int(numero[2])]
    if int(numero) == 100:
        return "cem"
    elif int(numero) == 0 or int(numero[1:]) == 0:
        return centena
    elif int(numero[1:]) < 20:
        return f'{centena + " e " if centena != "zero" else ""}{DICIONARIO_CARDINAIS[int(numero[1:])]}'
    elif int(numero[2]) == 0:
        return f'{centena + " e " if centena != "zero" else ""}{dezena if dezena != "zero" else ""}'
    else:
        return f'{centena + " e " if centena != "zero" else ""}{dezena + " e " if dezena != "zero" else ""}{unidade}'


def trata_longos(numero, separador):
    """
    Transcreve números maiores que 1000 em algarismos para um string representando
    o número por extenso.
    """

    def ajusta_separador(separador):
        """Ajusta o separador para a função trata_longos."""
        if separador == "e":
            return " e"
        elif separador == " ":
            return ""
        else:
            return separador

    def aplica_multiplicador_milhares(multiplicador_milhares, valor):
        """Aplica o multiplicador de milhares ao valor."""
        if multiplicador_milhares > 0:
            valor += f" {DICIONARIO_CARDINAIS[10**(3*multiplicador_milhares)]}"
            if int(grupo) > 1:
                valor = valor.replace("ão", "ões")
        return valor

    multiplicador_milhares = 0
    lista_numeros = []
    numero_str = str(numero)
    numero_str = numero_str.zfill((len(numero_str) + 2) // 3 * 3)
    grupos_de_digitos = [numero_str[i : i + 3] for i in range(0, len(numero_str), 3)]

    for grupo in grupos_de_digitos[::-1]:
        valor = trata_centena(grupo)
        if valor != "zero":
            valor = aplica_multiplicador_milhares(multiplicador_milhares, valor)
            lista_numeros.append(valor)
        multiplicador_milhares += 1

    if separador == "," or separador == " ":
        # marcador para a regra de separar por "e" o último e penúltimo elementos
        # quando inferior a 101 ou centena redonda
        if len(lista_numeros) > 1:
            if (
                int(grupos_de_digitos[-1]) < 101
                or int(grupos_de_digitos[-1][0]) > 1
                and grupos_de_digitos[-1][-2:] == "00"
            ):
                lista_numeros[0] = "***" + lista_numeros[0]
    separador = ajusta_separador(separador)

    return f"{separador} ".join(lista_numeros[::-1]).replace(f"{separador} ***", " e ")


def numeros(numero, gramatical=True, separador=","):
    """Transcreve um número em algarismos para um string representando o número por extenso."""
    numero_str, fracao = trata_numero(numero)
    inteiro = int(numero_str) if int(fracao) == 0 else None
    if "-" in numero_str:
        raise ValueError("Não é possível transcrever números negativos")
    elif inteiro > 10:
        if inteiro == 100:
            return DICIONARIO_CARDINAIS[100].replace("ento", "em")
        elif inteiro == 1000:
            return DICIONARIO_CARDINAIS[1000]
        if gramatical:
            raise ValueError(
                "Não é correto transcrever números maiores que 10 por extenso"
            )
    if inteiro < 1000:
        return trata_centena(str(numero).zfill(3))
    return trata_longos(numero, separador)


def moeda(numero, moeda="real"):
    """Transcreve um número em algarismos para um string representando o número por extenso."""
    numero_str, fracao = trata_numero(numero)
    inteiro = int(numero_str)

    algorismo_str = f"{inteiro:_},{fracao}"
    algorismo_str = algorismo_str.replace(".", ",").replace("_", ".")
    numero_extenso = numeros(numero_str, gramatical=False, separador=",")
    centavo_str = " centavo" if int(fracao) <= 1 else " centavos"
    fracao = trata_centena("0" + fracao.zfill(2)[:2])
    moeda_str = moeda if inteiro <= 1 else MOEDAS_PLURAIS[moeda]

    if moeda == "libra" and (numero_str[-1] == "1" or numero_str[-1] == "2"):
        numero_extenso = numero_extenso + "a"
        numero_extenso = numero_extenso.replace("doisa", "duas")

    conector = " e " if numero_extenso != "zero" and fracao != "zero" else ""
    centavo_str = fracao + centavo_str if fracao != "zero" else ""
    fecho = (
        " de " + moeda_str
        if numero_extenso == "zero"
        else (
            "zero " + moeda_str if fracao == "zero" and numero_extenso == "zero" else ""
        )
    )
    moeda_str = " " + moeda_str if numero_extenso != "zero" else ""
    numero_extenso = numero_extenso if numero_extenso != "zero" else ""

    return f"{DICIONARIO_MOEDAS[moeda]} {algorismo_str} ({numero_extenso}{moeda_str}{conector}{centavo_str}{fecho})"
