# Constantes e configurações do projeto

# database
DB = "products.db"

# Scrapers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
SITE_CONFIG = {
    "kabum.com.br": {
        "strategy: static",
        "name_selector": ("h1", {"class": "text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold"}),
        "price_selector": ("h4", {"class": "text-4xl text-secondary-500 font-bold transition-all duration-500"}),
    },
    "intheboxperfumes.com.br": {
        "strategy: dynamic",
        "name_selector": ("h1", {class="name"}),
        "price_selector": ("span", {class="cmp-price-price"}),
    },
    "nike.com.br": {
        "strategy": "dynamic",
        "name_selector": ("h1", {"data-testid": "product-name"}),
        "price_selector": ("span", {"data-testid": "main-price"}),
    }
}