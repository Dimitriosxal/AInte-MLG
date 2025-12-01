import json
from pathlib import Path

def load_products_db():
    db_path = Path(__file__).parent.parent / "products" / "products_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_product(title, db):
    for p in db:
        if p["title"] == title:
            return p
    return None
