"""Figuren hoofdstuk 5 – Niet-reagerend evenwicht (fasediagrammen)."""
import numpy as np

from huisstijl import K, figuur, kader, label, pijl  # noqa: F401

# Antoine (log10 p/mmHg, T in °C), NIST/Yaws, geldig ca. 0-150 °C
_ANTOINE = {"benzeen": (6.90565, 1211.033, 220.790), "tolueen": (6.95464, 1344.800, 219.482)}


def _psat(stof, T):
    A, B, C = _ANTOINE[stof]
    return 10 ** (A - B / (T + C)) * 1.01325 / 760  # bar


def _T_bubbel(x, P=1.01325):
    lo, hi = 60.0, 130.0
    for _ in range(60):
        T = (lo + hi) / 2
        if x * _psat("benzeen", T) + (1 - x) * _psat("tolueen", T) > P:
            hi = T
        else:
            lo = T
    return T


# ------------------------------------------------------- fasediagram water
def fasediagram():
    """p-T-fasediagram van water (logaritmische drukas, semi-kwantitatief)."""
    fig, ax = figuur(6.6, 4.8)
    Ttp, ptp = 273.16, 611.657
    Tc, pc = 647.1, 22.064e6
    # dampdruklijn: Clausius-Clapeyron door tripelpunt en kritisch punt
    T = np.linspace(Ttp, Tc, 300)
    B = np.log(pc / ptp) / (1 / Ttp - 1 / Tc)
    pv = ptp * np.exp(-B * (1 / T - 1 / Ttp))
    # sublimatielijn: dHsub = 51.1 kJ/mol
    Ts = np.linspace(200, Ttp, 100)
    ps = ptp * np.exp(-51100 / 8.314 * (1 / Ts - 1 / Ttp))
    # smeltlijn (licht negatieve helling, overdreven voor zichtbaarheid)
    pm = np.logspace(np.log10(ptp), 9, 100)
    Tm = Ttp - 7.4e-8 * (pm - ptp) * 3
    ax.semilogy(T - 273.15, pv, color=K.blauw, lw=2.4)
    ax.semilogy(Ts - 273.15, ps, color=K.paars, lw=2.4)
    ax.semilogy(Tm - 273.15, pm, color=K.accent, lw=2.4)
    ax.plot(Ttp - 273.15, ptp, "o", color=K.tekst, ms=7, zorder=5)
    ax.plot(Tc - 273.15, pc, "o", color=K.rood, ms=7, zorder=5)
    label(ax, 8, 260, "tripelpunt\n0.01 °C, 611 Pa", K.tekst, fontsize=10.5, va="top")
    label(ax, Tc - 273.15 - 8, pc * 2.2, "kritisch punt\n374 °C, 221 bar", K.rood, fontsize=10.5, ha="right")
    ax.axhline(101325, color=K.zacht, lw=1, ls=(0, (3, 3)))
    label(ax, -70, 1.4e5, "1 atm", K.zacht, fontsize=10)
    ax.plot(100, 101325, "o", color=K.blauw, ms=5)
    label(ax, 106, 6e4, "100 °C", K.blauw, fontsize=10)
    label(ax, -60, 1e6, "vast (ijs)", K.tekst, fontsize=12)
    label(ax, 120, 2e7, "vloeistof", K.tekst, fontsize=12)
    label(ax, 180, 3e3, "gas (damp)", K.tekst, fontsize=12)
    label(ax, 420, 1e8, "superkritisch", K.rood, fontsize=11)
    ax.set_xlim(-75, 480)
    ax.set_ylim(1, 1e9)
    ax.set_xlabel("temperatuur (°C)")
    ax.set_ylabel("druk (Pa)")
    return kader(fig)


# ---------------------------------------------------------- Pxy en Txy
def pxy_benzeen_tolueen():
    """P-x-y bij 90 °C (Raoult) met hefboomlijn voor z = 0.50."""
    fig, ax = figuur(6.4, 4.6)
    T = 90.0
    pA, pB = _psat("benzeen", T), _psat("tolueen", T)
    x = np.linspace(0, 1, 200)
    P = x * pA + (1 - x) * pB
    y = x * pA / P
    ax.fill_between(np.r_[x, y[::-1]], np.r_[P, P[::-1]], color=K.vlak_blauw, lw=0)
    ax.plot(x, P, color=K.blauw, lw=2.4, label="bubbelpuntlijn $P(x)$")
    ax.plot(y, P, color=K.rood, lw=2.4, label="dauwpuntlijn $P(y)$")
    Pz = 0.4 * pA + 0.6 * pB
    yz = 0.4 * pA / Pz
    ax.plot([0.4, yz], [Pz, Pz], color=K.tekst, lw=1.4)
    for xx, k in [(0.4, K.blauw), (0.5, K.tekst), (yz, K.rood)]:
        ax.plot(xx, Pz, "o", color=k, ms=6, zorder=5)
    label(ax, 0.40, Pz - 0.07, "$x_A$=0.40", K.blauw, ha="center", fontsize=10)
    label(ax, 0.50, Pz + 0.03, "$z_A$=0.50", K.tekst, ha="center", fontsize=10)
    label(ax, yz + 0.01, Pz - 0.07, f"$y_A$={yz:.2f}", K.rood, fontsize=10)
    label(ax, 0.50, 1.36, "vloeistof", K.tekst, fontsize=12)
    label(ax, 0.62, 0.62, "damp", K.tekst, fontsize=12)
    label(ax, 0.62, 0.98, "L + V", K.blauw, fontsize=11)
    ax.legend(loc="upper left", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.4, 1.5)
    ax.set_xlabel("molfractie benzeen $x_A$, $y_A$")
    ax.set_ylabel("druk $P$ (bar)")
    ax.set_title("benzeen–tolueen bij 90 °C", fontsize=12)
    return kader(fig)


def txy_benzeen_tolueen():
    """T-x-y en x-y bij 1 atm (Raoult + Antoine)."""
    fig, (ax, ax2) = figuur(9.6, 4.4, ncols=2)
    x = np.linspace(0, 1, 101)
    T = np.array([_T_bubbel(xi) for xi in x])
    y = x * _psat("benzeen", T) / 1.01325
    ax.fill_between(np.r_[x, y[::-1]], np.r_[T, T[::-1]], color=K.vlak_rood, lw=0)
    ax.plot(x, T, color=K.blauw, lw=2.4, label="bubbelpuntlijn")
    ax.plot(y, T, color=K.rood, lw=2.4, label="dauwpuntlijn")
    label(ax, 0.08, 86, "vloeistof", K.tekst, fontsize=11)
    label(ax, 0.62, 106, "damp", K.tekst, fontsize=11)
    ax.legend(loc="lower left", fontsize=10)
    ax.set_ylim(70, 115)
    ax.set_xlim(0, 1)
    ax.set_xlabel("molfractie benzeen")
    ax.set_ylabel("temperatuur (°C)")
    ax.set_title("$T$–$x$–$y$ bij 1 atm", fontsize=12)
    ax2.plot(x, y, color=K.accent, lw=2.4)
    ax2.plot([0, 1], [0, 1], color=K.zacht, lw=1, ls=(0, (3, 3)))
    label(ax2, 0.55, 0.42, "diagonaal $y = x$", K.zacht, fontsize=10)
    label(ax2, 0.12, 0.62, "evenwichtslijn", K.accent, fontsize=11)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect("equal")
    ax2.set_xlabel("$x$ benzeen (vloeistof)")
    ax2.set_ylabel("$y$ benzeen (damp)")
    ax2.set_title("$x$–$y$-diagram", fontsize=12)
    return kader(fig)


# ----------------------------------------------------- Raoult versus Henry
def raoult_henry():
    """Partiële dampdruk van een component met positieve afwijking (Margules A = 1.2)."""
    fig, ax = figuur(6.4, 4.6)
    A, pstar = 1.2, 1.0
    x = np.linspace(0, 1, 200)
    p = x * np.exp(A * (1 - x) ** 2) * pstar
    H = np.exp(A) * pstar
    ax.plot(x, p, color=K.tekst, lw=2.6, label="werkelijke $p_i$")
    ax.plot(x, x * pstar, color=K.blauw, lw=1.6, ls=(0, (5, 3)), label=r"Raoult: $p_i = x_i\,p_i^*$")
    xs = np.linspace(0, 0.45, 50)
    ax.plot(xs, xs * H, color=K.rood, lw=1.6, ls=(0, (5, 3)), label=r"Henry: $p_i = x_i\,H_i$")
    ax.plot(1, pstar, "o", color=K.blauw, ms=6)
    label(ax, 0.96, pstar + 0.06, "$p_i^*$", K.blauw, ha="right", fontsize=11)
    label(ax, 0.06, 0.05, "verdund: Henry geldt", K.rood, fontsize=10.5)
    label(ax, 0.66, 0.40, "bijna zuiver:\nRaoult geldt", K.blauw, fontsize=10.5)
    ax.legend(loc="upper left", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.6)
    ax.set_xlabel("molfractie $x_i$ in de vloeistof")
    ax.set_ylabel(r"partiële druk $p_i\,/\,p_i^*$")
    return kader(fig)


# ------------------------------------------------------------- eutecticum
def eutecticum():
    """Eutectisch diagram Pb-Sn (vereenvoudigd: geen vaste oplosbaarheid)."""
    fig, ax = figuur(6.4, 4.6)
    TPb, TSn, Te, we = 327.5, 232.0, 183.0, 61.9
    ax.plot([0, we], [TPb, Te], color=K.rood, lw=2.4)
    ax.plot([we, 100], [Te, TSn], color=K.rood, lw=2.4)
    ax.plot([0, 100], [Te, Te], color=K.tekst, lw=1.6)
    ax.plot(we, Te, "o", color=K.rood, ms=7, zorder=5)
    label(ax, we, Te - 22, "eutecticum\n61.9 % Sn, 183 °C", K.rood, ha="center", fontsize=10.5, va="top")
    label(ax, 45, 290, "vloeistof", K.tekst, fontsize=12)
    label(ax, 8, 215, "vloeistof\n+ vast Pb", K.blauw, fontsize=10.5)
    label(ax, 84, 190, "L + Sn", K.blauw, fontsize=10)
    label(ax, 30, 120, "vast Pb + vast Sn", K.tekst, fontsize=11)
    label(ax, 1, TPb + 6, "327 °C", K.tekst, fontsize=10)
    label(ax, 99, TSn + 6, "232 °C", K.tekst, fontsize=10, ha="right")
    ax.set_xlim(0, 100)
    ax.set_ylim(50, 360)
    ax.set_xlabel("massa-% tin")
    ax.set_ylabel("temperatuur (°C)")
    return kader(fig)


# ------------------------------------------------------------- ternair
# benaderende LLE-gegevens water (W) – aceton (A) – MIBK (S) bij 25 °C, massafracties (A, W)
_RAF = [(0.00, 0.98), (0.05, 0.93), (0.10, 0.875), (0.15, 0.82), (0.20, 0.77), (0.25, 0.71),
        (0.30, 0.655), (0.35, 0.59), (0.40, 0.52), (0.45, 0.43)]
_EXT = [(0.00, 0.02), (0.06, 0.025), (0.12, 0.03), (0.19, 0.04), (0.26, 0.05), (0.32, 0.065),
        (0.38, 0.08), (0.43, 0.10), (0.47, 0.13), (0.49, 0.17)]
_PLOOI = (0.48, 0.27)


def _xy(A, W):
    """Driehoek: W linksonder (0,0), S rechtsonder (1,0), A boven."""
    S = 1 - A - W
    return S + A / 2, A * np.sqrt(3) / 2


def _ternair_menging(zA=0.15, zW=0.35):
    """Bindlijn door het mengpunt (lineaire interpolatie tussen bindlijnen)."""
    def door(i, t):
        r = np.array(_RAF[i]) + t * (np.array(_RAF[i + 1]) - np.array(_RAF[i]))
        e = np.array(_EXT[i]) + t * (np.array(_EXT[i + 1]) - np.array(_EXT[i]))
        return r, e
    best = None
    for i in range(len(_RAF) - 1):
        for t in np.linspace(0, 1, 201):
            r, e = door(i, t)
            # afstand van M tot lijn R-E in (A, W)-coördinaten
            u, v = e - r, np.array([zA, zW]) - r
            d = (u[0] * v[1] - u[1] * v[0]) / np.linalg.norm(u)
            if best is None or abs(d) < best[0]:
                best = (abs(d), r, e)
    return best[1], best[2]


def ternair():
    """Ternair diagram water–aceton–MIBK met binodaal, bindlijnen en een extractievoorbeeld."""
    fig, ax = figuur(6.6, 5.8)
    h = np.sqrt(3) / 2
    ax.plot([0, 1, 0.5, 0], [0, 0, h, 0], color=K.tekst, lw=1.4)
    for f in np.arange(0.1, 1.0, 0.1):  # rasterlijnen
        for a, b in [((f, 1 - f), (f, 0)), ((0, f), (1 - f, f)), ((f, 0), (0, 1 - f))]:
            p1, p2 = _xy(a[0], a[1]), _xy(b[0], b[1])
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=K.rand, lw=0.6, zorder=0)
    pts = _RAF + [_PLOOI] + _EXT[::-1]
    X, Y = zip(*[_xy(a, w) for a, w in pts])
    ax.fill(X, Y, color=K.vlak_blauw, lw=0, zorder=1)
    ax.plot(X, Y, color=K.blauw, lw=2.2, zorder=2)
    for (ra, rw), (ea, ew) in list(zip(_RAF, _EXT))[1::2]:
        p1, p2 = _xy(ra, rw), _xy(ea, ew)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=K.blauw, lw=0.9, alpha=0.8, zorder=2)
    pp = _xy(*_PLOOI)
    ax.plot(*pp, "o", color=K.blauw, ms=5, zorder=4)
    label(ax, pp[0] + 0.03, pp[1] + 0.01, "plooipunt", K.blauw, fontsize=10)
    # extractievoorbeeld: F (30 % aceton in water) + S (zuiver MIBK) -> M -> R + E
    F, S, M = _xy(0.30, 0.70), _xy(0.0, 0.0), _xy(0.15, 0.35)
    ax.plot([F[0], S[0]], [F[1], S[1]], color=K.oker, lw=1.4, ls=(0, (4, 3)), zorder=3)
    r, e = _ternair_menging()
    R, E = _xy(*r), _xy(*e)
    ax.plot([R[0], E[0]], [R[1], E[1]], color=K.rood, lw=1.8, zorder=3)
    for P, n, k, dx, dy in [(F, "F", K.oker, -0.05, 0.0), (S, "S", K.oker, 0.0, -0.05), (M, "M", K.oker, 0.0, 0.03),
                            (R, "R", K.rood, -0.05, 0.0), (E, "E", K.rood, 0.02, 0.0)]:
        ax.plot(*P, "o", color=k, ms=6, zorder=5)
        label(ax, P[0] + dx, P[1] + dy, n, k, fontsize=11, ha="center", va="center")
    label(ax, -0.02, -0.05, "water", K.tekst, fontsize=11, ha="center", va="top")
    label(ax, 1.02, -0.05, "MIBK", K.tekst, fontsize=11, ha="center", va="top")
    label(ax, 0.5, h + 0.03, "aceton", K.tekst, fontsize=11, ha="center")
    label(ax, 0.5, 0.06, "twee vloeistoffasen", K.blauw, fontsize=10.5, ha="center")
    label(ax, 0.62, 0.55, "één fase", K.tekst, fontsize=11)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.1, h + 0.08)
    ax.set_aspect("equal")
    ax.axis("off")
    return kader(fig)


def mu_temperatuur():
    """μ(T) bij 1 bar voor ijs, water en damp; helling = -S_m."""
    fig, ax = figuur(6.4, 4.4)
    Tm, Tb = 273.15, 373.15
    S = {"vast": 41.0, "vloeistof": 70.0, "gas": 189.0}
    # kies mu_vloeistof(Tm) = 0; dan mu_vast(Tm) = 0, mu_gas(Tb) = mu_vl(Tb)
    T = np.linspace(200, 450, 300)
    mu_l = -S["vloeistof"] * (T - Tm) / 1000
    mu_s = -S["vast"] * (T - Tm) / 1000
    mu_lb = -S["vloeistof"] * (Tb - Tm) / 1000
    mu_g = mu_lb - S["gas"] * (T - Tb) / 1000
    stabiel = np.minimum(np.minimum(mu_s, mu_l), mu_g)
    for mu, k, nm, x, y in [(mu_s, K.blauw, "vaste stof", 222, -0.6), (mu_l, K.accent, "vloeistof", 322, -6.0),
                            (mu_g, K.rood, "gas", 402, -10.5)]:
        ax.plot(T, mu, color=k, lw=1.3, ls="--")
        label(ax, x, y, nm, k, ha="left", fontsize=11.5)
    ax.plot(T, stabiel, color=K.tekst, lw=3, alpha=0.85)
    for Tx, nm in [(Tm, "smeltpunt\n273 K"), (Tb, "kookpunt\n373 K")]:
        ax.axvline(Tx, color=K.zacht, lw=0.8, ls=":")
        label(ax, Tx + 3, 4.2, nm, K.zacht, fontsize=10.5, va="top")
    ax.set_xlim(200, 450)
    ax.set_ylim(-12, 5)
    ax.set_yticks([])
    ax.set_xlabel("temperatuur $T$ (K)")
    ax.set_ylabel(r"chemische potentiaal $\mu$")
    return kader(fig)


_ANTOINE_MEER = {  # log10 p/mmHg, T in °C (Dortmund/Yaws, ca. 0-150 °C)
    "water": (8.07131, 1730.63, 233.426),
    "ethanol": (8.20417, 1642.89, 230.300),
    "aceton": (7.11714, 1210.595, 229.664),
}


def dampdruk():
    """Dampdruk p*(T) van enkele vloeistoffen; snijpunt met 1 atm = normaal kookpunt."""
    fig, ax = figuur(6.4, 4.4)
    T = np.linspace(0, 120, 300)
    reeks = [("aceton", K.oker, _ANTOINE_MEER["aceton"]), ("benzeen", K.rood, _ANTOINE["benzeen"]),
             ("ethanol", K.groen, _ANTOINE_MEER["ethanol"]), ("tolueen", K.paars, _ANTOINE["tolueen"]),
             ("water", K.blauw, _ANTOINE_MEER["water"])]
    for nm, k, (A, B, C) in reeks:
        p = 10 ** (A - B / (T + C)) * 1.01325 / 760
        Tb = B / (A - np.log10(760)) - C
        ax.plot(T, p, color=k, lw=2.2, label=f"{nm} ({Tb:.0f} °C)")
        ax.plot(Tb, 1.01325, "o", color=k, ms=6, zorder=5)
    ax.legend(loc="upper left", fontsize=10, title="normaal kookpunt", title_fontsize=10)
    ax.axhline(1.01325, color=K.zacht, lw=0.9, ls=":")
    label(ax, 128, 0.97, "1 atm", K.zacht, fontsize=10, va="top", ha="right")
    ax.set_xlim(0, 130)
    ax.set_ylim(0, 2.0)
    ax.set_xlabel("temperatuur (°C)")
    ax.set_ylabel("dampdruk $p^*$ (bar)")
    return kader(fig)


def mengen_G():
    """ΔG_meng/RT voor een ideaal en een regelmatig mengsel (χ = ΔH-parameter / RT)."""
    fig, ax = figuur(6.4, 4.4)
    x = np.linspace(1e-4, 1 - 1e-4, 400)
    ideaal = x * np.log(x) + (1 - x) * np.log(1 - x)
    for chi, k, nm in [(0, K.accent, "ideaal ($\\Delta H_\\mathrm{meng}=0$)"), (1.5, K.oker, "zwak endotherm"),
                       (2.7, K.rood, "sterk endotherm: ontmenging")]:
        g = ideaal + chi * x * (1 - x)
        ax.plot(x, g, color=k, lw=2.2, label=nm)
    # dubbele raaklijn voor chi = 2.7 (symmetrisch: horizontaal door de minima)
    g = ideaal + 2.7 * x * (1 - x)
    i = np.argmin(g[: len(x) // 2])
    ax.plot([x[i], 1 - x[i]], [g[i], g[i]], color=K.rood, lw=1, ls="--")
    ax.plot([x[i], 1 - x[i]], [g[i], g[i]], "o", color=K.rood, ms=6)
    label(ax, 0.5, g[i] - 0.03, "twee fasen", K.rood, ha="center", va="top", fontsize=10.5)
    ax.axhline(0, color=K.as_, lw=0.8)
    ax.legend(loc="lower center", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.75, 0.12)
    ax.set_xlabel("molfractie $x_B$")
    ax.set_ylabel(r"$\Delta G_\mathrm{meng}/nRT$")
    return kader(fig)


def azeotroop():
    """P-x-y bij constante T voor Margules A = +1.4 en A = -1.4: drukmaximum en drukminimum."""
    fig, axs = figuur(9.6, 4.4, ncols=2)
    pA, pB = 1.0, 0.75
    x = np.linspace(0, 1, 300)
    for ax, A, titel in [(axs[0], 1.4, "positieve afwijking ($\\gamma > 1$)"),
                         (axs[1], -1.4, "negatieve afwijking ($\\gamma < 1$)")]:
        gA, gB = np.exp(A * (1 - x) ** 2), np.exp(A * x ** 2)
        P = x * gA * pA + (1 - x) * gB * pB
        y = x * gA * pA / P
        ax.plot([0, 1], [pB, pA], color=K.zacht, lw=1.2, ls="--")
        ax.plot(x, P, color=K.blauw, lw=2.4, label="bubbelpunt $P(x)$")
        ax.plot(y, P, color=K.rood, lw=2.4, label="dauwpunt $P(y)$")
        i = np.argmax(P) if A > 0 else np.argmin(P)
        ax.plot(x[i], P[i], "o", color=K.tekst, ms=7, zorder=5)
        dy = 0.06 if A > 0 else -0.06
        label(ax, x[i], P[i] + dy, "azeotroop: $x = y$", K.tekst, ha="center",
              va="bottom" if A > 0 else "top", fontsize=10.5)
        label(ax, 0.5, 0.5 * (pA + pB) + (-0.05 if A > 0 else 0.05), "Raoult", K.zacht, ha="center",
              va="top" if A > 0 else "bottom", fontsize=10)
        ax.set_title(titel, fontsize=12)
        ax.set_xlim(0, 1)
        ax.set_xlabel("molfractie $x_A$, $y_A$")
        ax.legend(loc="lower right" if A > 0 else "upper left", fontsize=9.5)
    axs[0].set_ylim(0.6, 1.45)
    axs[1].set_ylim(0.3, 1.1)
    axs[0].set_ylabel("druk $P$ (bar)")
    return kader(fig)


def margules():
    """Activiteitscoëfficiënten volgens Margules (één parameter)."""
    fig, ax = figuur(6.4, 4.2)
    x = np.linspace(0, 1, 200)
    for A, k in [(1.4, K.rood), (-1.4, K.blauw)]:
        ax.plot(x, np.exp(A * (1 - x) ** 2), color=k, lw=2.4)
        ax.plot(x, np.exp(A * x ** 2), color=k, lw=2.4, ls="--")
    ax.axhline(1, color=K.zacht, lw=1)
    label(ax, 0.06, 4.0, "$\\gamma_A^\\infty = e^{A}$", K.rood, fontsize=10.5, va="center")
    label(ax, 0.5, 2.2, "$A = +1.4$", K.rood, ha="center", fontsize=11)
    label(ax, 0.5, 0.3, "$A = -1.4$", K.blauw, ha="center", fontsize=11)
    label(ax, 0.98, 1.08, "ideaal", K.zacht, ha="right", fontsize=10)
    ax.plot([], [], color=K.tekst, lw=2, label="$\\gamma_A$")
    ax.plot([], [], color=K.tekst, lw=2, ls="--", label="$\\gamma_B$")
    ax.legend(loc="upper center", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.3)
    ax.set_xlabel("molfractie $x_A$")
    ax.set_ylabel("activiteitscoëfficiënt $\\gamma$")
    return kader(fig)
