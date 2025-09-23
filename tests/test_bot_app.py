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
            {'Id': 1, 'name': 'Produto A', 'url': 'https://example.com/a', 'target_price': 100.0, 'last_price': 50},
            {'Id': 2, 'name': 'Produto B', 'url': 'https://example.com/b', 'target_price': 200.0, 'last_price': 250}
        ]
        mock_update = MagicMock()
        mock_update.effective_chat.id = 12345
        mock_update.message.reply_text = AsyncMock()
        mock_context = MagicMock()
        await bot_app.list_products(mock_update, mock_context)
        # Verificando se o método foi chamado com o argumento correto
        mock_list_products.assert_called_with(12345)
        mock_update.message.reply_text.assert_called_once()
        # Pega o texto usado na função
        call_args = mock_update.message.reply_text.call_args
        replied_text = call_args.args[0]

        self.assertIn("ID: 1", replied_text)
        self.assertIn("Produto A", replied_text)
        self.assertIn("Último preço: N/A", replied_text)

        self.assertIn("ID: 2", replied_text)
        self.assertIn("Produto B", replied_text)
        self.assertIn("Último preço: 250", replied_text)
