# Fysicochemie – online cursus

Online versie van de cursus Fysicochemie (KU Leuven, Groep T), gebouwd met [Quarto](https://quarto.org).
Bij elke wijziging op `main` bouwt GitHub de site opnieuw en publiceert ze op GitHub Pages (map `.github/workflows`).

## Een pagina aanpassen

- Rechtstreeks op GitHub: open een `.qmd`-bestand, klik op het potlood, pas aan en kies **Commit changes**. Na 1 à 2 minuten staat de wijziging online.
- Wiskunde schrijf je zoals in LaTeX: `$...$` in de tekst, `$$...$$` apart. Een vergelijking krijgt een nummer met `$$ ... $$ {#eq-naam}` en je verwijst ernaar met `@eq-naam`.
- Kaders: `::: {.callout-tip}` + `## Voorbeeld: titel` + tekst + `:::`.

## Opmaak aanpassen

- **`kleuren-licht.scss`** en **`kleuren-donker.scss`**: de kleuren van de lichte en donkere weergave.
- **`stijl.scss`**: lettertypes, lettergrootte, regelafstand, ruimte tussen opsommingsitems en tabelstijl. Elke regel heeft uitleg in het Nederlands.
- **Eén tabel anders**: zet achter het bijschrift van de tabel bijvoorbeeld `{tbl-colwidths="[20,80]"}` voor kolombreedtes, of `{.striped .hover}` voor een andere stijl.
- **`_quarto.yml`**: titel, hoofdstukvolgorde, thema (`cosmo`/`darkly`, zie https://bootswatch.com voor alternatieven).

## Figuren

Figuren worden bij het bouwen getekend met Python (matplotlib), zodat ze dezelfde stijl hebben als de tekst en meeschakelen met het lichte en donkere thema.

- **`_figuren/huisstijl.py`** en **`_figuren/fysicochemie.mplstyle`**: kleuren, lettertype en lijnen. Kleuren altijd via `K` (bv. `K.accent`, `K.blauw`).
- **`_figuren/h1.py`**, **`h2.py`**, ...: één functie per figuur. Gegevens van echte gassen komen uit `_figuren/toestand.py`.
- In een hoofdstuk staat een figuur zo (het bijschrift onderaan, verwijzen met `@fig-boyle`):

````markdown
::: {#fig-boyle}
```{python}
#| renderings: [light, dark]
fig.toon(fig.boyle)
```

Isothermen voor een ideaal gas.
:::
````

- **Breedte**: standaard 70% van de tekstbreedte, gecentreerd, en het bijschrift volgt dezelfde breedte. Een andere breedte geef je met een klasse achter het label: `::: {#fig-boyle .klein}` (40%), `.smal` (55%), `.breed` (85%) of `.vol` (100%). De percentages zelf staan in `stijl.scss` onder "Breedte van de figuren". Op een gsm is elke figuur volle breedte.
- Lokaal bouwen vraagt Python met de pakketten uit `requirements.txt` (`pip install -r requirements.txt`).
- Een figuur los bekijken: `cd _figuren && python3 -c "import h1; h1.boyle().savefig('test.png')"`.

## Opnieuw omzetten vanuit LaTeX

`tools/tex2qmd.py` zet de LaTeX-hoofdstukken om naar `.qmd`:

```bash
python3 tools/tex2qmd.py <map-met-tex-bestanden> .
```

Interactieve onderdelen staan in `_interactief/` en worden met `{{< include ... >}}` ingevoegd, zodat ze een nieuwe omzetting overleven.
