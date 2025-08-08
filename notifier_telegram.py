# notificação para o Telegram
# Este script envia uma mensagem de teste para um bot do Telegram usando a API do Telegram.
import os

import dotenv
import requests

dotenv.load_dotenv()

# Variáveis de ambiente
# Certifique-se de que as variáveis BOT_TOKEN e CHAT_ID estão definidas no arquivo
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Mensagem de teste
MESSAGE = "Testando o bot"


def send_message(message):
    # Envia uma mensagem de teste para o bot do Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    print("Enviando notificação para o Telegram...")
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Notificação enviada com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar notificação: {e}")
        print(f"Status code: {e.response.status_code if e.response else 'N/A'}")
        print(f"Resposta da requisição: {e.response.text if e.response else 'N/A'}")


# Executando a função
if __name__ == "__main__":
    send_message(MESSAGE)
