import unittest

from webscraper import format_price


class TestFormatPrice(unittest.TestCase):
    def test_format_price(self):
        # Testa se o preço bruto é formatado corretamente para um float
        brute_price = "R$ 3.254,07"
        estimated_price = 3254.07
        self.assertEqual(format_price(brute_price), estimated_price)

    def test_format_price_with_invalid_price(self):
        # Testa se o formato de preço é inválido
        brute_price = "unavailable"
        estimated_price = None
        self.assertEqual(format_price(brute_price), estimated_price)

    def test_format_price_with_empty_price(self):
        # Testa se o preço retorna vazio
        brute_price = ""
        estimated_price = None
        self.assertEqual(format_price(brute_price), estimated_price)

    def test_format_price_with_spaces(self):
        # Testa se o preço com espaços é formatado corretamente
        brute_price = "  R$ 3.254,07  "
        estimated_price = 3254.07
        self.assertEqual(format_price(brute_price), estimated_price)
