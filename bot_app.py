# Script que vai fazer o bot rodar 24/7
import os
import logging
import asyncio
import database as db
from scrapers import webscraper
from utils import format_price_str, format_price
from settings import SITE_CONFIG
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from logger import logger

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("TOKEN de acesso ao bot não encontrado nas variáveis de ambiente.")


# Start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem quando o comando /start é emitido."""
    user = update.effective_user
    logger.info(f"Usuário {user.first_name} iniciou o bot.")
    welcome_message = (
        f"Olá, {user.first_name}! Bem-vindo ao Bot de Monitoramento de Preços. Use os comandos abaixo:\n"
        "/add <URL> <Preço Alvo> - Adiciona um produto\n"
        "/list - Lista todos os produtos\n"
        "/remove <ID do Produto> - Remove um produto da lista.\n"
        "/check - Verifica os preços dos produtos agora.\n\n"
        "Exemplo: /add https://www.example.com/produto 199.99"
    )
    await update.message.reply_text(welcome_message)


# add product command
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adiciona produto ao bot"""
    chat_id = update.effective_chat.id
    logger.info(f"Comando /add recebido...")
    try:
        url = context.args[0]
        target_price_str = context.args[1]
        target_price = format_price(target_price_str)
        logger.debug(f"Buscando informações do produto na URL: {url}")
        await update.message.reply_text(
            "Buscando as informações do produto, aguarde..."
        )
        # Busca o nome
        info = webscraper.get_product_info(url)
        if not info or not info.get("name"):
            logging.error(f"Falha ao obter informações do produto na URL: {url}")
            await update.message.reply_text(
                "Não foi possível obter as informações do produto. Verifique a URL e tente novamente."
            )
            return
        product_name = info["name"]

        # Adiciona o produto ao banco de dados
        db.add_product(url, product_name, target_price, chat_id)
        logger.info(
            f"Produto '{product_name}' adicionado com sucesso para o usuário {chat_id}."
        )
        await update.message.reply_text(
            f"Produto '{product_name}' adicionado com sucesso! Valor alvo: R$ {target_price:.2f}"
        )
    except (IndexError, ValueError):
        logger.error("Erro de formatação no comando /add.")
        await update.message.reply_text(
            "Formato inválido. Use: /add <URL> <Preço Alvo>"
        )
    except Exception as e:
        logger.error(f"Erro ao adicionar produto: {e}")
        await update.message.reply_text(
            "Ocorreu um erro ao adicionar o produto. Tente novamente."
        )


async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista os produtos monitorados"""
    try:
        products = db.list_products()
        if not products:
            logger.info("Nenhum produto encontrado na lista.")
            await update.message.reply_text("Nenhum produto encontrado na sua lista.")
            return
        message = "Produtos monitorados:\n"
        for product in products:
            target_price_str = format_price_str(product["target_price"])
            last_price_str = format_price_str(product["last_price"])
            if product["last_price"] == "Não definido":
                last_price_str = "Ainda não verificado"
            message += (
                f"ID: {product['id']}\n"
                f"Nome: {product['name']}\n"
                f"Preço Alvo: {target_price_str}\n"
                f"Último Preço: {last_price_str}\n"
                f"Link: {product['url']}\n\n"
            )
        logger.info(
            f"Listando {len(products)} produtos para o usuário {update.effective_chat.id}."
        )
        await update.message.reply_text(
            message, disable_web_page_preview=True, parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        await update.message.reply_text(
            "Ocorreu um erro ao listar os produtos. Tente novamente."
        )


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove um produto da lista"""
    try:
        product_id = int(context.args[0])
        success = db.remove_product(product_id)
        if success:
            logger.info(f"Produto com ID {product_id} removido com sucesso.")
            await update.message.reply_text(
                f"Produto com ID {product_id} removido com sucesso."
            )
        else:
            logger.warning(f"Produto com ID {product_id} não encontrado.")
            await update.message.reply_text(
                f"Produto com ID {product_id} não encontrado. Tente novamente!"
            )
    except (IndexError, ValueError):
        logger.error("Erro de formatação no comando /remove.")
        await update.message.reply_text(
            "Formato inválido. Use: /remove <ID do Produto>"
        )
    except Exception as e:
        logger.error(f"Erro ao remover produto: {e}")
        await update.message.reply_text(
            "Ocorreu um erro ao remover o produto. Tente novamente."
        )
async def check_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica os preços dos produtos de maneira agendada. Verificará todos os produtos no banco de dados."""
    logger.info("Iniciando verificação de preços...")
    all_products = await asyncio.to_thread(db.list_products)
    if not all_products:
        logger.info("Nenhum produto encontrado no banco de dados.")
        return
    for product in all_products:
        try:
            product_id = product["id"]
            product_url = product["url"]
            product_name = product["name"]
            product_target_price = product["target_price"]

            logger.info(f"Verificando preço do produto: {product_name}")
            product_info = await asyncio.to_thread(webscraper.get_product_info, product_url)
            if product_info is None:
                logger.warning(f"Não foi possível obter o preço do produto: {product_name}")
                db.update_product(product_id, product["last_price"])
                continue
            current_price = product_info["price"]
            logger.info(
                f"Preço atual do produto: {product_name}: {current_price}"
            )
            # Atualizando o preço do produto no banco de dados
            await asyncio.to_thread(db.update_product, product_id, current_price)
            if current_price <= product_target_price:
                message = (
                    f"🚨 *Alerta de Preço!* 🚨\n\n"
                    f"O produto atingiu o preço desejado!\n\n"
                    f"Produto: {product_name}\n"
                    f"*Preço Atual: R$ {current_price:.2f}*\n"
                    f"Preço Alvo: R$ {product_target_price:.2f}\n\n"
                    f"Corre pra ver! ➡️ {product_url}"
                )
                await update.message.reply_text(message, parse_mode="Markdown")
                db.update_product(product_id, current_price)
        except Exception as e:
            logger.error(f"Erro ao verificar preço do produto: {product_name}")
            logger.error(f"Erro: {e}")
    logger.info("Verificação de preços concluída.")

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para verificar os preços dos produtos imediatamente."""
    await update.message.reply_text("Iniciando verificação de preços...")
    await check_prices(update, context)
    await update.message.reply_text("Verificação de preços concluída.")
def main():
    """Inicia o bot"""
    db.setup_db()
    application = Application.builder().token(TOKEN).build()
    if not application:
        raise ValueError(
            "Erro ao iniciar o bot. Verifique o TOKEN e a conexão com a internet."
        )
    # Comandos do bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list_products))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("check", check_command))

    # Agendamento da tarefa
    job_queue = application.job_queue
    job_queue.run_repeating(check_prices, interval=3600, first=10)

    logger.info("Bot iniciado com sucesso.")
    application.run_polling()


if __name__ == "__main__":
    main()
