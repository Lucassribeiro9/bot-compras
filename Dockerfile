# Dockerfile para o bot de compras
FROM python:3.12-slim

# Instalação de dependências do sistema
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o container
COPY . .

# Executa o script principal do bot
CMD ["python", "-u", "main.py"]
