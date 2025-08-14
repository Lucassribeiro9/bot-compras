import requests
import re
from bs4 import BeautifulSoup


def get_product_info(url: str, config: dict) -> dict | None:
    # Busca os dados do produto em sites estáticos.
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        page = requests.get(url, headers=HEADERS)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Seletores da configuração
        price_tag, price_attr = config['price']
        name_tag, name_attr = config['name']
        
        # Procura os elementos
        price_element = soup.find(price_tag, price_attr)
        name_element = soup.find(name_tag, name_attr)

        if not price_element or not name_element:
            print(
                "Não foi possível encontrar o preço ou o nome do produto."
            )
            return None
        
        # Formata o preço
        price_text = price_element.get_text(strip=True)
        clean_price = re.sub(r"[^\d,]", "", price_text).replace(",", ".")
        if clean_price:
            final_price = float(clean_price) 
        else:
            final_price = None
        product_name = name_element.get_text(strip=True)
        if product_name and final_price is not None:
            return {
                "name": product_name,
                "price": final_price
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o preço: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado na extração de dados da URL {url}: {e}")
        return None
