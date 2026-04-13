import os
import shutil
import pandas as pd

CSV        = "/Users/Computer/Documents/Studium/Master/MA/CR/congress_gefilterte_dateien.csv"
OUTPUT_DIR = "/Users/Computer/Documents/Studium/Master/MA/CR/Congress_TXT_filtered"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(CSV)

for _, row in df.iterrows():
    src = row["pfad"]
    dst = os.path.join(OUTPUT_DIR, row["dateiname"])
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"Fehler bei {row['dateiname']}: {e}")

