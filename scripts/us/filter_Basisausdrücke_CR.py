import os
import pandas as pd

# Dateipfade
INPUT_DIR = "/Users/Computer/Documents/Studium/Master/MA/CR/Congress_TXT_clean"
OUTPUT    = "/Users/Computer/Documents/Studium/Master/MA/CR/congress_gefilterte_dateien.csv"

# Basisausdrücke
basisausdruecke = ["gender", "feminism", "feminist"]

# Filterung
treffer = []
dateien = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]

for i, dateiname in enumerate(dateien):
    pfad = os.path.join(INPUT_DIR, dateiname)
    try:
        with open(pfad, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()
        if any(begriff in text for begriff in basisausdruecke):
            treffer.append({"dateiname": dateiname, "pfad": pfad})
    except Exception as e:
        print(f"Fehler bei {dateiname}: {e}")
    if (i + 1) % 100 == 0:

# Output
df = pd.DataFrame(treffer)
df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
