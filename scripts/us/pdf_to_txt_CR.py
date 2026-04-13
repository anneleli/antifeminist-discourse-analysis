import os
from pathlib import Path
import pdfplumber


PDF_DIR = "/Users/Computer/Documents/Studium/Master/MA/CR/Congress_Downloads"
TXT_DIR = "/Users/Computer/Documents/Studium/Master/MA/CR/Congress_TXT"

Path(TXT_DIR).mkdir(exist_ok=True)


for pdf_path in sorted(Path(PDF_DIR).glob("*.pdf")):
    txt_path = Path(TXT_DIR) / f"{pdf_path.stem}.txt"
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  ✓ {pdf_path.stem}")
    except Exception as e:
        print(f"  ✗ {pdf_path.stem}: {e}")

print("Fertig.")