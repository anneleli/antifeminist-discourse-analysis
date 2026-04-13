
# Nachbereinigung der Congressional Record TXT-Dateien
# Entfernt Metadaten-Artefakte aus bereits konvertierten TXT-Dateien.

# Verwendung:
# python clean_txt.py --input ./Congress_TXT --output ./Congress_TXT_clean



import re
import argparse
import sys
from pathlib import Path
from tqdm import tqdm


def clean_text(text: str) -> str:

    lines = text.splitlines()
    cleaned = []

    for line in lines:

        # VerDate-Fußzeilen
        if re.match(r"VerDate\s+\w+\s+\d+\s+\d{4}", line):
            continue

        # Metadaten: rfrederick / emcdonald / smartinez on DSK...PROD
        if re.search(r"\w+ on DSK\w+PROD with \w+", line, re.I):
            continue

        # Fmt / Sfmt / Frm / Jkt / PO Codes
        if re.match(r"\s*(Fmt|Sfmt|Frm|Jkt|PO)\s+\d+\s*$", line):
            continue

        # E:\CR\FM\ Pfade
        if re.match(r"\s*E:\\CR\\FM\\", line):
            continue

        # H21JAPT1 / S21JAPT1 etc. (Druckerkennung)
        if re.match(r"\s*[HS]\d{2}\w+PT\d+\s*$", line):
            continue

        # Seitennummern allein auf einer Zeile (H433, S6935, E1855, D1153)
        if re.match(r"^\s*[HSED]\d{3,5}\s*$", line):
            continue

        # Wiederholte Seitenköpfe
        if re.match(r"^[HSED]\d{3,5}\s+CONGRESSIONAL RECORD", line):
            continue

        # Zersplitterter "E PLURIBUS UNUM" Schriftzug am Anfang
        if re.match(r"^\s*(E PL|UR|IB|NU|U|M|S)\s*$", line):
            continue

        # Spiegelschrift-Artefakte (ESUOH, TSEGID, htiw, llihld)
        if re.match(r"^\s*(ESUOH|TSEGID|htiw|llihld|DORP\w+)\s*$", line):
            continue

        # Leere oder nur Leerzeichen
        stripped = line.strip()
        if stripped == "":
            cleaned.append("")
            continue

        cleaned.append(line)

    # Mehrfache Leerzeilen auf max. 2 reduzieren
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned))

    # Silbentrennungen am Zeilenende zusammenführen
    result = re.sub(r"-\n([a-z])", r"\1", result)

    # Einzelne Wörter auf eigener Zeile zusammenführen
    lines2 = result.splitlines()
    merged = []
    i = 0
    while i < len(lines2):
        line = lines2[i]
        if (re.match(r"^\s*\w{1,20}\s*$", line) and
                not re.match(r"^\s*(f|Amen|Amen\.)\s*$", line) and  # "f" als Trennzeichen behalten
                i + 1 < len(lines2) and
                lines2[i + 1].strip() != "" and
                i > 0 and merged and merged[-1].strip() != ""):
            # An vorherige Zeile anhängen
            merged[-1] = merged[-1].rstrip() + " " + line.strip()
        else:
            merged.append(line)
        i += 1

    return "\n".join(merged).strip()


def main():
    parser = argparse.ArgumentParser(
        description="Nachbereinigung der Congressional Record TXT-Dateien"
    )
    parser.add_argument("--input",   required=True,          help="Ordner mit rohen TXT-Dateien")
    parser.add_argument("--output",  default="output_clean", help="Zielordner für bereinigte TXTs")
    parser.add_argument("--inplace", action="store_true",    help="Dateien direkt überschreiben")
    args = parser.parse_args()

    input_dir  = Path(args.input).resolve()
    output_dir = Path(args.output).resolve() if not args.inplace else None

    if not input_dir.is_dir():
        print(f"Fehler: Ordner nicht gefunden: {input_dir}")
        sys.exit(1)

    alle_txts = sorted(input_dir.rglob("*.txt"))

    if not alle_txts:
        print("Keine TXT-Dateien gefunden.")
        sys.exit(0)

    print(f"Gefunden: {len(alle_txts)} TXT-Dateien")
    fehler = []

    for txt_path in tqdm(alle_txts, unit="TXT", ncols=80):
        try:
            text = txt_path.read_text(encoding="utf-8", errors="ignore")
            bereinigt = clean_text(text)

            if args.inplace:
                ziel = txt_path
            else:
                rel  = txt_path.relative_to(input_dir)
                ziel = output_dir / rel
                ziel.parent.mkdir(parents=True, exist_ok=True)

            ziel.write_text(bereinigt, encoding="utf-8")

        except Exception as e:
            fehler.append((txt_path.name, str(e)))

    print(f"Fertig – Erfolgreich: {len(alle_txts) - len(fehler)} | Fehler: {len(fehler)}")
    if fehler:
        for name, msg in fehler:
            print(f"  • {name}: {msg}")


if __name__ == "__main__":
    main()