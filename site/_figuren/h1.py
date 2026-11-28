"""Figuren hoofdstuk 1 – Energie en de eerste hoofdwet."""
import numpy as np
import matplotlib.pyplot as plt

from huisstijl import K, figuur, kader, label, pijl, achter, toon  # noqa: F401
import toestand as ts

R = ts.R


# --------------------------------------------------------- soorten systemen
def systemen():
    """Open, gesloten, adiabatisch en geïsoleerd systeem: wat steekt de systeemgrens over?"""
    from matplotlib.patches import FancyBboxPatch
    fig, ax = figuur(9.2, 3.2)
    ax.set_axis_off()
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 6)
    titels = ["open", "gesloten", "adiabatisch", "geïsoleerd"]
    voorbeelden = ["bv. reactor, compressor", "bv. zuiger-cilinder", "bv. snelle compressie", "bv. ideale thermosfles"]
    for i, t in enumerate(titels):
        x0 = 0.9 + 5 * i
        ax.add_patch(FancyBboxPatch((x0, 1.4), 3.2, 2.9, boxstyle="round,pad=0.02,rounding_size=0.3",
                                    facecolor=K.vlak_accent, edgecolor=K.accent, lw=3.2 if i >= 2 else 1.6))
        label(ax, x0 + 1.6, 4.75, t, K.accent, ha="center", fontsize=13, fontweight="bold")
        label(ax, x0 + 1.6, 5.45, voorbeelden[i], K.zacht, ha="center", fontsize=9.5)
        label(ax, x0 + 1.6, 2.85, "systeem", K.zacht, ha="center", va="center", fontsize=11)
        if i == 0:  # massa in en uit
            pijl(ax, (x0 - 0.8, 3.6), (x0 + 0.6, 3.6), K.blauw, lw=2)
            pijl(ax, (x0 + 2.6, 3.6), (x0 + 4.0, 3.6), K.blauw, lw=2)
            label(ax, x0 + 1.6, 3.6, "massa", K.blauw, ha="center", va="center", fontsize=11)
        if i < 2:  # warmte
            pijl(ax, (x0 + 0.9, 0.2), (x0 + 0.9, 1.9), K.rood, lw=2)
            label(ax, x0 + 0.75, 0.55, "$Q$", K.rood, ha="right", fontsize=13)
        if i < 3:  # arbeid
            pijl(ax, (x0 + 2.3, 1.9), (x0 + 2.3, 0.2), K.oker, lw=2)
            label(ax, x0 + 2.45, 0.55, "$W$", K.oker, ha="left", fontsize=13)
        if i == 2:
            label(ax, x0 + 1.1, 0.7, "$Q = 0$", K.rood, ha="center", fontsize=11)
        if i == 3:
            label(ax, x0 + 1.6, 0.7, "geen massa, $Q$ of $W$", K.zacht, ha="center", fontsize=10.5)
    return kader(fig)


# ------------------------------------------- toestandsfunctie vs. padfunctie
def padfunctie():
    """Twee wegen tussen dezelfde toestanden: zelfde ΔU, andere arbeid."""
    fig, ax = figuur(6.4, 4.4)
    V1, V2, p1, p2 = 1.0, 4.0, 4.0, 1.0
    # weg A: eerst expansie bij p1, dan afkoelen bij V2; weg B: eerst afkoelen bij V1, dan expansie bij p2
    ax.fill_between([V1, V2], 0, p1, color=K.vlak_rood, lw=0, zorder=0)
    ax.fill_between([V1, V2], 0, p2, color=K.vlak_blauw, lw=0, zorder=0)
    ax.plot([V1, V2, V2], [p1, p1, p2], color=K.rood, lw=2.4)
    ax.plot([V1, V1, V2], [p1, p2, p2], color=K.blauw, lw=2.4)
    pijl(ax, (2.3, p1), (2.6, p1), K.rood, lw=2)
    pijl(ax, (V2, 2.7), (V2, 2.3), K.rood, lw=2)
    pijl(ax, (V1, 2.7), (V1, 2.3), K.blauw, lw=2)
    pijl(ax, (2.3, p2), (2.6, p2), K.blauw, lw=2)
    for (x, y, t) in [(V1, p1, "1"), (V2, p2, "2")]:
        ax.plot(x, y, "o", color=K.tekst, ms=8, zorder=5)
        label(ax, x - 0.12, y + 0.15, t, K.tekst, ha="right", fontsize=14, fontweight="bold")
    label(ax, 2.5, p1 + 0.2, "weg A", K.rood, ha="center", fontsize=12)
    label(ax, 2.5, p2 + 0.2, "weg B", K.blauw, ha="center", fontsize=12)
    label(ax, 2.5, 2.4, "extra arbeid\nlangs weg A", K.rood, ha="center", va="center", fontsize=11)
    label(ax, 2.5, 0.5, "arbeid langs weg B", K.blauw, ha="center", va="center", fontsize=11)
    label(ax, 4.25, 3.3, "$\\Delta U$ is voor beide\nwegen gelijk;\n$W$ en $Q$ niet",
          K.tekst, ha="left", va="center", fontsize=11.5)
    ax.set_xlim(0, 6.2)
    ax.set_ylim(0, 5)
    ax.set_xlabel("volume $V$")
    ax.set_ylabel("druk $p$")
    ax.set_xticks([])
    ax.set_yticks([])
    return kader(fig)


# ------------------------------------------------ arbeid vs. warmte (moleculair)
def arbeid_warmte():
    """Arbeid = geordende duw (zuiger), warmte = ongeordende botsingen (warme wand)."""
    from matplotlib.patches import Rectangle
    rng = np.random.default_rng(4)
    fig, ax = figuur(7.6, 3.4)
    ax.set_axis_off()
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6.6)
    ax.set_aspect("equal")
    # links: zuiger
    ax.add_patch(Rectangle((0.6, 0.6), 6.4, 4.6, facecolor="none", edgecolor=K.as_, lw=1.6))
    ax.add_patch(Rectangle((0.6, 0.6), 1.0, 4.6, facecolor=K.vlak_oker, edgecolor=K.oker, lw=1.6))
    pijl(ax, (-0.4, 2.9), (0.55, 2.9), K.oker, lw=2.4)
    gx, gy = np.meshgrid(np.linspace(2.3, 5.6, 4), np.linspace(1.2, 4.6, 4))
    xs = gx.ravel() + rng.uniform(-0.25, 0.25, 16); ys = gy.ravel() + rng.uniform(-0.2, 0.2, 16)
    for x, y in zip(xs, ys):
        ax.plot(x, y, "o", color=K.accent, ms=6)
        pijl(ax, (x, y), (x + 0.75, y), K.oker, lw=1.3)
    label(ax, 3.8, 5.6, "arbeid: geordend", K.oker, ha="center", fontsize=13, fontweight="bold")
    # rechts: warme wand
    ax.add_patch(Rectangle((8.8, 0.6), 6.4, 4.6, facecolor="none", edgecolor=K.as_, lw=1.6))
    ax.add_patch(Rectangle((8.8, 0.6), 0.5, 4.6, facecolor=K.vlak_rood, edgecolor=K.rood, lw=1.6))
    gx, gy = np.meshgrid(np.linspace(10.3, 14.3, 4), np.linspace(1.4, 4.4, 4))
    xs = gx.ravel() + rng.uniform(-0.25, 0.25, 16); ys = gy.ravel() + rng.uniform(-0.2, 0.2, 16)
    for x, y in zip(xs, ys):
        a = rng.uniform(0, 2 * np.pi); r = rng.uniform(0.45, 0.8)
        ax.plot(x, y, "o", color=K.accent, ms=6)
        pijl(ax, (x, y), (x + r * np.cos(a), y + r * np.sin(a)), K.rood, lw=1.3)
    label(ax, 9.05, 0.15, "warm", K.rood, ha="center", fontsize=10.5)
    label(ax, 12.0, 5.6, "warmte: ongeordend", K.rood, ha="center", fontsize=13, fontweight="bold")
    return kader(fig)


# ---------------------------------------------------------- Cp(T) van gassen
def cp_temperatuur():
    """Cp,m(T) = a + bT + cT^2 voor enkele gassen (tabel cp_coeff)."""
    fig, ax = figuur(6.4, 4.5)
    T = np.linspace(300, 1000, 200)
    data = [("CH$_4$", 14.9, 6.96e-2, -1.23e-5, K.oker),
            ("CO$_2$", 23.9, 5.21e-2, -2.20e-5, K.rood),
            ("H$_2$O(g)", 31.3, 5.99e-3, 4.12e-6, K.blauw),
            ("O$_2$", 25.4, 1.35e-2, -3.95e-6, K.groen),
            ("N$_2$", 28.5, 3.6e-4, 4.00e-6, K.accent),
            ("He", 20.8, 0, 0, K.zacht)]
    for naam, a, b, c, k in data:
        cp = a + b * T + c * T**2
        ax.plot(T, cp, color=k)
        label(ax, 1012, cp[-1], naam, k, va="center", fontsize=11.5)
    ax.axhline(2.5 * R, color=K.zacht, lw=0.8, ls=":")
    label(ax, 310, 2.5 * R + 0.6, r"$\frac{5}{2}R$", K.zacht, fontsize=11)
    ax.set_xlim(300, 1100)
    ax.set_ylim(15, 80)
    ax.set_xlabel("temperatuur $T$ (K)")
    ax.set_ylabel(r"$C_{p,\mathrm{m}}$ (J mol$^{-1}$ K$^{-1}$)")
    return kader(fig)


# ---------------------------------------------- enthalpiediagram (Hess)
def hess():
    """Enthalpieniveaus voor CH4 + 2 O2 -> CO2 + 2 H2O(l)."""
    fig, ax = figuur(6.4, 4.8)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1050, 120)
    niveaus = [(0.6, 3.4, 0, "C(s) + 2 H$_2$(g) + 2 O$_2$(g)\nelementen", K.zacht),
               (0.6, 3.4, -74.8, "CH$_4$(g) + 2 O$_2$(g)", K.blauw),
               (6.0, 9.4, -965.1, "CO$_2$(g) + 2 H$_2$O(l)", K.rood)]
    for x0, x1, h, t, k in niveaus:
        ax.plot([x0, x1], [h, h], color=k, lw=3)
    label(ax, 2.0, 15, "elementen", K.zacht, ha="center", va="bottom", fontsize=11)
    label(ax, 2.0, -95, "CH$_4$ + 2 O$_2$", K.blauw, ha="center", va="top", fontsize=12)
    label(ax, 7.7, -985, "CO$_2$ + 2 H$_2$O(l)", K.rood, ha="center", va="top", fontsize=12)
    ax.plot([3.4, 6.0], [0, 0], color=K.zacht, lw=1, ls=":")
    pijl(ax, (1.2, 0), (1.2, -74.8), K.blauw, lw=1.6)
    label(ax, 1.0, -40, r"$-74.8$", K.blauw, ha="right", va="center", fontsize=11)
    pijl(ax, (7.0, 0), (7.0, -965.1), K.oker, lw=1.6)
    label(ax, 7.2, -480, "$-393.5 + 2(-285.8)$\n$= -965.1$", K.oker, ha="left", va="center", fontsize=11)
    pijl(ax, (3.0, -74.8), (6.3, -965.1), K.accent, lw=2.2)
    label(ax, 4.55, -520, r"$\Delta_r H^\circ$" + "\n" + r"$= -890.3$ kJ/mol", K.accent, ha="right",
          va="center", fontsize=12.5, bbox=achter())
    ax.set_xticks([])
    ax.set_ylabel(r"$H$ t.o.v. de elementen (kJ/mol)")
    ax.spines["bottom"].set_visible(False)
    return kader(fig)


# ------------------------------------------------------------------ Boyle
def _boyle(ax):
    """Isothermen van een ideaal gas (1 mol)."""
    T = [200, 400, 600, 800]
    V = np.linspace(0.3, 6, 400)  # L
    for i, Ti in enumerate(T):
        p = 0.08314 * Ti / V  # bar
        k = K.warmte(i / (len(T) - 1))
        ax.plot(V, p, color=k)
        label(ax, 6.1, p[-1], f"{Ti} K", k, va="center", fontsize=11)
    pijl(ax, (0.9, 12), (2.6, 42), K.tekst, lw=1.4)
    label(ax, 2.7, 42, "stijgende\ntemperatuur", K.tekst, va="bottom", fontsize=11)
    label(ax, 3.4, 52, r"$pV = nRT$   ($n$ = 1 mol)", K.tekst, fontsize=12)
    ax.set_xlim(0, 6.8)
    ax.set_ylim(0, 60)
    ax.set_xlabel(r"volume $V$ (L)")
    ax.set_ylabel(r"druk $p$ (bar)")


def boyle():
    fig, ax = figuur(6.4, 4.6)
    _boyle(ax)
    return kader(fig)


# ------------------------------------------------- CO2-isothermen (reëel gas)
def _isothermen_co2(ax):
    """Isothermen van CO2 met condensatiegebied (Peng-Robinson)."""
    gas = "CO2"
    Tc = ts.GASSEN[gas][0]
    V = np.linspace(4.2e-5, 6.2e-4, 1500)  # m3/mol

    # tweefasengebied (koepel)
    Ts = np.linspace(225, Tc - 0.05, 80)
    sat = [ts.pr_verzadiging(T, gas) for T in Ts]
    Vl = [s[1] for s in sat]
    Vg = [s[2] for s in sat]
    pd = [s[0] for s in sat]
    koepelV = np.r_[Vl, Vg[::-1]] * 1e3
    koepelp = np.r_[pd, pd[::-1]] / 1e5
    ax.fill(koepelV, koepelp, color=K.vlak_blauw, alpha=0.7, lw=0, zorder=0)
    ax.plot(koepelV, koepelp, color=K.zacht, lw=1.2, ls=(0, (2, 2)), zorder=1)
    label(ax, 0.32, 18, "vloeistof + damp", K.blauw, ha="center", fontsize=11)

    # isothermen boven Tc
    for T, k in [(323.15, K.oker), (313.15, K.rood)]:
        p = ts.pr_druk(V, T, gas) / 1e5
        ax.plot(V * 1e3, p, color=k, label=f"{T - 273.15:.0f} °C")

    # kritische isotherm
    p = ts.pr_druk(V, Tc, gas) / 1e5
    ax.plot(V * 1e3, p, color=K.paars, label=r"31.04 °C ($T_c$)")
    Vc = 0.307 * ts.R * Tc / ts.GASSEN[gas][1]  # PR: Zc = 0.307
    pc = ts.pr_druk(np.array([Vc]), Tc, gas)[0] / 1e5
    ax.plot(Vc * 1e3, pc, "o", color=K.paars, ms=7, zorder=5)
    label(ax, 0.105, 28, "kritisch punt", K.paars, fontsize=11)
    pijl(ax, (0.115, 33), (Vc * 1e3 + 0.001, pc - 2.5), K.paars, lw=1.2)

    # isotherm onder Tc met horizontaal condensatiestuk
    T = 293.15
    ps, vl, vg = ts.pr_verzadiging(T, gas)
    p = ts.pr_druk(V, T, gas) / 1e5
    gas_tak = V >= vg
    vl_tak = V <= vl
    ax.plot(V[gas_tak] * 1e3, p[gas_tak], color=K.blauw, label="20 °C")
    ax.plot(V[vl_tak] * 1e3, p[vl_tak], color=K.blauw)
    ax.plot([vl * 1e3, vg * 1e3], [ps / 1e5] * 2, color=K.blauw)
    lus = (V > vl) & (V < vg)
    ax.plot(V[lus] * 1e3, p[lus], color=K.blauw, lw=1.1, ls=(0, (1.5, 2.5)), alpha=0.8)
    # de lus is het berekende, instabiele deel van de isotherm; in werkelijkheid volgt het gas C -> E
    label(ax, 0.215, 34, "instabiel deel van de\nberekende isotherm", K.blauw, fontsize=10, va="center")
    pijl(ax, (0.222, 40), (0.172, 59.8), K.blauw, lw=1.0)
    ax.legend(loc="upper right", title="isotherm", title_fontsize=11)

    # punten A-F op de 20 °C-isotherm
    def pt(Vm, naam, dx=0.0, dy=3.5):
        pp = ts.pr_druk(np.array([Vm]), T, gas)[0] / 1e5 if naam not in "CDE" else ps / 1e5
        ax.plot(Vm * 1e3, pp, "o", ms=7, mfc=K.achtergrond, mec=K.blauw, mew=1.8, zorder=6)
        label(ax, Vm * 1e3 + dx, pp + dy, naam, K.tekst, ha="center", fontsize=11.5, style="italic")

    pt(5.0e-4, "A")
    pt(2.6e-4, "B")
    pt(vg, "C", dy=-9)
    pt(0.5 * (vl + vg), "D", dy=-9)
    pt(vl, "E", dx=-0.014, dy=-9)
    pt(5.0e-5, "F", dx=-0.016, dy=0)

    ax.set_xlim(0, 0.62)
    ax.set_ylim(0, 140)
    ax.set_xlabel(r"molair volume $V_m$ (L mol$^{-1}$)")
    ax.set_ylabel(r"druk $p$ (bar)")


def isothermen_co2():
    fig, ax = figuur(6.6, 4.8)
    _isothermen_co2(ax)
    return kader(fig)


def _co2_ideaal(ax):
    """Dezelfde isothermen als in _isothermen_co2, maar berekend met de ideale gaswet."""
    V = np.linspace(0.005, 0.62, 800)  # L/mol
    for T, k, naam in [(323.15, K.oker, "50 °C"), (313.15, K.rood, "40 °C"),
                       (304.19, K.paars, "31.04 °C"), (293.15, K.blauw, "20 °C")]:
        ax.plot(V, 0.08314 * T / V, color=k, label=naam)
    ax.legend(loc="upper right", title="isotherm", title_fontsize=11)
    label(ax, 0.2, 34, "$p = RT/V_m$: geen condensatie,\ngeen kritisch punt", K.tekst, fontsize=10.5)
    ax.set_xlim(0, 0.62)
    ax.set_ylim(0, 140)
    ax.set_xlabel(r"molair volume $V_m$ (L mol$^{-1}$)")
    ax.set_ylabel(r"druk $p$ (bar)")


def isothermen_vergelijking():
    """CO2 berekend als ideaal gas (links) naast reëel CO2 (rechts), met dezelfde assen."""
    fig, (ax1, ax2) = figuur(12.4, 4.8, ncols=2)
    _co2_ideaal(ax1)
    _isothermen_co2(ax2)
    ax1.set_title("CO$_2$ als ideaal gas", fontsize=12.5)
    ax2.set_title("reëel gas: CO$_2$", fontsize=12.5)
    return kader(fig)


# ---------------------------------------------- algemene compressibiliteitskaart
def compressibiliteitskaart():
    """Z(p_r) bij vaste T_r: Lee-Kesler-curve + 'meetpunten' van vier gassen."""
    fig, ax = figuur(7.6, 5.0)
    pr = np.linspace(0.02, 7, 160)
    Trs = [1.0, 1.1, 1.2, 1.3, 1.5, 2.0]
    kleuren = [K.warmte(i / (len(Trs) - 1)) for i in range(len(Trs))]
    for Tr, k in zip(Trs, kleuren):
        Z = [ts.lee_kesler_Z(Tr, p) for p in pr]
        ax.plot(pr, Z, color=k, lw=2.2, zorder=3)
        tekst = f"$T_r$ = {Tr:.1f}"
        Z = np.array(Z)
        if Tr == 1.0:
            j = int(np.searchsorted(pr, 1.25))
            x, y = pr[j], Z[j] - 0.045
        elif Tr == 2.0:
            x, y = 2.6, Z[int(np.searchsorted(pr, 2.6))] - 0.035
        else:
            j = int(np.argmin(Z))
            x, y = pr[j], Z[j] + 0.035
        label(ax, x, y, tekst, k, ha="center", va="center", fontsize=10.5, zorder=6, bbox=achter())

    vormen = {"CH4": ("o", r"CH$_4$"), "N2": ("s", r"N$_2$"),
              "C2H6": ("^", r"C$_2$H$_6$"), "CO2": ("D", r"CO$_2$")}
    prp = np.array([0.5, 1.0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    for gas, (m, naam) in vormen.items():
        Tc, pc, _ = ts.GASSEN[gas]
        for Tr, k in zip([1.1, 1.3, 2.0], [kleuren[1], kleuren[3], kleuren[5]]):
            Z = [ts.pr_Z(Tr * Tc, p * pc, gas) for p in prp]
            ax.plot(prp, Z, m, ms=5.5, mfc=K.achtergrond, mec=K.tekst, mew=1.1, zorder=4)
        ax.plot([], [], m, ms=6, mfc=K.achtergrond, mec=K.tekst, mew=1.1, label=naam)
    ax.axhline(1, color=K.zacht, lw=1.2, ls=(0, (4, 3)), zorder=1)
    label(ax, 0.1, 1.02, "ideaal gas", K.zacht, va="bottom", fontsize=10.5)
    ax.legend(loc="lower right", title="berekend per gas", title_fontsize=10.5, ncols=2)
    ax.set_xlim(0, 7.2)
    ax.set_ylim(0.15, 1.12)
    ax.set_xlabel(r"gereduceerde druk $p_r = p/p_c$")
    ax.set_ylabel(r"compressibiliteitsfactor $Z = pV_m/RT$")
    return kader(fig)


# ------------------------------------------------------------- Z in functie van p
def compressiefactor():
    """Z(p) bij 300 K voor enkele gassen (Peng-Robinson)."""
    fig, ax = figuur(6.8, 4.6)
    p = np.linspace(1, 800, 400) * 1e5
    T = 300.0
    gassen = [("H2", r"H$_2$", K.rood), ("N2", r"N$_2$", K.accent),
              ("CH4", r"CH$_4$", K.oker), ("C2H4", r"C$_2$H$_4$", K.blauw)]
    ax.axhspan(0, 1, color=K.vlak_blauw, alpha=0.45, lw=0, zorder=0)
    ax.axhspan(1, 2, color=K.vlak_rood, alpha=0.45, lw=0, zorder=0)
    eind = []
    for gas, naam, k in gassen:
        Z = [ts.pr_Z(T, pi, gas) for pi in p]
        ax.plot(p / 1e5, Z, color=k)
        eind.append([Z[-1], naam, k])
    eind.sort()
    for j in range(1, len(eind)):  # labels niet laten overlappen
        eind[j][0] = max(eind[j][0], eind[j - 1][0] + 0.09)
    for z, naam, k in eind:
        label(ax, 812, z, naam, k, va="center")
    ax.axhline(1, color=K.zacht, lw=1.3, ls=(0, (4, 3)))
    label(ax, 640, 0.96, "ideaal gas ($Z$ = 1)", K.zacht, va="top", fontsize=11)
    label(ax, 790, 1.88, "afstoting domineert ($Z > 1$)", K.rood, ha="right", fontsize=11)
    label(ax, 790, 0.1, "aantrekking domineert ($Z < 1$)", K.blauw, ha="right", fontsize=11)
    label(ax, 30, 1.88, "$T$ = 300 K", K.tekst, fontsize=11)
    ax.set_xlim(0, 880)
    ax.set_ylim(0, 2)
    ax.set_xlabel(r"druk $p$ (bar)")
    ax.set_ylabel(r"compressiefactor $Z$")
    return kader(fig)


# ================================================================ VOORSTELLEN
def opwarmcurve_water():
    """Temperatuur van 1 kg water bij gelijkmatige warmtetoevoer (-20 °C ijs -> 120 °C stoom)."""
    fig, ax = figuur(7.2, 4.6)
    cp_ijs, cp_w, cp_s = 2.09, 4.18, 2.01  # kJ/(kg K)
    H_sm, H_v = 334, 2257  # kJ/kg
    Q = [0]
    Tt = [-20]
    stappen = [(cp_ijs * 20, 0), (H_sm, 0), (cp_w * 100, 100), (H_v, 100), (cp_s * 20, 120)]
    for dq, T in stappen:
        Q.append(Q[-1] + dq)
        Tt.append(T)
    ax.plot(Q, Tt, color=K.tekst, lw=2.6, zorder=3)
    segment_kleur = [K.blauw, K.paars, K.blauw, K.rood, K.rood]
    for i, k in enumerate(segment_kleur):
        ax.plot(Q[i:i + 2], Tt[i:i + 2], color=k, lw=2.8, zorder=4)

    def balk(q0, q1, tekst, k, y):
        ax.annotate("", xy=(q1, y), xytext=(q0, y),
                    arrowprops=dict(arrowstyle="<|-|>", color=k, lw=1.3, mutation_scale=12))
        label(ax, (q0 + q1) / 2, y + 4, tekst, k, ha="center", fontsize=10.5)

    balk(Q[1], Q[2], "smelten\n334 kJ", K.paars, 12)
    balk(Q[2], Q[3], "opwarmen 0→100 °C\n418 kJ", K.blauw, 112)
    balk(Q[3], Q[4], "verdampen  2257 kJ", K.rood, 112)
    label(ax, Q[1] + 25, -14, "ijs", K.blauw, fontsize=11)
    label(ax, 600, 62, "water", K.blauw, fontsize=11, ha="right")
    label(ax, Q[4] - 50, 122, "stoom", K.rood, ha="right", fontsize=11)
    label(ax, 1650, 55,
          "Verdampen kost ruim vijf keer zoveel\nenergie als water van 0 tot 100 °C opwarmen",
          K.tekst, ha="center", fontsize=11, style="italic")
    ax.set_xlim(0, Q[-1] * 1.03)
    ax.set_ylim(-30, 140)
    ax.set_xlabel("toegevoerde warmte $q$ per kg (kJ)")
    ax.set_ylabel("temperatuur (°C)")
    return kader(fig)


def compressie_pv():
    """Isotherme vs. adiabatische compressie van lucht van 1 naar 8 bar, en tweetrapscompressie met tussenkoeling."""
    fig, ax = figuur(6.8, 4.7)
    gamma = 1.4
    T1, p1 = 293.15, 1.0
    V1 = 0.08314 * T1 / p1  # L voor 1 mol
    p = np.linspace(p1, 8, 300)
    V_iso = p1 * V1 / p
    V_ad = V1 * (p1 / p) ** (1 / gamma)
    T2 = T1 * (8 / p1) ** ((gamma - 1) / gamma)
    ax.fill_betweenx(p, V_iso, V_ad, color=K.vlak_oker, lw=0, zorder=0)
    ax.plot(V_iso, p, color=K.blauw, label="isotherm (perfect gekoeld)")
    ax.plot(V_ad, p, color=K.rood, label="adiabatisch (geen koeling)")
    ax.plot(V1, p1, "o", color=K.tekst, zorder=5)
    label(ax, V1 + 0.4, p1 + 0.15, f"start: 1 bar, {T1 - 273.15:.0f} °C", K.tekst, fontsize=11)
    ax.plot(V_iso[-1], 8, "o", color=K.blauw, zorder=5)
    ax.plot(V_ad[-1], 8, "o", color=K.rood, zorder=5)
    label(ax, V_iso[-1] - 0.35, 8, f"{T1 - 273.15:.0f} °C", K.blauw, ha="right", va="center", fontsize=11)
    label(ax, V_ad[-1] + 0.35, 8, f"{T2 - 273.15:.0f} °C", K.rood, ha="left", va="center", fontsize=11)
    # tweetrapscompressie met tussenkoeling tot T1
    pm = np.sqrt(8 * p1)
    pa = np.linspace(p1, pm, 100)
    Va = V1 * (p1 / pa) ** (1 / gamma)
    Vm_iso = p1 * V1 / pm
    pb = np.linspace(pm, 8, 100)
    Vb = Vm_iso * (pm / pb) ** (1 / gamma)
    Tm = T1 * (pm / p1) ** ((gamma - 1) / gamma)
    ax.plot(Va, pa, color=K.groen, lw=1.8, ls="--")
    ax.plot([Va[-1], Vm_iso], [pm, pm], color=K.groen, lw=1.8, ls="--")
    ax.plot(Vb, pb, color=K.groen, lw=1.8, ls="--", label="2 trappen + tussenkoeling")
    ax.plot(Vb[-1], 8, "o", color=K.groen, zorder=5)
    label(ax, Va[-1] + 0.3, pm + 0.1, f"{Tm - 273.15:.0f} °C", K.groen, fontsize=10.5, va="bottom")
    label(ax, Vb[-1], 8.3, f"{Tm - 273.15:.0f} °C", K.groen, ha="center", fontsize=11)
    label(ax, 10.5, 5.2, "extra arbeid bij\nadiabatische compressie", K.oker,
          fontsize=11, ha="left", va="center")
    pijl(ax, (10.3, 5.0), (7.6, 3.6), K.oker, lw=1.3)
    ax.legend(loc="upper right")
    ax.set_xlim(0, V1 * 1.12)
    ax.set_ylim(0, 9.2)
    ax.set_xlabel("volume $V$ (L, 1 mol lucht)")
    ax.set_ylabel("druk $p$ (bar)")
    return kader(fig)


# ------------------------------------------- adiabatische vlamtemperatuur
_SHOMATE = {  # NIST WebBook: (Tmin, Tmax, A, B, C, D, E), cp in J/(mol K), t = T/1000
    "N2": [(100, 500, 28.98641, 1.853978, -9.647459, 16.63537, 0.000117),
           (500, 2000, 19.50583, 19.88705, -8.598535, 1.369784, 0.527601),
           (2000, 6000, 35.51872, 1.128728, -0.196103, 0.014662, -4.553760)],
    "O2": [(100, 700, 31.32234, -20.23531, 57.86644, -36.50624, -0.007374),
           (700, 2000, 30.03235, 8.772972, -3.988133, 0.788313, -0.741599),
           (2000, 6000, 20.91111, 10.72071, -2.020498, 0.146449, 9.245722)],
    "CO2": [(298, 1200, 24.99735, 55.18696, -33.69137, 7.948387, -0.136638),
            (1200, 6000, 58.16639, 2.720074, -0.492289, 0.038844, -6.447293)],
    "H2O": [(298, 1700, 30.09200, 6.832514, 6.793435, -2.534480, 0.082139),
            (1700, 6000, 41.96426, 8.622053, -1.499780, 0.098119, -11.15764)],
}


def _dH(stof, T):
    """H(T) - H(298.15 K) in J/mol (Shomate, stuksgewijs geïntegreerd)."""
    def F(c, T):
        t = T / 1000
        A, B, C, D, E = c
        return 1000 * (A * t + B * t**2 / 2 + C * t**3 / 3 + D * t**4 / 4 - E / t)
    tot, Tl = 0.0, 298.15
    for Tmin, Tmax, *c in _SHOMATE[stof]:
        if Tl >= Tmax:
            continue
        Th = min(T, Tmax)
        tot += F(c, Th) - F(c, Tl)
        Tl = Th
        if Tl >= T:
            break
    return tot


def _T_ad(overmaat, dcH=802.3e3):
    n = {"CO2": 1, "H2O": 2, "O2": 2 * overmaat, "N2": 2 * (1 + overmaat) * 3.76}
    lo, hi = 300.0, 4000.0
    for _ in range(60):  # bisectie
        T = (lo + hi) / 2
        if sum(v * _dH(s, T) for s, v in n.items()) > dcH:
            hi = T
        else:
            lo = T
    return T


def vlamtemperatuur():
    """Adiabatische vlamtemperatuur van CH4 in lucht vs. luchtovermaat."""
    fig, ax = figuur(6.6, 4.5)
    x = np.linspace(0, 200, 81)
    T = np.array([_T_ad(xi / 100) for xi in x])
    ax.axvspan(10, 20, color=K.vlak_oker, lw=0, zorder=0)
    label(ax, 15, 1250, "gangbaar\nin ovens", K.oker, ha="center", fontsize=10.5)
    ax.plot(x, T - 273.15, color=K.rood, lw=2.4)
    T0 = T[0] - 273.15
    ax.plot(0, T0, "o", color=K.rood, ms=7, zorder=5)
    label(ax, 23, T0 + 15, f"stoichiometrisch: {T0:.0f} °C", K.rood, fontsize=11)
    label(ax, 110, 1500, "meer lucht = meer stikstof\ndat mee opgewarmd moet worden", K.tekst,
          fontsize=11, style="italic")
    ax.set_xlim(0, 200)
    ax.set_ylim(700, 2200)
    ax.set_xlabel("luchtovermaat (%)")
    ax.set_ylabel(r"$T_\mathrm{ad}$ (°C)")
    return kader(fig)


# ------------------------------------------------- kinetische gastheorie
def kmt_botsing():
    """Eén molecule beweegt in de x-richting naar de wand en terug:
    impulsverandering 2mv_x per botsing, één botsing per 2L/v_x."""
    from matplotlib.patches import Rectangle
    fig, ax = figuur(7.4, 4.6)
    ax.set_axis_off()
    ax.set_xlim(-0.6, 7.6)
    ax.set_ylim(-1.3, 5.3)
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), 5, 4.4, facecolor=K.vlak_accent, edgecolor=K.accent, lw=2))
    ax.add_patch(Rectangle((5, 0), 0.18, 4.4, facecolor=K.accent, edgecolor=K.accent, lw=0))
    # x-as
    pijl(ax, (0.25, 0.35), (1.25, 0.35), K.tekst, lw=1.2)
    label(ax, 1.35, 0.35, "$x$", K.tekst, fontsize=12, va="center")
    # heen: molecule beweegt naar rechts met v_x
    y1, y2 = 2.75, 1.65
    ax.plot([0.9, 4.85], [y1, y1], color=K.zacht, lw=1, ls=":")
    ax.plot(0.9, y1, "o", color=K.blauw, ms=12, zorder=5)
    pijl(ax, (1.15, y1), (2.5, y1), K.oker, lw=2.4)
    label(ax, 1.8, y1 + 0.3, "$+v_x$", K.oker, fontsize=12, ha="center")
    label(ax, 3.6, y1 + 0.3, "voor: $+mv_x$", K.oker, fontsize=10.5, ha="center")
    # botsing en terug: -v_x
    ax.plot(4.85, (y1 + y2) / 2, "o", color=K.blauw, ms=12, zorder=5, alpha=0.55)
    ax.plot([4.85, 0.9], [y2, y2], color=K.zacht, lw=1, ls=":")
    ax.plot(3.9, y2, "o", color=K.blauw, ms=12, zorder=5)
    pijl(ax, (3.65, y2), (2.3, y2), K.rood, lw=2.4)
    label(ax, 3.0, y2 - 0.45, "$-v_x$", K.rood, fontsize=12, ha="center")
    label(ax, 1.4, y2 - 0.45, "na: $-mv_x$", K.rood, fontsize=10.5, ha="center")
    label(ax, 5.35, 2.2, "wand krijgt\n$\\Delta p = 2mv_x$", K.tekst, fontsize=10.5, va="center")
    # ribbe L en terugkeertijd
    ax.annotate("", xy=(0, -0.45), xytext=(5, -0.45), arrowprops=dict(arrowstyle="<->", color=K.tekst, lw=1.2))
    label(ax, 2.5, -0.6, "$L$: heen en terug $2L$, dus elke $2L/v_x$ een botsing", K.tekst, fontsize=10.5,
          ha="center", va="top")
    label(ax, 2.5, 4.8, "één molecule in een kubus", K.accent, fontsize=12, ha="center", fontweight="bold")
    return kader(fig)


# ------------------------------------------------ Van der Waals: twee correcties
def vdw_uitgesloten():
    """Stap 1 van Van der Waals: het uitgesloten volume rond een paar harde bollen."""
    from matplotlib.patches import Circle
    fig, ax = figuur(6.0, 4.9)
    ax.set_axis_off()
    ax.set_aspect("equal")
    # --- links: uitgesloten volume
    ax.set_xlim(-3.4, 5.0)
    ax.set_ylim(-3.2, 3.3)
    r = 1.0
    ax.add_patch(Circle((0, 0), 2 * r, facecolor=K.vlak_rood, edgecolor=K.rood, lw=1.6, ls="--", zorder=1))
    ax.add_patch(Circle((0, 0), r, facecolor=K.blauw, edgecolor=K.tekst, lw=1.2, zorder=3, alpha=0.85))
    ax.add_patch(Circle((2 * r, 0), r, facecolor=K.oker, edgecolor=K.tekst, lw=1.2, zorder=3, alpha=0.85))
    ax.plot([0, 2 * r], [0, 0], "o", color=K.tekst, ms=4, zorder=4)
    label(ax, 0, 0.25, "A", "white", ha="center", fontsize=12, fontweight="bold")
    label(ax, 2 * r, 0.25, "B", "white", ha="center", fontsize=12, fontweight="bold")
    # maataanduiding r en 2r
    ax.annotate("", xy=(2 * r, 0), xytext=(2 * r, -r), arrowprops=dict(arrowstyle="<->", color=K.tekst, lw=1.1), zorder=5)
    label(ax, 2 * r + 0.12, -0.55, "$r$", K.tekst, ha="left", va="center", fontsize=12)
    ax.annotate("", xy=(0, 0), xytext=(-1.414 * r, 1.414 * r),
                arrowprops=dict(arrowstyle="<->", color=K.rood, lw=1.3), zorder=5)
    label(ax, -1.25, 0.6, "$2r$", K.rood, ha="right", fontsize=12)
    label(ax, 0, -2.45, "uitgesloten bol: $\\frac{4}{3}\\pi(2r)^3 = 8\\cdot\\frac{4}{3}\\pi r^3$", K.rood,
          ha="center", va="top", fontsize=11)
    label(ax, 3.15, 1.75, "het middelpunt van B\nkomt nooit dichter\ndan $2r$ bij dat van A", K.tekst,
          fontsize=10.5, va="center")
    label(ax, 3.15, -1.2, "die bol hoort bij\néén paar: per molecule\n$4\\cdot\\frac{4}{3}\\pi r^3$ kwijt", K.tekst,
          fontsize=10.5, va="center")
    label(ax, 0.8, 3.15, "stap 1: uitgesloten volume $b$", K.accent, ha="center", fontsize=12.5, fontweight="bold")
    return kader(fig)


def vdw_aantrekking():
    """Stap 2 van Van der Waals: een molecule aan de wand wordt netto naar binnen getrokken."""
    from matplotlib.patches import Circle, Rectangle
    fig, ax2 = figuur(6.4, 4.9)
    ax2.set_axis_off()
    ax2.set_aspect("equal")
    # --- rechts: aantrekking aan de wand
    ax2.set_xlim(-0.4, 8.4)
    ax2.set_ylim(-1.3, 5.2)
    ax2.add_patch(Rectangle((0, 0), 7.2, 4.4, facecolor=K.vlak_accent, edgecolor="none", zorder=0))
    ax2.add_patch(Rectangle((7.2, 0), 0.22, 4.4, facecolor=K.accent, edgecolor="none", zorder=1))
    label(ax2, 7.75, 2.2, "wand", K.accent, rotation=90, ha="center", va="center", fontsize=11)
    rng = np.random.default_rng(3)

    def buren(xc, yc, hoeken):
        for h in hoeken:
            x, y = xc + 1.15 * np.cos(h), yc + 1.15 * np.sin(h)
            ax2.add_patch(Circle((x, y), 0.25, facecolor=K.zacht, edgecolor="none", alpha=0.55, zorder=2))
            pijl(ax2, (xc + 0.33 * np.cos(h), yc + 0.33 * np.sin(h)),
                 (xc + 0.8 * np.cos(h), yc + 0.8 * np.sin(h)), K.groen, lw=1.6)
    # molecule in het midden: buren rondom, krachten heffen elkaar op
    xa, ya = 2.0, 2.4
    buren(xa, ya, np.linspace(0, 2 * np.pi, 7)[:-1] + 0.3)
    ax2.add_patch(Circle((xa, ya), 0.3, facecolor=K.blauw, edgecolor=K.tekst, lw=1.1, zorder=3))
    label(ax2, xa, 0.6, "in het midden:\nnetto kracht nul", K.tekst, ha="center", va="top", fontsize=10.5)
    # molecule aan de wand: buren enkel links
    xb, yb = 6.6, 2.4
    buren(xb, yb, np.array([110, 150, 180, 210, 250]) * np.pi / 180)
    ax2.add_patch(Circle((xb, yb), 0.3, facecolor=K.blauw, edgecolor=K.tekst, lw=1.1, zorder=3))
    pijl(ax2, (xb - 0.2, yb + 1.55), (xb - 1.6, yb + 1.55), K.rood, lw=2.6)
    label(ax2, xb - 0.9, yb + 1.75, "netto naar binnen", K.rood, ha="center", fontsize=10.5)
    label(ax2, xb - 0.3, 0.6, "aan de wand:\nbotst zachter", K.tekst, ha="center", va="top", fontsize=10.5)
    label(ax2, 3.6, -0.75, "effect $\\propto$ (moleculen aan de wand) $\\times$ (buren) $\\propto (n/V)^2$", K.tekst,
          ha="center", va="top", fontsize=10.5)
    label(ax2, 3.8, 4.95, "stap 2: aantrekking $a$", K.accent, ha="center", fontsize=12.5, fontweight="bold")
    return kader(fig)


# ------------------------------------------- Van der Waals: kritiek punt
def _vdw_pr(Vr, Tr):
    return 8 * Tr / (3 * Vr - 1) - 3 / Vr**2


def _maxwell(Tr):
    """Gelijke-oppervlakteconstructie: (p_r, V_vloeistof, V_damp) bij T_r < 1."""
    # spinodalen: dp/dV = 0
    V = np.linspace(0.36, 30, 200000)
    dp = np.gradient(_vdw_pr(V, Tr), V)
    teken = np.where(np.diff(np.sign(dp)))[0]
    pmin, pmax = _vdw_pr(V[teken[0]], Tr), _vdw_pr(V[teken[1]], Tr)

    def wortels(p):
        # 3 p V^3 - (p + 8T) V^2 + 9 V - 3 = 0  (vdW in gereduceerde vorm, kubisch in V)
        r = np.roots([3 * p, -(p + 8 * Tr), 9, -3])
        r = np.sort(r[np.abs(r.imag) < 1e-9].real)
        return r[0], r[-1]

    def opp(p):
        Vl, Vg = wortels(p)
        I = 8 * Tr / 3 * np.log((3 * Vg - 1) / (3 * Vl - 1)) + 3 / Vg - 3 / Vl
        return I - p * (Vg - Vl)
    lo, hi = max(pmin, 1e-4) + 1e-9, pmax - 1e-9  # bisectie (geen scipy nodig)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if np.sign(opp(mid)) == np.sign(opp(lo)):
            lo = mid
        else:
            hi = mid
    p = 0.5 * (lo + hi)
    return (p, *wortels(p))


def vdw_isothermen():
    """Van der Waals-isothermen in gereduceerde vorm: lus onder T_c, buigpunt bij T_c, monotoon erboven."""
    fig, ax = figuur(7.4, 5.0)
    Vr = np.linspace(0.42, 5, 800)
    # tweefasengebied (koepel) uit de Maxwell-constructie
    Ts = np.linspace(0.8, 0.9999, 60)
    koepel = [_maxwell(t) for t in Ts]
    Vl = [k[1] for k in koepel] + [1.0]
    Vg = [k[2] for k in koepel] + [1.0]
    pk = [k[0] for k in koepel] + [1.0]
    xs = np.concatenate([Vl, Vg[::-1]])
    ys = np.concatenate([pk, pk[::-1]])
    ax.fill(xs, ys, color=K.vlak_blauw, lw=0, zorder=0)
    ax.plot(Vl, pk, color=K.blauw, lw=1.2, ls="--", zorder=1)
    ax.plot(Vg, pk, color=K.blauw, lw=1.2, ls="--", zorder=1)
    label(ax, 2.3, 0.43, "vloeistof + damp", K.blauw, ha="center", va="center", fontsize=11)
    for Tr, k in [(0.85, K.zacht), (0.9, K.zacht), (1.0, K.rood), (1.1, K.oker), (1.2, K.oker)]:
        p = _vdw_pr(Vr, Tr)
        if Tr < 1:
            pm, vl, vg = _maxwell(Tr)
            binnen = (Vr > vl) & (Vr < vg)
            ax.plot(np.where(binnen, np.nan, Vr), p, color=K.tekst, lw=1.8)
            ax.plot(Vr[binnen], p[binnen], color=K.tekst, lw=1, ls=":")
            ax.plot([vl, vg], [pm, pm], color=K.tekst, lw=1.8)
        else:
            ax.plot(Vr, p, color=k, lw=2.4 if Tr == 1 else 1.8)
        yl = {0.85: 0.27, 0.9: 0.37, 1.0: 0.48, 1.1: 0.59, 1.2: 0.70}[Tr]
        label(ax, 5.08, yl, f"$T/T_c$ = {Tr:g}", k if Tr >= 1 else K.tekst, va="center", fontsize=10.5)
    ax.plot(1, 1, "o", color=K.rood, ms=8, zorder=6)
    ax.annotate("kritiek punt: buigpunt\nmet horizontale raaklijn", xy=(1.03, 1.02), xytext=(2.6, 1.45),
                color=K.rood, fontsize=10.5, arrowprops=dict(arrowstyle="->", color=K.rood, lw=1.2))
    ax.annotate("lus van Van der Waals:\nin werkelijkheid een\nhorizontaal stuk", xy=(1.45, 0.66), xytext=(1.5, 0.12),
                color=K.zacht, fontsize=9.5, arrowprops=dict(arrowstyle="->", color=K.zacht, lw=1))
    ax.set_xlim(0.3, 5.9)
    ax.set_ylim(0, 1.8)
    ax.set_xlabel(r"gereduceerd volume $V_\mathrm{m}/V_{\mathrm{m},c}$")
    ax.set_ylabel(r"gereduceerde druk $p/p_c$")
    return kader(fig)


# ------------------------------------- arbeid hangt af van de weg (voorbeeld)
def arbeid_weg():
    """Isotherme expansie 1 -> 10 L bij 300 K: reversibel (links) en in één ruk tegen p_ext = p2 (rechts).
    De oppervlakte onder de weg is |W|."""
    fig, (ax1, ax2) = figuur(11.0, 4.4, ncols=2, sharey=True)
    n, T = 1.0, 300.0
    V = np.linspace(1, 10, 300)
    p = n * 8.314 * T / (V * 1e-3) / 1e5  # bar
    p1, p2 = p[0], p[-1]
    for ax in (ax1, ax2):
        ax.plot([1, 10], [p1, p2], "o", color=K.tekst, ms=7, zorder=6)
        label(ax, 1.25, p1, "1", K.tekst, va="center", fontsize=12, fontweight="bold")
        label(ax, 10, p2 + 1.6, "2", K.tekst, ha="center", fontsize=12, fontweight="bold")
        ax.set_xlim(0, 11)
        ax.set_ylim(0, 28)
        ax.set_xlabel("volume $V$ (L)")
    # links: reversibel
    ax1.fill_between(V, p, color=K.vlak_blauw, lw=0)
    ax1.plot(V, p, color=K.blauw, lw=2.4)
    label(ax1, 5.0, 1.6, "$|W|$ = 5.74 kJ", K.blauw, ha="center", fontsize=13, fontweight="bold")
    label(ax1, 3.0, 12, "$p_\\mathrm{ext} = p = nRT/V$\n(telkens in evenwicht)", K.blauw, fontsize=10.5)
    ax1.set_title("reversibel", fontsize=12.5)
    ax1.set_ylabel("druk $p$ (bar)")
    # rechts: in één ruk tegen p2
    ax2.plot(V, p, color=K.zacht, lw=1.3, ls="--")
    label(ax2, 2.6, 11, "isotherm\n(ter vergelijking)", K.zacht, fontsize=10)
    ax2.fill_between([1, 10], [p2, p2], color=K.vlak_rood, lw=0)
    ax2.plot([1, 10], [p2, p2], color=K.rood, lw=2.4)
    pijl(ax2, (1, p1 - 0.6), (1, p2 + 0.4), K.rood, lw=1.6)
    label(ax2, 1.25, 16, "$p_\\mathrm{ext}$ valt\nmeteen naar $p_2$", K.rood, fontsize=10)
    label(ax2, 5.5, 1.2, "$|W|$ = 2.24 kJ", K.rood, ha="center", va="center", fontsize=12, fontweight="bold")
    label(ax2, 4.2, p2 + 0.8, "$p_\\mathrm{ext}$ = 2.49 bar", K.rood, ha="center", fontsize=10.5)
    ax2.set_title("in één ruk tegen $p_\\mathrm{ext} = p_2$", fontsize=12.5)
    return kader(fig)



def _cilinder(ax, x0, titel, reactie, h_voor, hoogte_gas, warmte_in, arbeid_uit, Q, W, dU, rest):
    """Cilinder met zuiger bij constante druk; warmte door de bodem, arbeid via de zuiger.
    Gestippeld = zuigerstand voor de reactie (hoogte h_voor)."""
    from matplotlib.patches import Rectangle
    b, y0 = 4.0, 1.4
    yz = y0 + hoogte_gas
    ax.add_patch(Rectangle((x0, y0), b, hoogte_gas, facecolor=K.vlak_accent, edgecolor="none"))
    ax.plot([x0, x0, x0 + b, x0 + b], [y0 + 4.4, y0, y0, y0 + 4.4], color=K.as_, lw=1.8)
    if rest == "CaO(s)":
        ax.add_patch(Rectangle((x0 + 1.2, y0), 1.6, 0.35, facecolor=K.vlak_grijs, edgecolor=K.zacht, lw=1.0))
    else:
        ax.add_patch(Rectangle((x0, y0), b, 0.22, facecolor=K.vlak_blauw, edgecolor="none"))
    label(ax, x0 + 2.95, y0 + 0.04, rest, K.zacht, va="bottom", fontsize=9)
    ax.plot([x0, x0 + b], [y0 + h_voor, y0 + h_voor], color=K.zacht, lw=1.3, ls="--")
    label(ax, x0 - 0.15, y0 + h_voor, "voor", K.zacht, ha="right", va="center", fontsize=9.5)
    ax.add_patch(Rectangle((x0, yz), b, 0.35, facecolor=K.vlak_grijs, edgecolor=K.as_, lw=1.4))
    label(ax, x0 - 0.15, yz + 0.17, "na", K.as_, ha="right", va="center", fontsize=9.5)
    ytop = max(yz + 0.35, y0 + h_voor)
    for dx in (0.8, 2.0, 3.2):
        pijl(ax, (x0 + dx, ytop + 0.9), (x0 + dx, yz + 0.42), K.zacht, lw=1.2)
    label(ax, x0 + 2.0, ytop + 1.05, "atmosfeer, 1 bar", K.zacht, ha="center", fontsize=9.5)
    # beweging van de zuiger = richting van de arbeid
    xa = x0 + b + 0.7
    if arbeid_uit:
        pijl(ax, (xa, y0 + h_voor), (xa, yz + 0.35), K.oker, lw=2.6)
        tekst = f"systeem duwt\natmosfeer weg\n$W$ = {W}"
    else:
        pijl(ax, (xa, y0 + h_voor + 0.35), (xa, yz + 0.1), K.oker, lw=2.6)
        tekst = f"atmosfeer duwt\nzuiger in\n$W$ = {W}"
    label(ax, xa + 0.3, (y0 + h_voor + yz) / 2 + 0.2, tekst, K.oker, va="center",
          fontsize=10.5, fontweight="bold")
    for dx in (0.9, 2.0, 3.1):
        if warmte_in:
            pijl(ax, (x0 + dx, y0 - 1.1), (x0 + dx, y0 - 0.1), K.rood, lw=2.2)
        else:
            pijl(ax, (x0 + dx, y0 - 0.1), (x0 + dx, y0 - 1.1), K.rood, lw=2.2)
    label(ax, x0 + b + 0.3, y0 - 0.6, f"warmte {'in' if warmte_in else 'uit'}\n$Q_p = \\Delta H$ = {Q}",
          K.rood, va="center", fontsize=10.5, fontweight="bold")
    label(ax, x0 + b / 2, y0 + 0.85 if hoogte_gas > 1.5 else y0 - 1.9, f"$\\Delta U$ = {dU}", K.tekst, ha="center",
          fontsize=11, fontweight="bold")
    label(ax, x0 + b / 2, 7.35, titel, K.tekst, ha="center", fontsize=12.5, fontweight="bold")
    label(ax, x0 + b / 2, 6.8, reactie, K.tekst, ha="center", fontsize=10.5)


def _enthalpie_paneel():
    fig, ax = figuur(5.2, 3.6)
    ax.set_axis_off()
    ax.set_xlim(-1.2, 9.6)
    ax.set_ylim(-0.1, 7.7)
    ax.set_aspect("equal")
    return fig, ax


def enthalpie_thermolyse():
    """Thermolyse van CaCO3 bij constante druk (298 K, per mol): gas ontstaat, de zuiger schuift op
    en een deel van de toegevoerde warmte verlaat het systeem als arbeid. Pijlen niet op schaal."""
    fig, ax = _enthalpie_paneel()
    _cilinder(ax, 0.3, "thermolyse van kalksteen (298 K)", "CaCO$_3$(s) $\\to$ CaO(s) + CO$_2$(g)",
              0.4, 3.0, True, True, "+178.3 kJ", "$-$2.5 kJ", "+175.8 kJ", "CaO(s)")
    return kader(fig)


def enthalpie_vet():
    """Verbranding van tristearine bij constante druk (310 K, per mol): gas verdwijnt, de atmosfeer
    duwt de zuiger in en levert arbeid. Volume na/voor = 57/81.5. Pijlen niet op schaal."""
    fig, ax = _enthalpie_paneel()
    _cilinder(ax, 0.3, "verbranding van vet (310 K)",
              "C$_{57}$H$_{110}$O$_6$(s) + 81.5 O$_2$ $\\to$ 57 CO$_2$ + 55 H$_2$O(l)",
              2.6, 1.82, False, False, "$-$35 700 kJ", "+63 kJ", "$-$35 640 kJ", "H$_2$O(l)")
    return kader(fig)

def stromingsarbeid():
    """Stromingsarbeid: aan de inlaat duwt het fluïdum stroomopwaarts (denkbeeldige zuiger) een pakketje
    met kracht p1*A over zijn lengte L1 = V1/A naar binnen (arbeid p1V1 op het toestel); aan de uitlaat
    duwt het uittredende pakketje het fluïdum stroomafwaarts weg (arbeid p2V2 naar de omgeving)."""
    from matplotlib.patches import Rectangle, FancyBboxPatch
    fig, ax = figuur(7.4, 2.6)
    ax.set_axis_off()
    ax.set_xlim(-0.3, 18.3)
    ax.set_ylim(-0.2, 5.6)
    ax.set_aspect("equal")
    yb, h = 1.6, 1.6          # leiding: onderkant en hoogte
    # toestel
    ax.add_patch(FancyBboxPatch((7.0, 0.6), 4.0, 3.6, boxstyle="round,pad=0.05,rounding_size=0.3",
                                facecolor=K.vlak_grijs, edgecolor=K.as_, lw=1.6))
    label(ax, 9.0, 2.4, "toestel\n(open systeem)", K.tekst, ha="center", va="center", fontsize=11)
    # leidingen
    for x0, x1 in ((0.0, 7.0), (11.0, 18.0)):
        ax.plot([x0, x1], [yb, yb], color=K.as_, lw=1.6)
        ax.plot([x0, x1], [yb + h, yb + h], color=K.as_, lw=1.6)
        ax.add_patch(Rectangle((x0, yb), x1 - x0, h, facecolor=K.vlak_accent, edgecolor="none", zorder=0))
    # inlaat: pakketje net voor het toestel, denkbeeldige zuiger erachter
    ax.add_patch(Rectangle((4.4, yb), 2.6, h, facecolor=K.vlak_blauw, edgecolor=K.blauw, lw=1.6))
    ax.add_patch(Rectangle((4.15, yb), 0.25, h, facecolor=K.oker, edgecolor=K.oker))
    pijl(ax, (2.4, yb + h / 2), (4.05, yb + h / 2), K.oker, lw=2.6)
    label(ax, 1.2, yb + h / 2, "$F = p_1A$", K.oker, ha="center", va="center", fontsize=11, fontweight="bold")
    label(ax, 5.7, yb + h / 2, "$p_1, V_1$", K.blauw, ha="center", va="center", fontsize=11, fontweight="bold")
    pijl(ax, (4.4, yb - 0.45), (7.0, yb - 0.45), K.tekst, lw=1.1, stijl="<|-|>")
    label(ax, 5.7, yb - 0.95, "$L_1 = V_1/A$", K.tekst, ha="center", fontsize=10.5)
    label(ax, 3.4, yb + h + 0.35, "denkbeeldige zuiger:\nhet fluïdum stroomopwaarts", K.oker,
          ha="center", fontsize=9.5)
    label(ax, 3.5, 5.1, "inlaat: $p_1A \\cdot L_1 = p_1V_1$ geleverd aan het toestel", K.oker, ha="center",
          fontsize=11, fontweight="bold")
    # uitlaat: pakketje net buiten het toestel duwt stroomafwaarts weg
    ax.add_patch(Rectangle((11.0, yb), 2.4, h, facecolor=K.vlak_blauw, edgecolor=K.blauw, lw=1.6))
    label(ax, 12.2, yb + h / 2, "$p_2, V_2$", K.blauw, ha="center", va="center", fontsize=11, fontweight="bold")
    pijl(ax, (13.5, yb + h / 2), (15.4, yb + h / 2), K.oker, lw=2.6)
    label(ax, 16.6, yb + h / 2, "$F = p_2A$", K.oker, ha="center", va="center", fontsize=11, fontweight="bold")
    label(ax, 14.6, yb + h + 0.35, "duwt het fluïdum\nstroomafwaarts weg", K.oker, ha="center", fontsize=9.5)
    label(ax, 14.5, 5.1, "uitlaat: $p_2V_2$ geleverd aan de omgeving", K.oker, ha="center",
          fontsize=11, fontweight="bold")
    label(ax, 9.0, -0.1, "stroomrichting $\\rightarrow$", K.zacht, ha="center", fontsize=10)
    return kader(fig)


_CP_TAB = {  # tabel tab:cp_coeff (a, b, c), Cp in J/(mol K), 300-1000 K
    "N2": (28.5, 3.6e-4, 4.00e-6),
    "H2": (29.1, -6.1e-4, 1.65e-6),
    "NH3": (24.4, 3.86e-2, -6.40e-6),
}


def _H_tab(stof, T, T0=298.15):
    a, b, c = _CP_TAB[stof]
    return a * (T - T0) + b / 2 * (T**2 - T0**2) + c / 3 * (T**3 - T0**3)


def kirchhoff():
    """Ammoniaksynthese N2 + 3 H2 -> 2 NH3 (dHr(298) = -92.2 kJ, Cp uit tab:cp_coeff).
    Links: H van reagentia en producten t.o.v. de reagentia bij 298 K; de reagentia hebben de grotere
    Cp (steilere lijn), dus de kloof ΔrH wordt groter bij hogere T. Rechts: ΔrH(T) exact (integraal)
    en met constante ΔrCp(298)."""
    fig, (ax1, ax2) = figuur(11.0, 4.4, ncols=2)
    T = np.linspace(298.15, 1000, 200)
    H0 = -92.2
    Hr = (_H_tab("N2", T) + 3 * _H_tab("H2", T)) / 1000
    Hp = H0 + 2 * _H_tab("NH3", T) / 1000
    ax1.plot(T, Hr, color=K.blauw, lw=2.4)
    ax1.plot(T, Hp, color=K.rood, lw=2.4)
    label(ax1, 330, 62, "reagentia: N$_2$ + 3 H$_2$\n$\\Sigma C_p$ = 116 J/K (298 K)", K.blauw, fontsize=10.5)
    label(ax1, 700, -88, "producten: 2 NH$_3$\n$\\Sigma C_p$ = 71 J/K (298 K)", K.rood, fontsize=10.5)
    for Tx, txt in ((298.15, "$-$92.2 kJ"), (723.15, "$-$106.2 kJ")):
        hr = (_H_tab("N2", Tx) + 3 * _H_tab("H2", Tx)) / 1000
        hp = H0 + 2 * _H_tab("NH3", Tx) / 1000
        pijl(ax1, (Tx, hr), (Tx, hp + 1.0), K.tekst, lw=1.8)
        ax1.plot([Tx, Tx], [hr, hr], "o", color=K.blauw, ms=6)
        ax1.plot([Tx, Tx], [hp, hp], "o", color=K.rood, ms=6)
        label(ax1, Tx + 12, (hr + hp) / 2, f"$\\Delta_r H$ =\n{txt}", K.tekst, va="center", fontsize=10.5)
    ax1.set_xlim(250, 1000)
    ax1.set_ylim(-110, 85)
    ax1.set_xlabel("temperatuur $T$ (K)")
    ax1.set_ylabel("$H - H_\\mathrm{reagentia}(298\\,\\mathrm{K})$ (kJ)")
    ax1.set_title("enthalpie van reagentia en producten", fontsize=12)
    # rechts
    dCp298 = 2 * sum(np.array(_CP_TAB["NH3"]) * [1, 298.15, 298.15**2]) \
        - sum(np.array(_CP_TAB["N2"]) * [1, 298.15, 298.15**2]) \
        - 3 * sum(np.array(_CP_TAB["H2"]) * [1, 298.15, 298.15**2])
    ax2.plot(T, Hp - Hr, color=K.accent, lw=2.4)
    ax2.plot(T, H0 + dCp298 * (T - 298.15) / 1000, color=K.oker, lw=2.0, ls="--")
    label(ax2, 320, -122, "constante $\\Delta_r C_p$ = $-$45.5 J/K\n(waarde bij 298 K)", K.oker, fontsize=10.5)
    label(ax2, 760, -103, "exact: $\\int \\Delta_r C_p(T)\\,\\mathrm{d}T$", K.accent, fontsize=10.5)
    ax2.plot([723.15], [-106.15], "o", color=K.accent, ms=6)
    ax2.plot([723.15], [-111.53], "o", color=K.oker, ms=6)
    ax2.axvline(723.15, color=K.zacht, lw=1, ls=":")
    label(ax2, 728, -88.5, "450 °C", K.zacht, fontsize=10)
    ax2.set_xlim(250, 1000)
    ax2.set_ylim(-130, -85)
    ax2.set_xlabel("temperatuur $T$ (K)")
    ax2.set_ylabel("$\\Delta_r H$ (kJ per 2 mol NH$_3$)")
    ax2.set_title("reactie-enthalpie $\\Delta_r H(T)$", fontsize=12)
    return kader(fig)


def ammoniakfabriek():
    """Vereenvoudigde syntheselus van een ammoniakfabriek (Haber-Bosch): compressor met tussenkoeling,
    reactor met drie katalysatorbedden en tussenkoeling, condensor, recycle. Bij elk toestel de vraag
    die het hoofdstuk beantwoordt."""
    from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
    fig, ax = figuur(10.0, 4.6)
    ax.set_axis_off()
    ax.set_xlim(-0.5, 25.5)
    ax.set_ylim(-0.6, 12.4)
    ax.set_aspect("equal")
    lijn = dict(color=K.as_, lw=1.8)
    # voeding
    pijl(ax, (-0.4, 5.0), (2.3, 5.0), K.blauw, lw=2.2)
    label(ax, 0.9, 5.45, "N$_2$ + 3 H$_2$\n25 bar", K.blauw, ha="center", va="bottom", fontsize=10)
    # compressor (trapezium)
    ax.add_patch(Polygon([(2.4, 3.6), (2.4, 6.4), (5.6, 5.6), (5.6, 4.4)], closed=True,
                         facecolor=K.vlak_oker, edgecolor=K.oker, lw=1.8))
    label(ax, 4.0, 2.9, "compressor\n25 $\\to$ 200 bar", K.oker, ha="center", va="top", fontsize=10.5,
          fontweight="bold")
    pijl(ax, (4.0, 8.0), (4.0, 6.1), K.oker, lw=2.0)
    label(ax, 4.0, 8.15, "arbeid $W$", K.oker, ha="center", va="bottom", fontsize=10)
    # leiding naar reactor
    ax.plot([5.6, 8.0], [5.0, 5.0], **lijn)
    ax.plot([8.0, 8.0], [5.0, 10.0], **lijn)
    pijl(ax, (8.0, 10.0), (9.4, 10.0), K.as_, lw=1.8)
    # reactor met drie bedden
    ax.add_patch(FancyBboxPatch((9.5, 0.6), 3.0, 9.8, boxstyle="round,pad=0.05,rounding_size=0.6",
                                facecolor=K.achtergrond, edgecolor=K.rood, lw=1.8))
    for y0 in (7.4, 4.3, 1.2):
        ax.add_patch(Rectangle((9.8, y0), 2.4, 2.2, facecolor=K.vlak_rood, edgecolor=K.rood, lw=1.0))
    for yk in (6.85, 3.75):
        pijl(ax, (12.3, yk), (13.3, yk), K.rood, lw=1.8)
    label(ax, 12.55, 5.3, "tussen-\nkoeling:\n$Q$ uit", K.rood, va="center", fontsize=9.5)
    label(ax, 11.0, -0.3, "reactor 400–500 °C\n3 katalysatorbedden", K.rood, ha="center", va="top",
          fontsize=10.5, fontweight="bold")
    # naar condensor
    ax.plot([11.0, 11.0], [0.6, 0.0], **lijn)
    ax.plot([11.0, 15.0], [0.0, 0.0], **lijn)
    ax.plot([15.0, 15.0], [0.0, 4.6], **lijn)
    pijl(ax, (15.0, 4.6), (16.4, 4.6), K.as_, lw=1.8)
    # condensor
    ax.add_patch(FancyBboxPatch((16.5, 3.4), 3.0, 3.2, boxstyle="round,pad=0.05,rounding_size=0.4",
                                facecolor=K.vlak_blauw, edgecolor=K.blauw, lw=1.8))
    label(ax, 18.0, 5.0, "condensor\n$-$10 °C", K.blauw, ha="center", va="center", fontsize=10.5,
          fontweight="bold")
    pijl(ax, (18.0, 3.3), (18.0, 1.4), K.blauw, lw=2.2)
    label(ax, 18.0, 1.2, "vloeibaar NH$_3$", K.blauw, ha="center", va="top", fontsize=10.5)
    pijl(ax, (19.6, 4.2), (21.4, 4.2), K.rood, lw=1.8)
    label(ax, 21.6, 4.2, "warmte $Q$", K.rood, va="center", fontsize=10)
    # recycle
    ax.plot([18.0, 18.0], [6.6, 11.4], **lijn)
    ax.plot([18.0, 1.8], [11.4, 11.4], **lijn)
    ax.plot([1.8, 1.8], [11.4, 5.0], **lijn)
    label(ax, 10.0, 11.6, "recycle: niet-omgezet gas (ongeveer 80 %)", K.zacht, ha="center", va="bottom",
          fontsize=9.5)
    pijl(ax, (6.0, 11.4), (5.0, 11.4), K.as_, lw=1.8)
    return kader(fig)


_DHF = {"NH3": -46.1e3, "N2": 0.0, "H2": 0.0}       # Atkins, J/mol bij 298 K
_S298 = {"NH3": 192.45, "N2": 191.61, "H2": 130.68}  # Atkins, J/(mol K)


def _H_mengsel(n, T):
    return sum(v * (_DHF[s] + _H_tab(s, T)) for s, v in n.items())


def _samenstelling(y0, x):
    """Per 100 mol voeding (3:1 H2/N2 + y0 NH3), na x mol gevormd NH3."""
    n0 = 100 * (1 - y0)
    return {"N2": n0 / 4 - x / 2, "H2": 3 * n0 / 4 - 1.5 * x, "NH3": 100 * y0 + x}


def _y(n):
    return n["NH3"] / sum(n.values())


def _T_adiabatisch(n_in, T_in, n_uit):
    H0 = _H_mengsel(n_in, T_in)
    lo, hi = 300.0, 1500.0
    for _ in range(60):
        T = (lo + hi) / 2
        if _H_mengsel(n_uit, T) > H0:
            hi = T
        else:
            lo = T
    return T


def _y_evenwicht(T, p=200.0):
    """Ideaal gas, 3:1 voeding zonder inerten, p in bar; K uit ΔH, ΔS en Cp-tabel."""
    d = [_CP_TAB["NH3"][i] - 0.5 * _CP_TAB["N2"][i] - 1.5 * _CP_TAB["H2"][i] for i in range(3)]
    T0 = 298.15
    dH = _DHF["NH3"] + d[0] * (T - T0) + d[1] / 2 * (T**2 - T0**2) + d[2] / 3 * (T**3 - T0**3)
    dS = (_S298["NH3"] - 0.5 * _S298["N2"] - 1.5 * _S298["H2"]
          + d[0] * np.log(T / T0) + d[1] * (T - T0) + d[2] / 2 * (T**2 - T0**2))
    K = np.exp(-(dH - T * dS) / (R * T))
    lo, hi = 0.0, 0.99
    for _ in range(60):
        y = (lo + hi) / 2
        f = y / (((1 - y) / 4) ** 0.5 * (3 * (1 - y) / 4) ** 1.5) / p - K
        lo, hi = (lo, y) if f > 0 else (y, hi)
    return y


def ammoniak_bedden():
    """Temperatuur en NH3-gehalte in een reactor met drie adiabatische katalysatorbedden en
    tussenkoeling (200 bar, voeding 400 °C met 3 % NH3). In elk bed stijgt T langs een rechte
    (eerste hoofdwet) tot dicht bij het evenwicht; koelen brengt het gas terug naar 400 °C."""
    fig, ax = figuur(7.2, 4.6)
    Tc = np.linspace(380, 620, 200)
    ax.plot(Tc, [100 * _y_evenwicht(t + 273.15) for t in Tc], color=K.zacht, lw=2.0, ls="--")
    label(ax, 545, 21, "evenwicht\n(hoofdstuk 6)", K.zacht, fontsize=10.5)
    T_in, y = 673.15, 0.03
    for bed in range(3):
        n_in = _samenstelling(y, 0.0)
        xs, Ts, ys = np.linspace(0, 60, 1201), [], []
        for x in xs:
            n = _samenstelling(y, x)
            T = _T_adiabatisch(n_in, T_in, n)
            if _y(n) >= _y_evenwicht(T) - 0.02:
                break
            Ts.append(T - 273.15); ys.append(100 * _y(n))
        ax.plot(Ts, ys, color=K.rood, lw=2.6)
        label(ax, Ts[-1] - 4, ys[-1] + 0.5, f"bed {bed + 1}", K.rood, va="bottom", ha="right",
              fontsize=10.5, fontweight="bold")
        y = ys[-1] / 100
        if bed < 2:
            ax.plot([Ts[-1], T_in - 273.15], [ys[-1], ys[-1]], color=K.blauw, lw=2.0)
            pijl(ax, (Ts[-1] - 30, ys[-1]), (Ts[-1] - 60, ys[-1]), K.blauw, lw=2.0)
    label(ax, 485, 10.9, "tussenkoeling", K.blauw, ha="center", va="top", fontsize=10.5)
    ax.set_xlim(380, 620)
    ax.set_ylim(0, 30)
    ax.set_xlabel("temperatuur (°C)")
    ax.set_ylabel("NH$_3$ in het gas (mol %)")
    return kader(fig)


# ================================================= experimentele vertrekpunten (H1)
def _schema(fig, ax):
    ax.set_axis_off()
    ax.set_aspect("equal")


def gaswetten():
    """(a) Wet van Boyle: p tegen 1/V is een rechte. (b) Wet van Charles: V tegen t, extrapolatie naar -273.15 °C."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 4.0))
    fig.get_layout_engine().set(w_pad=0.3)
    inv = np.linspace(0, 1.0, 50)  # 1/V in L^-1
    for i, T in enumerate([273, 373, 473]):
        k = K.warmte(i / 2)
        a1.plot(inv, 0.08314 * T * inv, color=k, lw=2)
        label(a1, 1.02, 0.08314 * T, f"{T} K", k, va="center", fontsize=10.5)
    a1.set_xlim(0, 1.2)
    a1.set_ylim(0, 42)
    a1.set_xlabel(r"$1/V$ (L$^{-1}$)")
    a1.set_ylabel(r"druk $p$ (bar)")
    a1.set_title(r"(a) Boyle: bij vaste $T$ is $p \propto 1/V$", fontsize=11.5, color=K.tekst)
    label(a1, 0.05, 37, r"1 mol gas", K.zacht, fontsize=10.5)
    t_m = np.linspace(0, 300, 50)
    t_x = np.linspace(-273.15, 0, 50)
    for n, k in [(1.0, K.blauw), (0.5, K.groen), (0.25, K.oker)]:
        a2.plot(t_m, 0.08314 * n * (t_m + 273.15), color=k, lw=2)
        a2.plot(t_x, 0.08314 * n * (t_x + 273.15), color=k, lw=1.2, ls=(0, (3, 2)))
        label(a2, 305, 0.08314 * n * 573.15, f"{n:g} mol", k, va="center", fontsize=10.5)
    a2.axvspan(0, 300, color=K.vlak_grijs, lw=0, zorder=0)
    label(a2, 150, 50, "gemeten", K.zacht, ha="center", fontsize=10.5)
    label(a2, -140, 50, "geëxtrapoleerd", K.zacht, ha="center", fontsize=10.5)
    a2.plot([-273.15], [0], "o", color=K.rood, ms=7, zorder=5)
    pijl(a2, (-200, 30), (-271, 1.5), K.rood, lw=1.2)
    label(a2, -200, 31, r"$-273.15$ °C = 0 K", K.rood, ha="center", va="bottom", fontsize=10.5)
    a2.set_xlim(-300, 370)
    a2.set_ylim(0, 54)
    a2.set_xlabel(r"temperatuur $t$ (°C)")
    a2.set_ylabel(r"volume $V$ (L) bij 1 bar")
    a2.set_title("(b) Charles: bij vaste $p$ is $V \\propto T$", fontsize=11.5, color=K.tekst)
    return kader(fig)


def joule_thomson():
    """Proef van Joule en Thomson: gas wordt door een poreuze prop geperst; de temperatuur daalt."""
    fig, ax = figuur(8.4, 3.0)
    _schema(fig, ax)
    ax.set_aspect("auto")
    ax.add_patch(plt.Rectangle((0.3, 0.55), 9.4, 1.5, fc=K.vlak_grijs, ec=K.zacht, lw=1, hatch="///", alpha=0.6))
    ax.add_patch(plt.Rectangle((0.5, 0.75), 9.0, 1.1, fc=K.achtergrond, ec=K.as_, lw=1.6))
    label(ax, 5.0, 2.12, "isolatie: geen warmte-uitwisseling ($Q = 0$)", K.zacht, ha="center", va="bottom",
          fontsize=10.5)
    ax.add_patch(plt.Rectangle((4.7, 0.75), 0.6, 1.1, fc=K.vlak_oker, ec=K.oker, lw=1.4, hatch="..."))
    label(ax, 5.0, 0.62, "poreuze prop\n(of ventiel)", K.oker, ha="center", va="top", fontsize=10.5)
    ax.add_patch(plt.Rectangle((1.1, 0.75), 0.18, 1.1, fc=K.zacht, ec=K.as_))
    ax.add_patch(plt.Rectangle((8.6, 0.75), 0.18, 1.1, fc=K.zacht, ec=K.as_))
    pijl(ax, (0.6, 1.3), (1.05, 1.3), K.tekst, lw=1.6)
    pijl(ax, (8.85, 1.3), (9.4, 1.3), K.tekst, lw=1.6)
    rng = np.random.default_rng(4)
    for x, y in zip(rng.uniform(1.45, 4.55, 34), rng.uniform(0.85, 1.75, 34)):
        ax.add_patch(plt.Circle((x, y), 0.04, fc=K.rood, ec="none"))
    for x, y in zip(rng.uniform(5.45, 8.45, 12), rng.uniform(0.85, 1.75, 12)):
        ax.add_patch(plt.Circle((x, y), 0.04, fc=K.blauw, ec="none"))
    label(ax, 2.9, 2.5, r"hoge druk $p_1$, temperatuur $T_1$", K.rood, ha="center", fontsize=11)
    label(ax, 7.0, 2.5, r"lage druk $p_2$, temperatuur $T_2$", K.blauw, ha="center", fontsize=11)
    label(ax, 5.0, -0.25, r"luchtvoorbeeld: van 200 naar 1 bar koelt het gas ongeveer 40 K af",
          K.tekst, ha="center", fontsize=10.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 2.9)
    return kader(fig)


def joule_proef():
    """Proef van Joule: een dalend gewicht drijft een schoepenrad aan in geïsoleerd water."""
    fig, ax = figuur(6.4, 4.4)
    _schema(fig, ax)
    # vat
    ax.add_patch(plt.Rectangle((0.6, 0.4), 3.6, 2.6, fc=K.vlak_grijs, ec=K.zacht, lw=1, hatch="///", alpha=0.6))
    ax.add_patch(plt.Rectangle((0.8, 0.6), 3.2, 2.2, fc=K.vlak_blauw, ec=K.as_, lw=1.6))
    label(ax, 2.4, 0.15, "geïsoleerd vat met water", K.blauw, ha="center", va="top", fontsize=10.5)
    # as en schoepen
    ax.plot([2.4, 2.4], [1.0, 4.1], color=K.as_, lw=2.4)
    for y in (1.2, 1.7, 2.2):
        ax.add_patch(plt.Rectangle((1.6, y - 0.08), 1.6, 0.16, fc=K.zacht, ec=K.as_, lw=1))
    pijl(ax, (4.5, 2.5), (3.15, 2.2), K.tekst, lw=1.0)
    label(ax, 4.55, 2.5, "schoepenrad", K.tekst, va="center", fontsize=10)
    # trommel en touw
    ax.add_patch(plt.Rectangle((2.15, 3.7), 0.5, 0.4, fc=K.vlak_oker, ec=K.oker, lw=1.4))
    ax.plot([2.65, 5.6], [4.05, 4.05], color=K.as_, lw=1.2)
    ax.add_patch(plt.Circle((5.75, 3.9), 0.18, fc="none", ec=K.as_, lw=1.4))
    ax.plot([5.93, 5.93], [3.9, 2.2], color=K.as_, lw=1.2)
    ax.add_patch(plt.Rectangle((5.6, 1.5), 0.66, 0.7, fc=K.vlak_rood, ec=K.rood, lw=1.6))
    label(ax, 5.93, 1.85, "$m$", K.rood, ha="center", va="center", fontsize=12)
    pijl(ax, (6.6, 2.2), (6.6, 0.9), K.rood, lw=1.8)
    label(ax, 6.75, 1.55, "valt over\nhoogte $h$", K.rood, va="center", fontsize=10.5)
    # thermometer
    ax.add_patch(plt.Rectangle((1.05, 1.0), 0.14, 2.6, fc=K.achtergrond, ec=K.as_, lw=1.2))
    ax.add_patch(plt.Rectangle((1.07, 1.0), 0.10, 1.4, fc=K.rood, ec="none"))
    label(ax, 1.12, 3.7, "thermometer", K.tekst, ha="center", va="bottom", fontsize=10)
    label(ax, 3.0, 4.45, r"arbeid $W = mgh$  $\rightarrow$  $\Delta T\,$ van het water", K.tekst, fontsize=10.5)
    ax.set_xlim(0.3, 8.0)
    ax.set_ylim(-0.2, 4.7)
    return kader(fig)


def bomcalorimeter():
    """Bomcalorimeter: verbranding bij constant volume in een stalen bom, omringd door water."""
    fig, ax = figuur(6.6, 4.6)
    _schema(fig, ax)
    ax.add_patch(plt.Rectangle((0.3, 0.3), 5.4, 4.0, fc=K.vlak_grijs, ec=K.zacht, lw=1, hatch="///", alpha=0.6))
    label(ax, 3.0, 4.38, "isolerende mantel", K.zacht, ha="center", va="bottom", fontsize=10)
    ax.add_patch(plt.Rectangle((0.6, 0.6), 4.8, 3.3, fc=K.vlak_blauw, ec=K.as_, lw=1.6))
    label(ax, 4.6, 0.8, "water", K.blauw, ha="center", fontsize=10.5)
    # bom
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((2.0, 0.9), 1.8, 2.2, boxstyle="round,pad=0,rounding_size=0.25",
                                fc=K.vlak_accent, ec=K.as_, lw=2.4))
    label(ax, 2.9, 3.2, "stalen bom\n(O$_2$, 30 bar)", K.accent, ha="center", va="bottom", fontsize=10)
    ax.add_patch(plt.Rectangle((2.55, 1.3), 0.7, 0.2, fc=K.zacht, ec=K.as_))
    ax.add_patch(plt.Rectangle((2.65, 1.5), 0.5, 0.18, fc=K.vlak_oker, ec=K.oker))
    label(ax, 2.9, 1.15, "staal", K.oker, ha="center", va="top", fontsize=9.5)
    ax.plot([2.35, 2.35, 2.75], [3.1, 1.85, 1.62], color=K.rood, lw=1.2)
    ax.plot([3.45, 3.45, 3.05], [3.1, 1.85, 1.62], color=K.rood, lw=1.2)
    label(ax, 3.55, 2.4, "ontstekings-\ndraad", K.rood, fontsize=9.5, va="center")
    # roerder en thermometer
    ax.plot([1.2, 1.2], [1.0, 4.6], color=K.as_, lw=1.8)
    ax.add_patch(plt.Rectangle((0.95, 1.0), 0.5, 0.12, fc=K.zacht, ec=K.as_))
    label(ax, 1.2, 4.65, "roerder", K.tekst, ha="center", va="bottom", fontsize=10)
    ax.add_patch(plt.Rectangle((4.75, 1.4), 0.14, 3.2, fc=K.achtergrond, ec=K.as_, lw=1.2))
    ax.add_patch(plt.Rectangle((4.77, 1.4), 0.10, 1.6, fc=K.rood, ec="none"))
    label(ax, 4.82, 4.65, "thermometer", K.tekst, ha="center", va="bottom", fontsize=10)
    label(ax, 6.0, 2.6, "constant volume:\n" + r"$q_V = \Delta U$" + "\n\n" + r"$q_V = C_\mathrm{cal}\,\Delta T$",
          K.tekst, va="center", fontsize=11)
    ax.set_xlim(0.1, 8.0)
    ax.set_ylim(0.1, 5.1)
    return kader(fig)
