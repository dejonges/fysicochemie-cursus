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
