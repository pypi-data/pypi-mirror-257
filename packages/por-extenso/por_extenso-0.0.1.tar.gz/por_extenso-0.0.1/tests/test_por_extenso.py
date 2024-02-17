import unittest
from src.por_extenso import trata_numero, trata_centena, numeros, moeda


class TestTrataNumero(unittest.TestCase):
    def test_carrega_string(self):
        """
        Testa se consegue carregar digitos em forma de string
        """
        data = "10"
        result = trata_numero(data)
        self.assertEqual(result, ("10", "00"))

    def test_carrega_inteiro(self):
        """
        Testa se consegue carregar digitos em forma de número inteiro
        """
        data = 4
        result = trata_numero(data)
        self.assertEqual(result, ("4", "00"))

    def test_carrega_float(self):
        """
        Testa se consegue carregar digitos em forma de número inteiro
        """
        data = 1024.12
        result = trata_numero(data)
        self.assertEqual(result, ("1024", "12"))

    def test_0(self):
        """
        Testa se consegue carregar o número zero
        """
        data = "0"
        result = trata_numero(data)
        self.assertEqual(result, ("0", "00"))

    def test_1_087_08_string(self):
        """Testa se consegue carregar o número 1.087,00"""
        data = "1.087,08"
        result = trata_numero(data)
        self.assertEqual(result, ("1087", "08"))

    def test_1_023_008_087_10_string_ponto(self):
        """Testa se consegue carregar o número 1,023,008,087.10"""
        data = "1,023,008,087.10"
        result = trata_numero(data)
        self.assertEqual(result, ("1023008087", "10"))

    def test_1_023_008_087_00_string_virgula(self):
        """Testa se consegue carregar o número 1.023.008.087,00"""
        data = "1.023.008.087,00"
        result = trata_numero(data)
        self.assertEqual(result, ("1023008087", "00"))

    def test_1_023_008_087_milionesimos(self):
        data = 1.023_008_087
        result = trata_numero(data)
        self.assertEqual(result, ("1", "023008087"))


class TestTrataCentena(unittest.TestCase):
    def test_0(self):
        """
        Testa se consegue carregar o número zero
        """
        data = "000"
        result = trata_centena(data)
        self.assertEqual(result, "zero")

    def test_100(self):
        """
        Testa se consegue carregar o número cem
        """
        data = "100"
        result = trata_centena(data)
        self.assertEqual(result, "cem")

    def test_200(self):
        """
        Testa se consegue carregar o número duzentos
        """
        data = "200"
        result = trata_centena(data)
        self.assertEqual(result, "duzentos")

    def test_989(self):
        """
        Testa se consegue carregar o número novecentos e oitenta e nove
        """
        data = "989"
        result = trata_centena(data)
        self.assertEqual(result, "novecentos e oitenta e nove")

    def test_105(self):
        """
        Testa se consegue carregar o número cento e cinco
        """
        data = "105"
        result = trata_centena(data)
        self.assertEqual(result, "cento e cinco")


class TestPorExtenso(unittest.TestCase):
    def test_zero(self):
        """
        Testa se consegue carregar o número zero
        """
        data = 0
        result = numeros(data)
        self.assertEqual(result, "zero")

    def test_um(self):
        """
        Testa se consegue carregar o número um
        """
        data = 1
        result = numeros(data)
        self.assertEqual(result, "um")

    def test_dois(self):
        """
        Testa se consegue carregar o número dois
        """
        data = 2
        result = numeros(data)
        self.assertEqual(result, "dois")

    def test_tres(self):
        """
        Testa se consegue carregar o número três
        """
        data = 3
        result = numeros(data)
        self.assertEqual(result, "três")

    def test_quatro(self):
        """
        Testa se consegue carregar o número quatro
        """
        data = 4
        result = numeros(data)
        self.assertEqual(result, "quatro")

    def test_cinco(self):
        """
        Testa se consegue carregar o número cinco
        """
        data = 5
        result = numeros(data)
        self.assertEqual(result, "cinco")

    def test_seis(self):
        """
        Testa se consegue carregar o número seis
        """
        data = 6
        result = numeros(data)
        self.assertEqual(result, "seis")

    def test_sete(self):
        """
        Testa se consegue carregar o número sete
        """
        data = 7
        result = numeros(data)
        self.assertEqual(result, "sete")

    def test_oito(self):
        """
        Testa se consegue carregar o número oito
        """
        data = 8
        result = numeros(data)
        self.assertEqual(result, "oito")

    def test_nove(self):
        """
        Testa se consegue carregar o número nove
        """
        data = 9
        result = numeros(data)
        self.assertEqual(result, "nove")

    def test_dez(self):
        """
        Testa se consegue carregar o número dez
        """
        data = 10
        result = numeros(data)
        self.assertEqual(result, "dez")

    def test_cem(self):
        """
        Testa se consegue carregar o número cem
        """
        data = 100
        result = numeros(data)
        self.assertEqual(result, "cem")

    def text_mil(self):
        """
        Testa se consegue carregar o número mil
        """
        data = 1000
        result = numeros(data)
        self.assertEqual(result, "mil")


class TestPorExtensoGramatica(unittest.TestCase):
    def test_erro_maior_que_dez(self):
        """
        Testa se consegue carregar o número onze
        """
        data = 11
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)

    def test_erro_maior_que_cem(self):
        """
        Testa se consegue carregar o número cem
        """
        data = 101
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)

    def test_erro_maior_que_mil(self):
        """
        Testa se consegue carregar o número mil
        """
        data = 1001
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)

    def test_erro_maior_que_milhao(self):
        """
        Testa se consegue carregar o número um milhão
        """
        data = 1_000_001
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)

    def test_erro_maior_que_bilhao(self):
        """
        Testa se consegue carregar o número um bilhão
        """
        data = 1_000_000_001
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)

    def test_erro_maior_que_trilhao(self):
        """
        Testa se consegue carregar o número um trilhão
        """
        data = 1_000_000_000_001
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)


class TestPorExtensoNegativo(unittest.TestCase):
    def test_erro_negativo(self):
        """
        Testa se consegue carregar o número negativo
        """
        data = -1
        with self.assertRaises(ValueError):
            numeros(data, gramatical=True)


class TestPorExtensoForcado(unittest.TestCase):
    def test_onze(self):
        """
        Testa se consegue carregar o número onze
        """
        data = 11
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "onze")

    def test_doze(self):
        """
        Testa se consegue carregar o número doze
        """
        data = 12
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "doze")

    def test_treze(self):
        """Testa se consegue carregar o número treze"""
        data = 13
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "treze")

    def test_quatorze(self):
        """Testa se consegue carregar o número quatorze"""
        data = 14
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "quatorze")

    def test_quinze(self):
        """Testa se consegue carregar o número quinze"""
        data = 15
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "quinze")

    def test_dezesseis(self):
        """Testa se consegue carregar o número dezesseis"""
        data = 16
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "dezesseis")

    def test_dezessete(self):
        """Testa se consegue carregar o número dezessete"""
        data = 17
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "dezessete")

    def test_dezoito(self):
        """Testa se consegue carregar o número dezoito"""
        data = 18
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "dezoito")

    def test_dezenove(self):
        """Testa se consegue carregar o número dezenove"""
        data = 19
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "dezenove")

    def test_vinte(self):
        """Testa se consegue carregar o número vinte"""
        data = 20
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "vinte")

    def test_trinta(self):
        """Testa se consegue carregar o número trinta"""
        data = 30
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "trinta")

    def test_quarenta(self):
        """Testa se consegue carregar o número quarenta"""
        data = 40
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "quarenta")

    def test_cinquenta(self):
        """Testa se consegue carregar o número cinquenta"""
        data = 50
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "cinquenta")

    def test_sessenta(self):
        """Testa se consegue carregar o número sessenta"""
        data = 60
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "sessenta")

    def test_setenta(self):
        """Testa se consegue carregar o número setenta"""
        data = 70
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "setenta")

    def test_oitenta(self):
        """Testa se consegue carregar o número oitenta"""
        data = 80
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "oitenta")

    def test_noventa(self):
        """Testa se consegue carregar o número noventa"""
        data = 90
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "noventa")

    def test_cem(self):
        """Testa se consegue carregar o número cem"""
        data = 100
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "cem")

    def test_duzentos(self):
        """Testa se consegue carregar o número duzentos"""
        data = 200
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "duzentos")

    def test_trezentos(self):
        """Testa se consegue carregar o número trezentos"""
        data = 300
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "trezentos")

    def test_quatrocentos(self):
        """Testa se consegue carregar o número quatrocentos"""
        data = 400
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "quatrocentos")

    def test_quinhentos(self):
        """Testa se consegue carregar o número quinhentos"""
        data = 500
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "quinhentos")

    def test_seiscentos(self):
        """Testa se consegue carregar o número seiscentos"""
        data = 600
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "seiscentos")

    def test_setecentos(self):
        """Testa se consegue carregar o número setecentos"""
        data = 700
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "setecentos")

    def test_oitocentos(self):
        """Testa se consegue carregar o número oitocentos"""
        data = 800
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "oitocentos")

    def test_novecentos(self):
        """Testa se consegue carregar o número novecentos"""
        data = 900
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "novecentos")

    def test_mil(self):
        """Testa se consegue carregar o número mil"""
        data = 1000
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "mil")

    def test_milhao(self):
        """Testa se consegue carregar o número milhão"""
        data = 1_000_000
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "um milhão")

    def test_bilhao(self):
        """Testa se consegue carregar o número bilhão"""
        data = 1_000_000_000
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "um bilhão")

    def test_trilhao(self):
        """Testa se consegue carregar o número trilhão"""
        data = 1_000_000_000_000
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "um trilhão")


class TestPorExtensoNumeroQuebradoForcado(unittest.TestCase):
    def test_1_000_001(self):
        """Testa se consegue carregar o número 1_000_001"""
        data = 1_000_001
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "um milhão e um")

    def test_2_980_033(self):
        """Testa se consegue carregar o número 2_980_033"""
        data = 2_980_033
        result = numeros(data, gramatical=False, separador=",")
        self.assertEqual(
            result, "dois milhões, novecentos e oitenta mil e trinta e três"
        )

    def test_5_100_893_023(self):
        """Testa se consegue carregar o número 5_100_893_023"""
        data = 5_100_893_023
        result = numeros(data, gramatical=False, separador="e")
        self.assertEqual(
            result,
            "cinco bilhões e cem milhões e oitocentos e noventa e três mil e vinte e três",
        )

    def test_8_001_891_100_003(self):
        """Testa se consegue carregar o número 8_001_891_100_003"""
        data = 8_001_891_100_003
        result = numeros(data, gramatical=False, separador=" ")
        self.assertEqual(
            result,
            "oito trilhões um bilhão oitocentos e noventa e um milhões cem mil e três",
        )

    def test_193_034_001(self):
        """Testa se consegue carregar o número 193_034_002"""
        data = 193_034_023
        result = numeros(data, gramatical=False, separador=",")
        self.assertEqual(
            result,
            "cento e noventa e três milhões, trinta e quatro mil e vinte e três",
        )


class TestPorExtensoNumerosRedondos(unittest.TestCase):
    def test_5_018(self):
        """Testa se consegue carregar o número 5_018"""
        data = 5_018
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "cinco mil e dezoito")

    def test_2_600(self):
        """Testa se consegue carregar o número 2_600"""
        data = 2_600
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "dois mil e seiscentos")

    def test_1_000_700(self):
        """Testa se consegue carregar o número 1_000_700"""
        data = 1_000_700
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "um milhão e setecentos")

    def test_2_000_060_000(self):
        """Testa se consegue carregar o número 2_000_060_000"""
        data = 2_000_060_000
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "dois bilhões e sessenta mil")

    def test_190_000_100_000_000(self):
        """Testa se consegue carregar o número 190_000_100_000_000"""
        data = 190_000_100_000_000
        result = numeros(data, gramatical=False)
        self.assertEqual(result, "cento e noventa trilhões e cem milhões")


class TestMoedaPorExtenso(unittest.TestCase):
    def test_real(self):
        """Testa se consegue carregar o número 1"""
        data = 1
        result = moeda(data, "real")
        self.assertEqual(result, "R$ 1,00 (um real)")

    def test_193_034_001_01(self):
        """Testa se consegue carregar o número 193_034_001"""
        data = 193_034_001.01
        result = moeda(data, "real")
        self.assertEqual(
            result,
            "R$ 193.034.001,01 (cento e noventa e três milhões, trinta e quatro mil e um reais e um centavo)",
        )

    def test_oculta_centavos(self):
        """Testa se consegue carregar o número 193_034_001"""
        data = 193_034_001
        result = moeda(data, "real")
        self.assertEqual(
            result,
            "R$ 193.034.001,00 (cento e noventa e três milhões, trinta e quatro mil e um reais)",
        )

    def test_dolar(self):
        """Testa se consegue carregar o número 1"""
        data = 1
        result = moeda(data, "dólar")
        self.assertEqual(result, "US$ 1,00 (um dólar)")

    def test_dolar_plural(self):
        """Testa se consegue carregar o número 2"""
        data = 2
        result = moeda(data, "dólar")
        self.assertEqual(result, "US$ 2,00 (dois dólares)")

    def test_euro(self):
        """Testa se consegue carregar o número 1"""
        data = 1
        result = moeda(data, "euro")
        self.assertEqual(result, "€ 1,00 (um euro)")

    def test_euro_plural(self):
        """Testa se consegue carregar o número 2"""
        data = 2
        result = moeda(data, "euro")
        self.assertEqual(result, "€ 2,00 (dois euros)")

    def test_libra(self):
        """Testa se consegue carregar o número 1"""
        data = 1
        result = moeda(data, "libra")
        self.assertEqual(result, "£ 1,00 (uma libra)")

    def test_libra_plural(self):
        """Testa se consegue carregar o número 2"""
        data = 2
        result = moeda(data, "libra")
        self.assertEqual(result, "£ 2,00 (duas libras)")

    def test_iene(self):
        """Testa se consegue carregar o número 1"""
        data = 1
        result = moeda(data, "iene")
        self.assertEqual(result, "¥ 1,00 (um iene)")

    def test_iene_plural(self):
        """Testa se consegue carregar o número 2"""
        data = 2
        result = moeda(data, "iene")
        self.assertEqual(result, "¥ 2,00 (dois ienes)")

    def teste_peso(self):
        """Testa se consegue carregar o número 1"""
        data = 1
        result = moeda(data, "peso")
        self.assertEqual(result, "ARS$ 1,00 (um peso)")

    def teste_peso_plural(self):
        """Testa se consegue carregar o número 2"""
        data = 2
        result = moeda(data, "peso")
        self.assertEqual(result, "ARS$ 2,00 (dois pesos)")


class TestMoedaCentavos(unittest.TestCase):
    def test_um_centavo(self):
        """Testa se consegue carregar o valor R$ 0,01"""
        data = 0.01
        result = moeda(data, "real")
        self.assertEqual(result, "R$ 0,01 (um centavo de real)")

    def test_sessenta_e_dois_centavos(self):
        """Testa se consegue carregar o valor R$ 0,62"""
        data = 0.62
        result = moeda(data, "real")
        self.assertEqual(result, "R$ 0,62 (sessenta e dois centavos de real)")

    # def test_seiscentos_e_vinte_e_quatro_milesimos(self):
    #     """Testa se consegue carregar o valor R$ 0,624"""
    #     data = 0.624
    #     result = moeda(data, "real")
    #     self.assertEqual(
    #         result, "R$ 0,624 (seiscentos e vinte e quatro milésimos de real)"
    #     )

    # def test_oito_reais_e_cinquenta_e_seis_milesimos(self):
    #     """Testa se consegue carregar o valor R$ 8,056"""
    #     data = 8.056
    #     result = moeda(data, "real")
    #     self.assertEqual(result, "R$ 8,056 (oito reais e cinquenta e seis milésimos)")
