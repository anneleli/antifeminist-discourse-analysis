import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re

# Dateipfade
INPUT          = "/Users/Computer/Documents/Studium/Master/Masterarbeit/BT/korpus_bundestag_gefiltert.csv"
OUTPUT_JAHRE   = "/Users/Computer/Documents/Studium/Master/Masterarbeit/BT/frequenz_nach_jahr.csv"       # NEU
OUTPUT_FRAKTION = "/Users/Computer/Documents/Studium/Master/Masterarbeit/BT/frequenz_nach_fraktion.csv"  # NEU
OUTPUT_GRAFIK  = "/Users/Computer/Documents/Studium/Master/Masterarbeit/BT/frequenzanalyse_bundestag.png"

# Daten laden
df = pd.read_csv(INPUT, low_memory=False)
df["sitzung_datum"] = pd.to_datetime(df["sitzung_datum"], errors="coerce")
df["sitzung_jahr"] = df["sitzung_datum"].dt.year
df["rede_text"] = df["rede_text"].fillna("").str.lower()

print(f"Korpus geladen: {len(df)} Reden, {df['sitzung_jahr'].min()}–{df['sitzung_jahr'].max()}")

# Deutsche Kampfbegriffe
kampfbegriffe = {
    "Genderismus":      r"genderismus",
    "Gender-Ideologie": r"gender.?ideologie",
    "Genderwahn":       r"genderwahn",
}

# Absolute Häufigkeiten
print("\n" + "="*55)
print("ABSOLUTE HÄUFIGKEITEN IM GESAMTKORPUS")
print("="*55)

for begriff, muster in kampfbegriffe.items():
    treffer_pro_rede = df["rede_text"].apply(
        lambda text: len(re.findall(muster, text))
    )
    df[f"n_{begriff}"] = treffer_pro_rede
    gesamt_erwaeh = treffer_pro_rede.sum()
    anzahl_reden  = (treffer_pro_rede > 0).sum()
    print(f"{begriff:<20}: {gesamt_erwaeh:>4} Erwähnungen in {anzahl_reden:>4} Reden")

# Jahresweise Häufigkeiten
print("\n" + "="*55)
print("JAHRESWEISE HÄUFIGKEITEN (Erwähnungen pro Jahr)")
print("="*55)

zählspalten = [f"n_{b}" for b in kampfbegriffe]
jahres_df = df.groupby("sitzung_jahr")[zählspalten].sum()
jahres_df.columns = list(kampfbegriffe.keys())
print(jahres_df.to_string())

jahres_df.to_csv(OUTPUT_JAHRE, encoding="utf-8-sig")  # NEU
print(f"\nGespeichert: {OUTPUT_JAHRE}")               # NEU

# Häufigkeiten nach Fraktion
print("\n" + "="*55)
print("HÄUFIGKEITEN NACH FRAKTION")
print("="*55)

fraktions_df = df.groupby("redner_fraktion")[zählspalten].sum()
fraktions_df.columns = list(kampfbegriffe.keys())
fraktions_df["Gesamt"] = fraktions_df.sum(axis=1)
fraktions_df = fraktions_df.sort_values("Gesamt", ascending=False)
print(fraktions_df.to_string())

fraktions_df.to_csv(OUTPUT_FRAKTION, encoding="utf-8-sig")  # NEU
print(f"\nGespeichert: {OUTPUT_FRAKTION}")                   # NEU

# Geimeinsames Auftreten von Kampfbegriffen
print("\n" + "="*55)
print("GEMEINSAMES AUFTRETEN IN EINER REDE")
print("="*55)

namen = list(kampfbegriffe.keys())
for i, b1 in enumerate(namen):
    for b2 in namen[i+1:]:
        beide = ((df[f"n_{b1}"] > 0) & (df[f"n_{b2}"] > 0)).sum()
        print(f"{b1} + {b2}: {beide} Reden")

alle_drei = (
    (df[f"n_{namen[0]}"] > 0) &
    (df[f"n_{namen[1]}"] > 0) &
    (df[f"n_{namen[2]}"] > 0)
).sum()
print(f"Alle drei zusammen: {alle_drei} Reden")

# Visualisierung 
fig, ax = plt.subplots(figsize=(11, 5))

farben = ["#2c7bb6", "#d7191c", "#1a9641"]
marker = ["o", "s", "^"]

for begriff, farbe, mark in zip(kampfbegriffe.keys(), farben, marker):
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
    "Häufigkeit antifeministischer Kampfbegriffe im Deutschen Bundestag (2015–2025)",
    fontsize=12, pad=12
)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.legend(fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_xlim(jahres_df.index.min() - 0.3, jahres_df.index.max() + 0.3)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig(OUTPUT_GRAFIK, dpi=150)
print(f"\nGrafik gespeichert: {OUTPUT_GRAFIK}")
plt.show()