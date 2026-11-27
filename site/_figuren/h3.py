"""Figuren hoofdstuk 3 – Spontaniteit."""
import numpy as np

from huisstijl import K, figuur, kader, label, pijl, schema, achter  # noqa: F401


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


# ================================================================ CASE: DE WARMTEPOMP
def warmtepomp_schema():
    """Kringloop van een warmtepomp: verdamper buiten, compressor, condensor binnen, expansieventiel."""
    import matplotlib.pyplot as plt
    fig, ax = figuur(7.6, 4.6)
    schema(fig, ax)
    # zones
    ax.add_patch(plt.Rectangle((-0.2, -0.3), 3.2, 4.6, fc=K.vlak_blauw, ec="none", zorder=0))
    ax.add_patch(plt.Rectangle((5.0, -0.3), 3.2, 4.6, fc=K.vlak_rood, ec="none", zorder=0))
    label(ax, 1.4, 4.05, "buiten, 5 °C", K.blauw, ha="center", fontsize=12)
    label(ax, 6.6, 4.05, "woning, 20 °C", K.rood, ha="center", fontsize=12)
    # toestellen
    def blok(x, y, w, h, tekst, k, fc):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=k, lw=1.8, zorder=2))
        label(ax, x + w / 2, y + h / 2, tekst, k, ha="center", va="center", fontsize=10.5, zorder=3)
    blok(1.9, 0.9, 1.0, 1.6, "verdamper\n−5 °C", K.blauw, K.achtergrond)
    blok(5.1, 0.9, 1.0, 1.6, "condensor\n35 °C", K.rood, K.achtergrond)
    blok(3.55, 2.95, 0.9, 0.6, "compressor", K.paars, K.achtergrond)
    blok(3.6, -0.05, 0.8, 0.5, "ventiel", K.oker, K.achtergrond)
    # leidingen
    k = K.zacht
    ax.plot([2.4, 2.4, 3.55], [2.5, 3.25, 3.25], color=k, lw=2)
    ax.plot([4.45, 5.6, 5.6], [3.25, 3.25, 2.5], color=k, lw=2)
    ax.plot([5.6, 5.6, 4.4], [0.9, 0.2, 0.2], color=k, lw=2)
    ax.plot([3.6, 2.4, 2.4], [0.2, 0.2, 0.9], color=k, lw=2)
    for xy0, xy1 in [((2.4, 2.9), (2.4, 3.15)), ((5.6, 2.9), (5.6, 2.6)), ((5.0, 0.2), (4.7, 0.2)),
                     ((3.2, 0.2), (2.9, 0.2))]:
        pijl(ax, xy0, xy1, k, lw=2)
    label(ax, 2.95, 3.35, "damp", K.zacht, ha="center", va="bottom", fontsize=9.5)
    label(ax, 5.05, 3.35, "hete damp", K.zacht, ha="center", va="bottom", fontsize=9.5)
    label(ax, 4.95, 0.3, "vloeistof", K.zacht, ha="center", va="bottom", fontsize=9.5)
    label(ax, 3.05, 0.3, "koude\nnevel", K.zacht, ha="center", va="bottom", fontsize=9.5)
    # energiestromen
    pijl(ax, (0.3, 1.7), (1.85, 1.7), K.blauw, lw=3)
    label(ax, 1.05, 1.85, r"$Q_\mathrm{c}$", K.blauw, ha="center", va="bottom", fontsize=13)
    label(ax, 1.05, 1.5, "uit de\nbuitenlucht", K.blauw, ha="center", va="top", fontsize=9.5)
    pijl(ax, (6.15, 1.7), (7.7, 1.7), K.rood, lw=3)
    label(ax, 6.95, 1.85, r"$Q_\mathrm{h}$", K.rood, ha="center", va="bottom", fontsize=13)
    label(ax, 6.95, 1.5, "naar de\nvloerverwarming", K.rood, ha="center", va="top", fontsize=9.5)
    pijl(ax, (4.0, 4.3), (4.0, 3.6), K.paars, lw=3)
    label(ax, 4.12, 4.05, r"$W$ (elektriciteit)", K.paars, va="center", fontsize=11)
    label(ax, 4.0, 1.55, r"$Q_\mathrm{h} = Q_\mathrm{c} + W$", K.tekst, ha="center", fontsize=12)
    ax.set_xlim(-0.3, 8.3)
    ax.set_ylim(-0.4, 4.6)
    return kader(fig)


def twee_blokken():
    """Aantal microtoestanden van twee blokken die 100 energiekwanta delen."""
    from math import comb, log10
    fig, ax = figuur(6.8, 4.4)
    NA, NB, q = 300, 200, 100
    qa = np.arange(q + 1)
    lg = np.array([log10(comb(int(a) + NA - 1, int(a))) + log10(comb(q - int(a) + NB - 1, q - int(a))) for a in qa])
    ax.fill_between(qa, lg, lg.min() - 5, color=K.vlak_accent, lw=0)
    ax.plot(qa, lg, color=K.accent)
    m = int(qa[np.argmax(lg)])
    ax.plot(m, lg.max(), "o", color=K.accent, ms=8, zorder=5)
    label(ax, m, lg.max() + 1.2, f"meest waarschijnlijk: {m} kwanta in A\n(evenveel energie per oscillator)",
          K.accent, ha="center", va="bottom", fontsize=10.5)
    ax.plot(90, lg[90], "o", color=K.rood, ms=8, zorder=5)
    label(ax, 88, lg[90] - 1.5, "start: A heet\n(90 kwanta)", K.rood, ha="right", va="top", fontsize=10.5)
    pijl(ax, (89, lg[90] + 0.8), (66, lg[66] + 0.6), K.rood, lw=1.4, connectionstyle="arc3,rad=0.25")
    label(ax, 79, lg[78] + 2.2, r"$\times 10^{8}$", K.rood, ha="center", fontsize=11)
    ax.set_xlim(0, 100)
    ax.set_ylim(lg[0] - 3, lg.max() + 7)
    ax.set_xlabel("aantal energiekwanta in blok A (van de 100)")
    ax.set_ylabel(r"$\log_{10}\,\Omega_\mathrm{totaal}$")
    label(ax, 2, lg.max() + 5.5, "blok A: 300 oscillatoren, blok B: 200", K.zacht, fontsize=10.5)
    return kader(fig)


def cop_warmtepomp():
    """Maximale COP (Carnot) van een warmtepomp tegenover de afgiftetemperatuur."""
    fig, ax = figuur(6.8, 4.4)
    th = np.linspace(25, 70, 300)
    for tc, k, y in [(7, K.accent, 0), (-7, K.blauw, 0)]:
        cop = (th + 273.15) / (th - tc)
        ax.plot(th, cop, color=k)
        ax.fill_between(th, 0.40 * cop, 0.50 * cop, color=k, alpha=0.18, lw=0)
    label(ax, 70.6, 343.15 / 63, "Carnot,\nbuiten 7 °C", K.accent, fontsize=10, va="center")
    label(ax, 70.6, 343.15 / 77 - 0.5, "Carnot,\nbuiten −7 °C", K.blauw, fontsize=10, va="top")
    label(ax, 26, 0.7, "gekleurde banden: echte toestellen (40 tot 50 % van Carnot)", K.zacht, fontsize=10.5, bbox=achter(), zorder=6)
    for t, naam in [(35, "vloerverwarming"), (55, "radiatoren")]:
        ax.axvline(t, color=K.zacht, lw=1, ls=(0, (3, 3)))
        label(ax, t + 0.5, 13.5, naam, K.zacht, fontsize=10.5)
    ax.set_xlim(25, 80)
    ax.set_xticks(range(25, 75, 5))
    ax.set_ylim(0, 19)
    ax.set_xlabel("afgiftetemperatuur in de woning (°C)")
    ax.set_ylabel(r"COP = $Q_\mathrm{h}/W$")
    return kader(fig)
