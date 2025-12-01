import json
from pathlib import Path
from generator.sheet_generator import generate_a4_sheet

def load_products():
    path = Path(__file__).parent.parent / "products" / "products_db.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_list(lst, size):
    """Κόβει λίστα σε κομμάτια των size"""
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

def main():
    products = load_products()
    print(f"Βρέθηκαν {len(products)} προϊόντα στο JSON.")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    page = 1
    for batch in chunk_list(products, 20):
        filename = f"a4_sheet_{page}.png"
        output_path = output_dir / filename

        print(f"➡ Δημιουργία σελίδας {page} ({len(batch)} προϊόντα)…")

        generate_a4_sheet(batch, output_path=str(output_path))

        print(f"✔ Αποθηκεύτηκε: {output_path}")

        page += 1

    print("🎉 Όλες οι σελίδες δημιουργήθηκαν επιτυχώς!")

if __name__ == "__main__":
    main()
