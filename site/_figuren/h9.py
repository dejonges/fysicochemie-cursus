"""Figuren hoofdstuk 9 – Chemische kinetiek."""
import numpy as np

from huisstijl import K, figuur, kader, label, pijl  # noqa: F401

_R = 8.314


def ordes():
    """[A](t) voor nulde, eerste en tweede orde met dezelfde beginsnelheid."""
    fig, ax = figuur(6.4, 4.2)
    t = np.linspace(0, 10, 300)
    A0, r0 = 1.0, 0.2
    nul = np.clip(A0 - r0 * t, 0, None)
    een = A0 * np.exp(-r0 / A0 * t)
    twee = 1 / (1 / A0 + r0 / A0**2 * t)
    ax.plot(t, nul, color=K.rood, lw=2.4)
    ax.plot(t, een, color=K.accent, lw=2.4)
    ax.plot(t, twee, color=K.oker, lw=2.4)
    label(ax, 5.2, 0.04, "nulde orde (rechte)", K.rood, fontsize=10.5)
    label(ax, 6.2, 0.13, "eerste orde (exponentieel)", K.accent, fontsize=10.5)
    label(ax, 6.2, 0.47, "tweede orde (traag staartje)", K.oker, fontsize=10.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("tijd (willekeurige eenheid)")
    ax.set_ylabel("$[A]/[A]_0$")
    return kader(fig)


def arrhenius():
    """Arrheniusgrafiek: ln k tegen 1/T voor een lage en een hoge activeringsenergie."""
    fig, ax = figuur(6.4, 4.2)
    T1, k1, T2, k2 = 300, 1.5e-3, 350, 6.0e-2
    Ea = -_R * np.log(k2 / k1) / (1 / T2 - 1 / T1)
    lnA = np.log(k1) + Ea / (_R * T1)
    x = np.linspace(2.7e-3, 3.45e-3, 50)
    ax.plot(x * 1e3, lnA - Ea / _R * x, color=K.accent, lw=2.4)
    ax.plot([1e3 / T1, 1e3 / T2], [np.log(k1), np.log(k2)], "o", color=K.accent, ms=7)
    # steilere rechte, Ea = 150 kJ/mol, zelfde k bij 350 K
    Eb = 150e3
    lnAb = np.log(k2) + Eb / (_R * T2)
    ax.plot(x * 1e3, lnAb - Eb / _R * x, color=K.rood, lw=2.0, ls=(0, (5, 3)))
    label(ax, 3.05, -2.2, f"$E_a$ = {Ea / 1e3:.0f} kJ/mol\nhelling $-E_a/R$", K.accent, fontsize=10.5)
    label(ax, 2.72, -9.5, "$E_a$ = 150 kJ/mol:\nveel gevoeliger voor $T$", K.rood, fontsize=10.5)
    ax.set_xlabel("$1000/T$ (K$^{-1}$)")
    ax.set_ylabel("$\\ln k$")
    ax.set_xlim(2.7, 3.45)
    ax.set_ylim(-14, 1)
    return kader(fig)


def maxwell_boltzmann():
    """Snelheidsverdeling van N2 bij 300 K en 1000 K."""
    fig, ax = figuur(6.4, 4.0)
    M = 0.028
    v = np.linspace(0, 2000, 500)
    for T, kl, x0 in [(300, K.blauw, 180), (1000, K.rood, 950)]:
        a = M / (2 * _R * T)
        f = 4 * np.pi * (a / np.pi) ** 1.5 * v**2 * np.exp(-a * v**2)
        ax.plot(v, f * 1e3, color=kl, lw=2.4)
        vm = np.sqrt(8 * _R * T / (np.pi * M))
        ax.axvline(vm, color=kl, lw=1, ls=":")
        label(ax, x0, f.max() * 1e3 * 1.03, f"{T} K", kl, fontsize=11)
    label(ax, 1250, 1.25, "staart met snelle moleculen:\ngroeit sterk met $T$", K.zacht, fontsize=10)
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 2.3)
    ax.set_xlabel("snelheid $v$ (m/s)")
    ax.set_ylabel("$f(v)$ (10$^{-3}$ s/m)")
    return kader(fig)


def reactiecoordinaat():
    """Energieprofiel met en zonder katalysator."""
    fig, ax = figuur(6.4, 4.2)
    x = np.linspace(0, 1, 400)
    E_r, E_p = 0.0, -0.6
    basis = E_r + (E_p - E_r) * (1 / (1 + np.exp(-(x - 0.5) * 14)))
    onkat = basis + 1.6 * np.exp(-((x - 0.5) / 0.11) ** 2)
    kat = basis + 0.75 * np.exp(-((x - 0.36) / 0.08) ** 2) + 0.55 * np.exp(-((x - 0.66) / 0.08) ** 2) \
        - 0.25 * np.exp(-((x - 0.51) / 0.06) ** 2)
    ax.plot(x, onkat, color=K.rood, lw=2.4)
    ax.plot(x, kat, color=K.accent, lw=2.4)
    ax.annotate("", xy=(0.5, onkat.max()), xytext=(0.5, 0), arrowprops=dict(arrowstyle="<->", color=K.rood, lw=1.2))
    label(ax, 0.56, 0.95, "$E_{a,\\mathrm{onkat}}$", K.rood, fontsize=11)
    ax.annotate("", xy=(0.36, kat[np.argmin(abs(x - 0.36))]), xytext=(0.36, 0),
                arrowprops=dict(arrowstyle="<->", color=K.accent, lw=1.2))
    label(ax, 0.16, 0.45, "$E_{a,\\mathrm{kat}}$", K.accent, fontsize=11)
    ax.axhline(0, xmin=0, xmax=0.25, color=K.zacht, lw=1, ls=":")
    ax.annotate("", xy=(0.92, E_p), xytext=(0.92, 0), arrowprops=dict(arrowstyle="<->", color=K.zacht, lw=1.2))
    label(ax, 0.80, -0.30, "$\\Delta_rH$", K.zacht, fontsize=11)
    label(ax, 0.02, 0.08, "reagentia", K.tekst, fontsize=10.5)
    label(ax, 0.80, -0.72, "producten", K.tekst, fontsize=10.5)
    label(ax, 0.30, -0.45, "geadsorbeerd\nintermediair", K.accent, fontsize=9.5, ha="center")
    pijl(ax, (0.36, -0.40), (0.49, -0.50), K.accent, 1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("reactieco\u00f6rdinaat")
    ax.set_ylabel("energie")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.85, 1.8)
    return kader(fig)


def serie_reactie():
    """A -> B -> C: concentratieverloop en optimum voor het tussenproduct."""
    fig, ax = figuur(6.4, 4.2)
    k1, k2 = 0.10, 0.05
    t = np.linspace(0, 80, 400)
    A = np.exp(-k1 * t)
    B = k1 / (k2 - k1) * (np.exp(-k1 * t) - np.exp(-k2 * t))
    C = 1 - A - B
    ax.plot(t, A, color=K.blauw, lw=2.4)
    ax.plot(t, B, color=K.accent, lw=2.4)
    ax.plot(t, C, color=K.rood, lw=2.4)
    tm = np.log(k2 / k1) / (k2 - k1)
    Bm = (k1 / k2) ** (k2 / (k2 - k1))
    ax.plot(tm, Bm, "o", color=K.accent, ms=7)
    ax.plot([tm, tm], [0, Bm], color=K.accent, lw=1, ls=":")
    label(ax, 20, 0.58, f"maximum: $t$ = {tm:.1f} min,\n$[B]/[A]_0$ = {Bm:.2f}", K.accent, fontsize=10.5)
    label(ax, 3, 0.86, "A", K.blauw, fontsize=12)
    label(ax, 55, 0.25, "B (gewenst)", K.accent, fontsize=11)
    label(ax, 55, 0.80, "C (ongewenst)", K.rood, fontsize=11)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("tijd (min)")
    ax.set_ylabel("concentratie / $[A]_0$")
    return kader(fig)


def semenov():
    """Warmteproductie en warmteafvoer in een gekoelde reactor."""
    fig, ax = figuur(6.4, 4.4)
    T = np.linspace(380, 470, 400)
    Ea, UA = 100e3, 0.16
    q_gen = np.exp(-Ea / _R * (1 / T - 1 / 400))
    ax.plot(T, q_gen, color=K.rood, lw=2.6, label="warmteproductie $\\propto e^{-E_a/RT}$")
    dq = q_gen * Ea / (_R * T**2)
    i = np.argmin(abs(dq - UA))
    Tkrit = T[i] - q_gen[i] / UA
    for Tc, kl, ls, naam in [(385.0, K.accent, "-", "afvoer, $T_c$ = 385 K: stabiel"),
                             (Tkrit, K.oker, (0, (5, 3)), f"afvoer, $T_c$ = {Tkrit:.0f} K: kritisch"),
                             (400.0, K.paars, "-", "afvoer, $T_c$ = 400 K: runaway")]:
        ax.plot(T, UA * (T - Tc), color=kl, lw=1.8, ls=ls, label=naam)
    ax.plot(T[i], q_gen[i], "o", color=K.oker, ms=6)
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    label(ax, 440, 1.0, "afvoer = $UA(T - T_c)$", K.zacht, fontsize=10)
    ax.set_xlim(380, 470)
    ax.set_ylim(0, 9)
    ax.set_xlabel("reactortemperatuur $T$ (K)")
    ax.set_ylabel("warmtestroom (relatief)")
    return kader(fig)


def lh_er():
    """Snelheid tegen p_A volgens Langmuir-Hinshelwood en Eley-Rideal."""
    fig, ax = figuur(6.4, 4.2)
    p = np.linspace(0, 20, 400)
    KA, KB, pB = 1.0, 1.0, 1.0
    lh = KA * KB * p * pB / (1 + KA * p + KB * pB) ** 2
    er = KA * p * pB / (1 + KA * p)
    ax.plot(p, lh / lh.max(), color=K.accent, lw=2.4)
    ax.plot(p, er / er.max(), color=K.rood, lw=2.4)
    label(ax, 6, 0.48, "Langmuir–Hinshelwood:\nmaximum, daarna daling", K.accent, fontsize=10.5)
    label(ax, 8, 1.0, "Eley–Rideal: plateau", K.rood, fontsize=10.5)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("partiële druk $p_A$ (bar, bij vaste $p_B$)")
    ax.set_ylabel("snelheid (genormaliseerd)")
    return kader(fig)
