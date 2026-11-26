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


def dG_temperatuur():
    """ΔG° = ΔH° − TΔS° voor de vier tekencombinaties (reële reacties)."""
    fig, ax = figuur(6.8, 4.8)
    T = np.linspace(0, 1400, 200)
    gevallen = [  # dH (kJ), dS (J/K), label, kleur, x-positie label
        (-196, 125, "2 H$_2$O$_2$ → 2 H$_2$O + O$_2$\n$\\Delta H<0,\\ \\Delta S>0$: altijd", K.groen, 1000),
        (285, -137, "3 O$_2$ → 2 O$_3$\n$\\Delta H>0,\\ \\Delta S<0$: nooit", K.rood, 300),
        (-92, -199, "N$_2$ + 3 H$_2$ → 2 NH$_3$\n$\\Delta H<0,\\ \\Delta S<0$: onder 460 K", K.blauw, 1000),
        (178, 161, "CaCO$_3$ → CaO + CO$_2$\n$\\Delta H>0,\\ \\Delta S>0$: boven 1100 K", K.oker, 150),
    ]
    ax.axhspan(-500, 0, color=K.vlak_groen, lw=0, zorder=0)
    ax.axhline(0, color=K.as_, lw=1)
    for dH, dS, t, k, xl in gevallen:
        G = dH - T * dS / 1000
        ax.plot(T, G, color=k, lw=2.4)
        if dH * dS > 0:
            Ts = dH * 1000 / dS
            ax.plot(Ts, 0, "o", color=k, ms=7, zorder=5)
    label(ax, 1380, -150, gevallen[0][2], K.groen, ha="right", va="center", fontsize=10.5)
    label(ax, 30, 420, gevallen[1][2], K.rood, ha="left", va="center", fontsize=10.5)
    label(ax, 1380, 265, gevallen[2][2], K.blauw, ha="right", va="center", fontsize=10.5)
    label(ax, 30, 245, gevallen[3][2], K.oker, ha="left", va="center", fontsize=10.5)
    label(ax, 30, -430, "spontaan: $\\Delta G^\\circ < 0$", K.groen, fontsize=11.5)
    ax.set_xlim(0, 1400)
    ax.set_ylim(-480, 520)
    ax.set_xlabel("temperatuur $T$ (K)")
    ax.set_ylabel("$\\Delta_r G^\\circ = \\Delta_r H^\\circ - T\\Delta_r S^\\circ$ (kJ/mol)")
    return kader(fig)


def microtoestanden():
    """Aantal microtoestanden Ω(n links) voor N = 4 en N = 1000 moleculen in twee helften."""
    from math import comb, lgamma
    import matplotlib.pyplot as plt
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.6))
    fig.get_layout_engine().set(w_pad=0.18, h_pad=0.18)
    n = np.arange(5)
    a1.bar(n, [comb(4, int(k)) for k in n], color=K.accent, width=0.6)
    for k in n:
        a1.text(k, comb(4, int(k)) + 0.15, str(comb(4, int(k))), ha="center", color=K.tekst, fontsize=11)
    a1.set_xticks(n)
    a1.set_ylim(0, 7.2)
    a1.set_xlabel("aantal moleculen links")
    a1.set_ylabel(r"aantal microtoestanden $\Omega$")
    a1.set_title("$N = 4$: alles links kans 1/16", color=K.tekst, fontsize=12)
    N = 1000
    x = np.arange(N + 1)
    lnW = np.array([lgamma(N + 1) - lgamma(k + 1) - lgamma(N - k + 1) for k in x])
    p = np.exp(lnW - lnW.max())
    a2.fill_between(x / N, p, color=K.vlak_accent, lw=0)
    a2.plot(x / N, p, color=K.accent, lw=2)
    a2.set_xlim(0, 1)
    a2.set_ylim(0, 1.15)
    a2.set_yticks([])
    a2.set_xlabel("fractie moleculen links")
    a2.set_ylabel(r"$\Omega$ / $\Omega_\mathrm{max}$")
    a2.set_title("$N = 1000$: alles links kans $10^{-301}$", color=K.tekst, fontsize=12)
    return kader(fig)


def carnotfactor():
    """Exergie van warmte: 1 - T0/T bij T0 = 293 K."""
    fig, ax = figuur(6.4, 4.3)
    T0 = 293.15
    tc = np.linspace(20, 600, 300)
    f = 1 - T0 / (tc + 273.15)
    ax.fill_between(tc, f, color=K.vlak_accent, lw=0)
    ax.plot(tc, f, color=K.accent, lw=2.4)
    pos = {80: (95, 0.05, "left", "bottom"), 180: (170, 0.39, "right", "bottom"), 400: (390, 0.6, "right", "bottom")}
    for t, naam, k in [(80, "restwarmte 80 °C", K.blauw), (180, "stoom 180 °C", K.oker),
                       (400, "stoom 400 °C", K.rood)]:
        v = 1 - T0 / (t + 273.15)
        ax.plot(t, v, "o", color=k, ms=7, zorder=5)
        x, y, ha, va = pos[t]
        label(ax, x, y, f"{naam}: {v:.2f}", k, fontsize=10.5, ha=ha, va=va)
    label(ax, 470, 0.15, "bruikbaar als arbeid\n(exergie)", K.accent, fontsize=11, ha="center")
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 0.8)
    ax.set_xlabel("temperatuur van de warmte (°C)")
    ax.set_ylabel(r"$W_\mathrm{max}/Q = 1 - T_0/T$")
    return kader(fig)
