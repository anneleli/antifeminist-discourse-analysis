import os
import re
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import defaultdict
import pandas as pd

# Dateipfade
INPUT_DIR       = "/Users/Computer/Documents/Studium/Master/MA/CR/filter_congress/Congress_TXT_filtered"
OUTPUT_JAHRE    = "/Users/Computer/Documents/Studium/Master/MA/CR/frequenz_nach_jahr_congress.csv"
OUTPUT_GRAFIK   = "/Users/Computer/Documents/Studium/Master/MA/CR/frequenzanalyse_congress.png"
OUTPUT_TREFFER  = "/Users/Computer/Documents/Studium/Master/MA/CR/treffer_dateien.csv"

# Kampfbegriffe
kampfbegriffe = {
    "gender ideology": r"gender ideology",
    "gender theory":   r"gender theory",
}

# DAtum aus Dateiname
def extract_year(filename):
    match = re.search(r"(\d{4})-\d{2}-\d{2}", filename)
    return int(match.group(1)) if match else None


jahres_counts   = defaultdict(lambda: defaultdict(int))
gesamt_counts   = defaultdict(int)
treffer_dateien = defaultdict(set)

txt_files = sorted(Path(INPUT_DIR).glob("*.txt"))

for filepath in txt_files:
    year = extract_year(filepath.name)
    if year is None:
        continue
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read().lower()
    for begriff, muster in kampfbegriffe.items():
        treffer = len(re.findall(muster, text))
        if treffer > 0:
            jahres_counts[year][begriff] += treffer
            gesamt_counts[begriff] += treffer
            treffer_dateien[begriff].add(filepath.name)

# Absolute Häufigkeiten
print("ABSOLUTE HÄUFIGKEITEN IM GESAMTKORPUS")
for begriff in kampfbegriffe:
    print(f"{begriff:<20}: {gesamt_counts[begriff]:>4} Erwähnungen in {len(treffer_dateien[begriff]):>4} Dateien")

# Jahresweise Häufigkeiten
print("JAHRESWEISE HÄUFIGKEITEN (Erwähnungen pro Jahr)")
alle_jahre = sorted(jahres_counts.keys())
begriffe   = list(kampfbegriffe.keys())

print(f"{'Jahr':<8}", end="")
for b in begriffe:
    print(f"{b:<25}", end="")
print()

rows = []
for jahr in alle_jahre:
    row = {"year": jahr}
    print(f"{jahr:<8}", end="")
    for b in begriffe:
        n = jahres_counts[jahr][b]
        row[b] = n
        print(f"{n:<25}", end="")
    print()
    rows.append(row)

# Output Jahresfrequenz
with open(OUTPUT_JAHRE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["year"] + begriffe)
    writer.writeheader()
    writer.writerows(rows)

# Output Trefferdateien
treffer_rows = []
for begriff in kampfbegriffe:
    for dateiname in sorted(treffer_dateien[begriff]):
        treffer_rows.append({
            "dateiname": dateiname,
            "begriff":   begriff,
            "year":      extract_year(dateiname)
        })

with open(OUTPUT_TREFFER, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["dateiname", "begriff", "year"])
    writer.writeheader()
    writer.writerows(treffer_rows)

# Visualisierung
jahres_df = pd.DataFrame(rows).set_index("year")

fig, ax = plt.subplots(figsize=(11, 5))
farben = ["#2c7bb6", "#d7191c"]
marker = ["o", "s"]

for begriff, farbe, mark in zip(begriffe, farben, marker):
    ax.plot(
        jahres_df.index,
        jahres_df[begriff],
        label=begriff,
        color=farbe,
        marker=mark,
        linewidth=2,
        markersize=6,
    )

ax.set_xlabel("Jahr", fontsize=12)
ax.set_ylabel("Anzahl Erwähnungen", fontsize=12)
ax.set_title(
    "Häufigkeit antifeministischer Kampfbegriffe im U.S. Congress (2015–2025)",
    fontsize=12, pad=12
)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.legend(fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_xlim(jahres_df.index.min() - 0.3, jahres_df.index.max() + 0.3)
ax.set_ylim(bottom=0)
plt.tight_layout()
plt.savefig(OUTPUT_GRAFIK, dpi=150)
plt.show()