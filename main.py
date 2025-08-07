from webscraper import buscar_preco
from notifier_telegram import send_message
import dotenv
dotenv.load_dotenv()

URL = "https://www.kabum.com.br/produto/904276/console-sony-playstation-5-slim-edicao-digital-ssd-1tb-controle-sem-fio-dualsense-2-jogos-digitais"
TARGET_PRICE = 3500

def check_price():
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

if __name__ == "__main__":
    check_price()