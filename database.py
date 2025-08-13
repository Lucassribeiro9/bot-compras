import sqlite3

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

if __name__ == "__main__":
    setup_db()