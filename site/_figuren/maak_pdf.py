"""Teken alle figuren als PDF voor het boek (map Figuren/ naast main.tex).

Gebruik:  python3 maak_pdf.py <uitvoermap>
Wordt automatisch uitgevoerd bij elke wijziging (zie .github/workflows).
"""
import sys
from pathlib import Path

import logging
import matplotlib
logging.getLogger("fontTools").setLevel(logging.ERROR)
matplotlib.use("Agg")

sys.path.insert(0, str(Path(__file__).parent))
import alle  # noqa: E402

uit = Path(sys.argv[1])
uit.mkdir(parents=True, exist_ok=True)
for naam, functie in alle.FIGUREN.items():
    alle.bewaar_boek(functie, uit / f"{naam}.pdf")
    print("  ", naam)
# PDF's van figuren die niet meer bestaan opruimen
for pdf in uit.glob("*.pdf"):
    if pdf.stem not in alle.FIGUREN:
        pdf.unlink()
print(len(alle.FIGUREN), "figuren")
