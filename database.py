import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB = "products.db"

def get_conn():
    """ Criando conexão com o banco de dados """
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def setup_db():
    """ Criando a tabela de produtos caso ela não exista """
    print("Configurando o banco de dados...")
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS products (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           url TEXT NOT NULL UNIQUE,
                           target_price REAL NOT NULL,
                           last_price REAL,
                           chat_id INTEGER NOT NULL,
                           last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );
        """)
        conn.commit()
        print("Banco de dados configurado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao configurar o banco de dados: {e}")
    finally:
        conn.close()

def add_product(url: str, target_price: float, chat_id: int):
    """ Adiciona um produto ao banco de dados """
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (url, target_price, chat_id) VALUES (?, ?, ?)", (url, target_price, chat_id))
        conn.commit()
        print(f"Produto adicionado: {url}")
    except sqlite3.IntegrityError:
        print(f"Erro ao adicionar produto: URL {url} já existente")
    finally:
        conn.close()

def list_products():
    """ Lista todos os produtos do banco de dados """
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Erro ao listar produtos: {e}")
    finally:
        conn.close()

def update_product(product_id: int, new_price: float):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        now_time = datetime.now()
        cursor.execute("UPDATE products SET last_price = ?, last_checked = ? WHERE id = ?", (new_price, now_time, product_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    CHAT_ID = os.getenv("CHAT_ID")
    setup_db()
    print("Adicionando produto de teste")
    add_product(
        url="https://www.kabum.com.br/produto/904276/console-sony-playstation-5-slim-edicao-digital-ssd-1tb-controle-sem-fio-dualsense-2-jogos-digitais",
        target_price=3300,
        chat_id=CHAT_ID
    )
