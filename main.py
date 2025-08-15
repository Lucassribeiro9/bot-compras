# arquivo principal
from scrapers import webscraper
import database as db
from datetime import datetime
from notifier_telegram import send_message


def main():
    # verifica se o preço do produto atingiu o valor alvo e envia notificação
    print(
        f"Iniciando verificação de preço: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} "
    )
    try:
        check_products = db.list_products()
    except Exception as e:
        print(f"Erro ao verificar produtos: {e}")
        return

    if not check_products:
        print("Nenhum produto encontrado no banco de dados.")
        return
    print(f"Encontrados {len(check_products)} produtos no banco de dados.")
    for product in check_products:
        try:
            product_id = product["id"]
            product_url = product["url"]
            product_name = product["name"]
            product_target_price = product["target_price"]

            print(f"Verificando preço do produto: {product_name}")
            product_info = webscraper.get_product_info(product_url)
            if product_info is None:
                print(f"Não foi possível obter o preço do produto: {product_name}")
                db.update_product(product_id, product["last_price"])
                continue
            current_price = product_info["price"]
            print(
                f"Preço atual: R${current_price:.2f} | Preço alvo: R${product_target_price:.2f}"
            )
            if current_price <= product_target_price:
                message = (
                    f"🚨 *Alerta de Preço!* 🚨\n\n"
                    f"O produto atingiu o preço desejado!\n\n"
                    f"*Preço Atual: R$ {current_price:.2f}*\n"
                    f"Preço Alvo: R$ {product_target_price:.2f}\n\n"
                    f"Corre pra ver! ➡️ {product_url}"
                )
                send_message(message)
                db.update_product(product_id, current_price)
            else:
                print("O preço ainda não atingiu o alvo.")
                message = (
                    f"O preço ainda não atingiu o alvo.\n\n"
                    f"Preço atual: R${current_price:.2f}\n"
                    f"Preço alvo: R${product_target_price:.2f}\n"
                    f"Corre pra ver! ➡️ {product_url}"
                )
                send_message(message)
                db.update_product(product_id, current_price)
        except Exception as e:
            print(f"Erro ao verificar preço do produto: {product_name}")
            print(f"Erro: {e}")
    print(f"Verificação concluída em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


# Executando a verificação de preço
if __name__ == "__main__":
    db.setup_db()
    main()
