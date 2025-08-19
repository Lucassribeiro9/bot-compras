# Populando banco de dados com dados iniciais para testes no Actions
import json
import os
from database import setup_db, add_product
from dotenv import load_dotenv
from settings import JSON_FILE

load_dotenv()


def seed_database():
    """Lê o JSON e popula o banco de dados."""
    print("Iniciando o processo de seeding...")

    CHAT_ID = os.getenv("CHAT_ID")
    if not CHAT_ID:
        print("CHAT_ID não encontrado nas variáveis de ambiente.")
        return
    try:
        with open("JSON_FILE", "r", encoding="utf-8") as file:
            products = json.load(file)
            print(f"Arquivo {JSON_FILE} carregado com sucesso.")
            print(f"Carregando {len(products)} produtos do arquivo JSON...")
    except FileNotFoundError:
        print(f"Arquivo {JSON_FILE} não encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o JSON no arquivo {JSON_FILE}.")
        return
    if not products:
        print("Nenhum produto encontrado no arquivo JSON.")
        return
    for product in products:
        try:
            add_product(
                name=product["name"],
                url=product["url"],
                target_price=product["target_price"],
                chat_id=CHAT_ID,
            )
        except Exception as e:
            print(f"Erro ao adicionar produto {product['name']}: {e}")
            continue
    print("Banco de dados populado com sucesso!")


if __name__ == "__main__":
    setup_db()
    seed_database()
    print("Seeding concluído.")
