# Dockerfile para o bot de compras
FROM python:3.11-slim-bullseye

# Instalação de dependências do sistema
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala o Chrome e dependências
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # Dependências do Chrome/Selenium
    libglib2.0-0 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libxtst6 \
    --no-install-recommends
# Baixa o chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Instala o Google Chrome e as dependências do Selenium
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y
# Remove o arquivo .deb para economizar espaço
RUN rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*
# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o container
COPY . .

# Executa o script principal do bot
CMD ["python", "-u", "bot_app.py"]
