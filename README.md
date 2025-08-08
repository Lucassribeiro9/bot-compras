# Bot de Compras

O projeto consiste em criar um bot automatizado que monitora preços de produtos em um site e envia alertas quando o preço desejado é atingido. Ideal para aqueles que querem economizar e comprar no momento certo. Esse projeto servirá de exemplo para aplicações futuras. O intuito no começo era apenas criar o bot, mas como ele está servindo também como estudo para aprimorar minhas habilidades com Python e simular um projeto real, fiz desde a criação do bot à construção do ecossistema por completo, usando Docker e o Github Actions para realizar o CI/CD.

## Funcionalidades

- Monitora o preço de produtos em uma URL específica.
- Compara o preço atual com um preço alvo definido pelo usuário.
- Envia notificações via Telegram quando o preço alvo é atingido.
- Executa verificações de preço em intervalos programados.

## Tecnologias Utilizadas

- **Python**: Linguagem utilizada para a criação do algoritmo.
- **BeautifulSoup**: Para scraping de dados da web.
- **Requests**: Para fazer requisições HTTP.
- **Python-dotenv**: Para gerenciar variáveis de ambiente.
- **Docker**: Para gerar a imagem Docker e executar o ambiente de execução.
- **Telegram API**: Para envio de notificações.

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/bot-compras.git
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente. Para as demais constantes, recomendo criar um arquivo `config.py` ou `consts.py`. Caso precise de uma referência para o `.env`, veja o `.env-example` também.

   ```python
   BOT_TOKEN=seu_token_do_telegram
   CHAT_ID=seu_chat_id_do_telegram
   URL_PRODUTO=url_do_produto
   PRECO_ALVO=preco_desejado
   ```

4. Execute o bot:

   ```bash
   python main.py
   ```

5. (Opcional) Construa a imagem Docker e execute-a:

   ```bash
   docker build -t bot-compras .
   docker run -d --name bot-compras bot-compras
   ```

6. (Opcional) Execute o bot usando Docker-Compose:
   ```bash
   docker-compose up
   ```

## Uso

- O bot irá verificar o preço do produto na URL especificada e enviar uma notificação para o Telegram se o preço atingir ou for menor que o preço alvo.
- As verificações são realizadas a cada 8 horas por padrão, mas podem ser ajustadas no arquivo de workflow do GitHub Actions.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
