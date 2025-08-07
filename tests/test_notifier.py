import unittest
from unittest.mock import patch
from notifier_telegram import send_message


class TestNotifier(unittest.TestCase):
    @patch("notifier_telegram.requests.post")
    def test_send_message(self, mock_post):
        mock_post.return_value.status_code = 200
        test_message = "Test message"
        send_message(test_message)
        self.assertTrue(mock_post.called)
