import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import format_price
from selenium.common.exceptions import NoSuchElementException


def get_product_info(url: str, config: dict) -> dict | None:
    # Busca os dados do produto em sites dinâmicos.
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # Iniciando navegador com as novas opções
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
        wait_time = config.get("wait_time", 5)
        print(f"Aguardando {wait_time} segundos para a página carregar...")
        time.sleep(wait_time)
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
        if name_text and final_price is not None:
            return{"name": name_text, "price": final_price}
        else:
            print("Não foi possível extrair o nome ou o preço do produto.")
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
    URL = "https://www.intheboxperfumes.com.br/produto/envoy-100ml-197"
    config_url = {
        "strategy": "dynamic",
        "name_selector": 'h1[class="name"]',
        "price_selector": 'span[class="cmp-price-price"]',
        "wait_time": 5,
    }
    product_info = get_product_info(URL, config_url)
    if product_info:
        print(f"\n✅ SUCESSO! Informações do produto: {product_info}")
    else:
        print("\n❌ FALHA! Não foi possível obter as informações.")
