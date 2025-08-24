import sqlite3
import os
from settings import DB
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")


def get_conn():
    """Criando conexão com o banco de dados"""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def setup_db(connection=None):
    """Criando a tabela de produtos caso ela não exista"""
    print("Configurando o banco de dados...")
    conn = connection if connection else get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
                       CREATE TABLE IF NOT EXISTS products (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           url TEXT NOT NULL UNIQUE,
                           name TEXT NOT NULL,
                           target_price REAL NOT NULL,
                           last_price REAL,
                           chat_id INTEGER NOT NULL,
                           last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );
        """
        )
        conn.commit()
        print("Banco de dados configurado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao configurar o banco de dados: {e}")
    finally:
        if not connection:
            conn.close()


def add_product(url: str, name: str, target_price: float, chat_id: int, connection=None):
    """Adiciona um produto ao banco de dados"""
    conn = connection if connection else get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (url, name, target_price, chat_id) VALUES (?, ?, ?, ?)",
            (url, name, target_price, chat_id),
        )
        conn.commit()
        print(f"Produto adicionado: {url}")
    except sqlite3.IntegrityError:
        print(f"Erro ao adicionar produto: URL {url} já existente")
    finally:
        if not connection:
            conn.close()


def list_products(connection=None):
    """Lista todos os produtos do banco de dados"""
    conn = connection if connection else get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Erro ao listar produtos: {e}")
    finally:
        if not connection:
            conn.close()


def update_product(product_id: int, new_price: float, connection=None):
    """Atualiza o preço do produto no banco de dados"""
    conn = connection if connection else get_conn()
    try:
        cursor = conn.cursor()
        now_time = datetime.now()
        cursor.execute(
            "UPDATE products SET last_price = ?, last_checked = ? WHERE id = ?",
            (new_price, now_time, product_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        if not connection:
            conn.close()

def remove_product(product_id: int, connection=None):
    """Remove um produto do banco de dados"""
    conn = connection if connection else get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Nenhum produto encontrado com ID {product_id}")
            return False
        print(f"Produto com ID {product_id} removido com sucesso")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao remover produto: {e}")
        return False
    finally:
        if not connection:
            conn.close()
if __name__ == "__main__":
    setup_db()
    print("Adicionando produtos de teste...")
    # Playstation 5 Slim
    add_product(
        url="https://www.kabum.com.br/produto/904276/console-sony-playstation-5-slim-edicao-digital-ssd-1tb-controle-sem-fio-dualsense-2-jogos-digitais",
        name="Playstation 5 Slim",
        target_price=3300,
        chat_id=CHAT_ID,
    )
    # Camiseta Adidas
    add_product(
        url="https://www.intheboxperfumes.com.br/produto/envoy-100ml-197",
        name="Envoy - 100ml",
        target_price=140,
        chat_id=CHAT_ID,
    )
    print("Produtos adicionados com sucesso!")
