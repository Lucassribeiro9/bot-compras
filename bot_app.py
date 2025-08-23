# Script que vai fazer o bot rodar 24/7
import os
import logging
import database
import scrapers.webscraper
from settings import SITE_CONFIG
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TOKEN")
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
        "/add <URL> <Nome do Produto> <Preço Alvo> - Adiciona um produto\n"
        "/list - Lista todos os produtos\n"
        "/remove <ID do Produto> - Remove um produto da lista.\n"
    )
    await update.message.reply_text(welcome_message)