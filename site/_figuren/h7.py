"""Figuren hoofdstuk 7 – Elektrochemie (cellen, elektrodekinetiek, corrosie, Pourbaix)."""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

from huisstijl import K, figuur, kader, label, pijl  # noqa: F401

_R, _T, _F = 8.314, 298.15, 96485.0
_LN10 = np.log(10)
_G_WATER = -237.13  # kJ/mol, NBS-tabellen

# Pourbaix-gegevens per metaalatoom: (naam, O-atomen, H-atomen, lading, dfG° kJ/mol, opgelost?)
# Bron: NBS Tables of Chemical Thermodynamic Properties (1982) en Pourbaix, Atlas (1974).
_SOORTEN = {
    "Zn": [("Zn", 0, 0, 0, 0.0, 0), ("Zn$^{2+}$", 0, 0, 2, -147.06, 1),
           ("Zn(OH)$_2$", 2, 2, 0, -553.5, 0), ("ZnO$_2^{2-}$", 2, 0, -2, -384.2, 1)],
    "Fe": [("Fe", 0, 0, 0, 0.0, 0), ("Fe$^{2+}$", 0, 0, 2, -78.90, 1), ("Fe$^{3+}$", 0, 0, 3, -4.7, 1),
           ("Fe$_3$O$_4$", 4 / 3, 0, 0, -1015.4 / 3, 0), ("Fe$_2$O$_3$", 1.5, 0, 0, -742.2 / 2, 0),
           ("HFeO$_2^-$", 2, 1, -1, -379.2, 1)],
    "Cu": [("Cu", 0, 0, 0, 0.0, 0), ("Cu$^{2+}$", 0, 0, 2, 65.49, 1), ("Cu$_2$O", 0.5, 0, 0, -146.0 / 2, 0),
           ("CuO", 1, 0, 0, -129.7, 0), ("CuO$_2^{2-}$", 2, 0, -2, -183.6, 1)],
    "Al": [("Al", 0, 0, 0, 0.0, 0), ("Al$^{3+}$", 0, 0, 3, -485.0, 1),
           ("Al(OH)$_3$", 3, 3, 0, -1154.9, 0), ("Al(OH)$_4^-$", 4, 4, -1, -1305.3, 1)],
}


def _G(soort, E, pH, a=1e-6):
    """Gibbsenergie (J) van M + o H2O -> soort + m H+ + n e-, bij potentiaal E en pH."""
    _, o, h, z, g, opgelost = soort
    m = 2 * o - h
    n = m + z
    return (g * 1000 + (_R * _T * np.log(a) if opgelost else 0)
            - m * _R * _T * _LN10 * pH - o * _G_WATER * 1000 - n * _F * E)


def _pourbaix(ax, metaal, E_min, E_max, pH_min=-1, pH_max=15, plaats=None, titel=None, pijlen=None):
    pH = np.linspace(pH_min, pH_max, 640)
    E = np.linspace(E_min, E_max, 640)
    P, EE = np.meshgrid(pH, E)
    soorten = _SOORTEN[metaal]
    kaart = np.argmin([_G(s, EE, P) for s in soorten], axis=0)
    kleur = []
    for i, s in enumerate(soorten):
        if i == 0:
            kleur.append(K.vlak_groen)
        elif s[5]:
            kleur.append(K.vlak_rood)
        else:
            kleur.append(K.vlak_blauw)
    from matplotlib.colors import ListedColormap
    ax.imshow(kaart, origin="lower", extent=(pH_min, pH_max, E_min, E_max), aspect="auto",
              cmap=ListedColormap(kleur), vmin=-0.5, vmax=len(soorten) - 0.5, interpolation="nearest")
    ax.contour(P, EE, kaart, levels=np.arange(len(soorten)) + 0.5, colors=K.tekst, linewidths=1.3)
    # stabiliteitsgebied van water
    ax.plot(pH, 1.229 - 0.0592 * pH, color=K.accent, lw=1.6, ls=(0, (5, 3)))
    ax.plot(pH, -0.0592 * pH, color=K.accent, lw=1.6, ls=(0, (5, 3)))
    plaats = plaats or {}
    pijlen = pijlen or {}
    for i, s in enumerate(soorten):
        mask = kaart == i
        if not mask.any():
            continue
        if i in pijlen:
            (xt, yt), (xp, yp) = pijlen[i]
            ax.annotate(s[0], xy=(xp, yp), xytext=(xt, yt), color=K.tekst, fontsize=11, ha="center",
                        va="center", arrowprops=dict(arrowstyle="-", color=K.tekst, lw=1))
            continue
        x, y = plaats.get(i, (P[mask].mean(), EE[mask].mean()))
        ax.text(x, y, s[0], color=K.tekst, fontsize=11, ha="center", va="center")
    ax.set_xlim(pH_min, pH_max)
    ax.set_ylim(E_min, E_max)
    ax.set_xlabel("pH")
    ax.set_ylabel("potentiaal $E$ (V t.o.v. SHE)")
    if titel:
        ax.set_title(titel, color=K.tekst, fontsize=12)


# ------------------------------------------------------------- Daniell-cel
def daniell_cel():
    """Schema van de Daniell-cel."""
    fig, ax = figuur(6.8, 4.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.0, 6.4)
    ax.axis("off")
    for x0, kl, vlak, naam, opl in [(0.6, K.blauw, K.vlak_blauw, "Zn", "ZnSO$_4$(aq)"),
                                    (6.2, K.rood, K.vlak_rood, "Cu", "CuSO$_4$(aq)")]:
        ax.add_patch(Rectangle((x0, 0.4), 3.2, 2.6, facecolor=vlak, edgecolor=K.as_, lw=1.4))
        ax.add_patch(Rectangle((x0 + 1.35, 1.0), 0.5, 3.4, facecolor=kl, edgecolor=K.as_, lw=1))
        ax.text(x0 + 1.6, 4.65, naam, ha="center", color=K.tekst, fontsize=12, weight="bold")
        ax.text(x0 + 1.6, 0.65, opl, ha="center", color=K.tekst, fontsize=10.5)
    # zoutbrug
    ax.plot([3.3, 3.3, 6.7, 6.7], [2.0, 3.6, 3.6, 2.0], color=K.oker, lw=9, solid_capstyle="butt", alpha=0.85)
    ax.text(5.0, 3.85, "zoutbrug (ionen)", ha="center", color=K.oker, fontsize=10.5)
    # draad en voltmeter
    ax.plot([2.2, 2.2, 4.4], [4.4, 5.7, 5.7], color=K.as_, lw=1.6)
    ax.plot([5.6, 7.8, 7.8], [5.7, 5.7, 4.4], color=K.as_, lw=1.6)
    ax.add_patch(FancyBboxPatch((4.4, 5.3), 1.2, 0.8, boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=K.achtergrond, edgecolor=K.as_, lw=1.4))
    ax.text(5.0, 5.7, "1.10 V", ha="center", va="center", color=K.tekst, fontsize=11)
    pijl(ax, (2.8, 6.05), (4.1, 6.05), K.accent, 1.6)
    ax.text(3.45, 6.25, "e$^-$", ha="center", color=K.accent, fontsize=11)
    ax.text(2.2, -0.75, "anode (−): Zn → Zn$^{2+}$ + 2e$^-$", ha="center", color=K.blauw, fontsize=10.5)
    ax.text(7.8, -0.75, "kathode (+): Cu$^{2+}$ + 2e$^-$ → Cu", ha="center", color=K.rood, fontsize=10.5)
    return kader(fig)


# ------------------------------------------------------ elektrolyser
def elektrolyser_polarisatie():
    """Celspanning van een PEM-elektrolyser opgesplitst in verliezen."""
    fig, ax = figuur(6.6, 4.4)
    i = np.linspace(0.01, 2.5, 300)  # A/cm2
    E_rev = 1.229
    eta_a = 0.05 * np.log10(i / 1e-6)
    eta_k = 0.03 * np.log10(i / 1e-3)
    ohm = 0.15 * i
    lagen = [E_rev + 0 * i, E_rev + eta_k, E_rev + eta_k + eta_a, E_rev + eta_k + eta_a + ohm]
    vlak = [K.vlak_blauw, K.vlak_oker, K.vlak_rood]
    namen = ["kathode-overspanning", "anode-overspanning (O$_2$)", "ohmse verliezen $iR$"]
    for j in range(3):
        ax.fill_between(i, lagen[j], lagen[j + 1], color=vlak[j], lw=0)
    ax.plot(i, lagen[-1], color=K.tekst, lw=2.4)
    ax.axhline(E_rev, color=K.accent, lw=1.6)
    ax.axhline(1.481, color=K.paars, lw=1.4, ls=(0, (5, 3)))
    label(ax, 2.45, 1.20, "omkeerbaar: 1.23 V", K.accent, fontsize=10.5, ha="right", va="top")
    label(ax, 2.45, 1.47, "thermoneutraal: 1.48 V", K.paars, fontsize=10.5, ha="right", va="top")
    label(ax, 1.7, 1.30, namen[0], K.tekst, fontsize=10)
    label(ax, 1.0, 1.53, namen[1], K.tekst, fontsize=10)
    label(ax, 1.75, 1.83, namen[2], K.tekst, fontsize=10)
    label(ax, 0.55, 1.80, "celspanning", K.tekst, fontsize=11, ha="right")
    ax.set_xlim(0, 2.5)
    ax.set_ylim(1.1, 2.15)
    ax.set_xlabel("stroomdichtheid $i$ (A/cm$^2$)")
    ax.set_ylabel("celspanning (V)")
    return kader(fig)


# ------------------------------------------------------------- Evans
def evans_diagram():
    """Gemengde potentiaal: anodische Fe-oplossing en kathodische O2-reductie."""
    fig, ax = figuur(6.6, 4.4)
    logi = np.linspace(-9, -2, 400)  # log10 i (A/cm2)
    # anodisch: Fe -> Fe2+, E = Eeq + 0.06 log(i/i0)
    Ea = -0.59 + 0.06 * (logi - (-8))
    # kathodisch: O2-reductie, Tafel + diffusiegrens iL
    iL = 2e-5
    i = 10 ** logi
    Ek = np.where(i < iL * 0.999, 0.6 - 0.12 * (logi - (-10)) + 0.0296 * np.log10(np.clip(1 - i / iL, 1e-9, 1)), np.nan)
    ax.plot(logi, Ea, color=K.blauw, lw=2.4)
    ax.plot(logi, Ek, color=K.rood, lw=2.4)
    ax.plot([np.log10(iL)] * 2, [-0.8, np.nanmin(Ek)], color=K.rood, lw=2.4)
    # snijpunt
    from numpy import interp
    d = Ea - np.nan_to_num(Ek, nan=-9)
    j = np.argmin(np.abs(d[:np.searchsorted(logi, np.log10(iL))]))
    x0, y0 = logi[j], Ea[j]
    x0 = np.log10(iL)
    y0 = interp(x0, logi, Ea)
    ax.plot(x0, y0, "o", color=K.tekst, ms=7, zorder=5)
    ax.plot([x0, x0], [-0.8, y0], color=K.zacht, lw=1, ls=":")
    ax.plot([-9, x0], [y0, y0], color=K.zacht, lw=1, ls=":")
    label(ax, -8.9, y0 + 0.02, "$E_\\mathrm{corr}$", K.tekst, fontsize=11, va="bottom")
    label(ax, x0 + 0.1, -0.78, "$i_\\mathrm{corr}$", K.tekst, fontsize=11)
    label(ax, -8.8, -0.74, "Fe → Fe$^{2+}$ + 2e$^-$ (anodisch)", K.blauw, fontsize=10.5)
    label(ax, -7.2, 0.30, "O$_2$ + 2H$_2$O + 4e$^-$ → 4OH$^-$\n(kathodisch)", K.rood, fontsize=10.5)
    label(ax, -4.55, -0.05, "diffusiegrens:\nmeer O$_2$ of\nstroming → hoger $i_\\mathrm{corr}$", K.rood, fontsize=10, ha="left")
    ax.set_xlim(-9, -2)
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlabel("log$_{10}$ stroomdichtheid (A/cm$^2$)")
    ax.set_ylabel("potentiaal $E$ (V t.o.v. SHE)")
    return kader(fig)


# --------------------------------------------------------- Pourbaix
def pourbaix_water():
    """Stabiliteitsgebied van water in het E-pH-vlak."""
    fig, ax = figuur(6.4, 4.4)
    pH = np.linspace(0, 14, 50)
    boven = 1.229 - 0.0592 * pH
    onder = -0.0592 * pH
    ax.fill_between(pH, onder, boven, color=K.vlak_accent, lw=0)
    ax.plot(pH, boven, color=K.accent, lw=2.2)
    ax.plot(pH, onder, color=K.accent, lw=2.2)
    label(ax, 7, 0.42, "water stabiel", K.accent, fontsize=12, ha="center")
    label(ax, 9.5, 1.15, "water wordt geoxideerd:\n2H$_2$O → O$_2$ + 4H$^+$ + 4e$^-$", K.rood, fontsize=10.5, ha="center")
    label(ax, 4.5, -0.85, "water wordt gereduceerd:\n2H$^+$ + 2e$^-$ → H$_2$", K.blauw, fontsize=10.5, ha="center")
    label(ax, 1.0, 1.25, "1.23 − 0.059 pH", K.accent, fontsize=10, rotation=-8)
    label(ax, 1.0, 0.03, "0 − 0.059 pH", K.accent, fontsize=10, rotation=-8)
    ax.annotate("", xy=(12, 1.229 - 0.0592 * 12), xytext=(12, -0.0592 * 12),
                arrowprops=dict(arrowstyle="<->", color=K.zacht, lw=1.2))
    label(ax, 12.2, 0.0, "1.23 V", K.zacht, fontsize=10)
    ax.set_xlim(0, 14)
    ax.set_ylim(-1.2, 1.6)
    ax.set_xlabel("pH")
    ax.set_ylabel("potentiaal $E$ (V t.o.v. SHE)")
    return kader(fig)


def pourbaix_zink():
    """Pourbaix-diagram van zink, 25 °C, ionactiviteit 10^-6."""
    fig, ax = figuur(6.4, 4.6)
    _pourbaix(ax, "Zn", -1.8, 1.4, -1, 15, plaats={0: (7, -1.5), 1: (3.5, 0.2), 2: (10.4, 0.2), 3: (13.5, 0.2)})
    label(ax, 3.5, -0.2, "corrosie", K.rood, fontsize=10, ha="center")
    label(ax, 10.4, -0.2, "passief", K.blauw, fontsize=10, ha="center")
    label(ax, 7, -1.68, "immuun", K.groen, fontsize=10, ha="center")
    return kader(fig)


def pourbaix_ijzer():
    """Pourbaix-diagram van ijzer, 25 °C, ionactiviteit 10^-6."""
    fig, ax = figuur(6.4, 4.8)
    _pourbaix(ax, "Fe", -1.4, 1.6, -1, 15,
              plaats={0: (6, -1.15), 1: (2.5, -0.1), 2: (0.3, 1.45), 3: (11, -0.53), 4: (9, 0.6)},
              pijlen={5: ((12.6, -1.25), (14.6, -0.93))})
    label(ax, 2.5, -0.3, "corrosie", K.rood, fontsize=10, ha="center")
    label(ax, 9, 0.4, "passief", K.blauw, fontsize=10, ha="center")
    label(ax, 6, -1.32, "immuun", K.groen, fontsize=10, ha="center")
    return kader(fig)


def pourbaix_al_cu():
    """Pourbaix-diagrammen van aluminium en koper naast elkaar."""
    fig, (a1, a2) = figuur(9.6, 4.4, ncols=2)
    _pourbaix(a1, "Al", -2.6, 1.4, -1, 15, titel="aluminium",
              plaats={0: (7, -2.4), 1: (1.5, -0.4), 2: (6.8, -1.25), 3: (12.5, -0.4)})
    _pourbaix(a2, "Cu", -1.0, 1.4, -1, 15, titel="koper",
              plaats={0: (7, -0.6), 1: (2.5, 0.9), 3: (9.5, 0.75), 4: (14.3, 0.75)},
              pijlen={2: ((11.2, -0.55), (9.5, 0.0))})
    a2.set_ylabel("")
    return kader(fig)


def waterstof_spanning():
    """Elektriciteitsverbruik per kg H2 in functie van de celspanning (Faraday), met kenmerkende spanningen."""
    fig, ax = figuur(6.6, 4.2)
    F, M = 96485.0, 2.016e-3
    U = np.linspace(1.0, 2.3, 100)
    kwh = 2 * F * U / M / 3.6e6
    ax.axvspan(1.0, 1.48, color=K.vlak_blauw, lw=0)
    ax.axvspan(1.48, 2.3, color=K.vlak_accent, lw=0)
    label(ax, 1.05, 58, "elektrolyser\nkoelt af", K.blauw, fontsize=10, va="top")
    label(ax, 2.25, 25, "elektrolyser warmt op:\nkoeling nodig", K.accent, fontsize=10, ha="right")
    ax.plot(U, kwh, color=K.tekst, lw=2.2)
    for u, nm, k in [(1.23, "omkeerbaar\n$\\Delta_rG^\\circ/nF$", K.groen), (1.48, "thermoneutraal\n$\\Delta_rH^\\circ/nF$", K.oker),
                     (1.9, "PEM bij\n2 A/cm²", K.rood)]:
        e = 2 * F * u / M / 3.6e6
        ax.plot(u, e, "o", color=k, ms=7, zorder=5)
        ax.plot([u, u], [20, e], color=k, lw=1, ls=":")
        if u < 1.3:
            label(ax, u + 0.03, e - 1.5, f"{nm}\n{u:.2f} V → {e:.1f} kWh/kg", k, fontsize=9.5, va="top")
        else:
            label(ax, u - 0.02, e + 1.2, f"{nm}\n{u:.2f} V → {e:.1f} kWh/kg", k, fontsize=9.5, ha="right", va="bottom")
    ax.set_xlim(1.0, 2.3)
    ax.set_ylim(20, 62)
    ax.set_xlabel("celspanning $U$ (V)")
    ax.set_ylabel("elektriciteit per kg H$_2$ (kWh/kg)")
    return kader(fig)
