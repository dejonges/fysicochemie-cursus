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


def isothermen_vergelijking():
    """Ideaal gas (links) naast CO2 (rechts): waar de ideale gaswet faalt."""
    fig, (ax1, ax2) = figuur(12.4, 4.8, ncols=2)
    _boyle(ax1)
    _isothermen_co2(ax2)
    ax1.set_title("ideaal gas", fontsize=12.5)
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
