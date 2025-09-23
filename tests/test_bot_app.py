import unittest
import bot_app
from unittest.mock import patch, MagicMock, AsyncMock

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
        self.assertIn("/add", replied_text)  