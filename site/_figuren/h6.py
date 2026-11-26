"""Figuren hoofdstuk 6 – Reagerend evenwicht."""
import numpy as np
from matplotlib.patches import FancyBboxPatch

from huisstijl import K, figuur, kader, label, pijl  # noqa: F401

R = 8.314
# SO2 + 1/2 O2 <-> SO3 ; standaardwaarden bij 298 K (NIST), constant verondersteld
_DH, _DS = -98.9e3, -94.0
_Y0 = dict(SO2=0.10, O2=0.11, N2=0.79)
_CP = 32.0  # J/(mol K), gemiddeld voor het gasmengsel
_DTAD = _Y0["SO2"] * -_DH / _CP  # adiabatische temperatuurstijging bij X = 1


def _X_eq(T, P=1.0):
    Kp = np.exp(-(_DH - T * _DS) / (R * T))
    lo, hi = 0.0, 0.999999
    for _ in range(60):
        X = (lo + hi) / 2
        f = X / (1 - X) * np.sqrt((1 - 0.05 * X) / (0.11 - 0.05 * X)) - Kp * np.sqrt(P)
        lo, hi = (X, hi) if f < 0 else (lo, X)
    return X


def _bed(T_in, X_in):
    """Snijpunt van de adiabatische lijn T = T_in + DTAD (X - X_in) met de evenwichtscurve, tot 95 %."""
    Xs = np.linspace(X_in, 1, 2000)
    Ts = T_in + _DTAD * (Xs - X_in)
    Xe = np.array([_X_eq(t) for t in Ts])
    i = np.argmax(Xs >= Xe)
    X_uit = X_in + 0.95 * (Xs[i] - X_in)
    return X_uit, T_in + _DTAD * (X_uit - X_in)


def so2_bedden():
    """Evenwichtsomzetting SO2 -> SO3 en drie adiabatische bedden met tussenkoeling."""
    fig, ax = figuur(6.6, 4.7)
    T = np.linspace(380, 700, 200) + 273.15
    ax.plot(T - 273.15, [_X_eq(t) for t in T], color=K.blauw, lw=2.6)
    label(ax, 640, 0.42, "evenwicht\n(1 bar)", K.blauw, fontsize=11)
    X, T_in = 0.0, 420 + 273.15
    for n in range(3):
        X_uit, T_uit = _bed(T_in, X)
        ax.plot([T_in - 273.15, T_uit - 273.15], [X, X_uit], color=K.rood, lw=2.2)
        label(ax, (T_in + T_uit) / 2 - 273.15 - 8, (X + X_uit) / 2, f"bed {n + 1}", K.rood, fontsize=10.5, ha="right")
        T_nieuw = 430 + 273.15
        if n < 2:
            ax.plot([T_uit - 273.15, T_nieuw - 273.15], [X_uit, X_uit], color=K.accent, lw=1.6, ls=(0, (4, 3)))
        X, T_in = X_uit, T_nieuw
    label(ax, 525, 0.57, "tussenkoeling", K.accent, fontsize=10.5)
    ax.set_xlim(380, 700)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("temperatuur (°C)")
    ax.set_ylabel("omzetting $X_{\\mathrm{SO_2}}$")
    return kader(fig)


def haber_bosch_schema():
    """Vereenvoudigd blokschema van de Haber-Boschlus met recycle en purge."""
    fig, ax = figuur(7.2, 3.6)
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 5)
    ax.axis("off")

    def blok(x, y, b, h, tekst, k):
        ax.add_patch(FancyBboxPatch((x, y), b, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                                    fc=K.vlak_blauw, ec=k, lw=1.6))
        label(ax, x + b / 2, y + h / 2, tekst, k, ha="center", va="center", fontsize=10.5)

    blok(1.6, 2.3, 1.4, 1.0, "menger +\ncompressor", K.tekst)
    blok(4.0, 2.1, 1.7, 1.4, "reactor\nFe-katalysator\n450 °C, 200 bar", K.rood)
    blok(6.7, 2.3, 1.6, 1.0, "koeler +\nscheider", K.blauw)
    pijl(ax, (0.2, 2.8), (1.6, 2.8))
    label(ax, 0.2, 3.0, "N$_2$ + 3 H$_2$", K.tekst, fontsize=10.5)
    pijl(ax, (3.05, 2.8), (4.0, 2.8))
    pijl(ax, (5.75, 2.8), (6.7, 2.8))
    pijl(ax, (7.5, 2.25), (7.5, 0.9))
    label(ax, 7.65, 1.0, "vloeibaar NH$_3$", K.blauw, fontsize=10.5)
    # recycle
    ax.plot([8.35, 9.2, 9.2, 2.3], [2.8, 2.8, 4.4, 4.4], color=K.accent, lw=1.6)
    pijl(ax, (2.3, 4.4), (2.3, 3.35), K.accent)
    label(ax, 5.0, 4.55, "recycle: niet-omgezet N$_2$ + H$_2$ (± 75 %)", K.accent, fontsize=10.5, ha="center")
    pijl(ax, (9.2, 3.6), (9.85, 3.6), K.oker)
    label(ax, 9.95, 3.6, "purge\n(Ar, CH$_4$)", K.oker, fontsize=9.5, va="center")
    return kader(fig)


def g_reactiecoordinaat():
    """G van een ideaal gasmengsel A <-> B in functie van de reactiecoördinaat."""
    fig, ax = figuur(6.4, 4.2)
    T, dG0 = 298.15, -3000.0
    xi = np.linspace(1e-4, 1 - 1e-4, 400)
    zonder = xi * dG0
    G = zonder + R * T * ((1 - xi) * np.log(1 - xi) + xi * np.log(xi))
    G, zonder = G / 1e3, zonder / 1e3
    ax.plot(xi, zonder, color=K.zacht, lw=1.3, ls=(0, (4, 3)))
    ax.plot(xi, G, color=K.accent, lw=2.6)
    i = np.argmin(G)
    ax.plot(xi[i], G[i], "o", color=K.accent, ms=7)
    ax.plot([xi[i] - 0.12, xi[i] + 0.12], [G[i], G[i]], color=K.oker, lw=1.4)
    label(ax, xi[i], G[i] - 0.28, f"evenwicht $\\xi_\\mathrm{{eq}}$ = {xi[i]:.2f}\n$\\Delta_rG = 0$",
          K.oker, fontsize=10.5, ha="center", va="top")
    pijl(ax, (0.25, -1.15), (0.40, -1.85), K.accent, 1.4)
    label(ax, 0.06, -1.55, "$\\Delta_rG < 0$:\nreactie loopt\nnaar rechts", K.accent, fontsize=10)
    pijl(ax, (0.985, -3.35), (0.90, -3.72), K.rood, 1.4)
    label(ax, 0.995, -2.15, "$\\Delta_rG > 0$:\nterugreactie", K.rood, fontsize=10, ha="right")
    label(ax, 0.30, -0.35, "zonder menging (rechte)", K.zacht, fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(-4.7, 0.3)
    ax.set_xlabel("reactiecoördinaat $\\xi$ (mol)")
    ax.set_ylabel("$G - G_\\mathrm{reagentia}$ (kJ)")
    return kader(fig)


def vanthoff_ammoniak():
    """Van 't Hoff-diagram voor N2 + 3 H2 <-> 2 NH3 met constante reactie-enthalpie."""
    fig, ax = figuur(6.4, 4.2)
    dH, lnK1, T1 = -92e3, np.log(6e5), 298.15
    x = np.linspace(1 / 800, 1 / 280, 50)
    lnK = lnK1 - dH / R * (x - 1 / T1)
    ax.plot(x * 1e3, lnK, color=K.accent, lw=2.4)
    for T in (298.15, 700.0):
        y = lnK1 - dH / R * (1 / T - 1 / T1)
        ax.plot(1e3 / T, y, "o", color=K.rood, ms=7)
        dx, ha = (0.07, "left") if T > 500 else (-0.07, "right")
        label(ax, 1e3 / T + dx, y, f"{T:.0f} K: $\\ln K$ = {y:.1f}", K.rood, fontsize=10.5, va="center", ha=ha)
    ax.axhline(0, color=K.zacht, lw=0.8)
    label(ax, 2.35, -6, "helling $-\\Delta_rH^\\circ/R$ = +11 070 K\n(exotherm: $K$ daalt bij hogere $T$)",
          K.accent, fontsize=10.5)
    ax.set_xlim(1.25, 3.6)
    ax.set_ylim(-12, 16)
    ax.set_xlabel("$1000/T$ (K$^{-1}$)")
    ax.set_ylabel("$\\ln K$")
    return kader(fig)


def nh3_druk():
    """Evenwichtsmolfractie NH3 bij 700 K in functie van de druk (stoichiometrische voeding)."""
    fig, ax = figuur(6.4, 4.2)
    Kp = 3e-4

    def y(P):
        lo, hi = 0.0, 0.999999
        for _ in range(60):
            xi = (lo + hi) / 2
            n = 4 - 2 * xi
            f = (2 * xi / n) ** 2 / ((1 - xi) / n * (3 * (1 - xi) / n) ** 3) / P**2 - Kp
            lo, hi = (xi, hi) if f < 0 else (lo, xi)
        return 2 * xi / (4 - 2 * xi)

    P = np.linspace(1, 320, 300)
    ax.axvspan(150, 300, color=K.vlak_accent, lw=0)
    label(ax, 225, 5, "industrieel\n150–300 bar", K.accent, fontsize=10, ha="center")
    ax.plot(P, [100 * y(p) for p in P], color=K.blauw, lw=2.4)
    Pt = [1, 10, 50, 100, 200, 300]
    ax.plot(Pt, [100 * y(p) for p in Pt], "o", color=K.blauw, ms=6)
    label(ax, 20, 44, "700 K, N$_2$ : H$_2$ = 1 : 3\n$K_p \\approx 3\\times10^{-4}$", K.zacht, fontsize=10.5)
    ax.set_xlim(0, 320)
    ax.set_ylim(0, 55)
    ax.set_xlabel("totale druk $P$ (bar)")
    ax.set_ylabel("$y_\\mathrm{NH_3}$ bij evenwicht (%)")
    return kader(fig)


def K_temperatuur():
    """log10 K tegen T voor vijf industriële reacties (ΔH° en ΔS° bij 298 K constant verondersteld)."""
    fig, ax = figuur(6.6, 4.4)
    reacties = [  # naam, ΔH (kJ/mol), ΔS (J/mol K), kleur, exo/endo
        ("N$_2$ + 3 H$_2$ → 2 NH$_3$", -92.2, -198.7, K.blauw),
        ("2 SO$_2$ + O$_2$ → 2 SO$_3$", -197.8, -188.0, K.paars),
        ("CO + H$_2$O → CO$_2$ + H$_2$", -41.2, -42.1, K.groen),
        ("CH$_4$ + H$_2$O → CO + 3 H$_2$", 206.1, 214.6, K.rood),
        ("CaCO$_3$ → CaO + CO$_2$", 178.3, 160.6, K.oker),
    ]
    T = np.linspace(298, 1300, 300)
    for nm, dH, dS, k in reacties:
        logK = (-(dH * 1e3) / (R * T) + dS / R) / np.log(10)
        ax.plot(T - 273.15, logK, color=k, lw=2.3, label=nm, ls="-" if dH < 0 else "--")
        Tx = dH * 1e3 / dS
        if 298 < Tx < 1300:
            ax.plot(Tx - 273.15, 0, "o", color=k, ms=6, zorder=5)
    ax.axhline(0, color=K.as_, lw=1)
    label(ax, 420, -12, "volle lijn: exotherm, $K$ daalt\nstreepjes: endotherm, $K$ stijgt", K.zacht, fontsize=10)
    ax.legend(loc="upper right", fontsize=9.5)
    ax.set_xlim(25, 1030)
    ax.set_ylim(-15, 25)
    ax.set_xlabel("temperatuur (°C)")
    ax.set_ylabel("$\\log_{10} K$")
    return kader(fig)
