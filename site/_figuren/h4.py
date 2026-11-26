"""Figuren hoofdstuk 4 – Intermoleculaire krachten."""
import numpy as np
from matplotlib.ticker import NullFormatter

from huisstijl import K, figuur, kader, label, achter  # noqa: F401


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


def kookpunt_hydriden():
    """Normaal kookpunt van de hydriden van groep 14-17 (CRC Handbook)."""
    fig, ax = figuur(6.6, 4.6)
    per = [2, 3, 4, 5]
    data = [
        ("groep 14: CH$_4$ … SnH$_4$", [-161.5, -111.9, -88.5, -52.0], K.zacht, ["CH$_4$", "SiH$_4$", "GeH$_4$", "SnH$_4$"]),
        ("groep 15: NH$_3$ … SbH$_3$", [-33.3, -87.7, -62.5, -17.0], K.groen, ["NH$_3$", "PH$_3$", "AsH$_3$", "SbH$_3$"]),
        ("groep 16: H$_2$O … H$_2$Te", [100.0, -60.3, -41.3, -2.0], K.blauw, ["H$_2$O", "H$_2$S", "H$_2$Se", "H$_2$Te"]),
        ("groep 17: HF … HI", [19.5, -85.1, -66.8, -35.4], K.rood, ["HF", "HCl", "HBr", "HI"]),
    ]
    for naam, Tb, k, lab in data:
        ax.plot(per, Tb, "o-", color=k, lw=2, ms=7)
        label(ax, 5.12, Tb[-1], lab[-1], k, va="center", fontsize=10.5)
        label(ax, 1.88, Tb[0], lab[0], k, va="center", ha="right", fontsize=10.5)
    ax.plot([2, 3], [-100, -60.3], color=K.blauw, lw=1.2, ls=":")
    label(ax, 2.05, -112, "verwacht zonder\nwaterstofbruggen", K.blauw, fontsize=10, va="top")
    ax.set_xticks(per)
    ax.set_xticklabels(["2", "3", "4", "5"])
    ax.set_xlim(1.5, 5.6)
    ax.set_ylim(-180, 120)
    ax.set_xlabel("periode van het centrale atoom")
    ax.set_ylabel("normaal kookpunt (°C)")
    return kader(fig)


def kookpunt_alkanen():
    """Kookpunt van n-alkanen C1-C10 en de edelgassen tegen het aantal elektronen (CRC)."""
    fig, ax = figuur(6.6, 4.4)
    n = np.arange(1, 11)
    Tb = [-161.5, -88.6, -42.1, -0.5, 36.1, 68.7, 98.4, 125.6, 150.8, 174.1]
    e = 8 * n + 2  # elektronen in CnH2n+2
    ax.plot(e, Tb, "o-", color=K.accent, lw=2, ms=6)
    for i in [0, 3, 4, 9]:
        label(ax, e[i] - 2, Tb[i] + 9, f"C$_{{{n[i]}}}$", K.accent, ha="right", fontsize=10.5)
    edel = [("He", 2, -268.9), ("Ne", 10, -246.1), ("Ar", 18, -185.8), ("Kr", 36, -153.2), ("Xe", 54, -108.1),
            ("Rn", 86, -61.7)]
    ax.plot([d[1] for d in edel], [d[2] for d in edel], "s-", color=K.oker, lw=2, ms=6)
    for nm, x, y in edel:
        label(ax, x + 2, y - 4, nm, K.oker, va="top", fontsize=10.5)
    label(ax, 68, 85, "n-alkanen", K.accent, fontsize=12)
    label(ax, 62, -150, "edelgassen", K.oker, fontsize=12)
    ax.axhline(20, color=K.zacht, lw=0.8, ls=":")
    label(ax, 88, 26, "kamertemperatuur", K.zacht, fontsize=10, ha="right")
    ax.set_xlim(0, 90)
    ax.set_ylim(-290, 200)
    ax.set_xlabel("aantal elektronen per molecule")
    ax.set_ylabel("normaal kookpunt (°C)")
    return kader(fig)


def trouton():
    """ΔHvap tegen Tb: regel van Trouton (≈ 87 J/(mol K)) en afwijkingen door H-bruggen."""
    fig, ax = figuur(6.4, 4.5)
    data = [("N$_2$", 77.4, 5.6), ("CH$_4$", 111.7, 8.2), ("Ar", 87.3, 6.4), ("CCl$_4$", 349.8, 29.8),
            ("benzeen", 353.2, 30.7), ("CHCl$_3$", 334.3, 29.4), ("hexaan", 341.9, 28.9),
            ("NH$_3$", 239.8, 23.4), ("ethanol", 351.5, 38.6), ("H$_2$O", 373.15, 40.7)]
    T = np.linspace(0, 420, 10)
    ax.fill_between(T, 85 * T / 1000, 88 * T / 1000, color=K.vlak_accent, lw=0)
    ax.plot(T, 87 * T / 1000, color=K.accent, lw=1.5, ls="--")
    label(ax, 175, 8, r"Trouton: $\Delta S_\mathrm{vap} \approx 87$ J mol$^{-1}$ K$^{-1}$", K.accent,
          fontsize=11, rotation=0)
    hb = {"NH$_3$", "ethanol", "H$_2$O"}
    for nm, Tb, dH in data:
        k = K.blauw if nm in hb else K.tekst
        ax.plot(Tb, dH, "o", color=k, ms=7, zorder=5)
        dx, ha = {"hexaan": (0, "center"), "CHCl$_3$": (-8, "right")}.get(nm, (8, "left"))
        dy = {"benzeen": 1.6, "CCl$_4$": -0.4, "hexaan": -2.6, "CHCl$_3$": 0.8}.get(nm, 0)
        label(ax, Tb + dx, dH + dy, nm, k, fontsize=10.5, ha=ha, va="center")
    label(ax, 20, 39, "waterstofbruggen:\nboven de lijn", K.blauw, fontsize=11)
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 46)
    ax.set_xlabel("normaal kookpunt $T_b$ (K)")
    ax.set_ylabel(r"$\Delta H_\mathrm{vap}$ (kJ/mol)")
    return kader(fig)
