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


def expansie_cellen():
    """Isotherme expansie: met het dubbele volume heeft elke molecule twee keer zoveel plaatsen."""
    import matplotlib.pyplot as plt
    fig, ax = figuur(8.0, 3.4)
    schema(fig, ax)

    def vat(x0, nx, kleur, titel, posities):
        for i in range(nx):
            for j in range(4):
                ax.add_patch(plt.Rectangle((x0 + i * 0.5, j * 0.5), 0.5, 0.5, fc="none", ec=K.zacht, lw=0.6))
        ax.add_patch(plt.Rectangle((x0, 0), nx * 0.5, 2.0, fc="none", ec=K.as_, lw=1.8))
        for (i, j) in posities:
            ax.add_patch(plt.Circle((x0 + i * 0.5 + 0.25, j * 0.5 + 0.25), 0.15, fc=kleur, ec="none"))
        label(ax, x0 + nx * 0.25, 2.2, titel, K.tekst, ha="center", va="bottom", fontsize=11)

    vat(0.0, 4, K.blauw, "volume $V_1$: 16 cellen", [(0, 3), (2, 1), (3, 2)])
    vat(3.6, 8, K.rood, "volume $V_2 = 2V_1$: 32 cellen", [(1, 0), (4, 3), (6, 1)])
    pijl(ax, (2.2, 1.0), (3.4, 1.0), K.tekst, lw=1.8)
    label(ax, 1.0, -0.3, r"3 moleculen: $16^3 = 4096$ schikkingen", K.blauw, ha="center", va="top", fontsize=10.5)
    label(ax, 5.6, -0.3, r"3 moleculen: $32^3 = 32\,768$ schikkingen ($\times 2^3$)", K.rood, ha="center",
          va="top", fontsize=10.5)
    label(ax, 3.8, -0.95, r"algemeen: $\Omega \propto (V/v_0)^N$, dus $\Omega_2/\Omega_1 = (V_2/V_1)^N$",
          K.tekst, ha="center", va="top", fontsize=11)
    ax.set_xlim(-0.2, 7.8)
    ax.set_ylim(-1.5, 2.7)
    return kader(fig)


def menging_rooster():
    """Mengen op een rooster: 8 A en 8 B, eerst gescheiden (1 schikking), daarna gemengd (12 870 schikkingen)."""
    import matplotlib.pyplot as plt
    fig, ax = figuur(8.0, 3.4)
    schema(fig, ax)
    rng = np.random.default_rng(3)

    def rooster(x0, kleuren, titel):
        for idx, k in enumerate(kleuren):
            i, j = idx % 4, idx // 4
            ax.add_patch(plt.Rectangle((x0 + i * 0.5, j * 0.5), 0.5, 0.5, fc="none", ec=K.zacht, lw=0.6))
            ax.add_patch(plt.Circle((x0 + i * 0.5 + 0.25, j * 0.5 + 0.25), 0.17, fc=k, ec="none"))
        ax.add_patch(plt.Rectangle((x0, 0), 2.0, 2.0, fc="none", ec=K.as_, lw=1.8))
        label(ax, x0 + 1.0, 2.2, titel, K.tekst, ha="center", va="bottom", fontsize=11)

    voor = [K.blauw if (idx % 4) < 2 else K.oker for idx in range(16)]
    na = [K.blauw] * 8 + [K.oker] * 8
    rng.shuffle(na)
    rooster(0.4, voor, "voor: A links, B rechts")
    ax.plot([1.4, 1.4], [0, 2.0], color=K.as_, lw=2.2)
    rooster(4.4, na, "na: willekeurig gemengd")
    pijl(ax, (2.7, 1.0), (4.1, 1.0), K.tekst, lw=1.8)
    label(ax, 1.4, -0.3, r"$\Omega = 1$", K.tekst, ha="center", va="top", fontsize=11.5)
    label(ax, 5.4, -0.3, r"$\Omega = \dfrac{16!}{8!\,8!} = 12\,870$", K.tekst, ha="center", va="top", fontsize=11.5)
    label(ax, 6.7, 1.45, "A", K.blauw, fontsize=12, fontweight="bold")
    label(ax, 6.7, 0.95, "B", K.oker, fontsize=12, fontweight="bold")
    ax.set_xlim(0.2, 7.2)
    ax.set_ylim(-1.3, 2.7)
    return kader(fig)


def warmtestroom_entropie():
    """1 kJ warmte van koffie (80 °C) naar de kamer (20 °C): entropiebalans."""
    import matplotlib.pyplot as plt
    fig, ax = figuur(7.4, 3.2)
    schema(fig, ax)
    ax.add_patch(plt.Rectangle((0.0, 0.3), 2.4, 1.6, fc=K.vlak_rood, ec=K.rood, lw=1.8))
    ax.add_patch(plt.Rectangle((5.0, 0.3), 2.4, 1.6, fc=K.vlak_blauw, ec=K.blauw, lw=1.8))
    label(ax, 1.2, 1.35, "koffie\n$T_\\mathrm{h}$ = 353 K", K.rood, ha="center", va="center", fontsize=11)
    label(ax, 6.2, 1.35, "kamer\n$T_\\mathrm{c}$ = 293 K", K.blauw, ha="center", va="center", fontsize=11)
    pijl(ax, (2.5, 1.1), (4.9, 1.1), K.oker, lw=3)
    label(ax, 3.7, 1.25, r"$q$ = 1000 J", K.oker, ha="center", va="bottom", fontsize=11.5)
    label(ax, 1.2, 0.6, r"$\Delta S = -\dfrac{1000}{353} = -2.83$ J/K", K.rood, ha="center", va="center",
          fontsize=10)
    label(ax, 6.2, 0.6, r"$\Delta S = +\dfrac{1000}{293} = +3.41$ J/K", K.blauw, ha="center", va="center",
          fontsize=10)
    label(ax, 3.7, -0.15, r"totaal: $\Delta S_\mathrm{univ} = +0.58$ J/K $> 0$: spontaan", K.tekst,
          ha="center", va="top", fontsize=11.5)
    label(ax, 3.7, -0.65, "omgekeerd (kamer → koffie) zou −0.58 J/K geven: onmogelijk", K.zacht,
          ha="center", va="top", fontsize=10.5)
    ax.set_xlim(-0.1, 7.5)
    ax.set_ylim(-1.0, 2.1)
    return kader(fig)


def entropiebalans_water():
    """Entropiebalans voor 2 H2 + O2 -> 2 H2O(l) bij 298 K: systeem, omgeving, universum."""
    fig, ax = figuur(6.4, 4.0)
    namen = ["systeem\n(de reactie)", "omgeving\n(ontvangt de warmte)", "universum\n(som)"]
    waarden = [-326.6, 1917, 1590]
    kleuren = [K.blauw, K.rood, K.accent]
    ax.bar(range(3), waarden, color=kleuren, width=0.55)
    ax.axhline(0, color=K.as_, lw=1)
    for i, v in enumerate(waarden):
        label(ax, i, v + (60 if v > 0 else -60), f"{v:+.0f}", kleuren[i], ha="center",
              va="bottom" if v > 0 else "top", fontsize=11.5)
    ax.set_xticks(range(3))
    ax.set_xticklabels(namen)
    ax.set_ylabel(r"$\Delta S$ (J K$^{-1}$, per 2 mol H$_2$O)")
    ax.set_ylim(-600, 2250)
    return kader(fig)


def vrije_expansie():
    """Proef van Joule (vrije expansie): twee koperen vaten in een waterbad, één gevuld, één vacuüm."""
    import matplotlib.pyplot as plt
    fig, ax = figuur(7.0, 3.6)
    schema(fig, ax)
    ax.add_patch(plt.Rectangle((0.2, 0.2), 6.6, 2.6, fc=K.vlak_blauw, ec=K.as_, lw=1.6))
    label(ax, 3.5, 0.05, "waterbad", K.blauw, ha="center", va="top", fontsize=10.5)
    rng = np.random.default_rng(7)
    for xc, gevuld, tekst in [(1.7, True, "gas, 22 bar"), (5.3, False, "vacuüm")]:
        ax.add_patch(plt.Circle((xc, 1.5), 0.95, fc=K.achtergrond, ec=K.oker, lw=2.2))
        if gevuld:
            for x, y in zip(rng.uniform(-0.6, 0.6, 40), rng.uniform(-0.6, 0.6, 40)):
                if x * x + y * y < 0.62:
                    ax.add_patch(plt.Circle((xc + x, 1.5 + y), 0.04, fc=K.rood, ec="none"))
        label(ax, xc, 2.62, tekst, K.tekst, ha="center", va="bottom", fontsize=10.5,
              bbox=achter(fc=K.vlak_blauw))
    ax.add_patch(plt.Rectangle((2.65, 1.42), 1.7, 0.16, fc=K.oker, ec="none"))
    ax.add_patch(plt.Circle((3.5, 1.5), 0.17, fc=K.achtergrond, ec=K.as_, lw=1.6))
    ax.plot([3.38, 3.62], [1.38, 1.62], color=K.as_, lw=1.6)
    label(ax, 3.5, 1.15, "kraan", K.tekst, ha="center", va="top", fontsize=10)
    ax.add_patch(plt.Rectangle((6.3, 0.5), 0.12, 2.8, fc=K.achtergrond, ec=K.as_, lw=1.2))
    ax.add_patch(plt.Rectangle((6.32, 0.5), 0.08, 1.3, fc=K.rood, ec="none"))
    label(ax, 6.36, 3.38, "thermometer", K.tekst, ha="center", va="bottom", fontsize=10)
    label(ax, 7.1, 1.5, "kraan open:\ngas vult beide vaten,\n$T$ van het bad\nverandert niet", K.tekst,
          va="center", fontsize=10.5)
    ax.set_xlim(0.0, 9.3)
    ax.set_ylim(-0.3, 3.8)
    return kader(fig)
