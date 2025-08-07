import requests
from bs4 import BeautifulSoup
import re


def format_price(price: str) -> float:
    # Recebe um preço limpo
    if not price:
        return None
    clean_price = re.sub(r"[^\d,]", "", price).replace(",", ".")
    if not clean_price:
        print("Não foi possível extrair um número válido do preço.")
        return None
    return float(clean_price)

def buscar_preco(url: str) -> float | None:
    print(f"Buscando o preço do produto no site: {url}")

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        page = requests.get(url, headers=HEADERS)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")
        class_css = "text-4xl text-secondary-500 font-bold transition-all duration-500"
        price = soup.find(
            "h4",
            class_=class_css
        )

        if not price:
            print("Preço não encontrado no site. Nada encontrado na classe: {class_css}")
            return None
        price_text = price.get_text(strip=True)
        print(f"Preço encontrado: {price_text}")


        final_price = format_price(price_text)
        if final_price is None:
            print("Não foi possível formatar o preço.")
            return None
        print(f"Preço final: {final_price}")
        return final_price
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o preço: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None


if __name__ == "__main__":
    TEST_URL = "https://www.kabum.com.br/produto/904276/console-sony-playstation-5-slim-edicao-digital-ssd-1tb-controle-sem-fio-dualsense-2-jogos-digitais"
    price = buscar_preco(TEST_URL)
    if price is not None:
        print(f"\n✅ SUCESSO! O preço final extraído é: R${price:.2f}")
    else:
        print("\n❌ FALHA! Não foi possível obter o preço.")
