"""Figuren hoofdstuk 4 – Intermoleculaire krachten."""
import numpy as np
from matplotlib.ticker import NullFormatter

from huisstijl import K, figuur, kader, label  # noqa: F401


def reikwijdte():
    """|V(r)| relatief t.o.v. r = 0.3 nm voor 1/r, 1/r^4 en 1/r^6 (log-log)."""
    fig, ax = figuur(6.6, 4.5)
    r0 = 0.3
    r = np.linspace(0.3, 3.0, 300)
    reeks = [
        (1, "ion–ion  ($1/r$)", K.rood),
        (4, "ion–dipool  ($1/r^4$)", K.oker),
        (6, "Van der Waals  ($1/r^6$)", K.blauw),
    ]
    for n, naam, k in reeks:
        y = (r0 / r) ** n
        ax.loglog(r, y, color=k, lw=2.4)
        label(ax, 3.1, y[-1], naam, k, va="center", fontsize=11)
    ax.axhline(1e-2, color=K.zacht, lw=1, ls=(0, (3, 3)))
    label(ax, 1.25, 1.6e-2, "1 % van de waarde bij contact", K.zacht, fontsize=10)
    ax.set_xlim(0.3, 9)
    ax.set_ylim(2e-7, 1.6)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticks([0.3, 0.5, 1, 2, 3])
    ax.set_xticklabels(["0.3", "0.5", "1", "2", "3"])
    ax.set_xlabel("afstand $r$ (nm)")
    ax.set_ylabel(r"$|V(r)|\,/\,|V(0.3\ \mathrm{nm})|$")
    return kader(fig)


def lennard_jones():
    """Lennard-Jones-potentiaal van argon met afstotende en aantrekkende bijdrage."""
    fig, ax = figuur(6.4, 4.2)
    sig, eps = 0.340, 120.0  # nm, K (eps/kB)
    r = np.linspace(0.30, 0.80, 500)
    afst = 4 * eps * (sig / r) ** 12
    aantr = -4 * eps * (sig / r) ** 6
    ax.plot(r, afst, color=K.rood, lw=1.4, ls=(0, (4, 3)))
    ax.plot(r, aantr, color=K.blauw, lw=1.4, ls=(0, (4, 3)))
    ax.plot(r, afst + aantr, color=K.accent, lw=2.6)
    ax.axhline(0, color=K.zacht, lw=0.8)
    req = 2 ** (1 / 6) * sig
    ax.plot([req, req], [-eps, 0], color=K.zacht, lw=1, ls=":")
    ax.annotate("", xy=(req + 0.012, -eps), xytext=(req + 0.012, 0),
                arrowprops=dict(arrowstyle="<->", color=K.oker, lw=1.2))
    label(ax, req + 0.02, -40, "$\\varepsilon/k_B$ = 120 K", K.oker, fontsize=10.5)
    ax.plot(req, -eps, "o", color=K.accent, ms=6)
    label(ax, req - 0.005, -150, "$r_\\mathrm{eq}$ = 0.382 nm", K.accent, fontsize=10.5, ha="center")
    ax.plot(sig, 0, "o", color=K.tekst, ms=5)
    label(ax, sig + 0.006, 18, "$\\sigma$ = 0.340 nm", K.tekst, fontsize=10.5)
    label(ax, 0.42, 230, "afstoting $\\propto 1/r^{12}$", K.rood, fontsize=10.5)
    label(ax, 0.55, -105, "aantrekking $\\propto -1/r^{6}$", K.blauw, fontsize=10.5)
    label(ax, 0.68, -28, "totaal", K.accent, fontsize=11)
    ax.set_xlim(0.30, 0.80)
    ax.set_ylim(-200, 300)
    ax.set_xlabel("afstand $r$ (nm)")
    ax.set_ylabel("$V(r)/k_B$ (K)")
    return kader(fig)
