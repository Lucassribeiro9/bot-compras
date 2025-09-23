import unittest
import logging
import bot_app
from unittest.mock import patch, MagicMock, AsyncMock

logging.basicConfig(level=logging.INFO)
logging.getLogger("bot_app").setLevel(logging.DEBUG)
class TestBotCommand(unittest.IsolatedAsyncioTestCase):
    async def test_start_command(self):
        print("Iniciando teste do comando /start")
        # Cria os objetos
        mock_update = MagicMock()
        mock_update.effective_user.first_name = "TestUser"
        # Uso do AsyncMock para métodos assíncronos
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        # Chamando a função
        await bot_app.start(mock_update, mock_context)

        # Verificando se o método foi chamado com o argumento correto
        mock_update.message.reply_text.assert_called_once()
        # Pega o texto usado na função
        call_args = mock_update.message.reply_text.call_args
        replied_text = call_args.args[0]

        self.assertIn("Olá, TestUser!", replied_text)
    @patch('bot_app.db.list_products')
    async def test_list_products_command(self, mock_list_products):
        # Testando o comando /list
        print("Iniciando teste do comando /list")
        # Configura o mock para retornar uma lista de produtos
        mock_list_products.return_value = [
            {
                "id": 1,
                "name": "Produto A",
                "url": "https://example.com/a",
                "target_price": 100.0,
                "last_price": 95.0,
            },
            {
                "id": 2,
                "name": "Produto B",
                "url": "https://example.com/b",
                "target_price": 200.0,
                "last_price": 250.00,
            },
        ]
        mock_update = MagicMock()
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        await bot_app.list_products(mock_update, mock_context)
        # Verificando se o método foi chamado com o argumento correto
        mock_update.message.reply_text.assert_called_once()
        # Pega o texto usado na função
        call_args = mock_update.message.reply_text.call_args
        replied_text = call_args.args[0]

        self.assertIn("Produtos monitorados:", replied_text)
        self.assertIn("ID: 1", replied_text)
        self.assertIn("Nome: Produto A", replied_text)
        self.assertIn("Preço Alvo: R$ 100,00", replied_text)
        self.assertIn("Último Preço: R$ 95,00", replied_text)
        self.assertIn("Link: https://example.com/a", replied_text)

        self.assertIn("ID: 2", replied_text)
        self.assertIn("Nome: Produto B", replied_text)
        self.assertIn("Preço Alvo: R$ 200,00", replied_text)
        self.assertIn("Último Preço: R$ 250,00", replied_text)
        self.assertIn("Link: https://example.com/b", replied_text)