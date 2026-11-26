"""Figuren hoofdstuk 1 – Energie en de eerste hoofdwet."""
import numpy as np
import matplotlib.pyplot as plt

from huisstijl import K, figuur, kader, label, pijl, achter, toon  # noqa: F401
import toestand as ts

R = ts.R


# ------------------------------------------------------------------ Boyle
def boyle():
    """Isothermen van een ideaal gas (1 mol)."""
    fig, ax = figuur(6.4, 4.6)
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
    return kader(fig)


# ------------------------------------------------- CO2-isothermen (reëel gas)
def isothermen_co2():
    """Isothermen van CO2 met condensatiegebied (Peng-Robinson)."""
    fig, ax = figuur(6.6, 4.8)
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
    """Isotherme vs. adiabatische compressie van lucht van 1 naar 8 bar."""
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
    label(ax, V_iso[-1] - 0.25, 8.25, f"{T1 - 273.15:.0f} °C", K.blauw, ha="center", fontsize=11)
    label(ax, V_ad[-1] + 0.25, 8.25, f"{T2 - 273.15:.0f} °C", K.rood, ha="center", fontsize=11)
    label(ax, 10.5, 4.6, "extra arbeid die als warmte\nin het gas terechtkomt", K.oker,
          fontsize=11, ha="left", va="center")
    pijl(ax, (10.3, 4.45), (7.6, 3.5), K.oker, lw=1.3)
    ax.legend(loc="upper right")
    ax.set_xlim(0, V1 * 1.12)
    ax.set_ylim(0, 9.2)
    ax.set_xlabel("volume $V$ (L, 1 mol lucht)")
    ax.set_ylabel("druk $p$ (bar)")
    return kader(fig)
