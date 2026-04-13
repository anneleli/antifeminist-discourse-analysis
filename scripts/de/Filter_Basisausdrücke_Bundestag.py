import pandas as pd

# Dateipfade 
INPUT  = "/Users/Computer/Documents/Studium/Master/Masterarbeit/BT/CPP-BT_2026-01-17_DE_CSV_Reden_Gesamt.csv"
OUTPUT = "/Users/Computer/Documents/Studium/Master/Masterarbeit/BT/korpus_bundestag_gefiltert.csv"

# Relevante Spalten
spalten = [
    "sitzung_datum",
    "sitzung_jahr",
    "wahlperiode",
    "rede_id",
    "rede_text",
    "redner_vorname",
    "redner_nachname",
    "redner_fraktion",
    "redner_rolle_kurz",
]

# Einlesen der relevanten Spalten
df = pd.read_csv(INPUT, usecols=spalten, low_memory=False)
print(f"Ausgangskorpus: {len(df)} Reden")

# Untersuchungszeitraum eingrenzen
df["sitzung_datum"] = pd.to_datetime(df["sitzung_datum"], errors="coerce")
df = df[df["sitzung_datum"].dt.year.between(2015, 2025)]
print(f"Nach Zeitfilter (2015–2025): {len(df)} Reden")

# nach Keywords filtern
suchbegriffe = ["Gender", "Feminismus", "feministisch"]
muster = "|".join(suchbegriffe)

df["rede_text"] = df["rede_text"].fillna("")
gefiltert = df[df["rede_text"].str.contains(muster, case=False, na=False)]
print(f"Nach Keyword-Filter: {len(gefiltert)} Reden")

# Output
gefiltert.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

