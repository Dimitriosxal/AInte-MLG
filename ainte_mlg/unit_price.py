import re

def extract_amount_from_title(title: str):
    """
    Παίρνει από τον τίτλο π.χ.:
    - 85γρ
    - 500γρ
    - 1λτ
    - 750ml
    - 30Μ
    - 3x70γρ
    - 2x160γρ

    Γυρίζει:
    (ποσότητα_σε_μονάδα, τύπος_μονάδας)
    """

    title = title.lower()

    # Πλύσεις -> Μ
    m = re.search(r"(\d+)\s*μ", title)
    if m:
        return int(m.group(1)), "πλύση"

    # Πολλαπλασιασμός 3x70γρ ή 2x160γρ
    multi = re.search(r"(\d+)\s*x\s*(\d+)\s*(g|γρ|gr)", title)
    if multi:
        quantity = int(multi.group(1)) * int(multi.group(2))
        return quantity, "γραμμάρια"

    # Συσκευασίες 3x100ml
    multi_ml = re.search(r"(\d+)\s*x\s*(\d+)\s*(ml|μλ)", title)
    if multi_ml:
        quantity = int(multi_ml.group(1)) * int(multi_ml.group(2))
        return quantity, "ml"

    # Μονές ποσότητες σε γραμμάρια
    g = re.search(r"(\d+)\s*(g|γρ|gr)", title)
    if g:
        return int(g.group(1)), "γραμμάρια"

    # Μονές ποσότητες σε ml
    ml = re.search(r"(\d+)\s*(ml|μλ)", title)
    if ml:
        return int(ml.group(1)), "ml"

    # Λίτρα
    lt = re.search(r"(\d+)\s*(lt|λτ|l)", title)
    if lt:
        return int(lt.group(1)) * 1000, "ml"   # 1 λίτρο = 1000ml

    # Αν δεν βρει τίποτα
    return None, "τεμάχιο"



def format_unit_price_from_db(product: dict):
    """
    Παράγει τελικό κείμενο για την ταμπέλα:
    π.χ. "2,78€ / Κιλό"
    """

    title = product["title"]
    price = float(product["price"])

    amount, unit_type = extract_amount_from_title(title)

    # --------------------------------------
    # 1) Τεμάχιο – δεν έχει ποσότητα -> /Τεμάχιο
    # --------------------------------------
    if amount is None:
        unit_price = price
        return f"{unit_price:.2f}€ / Τεμάχιο".replace(".", ",")

    # --------------------------------------
    # 2) Πλύσεις
    # --------------------------------------
    if unit_type == "πλύση":
        if amount == 0:
            return "—"
        unit_price = price / amount
        return f"{unit_price:.2f}€ / Πλύση".replace(".", ",")

    # --------------------------------------
    # 3) Γραμμάρια → Κιλό
    # --------------------------------------
    if unit_type == "γραμμάρια":
        unit_price = price * (1000 / amount)
        return f"{unit_price:.2f}€ / Κιλό".replace(".", ",")

    # --------------------------------------
    # 4) Υγρά σε ml → Λίτρο
    # --------------------------------------
    if unit_type == "ml":
        unit_price = price * (1000 / amount)
        return f"{unit_price:.2f}€ / Λίτρο".replace(".", ",")

    # fallback
    return "—"
