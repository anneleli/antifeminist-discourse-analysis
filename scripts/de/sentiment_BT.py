import pandas as pd
import re


# SENTIMENT-ANALYSE-BT
# Lexikon: Rauh (2018), validiert für deutsche Parlamentssprache


# Dateipfade
INPUT_KORPUS  = "/Users/Computer/Documents/Studium/Master/MA/BT/Filter_BT/korpus_bundestag_gefiltert.csv"
INPUT_LEXIKON = "/Users/Computer/Documents/Studium/Master/MA/BT/Sentiment/rauh_lexikon.csv"
INPUT_NEGATION= "/Users/Computer/Documents/Studium/Master/MA/BT/Sentiment/rauh_negation.csv"
OUTPUT        = "/Users/Computer/Documents/Studium/Master/MA/BT/Sentiment/sentiment_kampfbegriffe.csv"

# Größe Kontextfenster
FENSTER = 50

# Kampfbegriffe als regex
kampfbegriffe = {
    "Genderideologie": r"gender.?ideologie",
    "Genderwahn":      r"genderwahn",
    "Genderismus":     r"genderismus",
}

# Daten laden
df = pd.read_csv(INPUT_KORPUS, low_memory=False)
df["rede_text"] = df["rede_text"].fillna("")
df["sitzung_datum"] = pd.to_datetime(df["sitzung_datum"], errors="coerce")
df["sitzung_jahr"] = df["sitzung_datum"].dt.year

lex = pd.read_csv(INPUT_LEXIKON)
posterms = set(lex[lex["sentiment"] == 1]["feature"].str.lower().str.strip())
negterms = set(lex[lex["sentiment"] == -1]["feature"].str.lower().str.strip())
neg = pd.read_csv(INPUT_NEGATION)

print(f"Korpus: {len(df)} Reden | Positive Terme: {len(posterms)} | Negative Terme: {len(negterms)}")


def extrahiere_kontext(text, muster, fenster=50):
    # Extrahiert 'fenster' Wörter links und rechts jedes Treffers
    woerter = text.split()
    kontexte = []
    text_lower = text.lower()

    for treffer in re.finditer(muster, text_lower):
        # Position des Treffers in Zeichen → Position in Wörtern
        pos_zeichen = treffer.start()
        woerter_davor = len(text[:pos_zeichen].split())
        start = max(0, woerter_davor - fenster)
        ende = min(len(woerter), woerter_davor + fenster + 1)
        kontexte.append(" ".join(woerter[start:ende]))

    return " ".join(kontexte)


def wende_negation_an(text, neg_df):
   # Ersetzt negierte Terme durch NOT_-Varianten
    for _, zeile in neg_df.iterrows():
        text = re.sub(zeile["pattern"], zeile["replacement"], text,
                      flags=re.IGNORECASE)
    return text


def berechne_sentiment(text, posterms, negterms):
   # Normalisierter Score
    woerter = text.lower().split()
    n = len(woerter)
    if n == 0:
        return 0, 0, 0, 0

    pos = sum(1 for w in woerter if w in posterms)
    neg_count = sum(1 for w in woerter if w in negterms)
    score = pos - neg_count
    score_norm = score / n if n > 0 else 0
    return score, score_norm, pos, neg_count


# Hauptanalyse
ergebnisse = []
for _, rede in df.iterrows():
    text = rede["rede_text"]
    
    alle_kontexte = []
    gefundene_begriffe = []

    for begriff, muster in kampfbegriffe.items():
        kontext = extrahiere_kontext(text, muster, FENSTER)
        if kontext:
            alle_kontexte.append(kontext)
            gefundene_begriffe.append(begriff)

    if not alle_kontexte:
        continue

    kontext_gesamt = " ".join(alle_kontexte)
    kontext_negiert = wende_negation_an(kontext_gesamt, neg)
    score, score_norm, pos, neg_count = berechne_sentiment(
        kontext_negiert, posterms, negterms
    )

    ergebnisse.append({
        "rede_id":          rede.get("rede_id", ""),
        "sitzung_datum":    rede.get("sitzung_datum", ""),
        "sitzung_jahr":     rede.get("sitzung_jahr", ""),
        "redner_fraktion":  rede.get("redner_fraktion", ""),
        "redner_vorname":   rede.get("redner_vorname", ""),
        "redner_nachname":  rede.get("redner_nachname", ""),
        "kampfbegriffe":    ", ".join(gefundene_begriffe),
        "sentiment":        score,
        "sentiment_norm":   score_norm,
        "pos_terme":        pos,
        "neg_terme":        neg_count,
        "kontext_laenge":   len(kontext_gesamt.split()),
    })

ergebnis_df = pd.DataFrame(ergebnisse)

# Ergebnisse ausgeben
print(ergebnis_df["sentiment_norm"].describe().round(4))
print(ergebnis_df.groupby("sitzung_jahr")["sentiment_norm"].mean().round(4))
print(ergebnis_df.groupby("redner_fraktion")["sentiment_norm"].mean().round(4).sort_values())

# Speichern
ergebnis_df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")