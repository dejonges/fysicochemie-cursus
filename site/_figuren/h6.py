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
