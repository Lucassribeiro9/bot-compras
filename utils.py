# Funções e classes genéricas (Reusabilidade)
import re
# formatando preço
def format_price(price: str) -> float:
    # Recebe um preço e tenta extrair o valor numérico dele.
    if not price:
        return None
    clean_price = re.sub(r"[^\d,]", "", price).replace(",", ".")
    if not clean_price:
        print("Não foi possível extrair um número válido do preço.")
        return None
    return float(clean_price)
