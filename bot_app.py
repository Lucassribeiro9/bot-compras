# Script que vai fazer o bot rodar 24/7
import os
import logging
import database as db
from scrapers import webscraper
from utils import format_price
from settings import SITE_CONFIG
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("TOKEN de acesso ao bot não encontrado nas variáveis de ambiente.")
# Configuração de log

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem quando o comando /start é emitido."""
    user = update.effective_user
    welcome_message = (
        f"Olá, {user.first_name}! Bem-vindo ao Bot de Monitoramento de Preços. Use os comandos abaixo:\n"
        "/add <URL> <Preço Alvo> - Adiciona um produto\n"
        "/list - Lista todos os produtos\n"
        "/remove <ID do Produto> - Remove um produto da lista.\n"
    )
    await update.message.reply_text(welcome_message)

# add product command
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adiciona produto ao bot"""
    chat_id = update.effective_chat.id
    try:
        url = context.args[0]
        target_price_str = context.args[1]
        target_price = format_price(target_price_str)
        await update.message.reply_text("Buscando as informações do produto, aguarde...")
        # Busca o nome
        info = webscraper.get_product_info(url)
        if not info or not info.get("name"):
            await update.message.reply_text("Não foi possível obter as informações do produto. Verifique a URL e tente novamente.")
            return
        product_name = info["name"]

        # Adiciona o produto ao banco de dados
        db.add_product(chat_id, product_name, url, target_price)
        await update.message.reply_text(f"Produto '{product_name}' adicionado com sucesso! Valor alvo: R$ {target_price:.2f}")
    except (IndexError, ValueError):
        await update.message.reply_text("Formato inválido. Use: /add <URL> <Preço Alvo>")
    except Exception as e:
        logging.error(f"Erro ao adicionar produto: {e}")
        await update.message.reply_text("Ocorreu um erro ao adicionar o produto. Tente novamente.")
async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista os produtos monitorados"""
    try:
        products = db.list_products()
        if not products:
            await update.message.reply_text("Nenhum produto encontrado na sua lista.")
            return
        message = "Produtos monitorados:\n"
        for product in products:
            message += (
                f"ID: {product['id']}\n"
                f"Nome: {product['name']}\n"
                f"URL: {product['url']}\n"
                f"Preço Alvo: R$ {product['target_price']:.2f}\n"
                f"Último Preço: R$ {product['last_price']:.2f}\n\n"
            )
        await update.message.reply_text(message)
    except Exception as e:
        logging.error(f"Erro ao listar produtos: {e}")
        await update.message.reply_text("Ocorreu um erro ao listar os produtos. Tente novamente.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove um produto da lista"""
    try:
        product_id = int(context.args[0])
        success = db.remove_product(product_id)
        if success:
            await update.message.reply_text(f"Produto com ID {product_id} removido com sucesso.")
        else:
            await update.message.reply_text(f"Produto com ID {product_id} não encontrado. Tente novamente!")
    except (IndexError, ValueError):
        await update.message.reply_text("Formato inválido. Use: /remove <ID do Produto>")
    except Exception as e:
        logging.error(f"Erro ao remover produto: {e}")
        await update.message.reply_text("Ocorreu um erro ao remover o produto. Tente novamente.")

def main():
    """Inicia o bot"""
    db.setup_db()
    application = Application.builder().token(TOKEN).build()
    if not application:
        raise ValueError("Erro ao iniciar o bot. Verifique o TOKEN e a conexão com a internet.")
    # Comandos do bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list_products))
    application.add_handler(CommandHandler("remove", remove))

    print("Bot iniciado com sucesso! Aguardando comandos...")
    application.run_polling()
if __name__ == "__main__":
    main()
