import re
import csv
from pathlib import Path
import pandas as pd
 
# Dateipfade
TREFFER_CSV = "/Users/Computer/Documents/Studium/Master/MA/CR/treffer_dateien.csv"
TXT_DIR     = "/Users/Computer/Documents/Studium/Master/MA/CR/filter_congress/Congress_TXT_filtered"
OUTPUT_CSV  = "/Users/Computer/Documents/Studium/Master/MA/CR/sprecher_treffer.csv"
 
KAMPFBEGRIFFE = ["gender ideology", "gender theory"]
 
# Erkennung der Sprechenden mit regex
def extract_speaker_before_hit(text, hit_pos, window=3000):
   
    pre_text = text[max(0, hit_pos - window):hit_pos]
 
    # Muster 1: Anerkennungszeile
    matches1 = list(re.finditer(
        r'Chair recognizes the gentle(?:man|woman) from ([A-Za-z\s]+?)\s*\((?:Mr\.|Mrs\.|Ms\.|Miss)\s+([A-Z][A-Z\s\-]+?)\)',
        pre_text
    ))
 
    # Muster 2: Direkte Redezeile
    matches2 = list(re.finditer(
        r'(?:^|\n)(?:Mr\.|Mrs\.|Ms\.|Miss)\s+([A-Z][A-Z\s\-]+?)\.',
        pre_text,
        re.MULTILINE
    ))
 
    last1 = matches1[-1] if matches1 else None
    last2 = matches2[-1] if matches2 else None
 
    if last1 and last2:
        if last1.start() > last2.start():
            return last1.group(2).strip().split()[0], last1.group(1).strip()
        else:
            return last2.group(1).strip().split()[0], "Unknown"
    elif last1:
        return last1.group(2).strip().split()[0], last1.group(1).strip()
    elif last2:
        return last2.group(1).strip().split()[0], "Unknown"
 
    return "Unknown", "Unknown"
 
# --- Hauptroutine ---
treffer_df = pd.read_csv(TREFFER_CSV)
 
results = []
 
for _, row in treffer_df.iterrows():
    dateiname = row["dateiname"]
    begriff   = row["begriff"]
    year      = row["year"]
    filepath  = Path(TXT_DIR) / dateiname
 
    if not filepath.exists():
        print(f"  Nicht gefunden: {dateiname}")
        continue
 
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
 
    text_lower = text.lower()
 
    for m in re.finditer(re.escape(begriff), text_lower):
        hit_pos = m.start()
        speaker, state = extract_speaker_before_hit(text, hit_pos)
 
        # Kontextfenster (50 Wörter links/rechts)
        words      = text.split()
        words_low  = text_lower.split()
        term_words = begriff.split()
        term_len   = len(term_words)
 
        context = ""
        for i in range(len(words_low) - term_len + 1):
            if words_low[i:i + term_len] == term_words:
                start   = max(0, i - 50)
                end     = min(len(words), i + 50 + term_len)
                context = " ".join(words[start:end])
                break
 
        results.append({
            "dateiname": dateiname,
            "year":      year,
            "begriff":   begriff,
            "speaker":   speaker,
            "state":     state,
            "party":     "",  # manuell via Bioguide ergänzen
            "context":   context,
        })
 
# Output
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f, fieldnames=["dateiname", "year", "begriff", "speaker", "state", "party", "context"]
    )
    writer.writeheader()
    writer.writerows(results)
 
print(f"\nFertig. {len(results)} Treffer gespeichert → {OUTPUT_CSV}")
print(f"\nEindeutige Sprecher*innen:")
sprecher = set(r["speaker"] for r in results if r["speaker"] != "Unknown")
for s in sorted(sprecher):
    print(f"  {s}")