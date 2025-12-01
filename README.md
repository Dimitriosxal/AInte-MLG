# MLG Labels  
A Python package for generating price labels for retail products, ready to print on A4 sheets (20-label layout).

## 📝 Overview
MLG Labels είναι ένα μικρό, εύχρηστο Python package που δέχεται JSON προϊόντων  
και επιστρέφει έτοιμα labels, μορφοποιημένα με σωστό μέγεθος για εκτύπωση.

Χρησιμοποιείται από το προσωπικό automation workflow για mini market & bakery environments.

---

## 🚀 Installation

```bash
pip install mlg-labels

or
 
ή για developers (editable mode):

pip install -e .

📦 JSON Input Format

Το package περιμένει ένα JSON με λίστα προϊόντων:
[
  {
    "name": "Παπαδοπούλου ψωμί τοστ",
    "price": 1.72,
    "volume": "700g",
    "brand": "Παπαδοπούλου"
  },
  {
    "name": "Ιωνίς εξαιρετικά παρθένο ελαιόλαδο",
    "price": 26.18,
    "volume": "3L",
    "brand": "Ιωνίς"
  }
]

🧩 Usage Example

from ainte_mlg.label_generator import generate_labels

products = [
    {"name": "Παπαδοπούλου ψωμί τοστ", "price": 1.72, "volume": "700g"},
    {"name": "Ιωνίς ελαιόλαδο", "price": 26.18, "volume": "3L"}
]

labels = generate_labels(products)

for label in labels:
    print(label)
	
Output example:

[ Παπαδοπούλου ψωμί τοστ ]
700g  
Τιμή: 1.72 €
----------------------
[ Ιωνίς ελαιόλαδο ]
3L  
Τιμή: 26.18 €
----------------------


🖨 Printing (A4)

Το package παράγει labels προσαρμοσμένα για:

20 labels per page

70mm × 37mm label size

Συμβατότητα με κοινά A4 label sheets (Amazon / e-shop)

🗂 Package Structure

ainte_mlg/
    __init__.py
    label_generator.py
    utils.py

🔧 Roadmap

 A4 PDF export

 Custom label templates

 Auto-detect volume & brand

 Integration with OCR Automation

 CLI: mlg generate products.json

📄 License

MIT License

👤 Author

Dimitrios Xalatsis
AI Integration Developer
