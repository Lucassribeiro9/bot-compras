import unittest
import sqlite3
from datetime import datetime
import database as db

# Criando classe para testes de banco de dados
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        db.setup_db(connection=self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_product(self):
        product = {
            "url": "http://example.com/product1",
            "name": "Produto 1",
            "target_price": 100.0,
            "chat_id": 123456789,
            "last_price": None,
        }
        db.add_product(connection=self.conn, product=product)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE url = ?", (product['url'],))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result['url'], product['url'])
        self.assertEqual(result['name'], product['name'])
        self.assertEqual(result['target_price'], product['target_price'])
        self.assertEqual(result['chat_id'], product['chat_id'])
    
    def test_list_products(self):
        """Testando produtos listados no banco de dados"""
        db.add_product(
            connection=self.conn,
            url="http://example.com/product1",
            name="Produto 1",
            target_price=100.0,
            chat_id=123456789
        )
        db.add_product(
            connection=self.conn,
            url="http://example.com/product2",
            name="Produto 2",
            target_price=200.0,
            chat_id=987654321
        )
        products = db.list_products(connection=self.conn)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['name'], "Produto 1")
        self.assertEqual(products[1]['name'], "Produto 2")
    