from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Χρώματα από το template
GREEN = (1, 179, 81)
BLUE = (4, 47, 208)
WHITE = (255, 255, 255)

# Διαστάσεις ΜΙΑΣ ετικέτας
LABEL_WIDTH = 500
LABEL_HEIGHT = 250

GREEN_HEIGHT = 80   # Πάνω πράσινη περιοχή τίτλου
BLUE_HEIGHT = LABEL_HEIGHT - GREEN_HEIGHT  # Κάτω μπλε περιοχή τιμής


def _load_font(size: int):
    """
    Φορτώνει μια καλή γραμματοσειρά από τα Windows.
    Αν δεν βρει, πέφτει σε default.
    """
    candidates = [
    "C:\\Windows\\Fonts\\arialbd.ttf",   # Arial Bold
    "C:\\Windows\\Fonts\\calibrib.ttf",  # Calibri Bold
    "C:\\Windows\\Fonts\\tahomabd.ttf",  # Tahoma Bold
]


    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue

    # fallback
    return ImageFont.load_default()


def _fit_text(draw, text, max_width, max_height, max_size):
    """
    Μειώνει το font size μέχρι το κείμενο να χωρέσει στο κουτί.
    """
    size = max_size
    while size > 8:
        font = _load_font(size)
        w, h = draw.textbbox((0, 0), text, font=font)[2:]
        if w <= max_width and h <= max_height:
            return font
        size -= 1
    return _load_font(8)


from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Χρώματα από το template
GREEN = (1, 179, 81)
BLUE = (4, 47, 208)
WHITE = (255, 255, 255)

# Διαστάσεις ΜΙΑΣ ετικέτας
LABEL_WIDTH = 500
LABEL_HEIGHT = 250

GREEN_HEIGHT = 80   # Πάνω πράσινη περιοχή τίτλου
BLUE_HEIGHT = LABEL_HEIGHT - GREEN_HEIGHT  # Κάτω μπλε περιοχή τιμής


def _load_font(size: int):
    """
    Φορτώνει μια καλή γραμματοσειρά από τα Windows.
    Αν δεν βρει, πέφτει σε default.
    """
    candidates = [
    "C:\\Windows\\Fonts\\arialbd.ttf",   # Arial Bold
    "C:\\Windows\\Fonts\\calibrib.ttf",  # Calibri Bold
    "C:\\Windows\\Fonts\\tahomabd.ttf",  # Tahoma Bold
]


    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue

    # fallback
    return ImageFont.load_default()


def _fit_text(draw, text, max_width, max_height, max_size):
    """
    Μειώνει το font size μέχρι το κείμενο να χωρέσει στο κουτί.
    """
    size = max_size
    while size > 8:
        font = _load_font(size)
        w, h = draw.textbbox((0, 0), text, font=font)[2:]
        if w <= max_width and h <= max_height:
            return font
        size -= 1
    return _load_font(8)


def generate_label(title: str, price: float, unit_price_text: str):
    """
    Δημιουργεί ΜΙΑ ετικέτα με:
    - πράσινο (τίτλος)
    - μπλε (μεγάλη τιμή)
    - κάτω αριστερά τιμή μονάδας "2,40€ / Κιλό"
    """

    img = Image.new("RGB", (LABEL_WIDTH, LABEL_HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    # ------- πράσινο πάνω --------
    draw.rectangle([(0, 0), (LABEL_WIDTH, GREEN_HEIGHT)], fill=GREEN)

    # ------- μπλε κάτω --------
    draw.rectangle([(0, GREEN_HEIGHT), (LABEL_WIDTH, LABEL_HEIGHT)], fill=BLUE)

    # =============================
    #       Τ Ι Τ Λ Ο Σ  (2 γραμμές)
    # =============================
    import textwrap

    max_width = LABEL_WIDTH - 40
    max_height = GREEN_HEIGHT - 20

    best_font = _load_font(34)
    best_lines = [title]

    for size in range(63, 21, -2):  # ψάχνουμε μεγάλο προς μικρό
        font = _load_font(size)

        words = title.split()
        lines = []
        current = ""

        for w in words:
            test = (current + " " + w).strip()
            w_box, h_box = draw.textbbox((0, 0), test, font=font)[2:]
            if w_box <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w

        if current:
            lines.append(current)

        # 2 γραμμές max
        if len(lines) > 2:
            lines = [lines[0], " ".join(lines[1:])]

        # ύψος
        heights = [draw.textbbox((0, 0), ln, font=font)[3] for ln in lines]
        total_h = sum(heights) + (len(lines) - 1) * 4

        if total_h <= max_height:
            best_font = font
            best_lines = lines
            break

    # Ζωγραφίζουμε
    current_y = (GREEN_HEIGHT - total_h) // 2
    for ln, lh in zip(best_lines, heights):
        lw, _ = draw.textbbox((0, 0), ln, font=best_font)[2:]
        lx = (LABEL_WIDTH - lw) // 2
        draw.text((lx, current_y), ln, font=best_font, fill=WHITE)
        current_y += lh + 4



    # =============================
    #     Κ Υ Ρ Ι Α   Τ Ι Μ Η
    # =============================
    price_str = f"{price:.2f}".replace(".", ",")
    left_part, right_part = price_str.split(",")

    big_font = _load_font(180)   # τεράστιο
    small_font = _load_font(70)  # δεκαδικά

    # €, /τεμ.
    euro_font = _load_font(int(70 * 0.60))
    per_font = _load_font(int(70 * 0.40))

    left_text = left_part
    decimal_text = "," + right_part
    euro_text = "€"
    per_item_text = "/τεμ."

    # Μετρήσεις
    lw, lh = draw.textbbox((0, 0), left_text, font=big_font)[2:]
    dw, dh = draw.textbbox((0, 0), decimal_text, font=small_font)[2:]
    ew, eh = draw.textbbox((0, 0), euro_text, font=euro_font)[2:]
    pw, ph = draw.textbbox((0, 0), per_item_text, font=per_font)[2:]

    total_width = lw + dw + ew + pw + 30
    total_height = max(lh, dh, eh, ph)

    px = (LABEL_WIDTH - total_width) // 2+40
    py = GREEN_HEIGHT + (BLUE_HEIGHT - total_height) // 2

    draw.text((px, py), left_text, font=big_font, fill=WHITE)
    px += lw

    draw.text((px, py + (lh - dh)), decimal_text, font=small_font, fill=WHITE)
    px += dw + 5

    draw.text((px, py + (lh - eh)), euro_text, font=euro_font, fill=WHITE)
    px += ew + 5

    draw.text((px, py + (lh - ph)), per_item_text, font=per_font, fill=WHITE)



    # =============================
    #     Τ Ι Μ Η  Μ Ο Ν Α Δ Α Σ
    # =============================
    from generator.unit_price import format_unit_price_from_db

    unit_text = format_unit_price_from_db(current_product)

    unit_font = _load_font(18)
    uw, uh = draw.textbbox((0, 0), unit_text, font=unit_font)[2:]

    draw.text((10, LABEL_HEIGHT - uh - 10), unit_text, font=unit_font, fill=WHITE)


    return img


def save_label_example():
    """
    Test demo – παράγει μια ετικέτα στο /output/
    """
    img = generate_label(
        "ΓΑΛΑ ΕΒΟΛ ΠΛΗΡΕΣ 1Λ",
        1.20,
        "1,20€ / Λίτρο"
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    out_path = output_dir / "example_label.png"
    img.save(out_path)
    print(f"Αποθηκεύτηκε στο: {out_path}")


if __name__ == "__main__":
    save_label_example()

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Χρώματα από το template
GREEN = (1, 179, 81)
BLUE = (4, 47, 208)
WHITE = (255, 255, 255)

# Διαστάσεις ΜΙΑΣ ετικέτας
LABEL_WIDTH = 500
LABEL_HEIGHT = 250

GREEN_HEIGHT = 80   # Πάνω πράσινη περιοχή τίτλου
BLUE_HEIGHT = LABEL_HEIGHT - GREEN_HEIGHT  # Κάτω μπλε περιοχή τιμής


def _load_font(size: int):
    """
    Φορτώνει γραμματοσειρά από Windows.
    """
    candidates = [
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf",
        "C:\\Windows\\Fonts\\tahomabd.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass
    return ImageFont.load_default()



def generate_label(product: dict):
    """
    Δέχεται ολόκληρο το product:
    {
      "title": "...",
      "price": ...,
      "amount": ...,
      "unit_type": ...
    }
    """

    title = product["title"]
    price = float(product["price"])

    from generator.unit_price import format_unit_price_from_db
    unit_text = format_unit_price_from_db(product)

    img = Image.new("RGB", (LABEL_WIDTH, LABEL_HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    # ------- πράσινο πάνω --------
    draw.rectangle([(0, 0), (LABEL_WIDTH, GREEN_HEIGHT)], fill=GREEN)

    # ------- μπλε κάτω --------
    draw.rectangle([(0, GREEN_HEIGHT), (LABEL_WIDTH, LABEL_HEIGHT)], fill=BLUE)

    # =============================
    #       Τ Ι Τ Λ Ο Σ (2 γραμμές)
    # =============================
    max_width = LABEL_WIDTH - 40
    max_height = GREEN_HEIGHT - 20

    best_font = _load_font(34)
    best_lines = [title]

    for size in range(50, 18, -2):
        font = _load_font(size)

        words = title.split()
        lines = []
        current = ""

        for w in words:
            test = (current + " " + w).strip()
            w_box, h_box = draw.textbbox((0, 0), test, font=font)[2:]
            if w_box <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w

        if current:
            lines.append(current)

        if len(lines) > 2:
            lines = [lines[0], " ".join(lines[1:])]

        heights = [draw.textbbox((0, 0), ln, font=font)[3] for ln in lines]
        total_h = sum(heights) + (len(lines) - 1) * 4

        if total_h <= max_height:
            best_font = font
            best_lines = lines
            break

    current_y = (GREEN_HEIGHT - total_h) // 2
    for ln, lh in zip(best_lines, heights):
        lw, _ = draw.textbbox((0, 0), ln, font=best_font)[2:]
        lx = (LABEL_WIDTH - lw) // 2
        draw.text((lx, current_y), ln, font=best_font, fill=WHITE)
        current_y += lh + 4

    # =============================
    #     Κ Υ Ρ Ι Α   Τ Ι Μ Η
    # =============================
    price_str = f"{price:.2f}".replace(".", ",")
    left_part, right_part = price_str.split(",")

    big_font = _load_font(120)
    small_font = _load_font(70)

    euro_font = _load_font(int(70 * 0.60))
    per_font = _load_font(int(70 * 0.40))

    left_text = left_part
    decimal_text = "," + right_part
    euro_text = "€"
    per_item_text = "/τεμ."

    lw, lh = draw.textbbox((0, 0), left_text, font=big_font)[2:]
    dw, dh = draw.textbbox((0, 0), decimal_text, font=small_font)[2:]
    ew, eh = draw.textbbox((0, 0), euro_text, font=euro_font)[2:]
    pw, ph = draw.textbbox((0, 0), per_item_text, font=per_font)[2:]

    total_width = lw + dw + ew + pw + 20
    total_height = max(lh, dh, eh, ph)

    px = (LABEL_WIDTH - total_width) // 2
    py = GREEN_HEIGHT + (BLUE_HEIGHT - total_height) // 2

    draw.text((px, py), left_text, font=big_font, fill=WHITE)
    px += lw

    draw.text((px, py + (lh - dh)), decimal_text, font=small_font, fill=WHITE)
    px += dw + 5

    draw.text((px, py + (lh - eh)), euro_text, font=euro_font, fill=WHITE)
    px += ew + 5

    draw.text((px, py + (lh - ph)), per_item_text, font=per_font, fill=WHITE)

    # =============================
    #     Τ Ι Μ Η  Μ Ο Ν Α Δ Α Σ
    # =============================
    unit_font = _load_font(18)
    uw, uh = draw.textbbox((0, 0), unit_text, font=unit_font)[2:]
    draw.text((10, LABEL_HEIGHT - uh - 10), unit_text, font=unit_font, fill=WHITE)

    return img



def save_label_example():
    img = generate_label({
        "title": "ΓΑΛΑ ΕΒΟΛ ΠΛΗΡΕΣ 1Λ",
        "price": 1.20,
        "amount": 1000,
        "unit_type": "λίτρο"
    })

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    out_path = output_dir / "example_label.png"
    img.save(out_path)
    print(f"Αποθηκεύτηκε στο: {out_path}")


if __name__ == "__main__":
    save_label_example()

