import pandas as pd
import os

# Dateipfade
INPUT      = "/Users/Computer/Documents/Studium/Master/MA/BT/Filter_BT/korpus_bundestag_gefiltert.csv"
OUTPUT_DIR = "/Users/Computer/Documents/Studium/Master/MA/BT/antconc_texte"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Daten laden
df = pd.read_csv(INPUT, low_memory=False)
df["rede_text"] = df["rede_text"].fillna("")


# Eine TXT-Datei pro Rede
for _, zeile in df.iterrows():
    dateiname = f"{zeile['rede_id']}_{zeile['sitzung_datum']}_{zeile['redner_fraktion']}.txt"
    # Sonderzeichen im Dateinamen bereinigen
    dateiname = "".join(c if c.isalnum() or c in "._-" else "_" for c in dateiname)
    pfad = os.path.join(OUTPUT_DIR, dateiname)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(zeile["rede_text"])
