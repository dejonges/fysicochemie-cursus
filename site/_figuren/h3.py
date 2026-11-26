"""Figuren hoofdstuk 3 – Spontaniteit."""
import numpy as np

from huisstijl import K, figuur, kader, label  # noqa: F401


def entropie_opwarming_water():
    """Molaire entropie van water van ijs bij -10 °C tot stoom bij 120 °C (1 bar)."""
    fig, ax = figuur(6.4, 4.4)
    Cp_ijs, Cp_w, Cp_st = 38.0, 75.3, 33.6
    dSf, dSv = 6010 / 273.15, 40700 / 373.15
    T1 = np.linspace(263.15, 273.15, 50)
    T2 = np.linspace(273.15, 373.15, 200)
    T3 = np.linspace(373.15, 393.15, 50)
    S1 = Cp_ijs * np.log(T1 / 263.15)
    S2 = S1[-1] + dSf + Cp_w * np.log(T2 / 273.15)
    S3 = S2[-1] + dSv + Cp_st * np.log(T3 / 373.15)
    for T, S, k in [(T1, S1, K.blauw), (T2, S2, K.accent), (T3, S3, K.rood)]:
        ax.plot(T - 273.15, S, color=k, lw=2.6)
    ax.plot([0, 0], [S1[-1], S2[0]], color=K.oker, lw=1.6, ls=(0, (4, 3)))
    ax.plot([100, 100], [S2[-1], S3[0]], color=K.oker, lw=1.6, ls=(0, (4, 3)))
    label(ax, 3, 10, f"smelten: +{dSf:.0f} J/(mol K)", K.oker, fontsize=10.5)
    label(ax, 97, 105, f"verdampen:\n+{dSv:.0f} J/(mol K)", K.oker, fontsize=10.5, ha="right")
    label(ax, -8, 8, "ijs", K.blauw, fontsize=11)
    label(ax, 45, 52, "vloeibaar water", K.accent, fontsize=11)
    label(ax, 104, 165, "stoom", K.rood, fontsize=11)
    label(ax, 104, S3[-1] - 24, f"totaal\n{S3[-1]:.0f} J/(mol K)", K.zacht, fontsize=10)
    ax.set_xlim(-12, 125)
    ax.set_ylim(0, 175)
    ax.set_xlabel("temperatuur (°C)")
    ax.set_ylabel("$S - S$(−10 °C) (J mol$^{-1}$ K$^{-1}$)")
    return kader(fig)
