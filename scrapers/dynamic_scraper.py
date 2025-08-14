import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import format_price
from selenium.common.exceptions import NoSuchElementException


def get_product_info(url: str, config: dict) -> dict | None:
    # Busca os dados do produto em sites dinâmicos.

    # Configuração do driver do Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(5)

    # Rodando no modo "headless"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    # Iniciando navegador com as novas opções
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        print("Aguardando a página carregar...")
        time.sleep(5)
    
        # Extraindo dados
        name_selector_css = config["name_selector"]
        price_selector_css = config["price_selector"]
        
        # Procurando os elementos
        name_element = driver.find_element(By.CSS_SELECTOR, name_selector_css)
        price_element = driver.find_element(By.CSS_SELECTOR, price_selector_css)
        
        # Extrai o texto
        name_text = name_element.text.strip()
        price_text = price_element.text.strip()
        print(f"Nome do produto: {name_text}")
        print(f"Preço do produto: {price_text}")
        
        # Formata o preço
        final_price = format_price(price_text)
        if final_price is None:
            return{"name": name_text, "price": final_price}
        return None
    except NoSuchElementException:
        print("Elemento não encontrado")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado na extração de dados da URL {url}: {e}")
        return None    
    finally:
        print("Fechando o navegador...")
        driver.quit()

if __name__ == "__main__":
    print("Testando o dynamic de forma isolada...")
    URL = "https://www.adidas.com.br/camiseta-dog-plane-genero-neutro/JD2830.html"
    config_url = {
        "strategy": "dynamic",
        "name_selector": 'h1[data-testid="product-title"]',
        "price_selector": 'div[data-testid="main-price"]',
        "wait_time": 5
    }
    product_info = get_product_info(URL, config_url)
    if product_info:
        print(f"\n✅ SUCESSO! Informações do produto: {product_info}")
    else:
        print("\n❌ FALHA! Não foi possível obter as informações.")