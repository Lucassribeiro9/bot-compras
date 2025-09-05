# Gerar logs da aplicação
import logging
import sys

def setup_logger():
    """Configura o logger para a aplicação."""
    
    # Formato da mensagem de log
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    
    # Cria o logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Define o nível de log para DEBUG
    
    # Cria um handler para saída no console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Define o nível de log para INFO no console
    console_handler.setFormatter(logging.Formatter(log_format)) # Define o formato do log no console
    logger.addHandler(console_handler) # Adiciona o handler ao logger
    
    # Escrever logs em um arquivo
    file_handler = logging.FileHandler("debug.log", mode='a', encoding='utf-8') # Modo append
    file_handler.setLevel(logging.DEBUG)  # Define o nível de log para DEBUG no arquivo
    file_handler.setFormatter(logging.Formatter(log_format)) # Define o formato do log no arquivo
    logger.addHandler(file_handler) # Adiciona o handler ao logger
    
    return logger

logger = setup_logger()