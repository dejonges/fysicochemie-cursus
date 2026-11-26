"""Gedeelde figuurstijl voor de cursus Fysicochemie.

Kleuren en lettertype volgen de Quarto-site (stijl.scss, kleuren-licht.scss,
kleuren-donker.scss): Source Sans 3, warm crème vlak, petrol als accent en de
tinten van de kaders. Elke figuur bestaat in een lichte en een donkere versie,
zodat ze meeschakelt met het thema van de site.

Gebruik in een hoofdstuk (.qmd):

    ```{python}
    #| include: false
    import sys; sys.path.insert(0, "_figuren")
    import h1 as fig
    ```

en daarna per figuur een codeblok:

    ```{python}
    #| label: fig-boyle
    #| fig-cap: "..."
    #| renderings: [light, dark]
    fig.toon(fig.boyle)
    ```

Een figuurfunctie gebruikt altijd de kleuren uit K (bv. K.accent), nooit
vaste kleurcodes; zo werkt ze in beide thema's.
"""
from pathlib import Path
from types import SimpleNamespace

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

MAP = Path(__file__).parent

for _f in (MAP / "lettertype").glob("*.ttf"):
    font_manager.fontManager.addfont(str(_f))
plt.style.use(MAP / "fysicochemie.mplstyle")

# In Jupyter/Quarto niet bijsnijden, zodat het afgeronde kader op de rand blijft.
try:
    from IPython import get_ipython

    _ip = get_ipython()
    if _ip is not None:
        _ip.run_line_magic("config", "InlineBackend.print_figure_kwargs = {'bbox_inches': None}")
except ImportError:
    pass

# ---------------------------------------------------------------- kleuren
# Elke kleur komt uit de site: accent (petrol) en de tekstkleuren van de kaders
# (toepassing = blauw, voorbeeld = groen, definitie = oker, besluit = paars).
# 'rood' (terracotta) is de enige toevoeging: nodig voor warm/heet vs. koud.
THEMAS = {
    "licht": dict(
        achtergrond="#faf9f5", tekst="#1f1e1b", as_="#3d3a35", zacht="#5e5a52", rand="#e6e2d8",
        accent="#1f5f6e", blauw="#1d4d86", groen="#2c6a37", oker="#a8780f", paars="#57407e",
        rood="#b4533a",
        vlak_accent="#e3eef0", vlak_blauw="#e6eef8", vlak_groen="#eef7ef", vlak_oker="#fbf1d4",
        vlak_paars="#f1ecf8", vlak_rood="#f8e6df", vlak_grijs="#ecebe5",
    ),
    "donker": dict(
        achtergrond="#1c1b19", tekst="#ebe8e1", as_="#d6d2c8", zacht="#a8a398", rand="#34322d",
        accent="#7cc3d3", blauw="#a9c8ef", groen="#a7d8ae", oker="#ecd58c", paars="#cdbcef",
        rood="#eaa08a",
        vlak_accent="#1d2d31", vlak_blauw="#1b2633", vlak_groen="#1b2a1e", vlak_oker="#2d2713",
        vlak_paars="#262033", vlak_rood="#33221d", vlak_grijs="#2b2a26",
    ),
}

# Boek (PDF): zoals licht, maar op wit papier en zonder afgerond kader.
THEMAS["boek"] = dict(THEMAS["licht"], achtergrond="#ffffff")

K = SimpleNamespace()  # actieve kleuren; altijd K.naam gebruiken


def gebruik(thema="licht"):
    """Activeer het lichte of donkere thema (kleuren in K + matplotlib-instellingen)."""
    k = THEMAS[thema]
    K.__dict__.update(k)
    K.thema = thema
    K.reeks = [k["accent"], k["rood"], k["oker"], k["blauw"], k["paars"], k["groen"]]
    # koud -> warm
    K.warmte = LinearSegmentedColormap.from_list(
        "warmte", [k["blauw"], k["paars"], k["rood"], k["oker"]])
    mpl.rcParams.update({
        "figure.facecolor": k["achtergrond"], "savefig.facecolor": k["achtergrond"],
        "text.color": k["tekst"], "axes.edgecolor": k["as_"], "axes.labelcolor": k["tekst"],
        "axes.titlecolor": k["tekst"], "xtick.color": k["as_"], "ytick.color": k["as_"],
        "xtick.labelcolor": k["tekst"], "ytick.labelcolor": k["tekst"],
        "legend.labelcolor": k["tekst"],
        "axes.prop_cycle": mpl.cycler(color=K.reeks),
    })


gebruik("licht")


def toon(functie, *args, **kw):
    """Teken een figuur eerst in het lichte en dan in het donkere thema.

    Quarto toont met `renderings: [light, dark]` automatisch de juiste versie.
    Een animatie (zie @animatie) wordt als speler in beide thema's getoond.
    """
    if getattr(functie, "animatie", None):
        return _toon_animatie(functie)
    for thema in ("licht", "donker"):
        gebruik(thema)
        f = functie(*args, **kw)
        plt.show()
        plt.close(f)
    gebruik("licht")


# ---------------------------------------------------------------- animaties
def animatie(beelden=48, interval=60, stilstaand=-1):
    """Maak van een figuurfunctie een animatie (enkel online; het boek krijgt één beeld).

    De functie geeft (fig, stap) terug, met stap(i) die beeld i tekent:

        @animatie(beelden=60, stilstaand=30)
        def golf():
            fig, ax = figuur()
            lijn, = ax.plot(x, np.sin(x))
            def stap(i):
                lijn.set_ydata(np.sin(x - i / 10))
            return kader(fig), stap

    `stilstaand` is het beeld dat in het boek komt (standaard het laatste).
    """
    def zet(functie):
        functie.animatie = dict(beelden=beelden, interval=interval, stilstaand=stilstaand)
        return functie
    return zet


def _toon_animatie(functie):
    from IPython.display import HTML, display
    from matplotlib.animation import FuncAnimation

    a = functie.animatie
    delen = []
    for thema in ("licht", "donker"):
        gebruik(thema)
        f, stap = functie()
        f.set_dpi(100)
        anim = FuncAnimation(f, stap, frames=a["beelden"], interval=a["interval"])
        try:  # compacte video (ffmpeg), anders een speler met losse beelden
            html = anim.to_html5_video().replace("<video ", "<video loop muted playsinline ")
        except Exception:
            html = anim.to_jshtml(default_mode="loop")
        delen.append(f'<div class="animatie-{thema}">{html}</div>')
        plt.close(f)
    gebruik("licht")
    display(HTML("".join(delen)))


def bewaar_boek(functie, pad):
    """Bewaar een figuur als PDF voor het boek (wit papier, vectorbeeld)."""
    gebruik("boek")
    a = getattr(functie, "animatie", None)
    if a:
        f, stap = functie()
        stap(range(a["beelden"])[a["stilstaand"]])
        f.text(0.985, 0.02, "animatie: zie online", ha="right", va="bottom",
               fontsize=9, color=K.zacht)
    else:
        f = functie()
    f.savefig(pad, metadata={"CreationDate": None, "ModDate": None, "Producer": None})
    plt.close(f)
    gebruik("licht")


def figuur(breedte=7.0, hoogte=4.6, **kw):
    """Nieuwe figuur met één of meer assen in de cursusstijl."""
    fig, ax = plt.subplots(figsize=(breedte, hoogte), **kw)
    fig.get_layout_engine().set(w_pad=0.18, h_pad=0.18)
    return fig, ax


def kader(fig):
    """Zacht afgerond kader rond de figuur (zoals de kaders op de site; niet in het boek)."""
    if K.thema == "boek":
        return fig
    w, h = fig.get_size_inches()
    r = 0.12  # inch
    fig.patches.append(
        FancyBboxPatch(
            (0.004, 0.004), 0.992, 0.992,
            boxstyle=f"round,pad=0,rounding_size={r / h}",
            mutation_aspect=w / h,
            transform=fig.transFigure, figure=fig,
            facecolor="none", edgecolor=K.rand, linewidth=1.6, zorder=-10,
        )
    )
    return fig


def label(ax, x, y, tekst, kleur=None, **kw):
    """Tekstlabel in de kleur van de curve waar het bij hoort."""
    kw.setdefault("fontsize", 11.5)
    return ax.text(x, y, tekst, color=kleur or K.tekst, **kw)


def pijl(ax, xy_van, xy_naar, kleur=None, lw=1.6, stijl="-|>", **kw):
    return ax.annotate(
        "", xy=xy_naar, xytext=xy_van,
        arrowprops=dict(arrowstyle=stijl, color=kleur or K.tekst, lw=lw,
                        shrinkA=0, shrinkB=0, mutation_scale=14, **kw),
    )


def achter(**kw):
    """bbox in de achtergrondkleur, om een label leesbaar over lijnen te zetten."""
    d = dict(boxstyle="round,pad=0.15", fc=K.achtergrond, ec="none")
    d.update(kw)
    return d


def schema(fig, ax):
    """Assen uitzetten voor een schematische tekening."""
    ax.set_axis_off()
    ax.set_aspect("equal")
    return fig, ax
