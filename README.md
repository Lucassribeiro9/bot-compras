# 🛒 Bot de Compras

[![CI/CD](https://github.com/Lucassribeiro9/bot-compras/actions/workflows/scheduled_run.yml/badge.svg)

Este projeto é um bot automatizado para **monitoramento de preços**.
Ele acompanha o valor de um produto em um site e envia **alertas no Telegram** assim que o preço desejado é atingido.

O objetivo inicial era criar apenas o bot, mas o projeto evoluiu para um **estudo prático de Python**, **Docker** e **GitHub Actions** (CI/CD), simulando um fluxo completo de desenvolvimento e implantação.

---

## ✨ Funcionalidades

- 🔍 **Monitoramento de preços** a partir de uma URL específica.
- 🎯 **Comparação automática** com o preço-alvo definido pelo usuário.
- 📲 **Notificações no Telegram** quando o preço for igual ou menor ao alvo.
- ⏳ **Execução periódica** com intervalo configurável (padrão: a cada 8h).

---

## 🛠 Tecnologias Utilizadas

- **[Python](https://www.python.org/)** → Lógica principal e manipulação de dados.
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** → Web scraping para extrair informações.
- **[Requests](https://docs.python-requests.org/)** → Requisições HTTP para acessar páginas.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** → Gerenciamento de variáveis de ambiente.
- **[Docker](https://www.docker.com/)** → Containerização para execução isolada.
- **[Telegram Bot API](https://core.telegram.org/bots/api)** → Envio de alertas diretamente para o chat.

---

## ⚙️ Configuração

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/Lucassribeiro9/bot-compras.git
cd bot-compras
```

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Criar e configurar o `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

> Veja o `.env-example` para referência.

```python
BOT_TOKEN=seu_token_do_telegram
CHAT_ID=seu_chat_id_do_telegram
URL_PRODUTO=url_do_produto
PRECO_ALVO=preco_desejado
```

> Para constantes adicionais, utilize um arquivo `config.py` ou `consts.py`.

### 4️⃣ Executar o bot localmente

```bash
python main.py
```

### 5️⃣ (Opcional) Executar com Docker

```bash
docker build -t bot-compras .
docker run -d --name bot-compras bot-compras
```

### 6️⃣ (Opcional) Executar com Docker Compose

```bash
docker-compose up -d
```

---

## 🚀 Uso

- O bot verifica o preço do produto e envia **notificação no Telegram** quando ele atingir ou ficar abaixo do valor definido.
- Intervalo padrão de execução: **8 horas** (configurável no workflow do GitHub Actions).

---

## 📌 Melhorias Futuras

- 📈 **Aumentar o catálogo de sites e produtos** monitorados.
- 🖥 **Usar Selenium** para aprimorar a busca e automação, permitindo lidar com páginas dinâmicas.
- 🧩 **Implementar arquitetura de microsserviços** para modularizar e escalar a aplicação.
- 🌥 **Rodar a aplicação em máquinas virtuais** na nuvem, como AWS EC2 ou Google Cloud Platform.

---

## 🤝 Contribuição

Contribuições são **bem-vindas**!
Abra uma **issue** para discutir melhorias ou envie um **pull request** com alterações sugeridas.
