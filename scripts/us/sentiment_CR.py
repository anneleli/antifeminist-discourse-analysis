import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Dateipfade
INPUT_CSV  = "/Users/Computer/Documents/Studium/Master/MA/CR/treffer_dateien.csv"
TXT_ORDNER = "/Users/Computer/Documents/Studium/Master/MA/CR/Umwandlung_pdftxt/Congress_TXT_clean"
OUTPUT_CSV = "/Users/Computer/Documents/Studium/Master/MA/CR/sentiment_congress.csv"
OUTPUT_PNG = "/Users/Computer/Documents/Studium/Master/MA/CR/sentiment_congress_nach_jahr.png"

# Größe Kontextfenster
FENSTER = 50

# Kampfbegriffe
kampfbegriffe = {
    "gender ideology": r"gender ideology",
    "gender theory":   r"gender theory",
}

# VADER initialisieren
analyzer = SentimentIntensityAnalyzer()

# Dateiliste laden
df = pd.read_csv(INPUT_CSV)


def extrahiere_kontext(text, muster, fenster=50):
    woerter = text.split()
    kontexte = []
    text_lower = text.lower()
    for treffer in re.finditer(muster, text_lower):
        pos_zeichen = treffer.start()
        woerter_davor = len(text[:pos_zeichen].split())
        start = max(0, woerter_davor - fenster)
        ende  = min(len(woerter), woerter_davor + fenster + 1)
        kontexte.append(" ".join(woerter[start:ende]))
    return " ".join(kontexte)


# Hauptanalyse
ergebnisse = []

for _, zeile in df.iterrows():
    dateiname = zeile["dateiname"]
    begriff   = zeile["begriff"]
    jahr      = zeile["year"]
    pfad      = os.path.join(TXT_ORDNER, dateiname)

    if not os.path.exists(pfad):
        print(f"Nicht gefunden: {dateiname}")
        continue

    with open(pfad, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    muster  = kampfbegriffe.get(begriff, re.escape(begriff))
    kontext = extrahiere_kontext(text, muster, FENSTER)

    if not kontext:
        continue

    scores = analyzer.polarity_scores(kontext)

    ergebnisse.append({
        "dateiname":          dateiname,
        "jahr":               jahr,
        "kampfbegriff":       begriff,
        "sentiment_compound": scores["compound"],
        "sentiment_pos":      scores["pos"],
        "sentiment_neg":      scores["neg"],
        "sentiment_neu":      scores["neu"],
        "kontext_laenge":     len(kontext.split()),
    })

ergebnis_df = pd.DataFrame(ergebnisse)

# Ausgabe Ergebnisse
print(f"Kontextfenster gesamt: {len(ergebnis_df)}")
print(ergebnis_df["sentiment_compound"].describe().round(4))
print(f"Negativ: {(ergebnis_df['sentiment_compound'] < -0.05).sum()} | "
      f"Neutral: {((ergebnis_df['sentiment_compound'] >= -0.05) & (ergebnis_df['sentiment_compound'] <= 0.05)).sum()} | "
      f"Positiv: {(ergebnis_df['sentiment_compound'] > 0.05).sum()}")
print(ergebnis_df.groupby("jahr")["sentiment_compound"].mean().round(4))
print(ergebnis_df.groupby("kampfbegriff")["sentiment_compound"].mean().round(4))

# Visualisierung
farben = ["#d7191c" if v < 0 else "#1a9641" for v in jahr_df.values]

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(jahr_df.index.astype(str), jahr_df.values, color=farben,
              edgecolor="white", width=0.6)

ax.axhline(y=0, color="black", linewidth=0.8)

for bar, val in zip(bars, jahr_df.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        val + (0.02 if val >= 0 else -0.04),
        f"{val:.4f}",
        ha="center", va="bottom" if val >= 0 else "top",
        fontsize=9
    )

ax.set_xlabel("Jahr", fontsize=11)
ax.set_ylabel("Mittlerer VADER compound score", fontsize=11)
ax.set_title(
    "Sentiment im Umfeld antifeministischer Kampfbegriffe\nnach Jahr (US-amerikanisches Teilkorpus, 2021–2025)",
    fontsize=11, pad=12
)
ax.set_ylim(min(jahr_df.values) - 0.15, max(jahr_df.values) + 0.15)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

neg_patch = mpatches.Patch(color="#d7191c", label="Negativ")
pos_patch = mpatches.Patch(color="#1a9641", label="Positiv")
ax.legend(handles=[neg_patch, pos_patch], fontsize=9, loc="lower right")

plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=150)
print(f"\nGrafik gespeichert: {OUTPUT_PNG}")
plt.show()

# CSV-Output
ergebnis_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")