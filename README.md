# Fysicochemie – cursus

Cursus Fysicochemie (KU Leuven, Groep T). **De LaTeX in deze map is de enige bron**, voor het boek (PDF) én voor de website <https://dejonges.github.io/fysicochemie-cursus/>.

## Werken in Overleaf

- Je schrijft in Overleaf, zoals altijd (`main.tex` + één `.tex` per hoofdstuk).
- **Menu → GitHub → Push to GitHub**: je wijzigingen gaan naar de website. Na een paar minuten staan ze online, ook als PDF (knop "PDF" op de site).
- **Menu → GitHub → Pull from GitHub**: haalt wat Claude heeft bijgewerkt (tekst of figuren) binnen in Overleaf.
- De mappen `site/` en `.github/` heb je in Overleaf niet nodig; laat ze gewoon staan.

## Figuren

- **Figuren uit Python** staan in `Figuren/` en worden automatisch gemaakt. Niet zelf aanpassen; vraag een wijziging aan Claude.

  ```latex
  \begin{figure}[htb]
      \centering
      \includegraphics[width=0.7\linewidth]{Figuren/boyle}
      \caption{...}
      \label{fig:Boyle}
  \end{figure}
  ```

  Op de website schakelt zo'n figuur mee met het lichte en donkere thema; in het boek staat ze op wit.
- **Een nieuwe figuur vragen**: verwijs naar een naam die nog niet bestaat (bv. `Figuren/fasediagram_water`) en beschrijf in het bijschrift wat je wil zien. In de PDF en op de site verschijnt een kader "Figuur in voorbereiding" tot de figuur er is.
- **Gewone afbeeldingen** (foto's, scans) blijven in `Afbeeldingen/`.
- **Geanimeerde figuren** bewegen enkel op de website. In het boek komt automatisch één stilstaand beeld met de vermelding "animatie: zie online".
- **Breedte**: `width=0.7\linewidth` is de standaard. Een andere breedte geldt zowel in het boek als op de site.

## Oefeningen en oplossingen

```latex
\begin{oefening}
Opgave ... (in het boek én op de site)
\end{oefening}
\begin{oplossing}
Uitwerking ... (enkel op de site, dichtgeklapt onder de oefening)
\end{oplossing}
```

## Interactieve onderdelen

`\interactief{arrhenius}` voegt op die plaats op de website de interactieve figuur uit `site/_interactief/arrhenius.qmd` in. In het boek staat er een kort kader met een verwijzing naar de site.

## Hoe het werkt (voor wie verder bouwt)

Bij elke wijziging op `main` doet GitHub (`.github/workflows/publiceer.yml`):

1. `site/_figuren/maak_pdf.py`: alle Python-figuren als PDF in `Figuren/` (en terug in de repo, zodat Overleaf ze krijgt);
2. het boek compileren met LaTeX (`main.pdf`, als download op de site);
3. `site/tools/tex2qmd.py . site`: de hoofdstukken uit `main.tex` omzetten naar Quarto-pagina's;
4. `quarto render` in `site/` en publiceren op GitHub Pages.

De `.qmd`-hoofdstukken worden niet bewaard: wie iets aan de site wil veranderen, past de LaTeX aan (inhoud) of `site/` (opmaak: `stijl.scss`, `kleuren-*.scss`, `_quarto.yml`).

Figuurcode: één functie per figuur in `site/_figuren/h1.py`, `h2.py`, ... De functienaam is de naam in `Figuren/<naam>`. Kleuren altijd via `K` (zie `site/_figuren/huisstijl.py`). Een animatie krijgt `@animatie(...)` en geeft `(fig, stap)` terug (uitleg in `huisstijl.py`).
