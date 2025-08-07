import requests
import dotenv
import os
dotenv.load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MESSAGE = "Testando o bot"

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
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
    send_message(TOKEN, CHAT_ID, MESSAGE)
        