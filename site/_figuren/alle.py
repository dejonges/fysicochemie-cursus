"""Alle figuren van de cursus onder hun naam, zodat een hoofdstuk ze kan oproepen.

De naam van een figuur is de naam van de functie in h1.py, h2.py, ... en dezelfde
naam als in de LaTeX:  \\includegraphics{Figuren/boyle}  ->  functie boyle() .
"""
import importlib
import inspect
from pathlib import Path

from huisstijl import toon, bewaar_boek  # noqa: F401

FIGUREN = {}
for _pad in sorted(Path(__file__).parent.glob("h*.py")):
    if _pad.stem in ("huisstijl",):
        continue
    _mod = importlib.import_module(_pad.stem)
    for _naam, _f in inspect.getmembers(_mod, inspect.isfunction):
        if _naam.startswith("_") or _f.__module__ != _mod.__name__:
            continue
        if _naam in FIGUREN:
            raise ValueError(f"figuurnaam {_naam} bestaat twee keer ({_pad.name})")
        FIGUREN[_naam] = _f
globals().update(FIGUREN)
