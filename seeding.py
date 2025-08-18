# Populando banco de dados com dados iniciais para testes no Actions
import json
import os
from database import setup_db, add_product
from dotenv import load_dotenv
load_dotenv()

def seed_database():
    """Lê o JSON e popula o banco de dados."""
    print("Iniciando o processo de seeding...")
    
    CHAT_ID = os.getenv("CHAT_ID")
    if not CHAT_ID:
        print("CHAT_ID não encontrado nas variáveis de ambiente.")
        return
    try:
        with open("products_to_monitor.json", "r", encoding="utf-8") as file:
            products = json.load(file)
    except FileNotFoundError:
        print("Arquivo products_to.json não encontrado.")
        return
    
    for product in products:
        add_product(
            name=product["name"],
            url=product["url"],
            target_price=product["target_price"],
            chat_id=CHAT_ID,
        )
    print("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    setup_db()
    seed_database()
    print("Seeding concluído.")       