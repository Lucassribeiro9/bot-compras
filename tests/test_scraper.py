import unittest
from webscraper import format_price


class TestFormatPrice(unittest.TestCase):
    def test_format_price(self):
        brute_price = "R$ 3.254,07"
        estimated_price = 3254.07
        self.assertEqual(format_price(brute_price), estimated_price)
    def test_format_price_with_invalid_price(self):
        brute_price = "R$ 3.254,07"
        estimated_price = None
        self.assertEqual(format_price(brute_price), estimated_price)
    def test_format_price_with_empty_price(self):
        brute_price = ""
        estimated_price = None
        self.assertEqual(format_price(brute_price), estimated_price)
    def test_format_price_with_spaces(self):
        brute_price = "  R$ 3.254,07  "
        estimated_price = 3254.07
        self.assertEqual(format_price(brute_price), estimated_price)
        
        