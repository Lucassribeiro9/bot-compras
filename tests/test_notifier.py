import unittest
from unittest.mock import patch

from notifier_telegram import send_message


class TestNotifier(unittest.TestCase):
    @patch("notifier_telegram.requests.post")
    def test_send_message(self, mock_post):
        # Verifica se a função de envio de mensagem foi chamada corretamente
        mock_post.return_value.status_code = 200
        test_message = "Test message"
        send_message(test_message)
        # Verifica se a requisição POST foi feita
        self.assertTrue(mock_post.called)
