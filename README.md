```markdown
# antifeminist-discourse-analysis

Dieses Repository enthält die Skripte und Ergebnisse der Masterarbeit  
**„Gender als Bedrohung: Eine digitale vergleichende Analyse antifeministischer 
Diskurse in Deutschland und den USA (2015–2025)" /  
„Framing 'Gender Ideology' as a Threat: A Digital Comparative Analysis  
of Antifeminist Narratives in Germany and the United States (2015–2025)"**  
(Digital Humanities, 2026).

## Projektbeschreibung

Die Arbeit untersucht, wie antifeministische Akteure in parlamentarischen  
Debatten Deutschlands und der USA Kampfbegriffe wie 'Genderideologie',  
'Genderwahn' und 'Genderismus' bzw. *gender ideology* und *gender theory*  
einsetzen, um Geschlechterpolitik als Bedrohung zu konstruieren.  
Grundlage bilden Plenarprotokolle des Deutschen Bundestages (CPP-BT)  
sowie Protokolle des US-amerikanischen Congressional Record (2015–2025).

## Datenquellen

Die Rohdaten sind nicht im Repository enthalten.  
Sie können hier bezogen werden:

- **Deutsches Teilkorpus:** Fobbe, S. (2026). *Corpus der Plenarprotokolle  
  des Deutschen Bundestages (CPP-BT)*. Zenodo.  
  https://doi.org/10.5281/zenodo.18177196
- **US-amerikanisches Teilkorpus:** Congressional Record.  
  https://www.congress.gov/congressional-record

## Struktur

```
antifeminist-discourse-analysis/
├── scripts/
│   ├── de/               # Skripte für das deutsche Teilkorpus
│   └── us/               # Skripte für das US-amerikanische Teilkorpus
└── results/
    ├── de/               # Ergebnisse deutsches Teilkorpus
    └── us/               # Ergebnisse US-amerikanisches Teilkorpus
```

## Skripte

| Skript | Sprache | Beschreibung |
|---|---|---|
| `filter_bundestag.py` | Python | Filterung des CPP-BT nach Basisausdrücken |
| `frequenzanalyse_kampfbegriffe.py` | Python | Frequenzanalyse der Kampfbegriffe |
| `sentiment_kampfbegriffe.py` | Python | Sentimentanalyse mit Rauh-Lexikon (DE) |
| `pdf_zu_txt.py` | Python | Konvertierung der Congressional Record PDFs |
| `clean_txt.py` | Python | Bereinigung der Textdateien |
| `sentiment_congress.py` | Python | Sentimentanalyse mit VADER (US) |
| `download_congressional_record.R` | R | Download der Congressional Record PDFs via API |

## Voraussetzungen

- Python 3.x
- Pakete: `pandas`, `re`, `pdfplumber`, `vaderSentiment`
- R (für `download_congressional_record.R`)

Installation der Python-Pakete:
```bash
pip install pandas pdfplumber vaderSentiment
```

## Reihenfolge der Ausführung

**Deutsches Teilkorpus:**
1. `filter_bundestag.py`
2. `frequenzanalyse_kampfbegriffe.py`
3. `sentiment_kampfbegriffe.py`

**US-amerikanisches Teilkorpus:**
1. `download_congressional_record.R`
2. `pdf_zu_txt.py`
3. `clean_txt.py`
4. `sentiment_congress.py`

## Lizenz

Dieses Repository dient ausschließlich wissenschaftlichen Zwecken.
```
