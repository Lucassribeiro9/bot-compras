# arquivo principal
import os

import dotenv

from notifier_telegram import send_message
from webscraper import buscar_preco

dotenv.load_dotenv()

# constantes
URL = os.getenv("URL_PRODUTO")
TARGET_PRICE_str = os.getenv("PRECO_ALVO")
TARGET_PRICE = float(TARGET_PRICE_str) if TARGET_PRICE_str else None


def check_price():
    # verifica se o preço do produto atingiu o valor alvo e envia notificação
    print("Verificando o preço do produto...")
    price = buscar_preco(URL)
    if price is not None:
        print(f"Preço atual: R${price:.2f}")
        if price <= TARGET_PRICE:
            message = (
                f"🚨 *Alerta de Preço Kabum!* 🚨\n\n"
                f"O produto atingiu o preço desejado!\n\n"
                f"*Preço Atual: R$ {price:.2f}*\n"
                f"Preço Alvo: R$ {TARGET_PRICE:.2f}\n\n"
                f"Corre pra ver! ➡️ {URL}"
            )
            send_message(message)
        else:
            print("O preço ainda não atingiu o alvo.")
            message = (
                f"O preço ainda não atingiu o alvo.\n\n"
                f"Preço atual: R${price:.2f}\n"
                f"Preço alvo: R${TARGET_PRICE:.2f}\n"
                f"Corre pra ver! ➡️ {URL}"
            )
            send_message(message)

    print("Verificação concluída.")


# Executando a verificação de preço
if __name__ == "__main__":
    check_price()
