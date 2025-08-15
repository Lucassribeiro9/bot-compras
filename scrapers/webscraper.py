from scrapers import static_scraper, dynamic_scraper
from settings import SITE_CONFIG


def get_product_info(url: str) -> dict | None:
    # Busca as informações do produto
    domain = next((d for d in SITE_CONFIG if d in url), None)
    if not domain:
        print(f"URL inválida: {url}")
        return None

    config = SITE_CONFIG[domain]
    strategy = config["strategy"]
    print(f"Usando a estratégia {strategy} para verificar domínio {domain}")
    if strategy == "static":
        return static_scraper.get_product_info(url, config)
    elif strategy == "dynamic":
        return dynamic_scraper.get_product_info(url, config)
    print(f"Estratégia {strategy} não suportada para o domínio {domain}")
    return None


# Executando a função de busca de preço com uma URL de teste
if __name__ == "__main__":
    print("Testando o webscraper de forma isolada...")
    DYNAMIC_URL = "https://www.intheboxperfumes.com.br/produto/envoy-100ml-197"
    STATIC_URL = "https://www.kabum.com.br/produto/904276/console-sony-playstation-5-slim-edicao-digital-ssd-1tb-controle-sem-fio-dualsense-2-jogos-digitais"
    print("Testando url estática")
    static_info = get_product_info(STATIC_URL)
    if static_info:
        print(f"\n✅ SUCESSO! Informações do produto: {static_info}")
    else:
        print("\n❌ FALHA! Não foi possível obter as informações.")
    print("Testando url dinâmica")
    dynamic_info = get_product_info(DYNAMIC_URL)
    if dynamic_info:
        print(f"\n✅ SUCESSO! Informações do produto: {dynamic_info}")
    else:
        print("\n❌ FALHA! Não foi possível obter as informações.")
