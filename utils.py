# Funções e classes genéricas (Reusabilidade)
import re


# formatando preço
def format_price(price: str) -> float | None:
    # Recebe um preço e tenta extrair o valor numérico dele.
    if not price:
        return None
    try:
        clean_price = re.sub(r"[^\d,]", "", price).replace(",", ".")
        if not clean_price:
            print("Não foi possível extrair um número válido do preço.")
            return None
        return float(clean_price)
    except (ValueError, AttributeError) as e:
        print(f"Erro ao formatar o preço: {e}")
        return None

def format_price_str(price) -> str:
    # Formata um preço float para string na moeda Real
    if not price:
        return None
    try:
        if price is not None:
            price_as_float = float(price)
        else:
            return None
    except (ValueError, TypeError):
        price_as_float = None
    if isinstance(price_as_float, float):
        return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "Não definido"