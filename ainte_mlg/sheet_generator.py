from pathlib import Path
from PIL import Image, ImageDraw
from .label_generator import generate_label

# A4 σε 300 DPI
A4_WIDTH = 2480
A4_HEIGHT = 3508

# Πόσες ετικέτες χωράνε
COLS = 5
ROWS = 4
PER_PAGE = COLS * ROWS


def generate_a4_sheet(products, output_path="output/a4_sheet.png"):
    """
    products = λίστα dictionaries:
    {
        "title": "...",
        "price": 1.20,
        "amount": ...,
        "unit_type": ...
    }
    """

    # Δημιουργούμε άδειο A4 καμβά (κάθετο)
    sheet = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))

    # Δείγμα ετικέτας για υπολογισμό μεγέθους
    sample = generate_label({
        "title": "Δοκιμή",
        "price": 1.0,
        "amount": 1000,
        "unit_type": "τεμάχιο"
    }).rotate(90, expand=True)

    new_w = A4_WIDTH // COLS
    new_h = A4_HEIGHT // ROWS

    index = 0

    for r in range(ROWS):
        for c in range(COLS):
            if index >= len(products):
                break

            p = products[index]

            # ΔΗΜΙΟΥΡΓΙΑ ΟΛΟΚΛΗΡΗΣ ΕΤΙΚΕΤΑΣ (unit price υπολογίζεται μέσα)
            label_img = generate_label(p)

            # Περιστροφή
            label_img = label_img.rotate(90, expand=True)

            # Μέγεθος για A4 πλέγμα
            label_img = label_img.resize((new_w, new_h), Image.LANCZOS)

            # Λεπτό περίγραμμα για κόψιμο
            border = ImageDraw.Draw(label_img)
            border.rectangle((0, 0, new_w - 1, new_h - 1), outline=(0, 0, 0), width=1)

            # Τοποθέτηση στο σωστό slot
            x = c * new_w
            y = r * new_h
            sheet.paste(label_img, (x, y))

            index += 1

    # Αποθήκευση προσωρινού αρχείου
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    temp_path = output_dir / "_temp_sheet.png"
    final_path = Path(output_path)

    sheet.save(temp_path)

    # Περιστροφή τελικής σελίδας
    rotated = Image.open(temp_path).rotate(-90, expand=True)
    rotated.save(final_path)

    # Σβήσιμο προσωρινού
    temp_path.unlink(missing_ok=True)

    print(f"➡ Rotated A4 σελίδα αποθηκεύτηκε: {final_path}")
