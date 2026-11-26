"""Figuren hoofdstuk 8 – Grensvlakken en materialen."""
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon, Rectangle

from huisstijl import K, figuur, kader, label, pijl  # noqa: F401


# ------------------------------------------------------------ bevochtiging
def contacthoek():
    """Druppel op een hydrofiel en een hydrofoob oppervlak, met contacthoek."""
    fig, axs = figuur(8.4, 3.2, ncols=2)
    for ax, theta, titel in [(axs[0], 40, "hydrofiel: $\\theta$ < 90°"), (axs[1], 130, "hydrofoob: $\\theta$ > 90°")]:
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-0.45, 2.1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.fill_between([-2.2, 2.2], -0.45, 0, color=K.vlak_grijs)
        ax.plot([-2.2, 2.2], [0, 0], color=K.as_, lw=1.4)
        t = np.radians(theta)
        a = 1.0 if theta < 90 else 0.7  # halve contactbreedte
        R = a / np.sin(t)
        yc = -R * np.cos(t)
        phi = np.linspace(0, 2 * np.pi, 400)
        x, y = R * np.cos(phi), yc + R * np.sin(phi)
        m = y >= 0
        ax.fill(np.r_[x[m]], np.r_[y[m]], color=K.vlak_blauw, zorder=1)
        ax.plot(x[m], y[m], color=K.blauw, lw=2.2, zorder=2)
        # raaklijn in het rechter contactpunt
        tx, ty = np.cos(np.pi - t), np.sin(np.pi - t)
        L = 0.9
        ax.plot([a, a + L * tx], [0, L * ty], color=K.rood, lw=1.6)
        ax.add_patch(Arc((a, 0), 0.7, 0.7, theta1=180 - theta, theta2=180, color=K.rood, lw=1.4))
        phi_l = np.radians(180 - theta / 2)
        ax.text(a + 0.55 * np.cos(phi_l), 0.55 * np.sin(phi_l), "$\\theta$", color=K.rood, fontsize=12,
                ha="center", va="center")
        ax.text(0, -0.3, "vaste stof", color=K.zacht, fontsize=10, ha="center")
        ax.set_title(titel, color=K.tekst, fontsize=12)
    return kader(fig)


# --------------------------------------------------------------- adsorptie
def langmuir_isotherm():
    """Langmuir-isothermen voor twee waarden van K."""
    fig, ax = figuur(6.4, 4.2)
    p = np.linspace(0, 10, 300)
    for Kv, kl, y in [(2.0, K.accent, 0.84), (0.2, K.rood, 0.50)]:
        th = Kv * p / (1 + Kv * p)
        ax.plot(p, th, color=kl, lw=2.4)
        label(ax, 7.0, y, f"$K$ = {Kv:g} bar$^{{-1}}$", kl, fontsize=11)
    ax.plot([0, 1.4], [0, 1.4 * 0.2], color=K.zacht, lw=1.2, ls=":")
    label(ax, 1.3, 0.08, "lineair: $\\theta \\approx Kp$", K.zacht, fontsize=10)
    ax.axhline(1, color=K.zacht, lw=1, ls=(0, (4, 3)))
    label(ax, 0.2, 1.02, "volledige monolaag", K.zacht, fontsize=10, va="bottom")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("druk $p$ (bar)")
    ax.set_ylabel("bedekkingsgraad $\\theta$")
    return kader(fig)


def bet_isotherm():
    """Stikstofadsorptie bij 77 K volgens BET, met monolaagpunt."""
    fig, ax = figuur(6.4, 4.2)
    x = np.linspace(0.001, 0.9, 400)
    C, Vm = 100, 46.0
    V = Vm * C * x / ((1 - x) * (1 - x + C * x))
    ax.plot(x, V, color=K.accent, lw=2.4)
    ax.axhline(Vm, color=K.oker, lw=1.2, ls=(0, (4, 3)))
    label(ax, 0.55, Vm + 4, "monolaag $V_m$ = 46 cm$^3$/g", K.oker, fontsize=10.5)
    ax.axvspan(0.05, 0.30, color=K.vlak_accent, lw=0)
    label(ax, 0.175, 205, "BET-gebied\n$x$ = 0.05–0.30", K.accent, fontsize=10, ha="center", va="top")
    label(ax, 0.62, 140, "meerdere lagen,\ndan condensatie", K.zacht, fontsize=10)
    ax.set_xlim(0, 0.9)
    ax.set_ylim(0, 215)
    ax.set_xlabel("relatieve druk $x = p/p_\\mathrm{sat}$")
    ax.set_ylabel("geadsorbeerd N$_2$ (cm$^3$ STP per g)")
    return kader(fig)


# ---------------------------------------------------------------- colloïden
def dlvo():
    """DLVO-energie: Van der Waals-aantrekking plus elektrostatische afstoting."""
    fig, ax = figuur(6.4, 4.2)
    h = np.linspace(0.25, 20, 500)  # nm
    vdw = -12.0 / h
    for kappa_inv, kl, naam in [(3.0, K.accent, "weinig zout: stabiel"), (0.45, K.rood, "veel zout: coagulatie")]:
        el = 60 * np.exp(-h / kappa_inv)
        ax.plot(h, el + vdw, color=kl, lw=2.4, label=naam)
    ax.plot(h, vdw, color=K.blauw, lw=1.3, ls=(0, (4, 3)))
    ax.axhline(0, color=K.zacht, lw=0.8)
    label(ax, 8.5, -6.5, "Van der Waals", K.blauw, fontsize=10)
    label(ax, 2.3, 25, "energiedrempel", K.accent, fontsize=10.5)
    label(ax, 9, 9, "weinig zout:\nstabiele dispersie", K.accent, fontsize=10.5)
    label(ax, 3.0, -14, "veel zout: geen drempel,\ndeeltjes klonteren", K.rood, fontsize=10.5)
    ax.set_xlim(0, 20)
    ax.set_ylim(-25, 32)
    ax.set_xlabel("afstand tussen deeltjes (nm)")
    ax.set_ylabel("interactie-energie (in $k_BT$)")
    return kader(fig)


# --------------------------------------------------------- vaste stoffen
def _kubus(ax, ox, kleur):
    hoek = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    d = np.array([0.38, 0.28])  # schuine projectie van de diepte
    voor = hoek + [ox, 0]
    achter = voor + d
    for P in (voor, achter):
        ax.add_patch(Polygon(P, closed=True, fill=False, edgecolor=K.as_, lw=1.0))
    for a, b in zip(voor, achter):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=K.as_, lw=1.0)
    return voor, achter, d


def kubische_roosters():
    """Primitief kubisch, BCC en FCC naast elkaar."""
    fig, ax = figuur(8.6, 3.4)
    ax.set_xlim(-0.3, 6.4)
    ax.set_ylim(-0.45, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    d = np.array([0.38, 0.28])

    def p(ox, x, y, z):
        return np.array([ox + x + z * d[0], y + z * d[1]])

    namen = [("primitief (P)\n1 atoom per cel", "P"), ("ruimtelijk gecentreerd (BCC)\n2 atomen per cel", "I"),
             ("vlakgecentreerd (FCC)\n4 atomen per cel", "F")]
    for k, (naam, soort) in enumerate(namen):
        ox = k * 2.2
        _kubus(ax, ox, K.as_)
        punten = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
        extra = []
        if soort == "I":
            extra = [(0.5, 0.5, 0.5)]
        if soort == "F":
            extra = [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5), (0, 0.5, 0.5), (1, 0.5, 0.5)]
        alle = sorted(punten + extra, key=lambda q: -q[2])
        for q in alle:
            xy = p(ox, *q)
            kl = K.accent if q in punten else K.rood
            ax.add_patch(Circle(xy, 0.085 if q in punten else 0.095, facecolor=kl, edgecolor=K.achtergrond,
                                lw=0.8, zorder=3 + (1 - q[2])))
        ax.text(ox + 0.65, -0.38, naam, ha="center", va="center", color=K.tekst, fontsize=10.5)
    return kader(fig)


def bragg_geometrie():
    """Twee roostervlakken en het weglengteverschil 2d sin(theta)."""
    fig, ax = figuur(6.4, 3.6)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-1.9, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")
    dd = 1.0
    for y in (0, -dd, -2 * dd):
        xs = np.arange(-3, 3.01, 0.6)
        ax.plot(xs, np.full_like(xs, y), "o", color=K.accent, ms=6)
        ax.plot([-3.1, 3.1], [y, y], color=K.rand, lw=1, zorder=0)
    th = np.radians(30)
    for y0, kl in [(0, K.rood), (-dd, K.oker)]:
        L = 2.6
        x0 = 0.0
        ax.annotate("", xy=(x0, y0), xytext=(x0 - L * np.cos(th), y0 + L * np.sin(th)),
                    arrowprops=dict(arrowstyle="-|>", color=kl, lw=1.8, mutation_scale=12))
        ax.annotate("", xy=(x0 + L * np.cos(th), y0 + L * np.sin(th)), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=kl, lw=1.8, mutation_scale=12))
    # weglengteverschil
    for s in (-1, 1):
        A = (s * dd * np.sin(th) * np.cos(th), -dd + dd * np.sin(th) ** 2)
        ax.plot([0, A[0]], [-dd, A[1]], color=K.paars, lw=3)
        ax.plot([0, A[0]], [0, A[1]], color=K.zacht, lw=1, ls=":")
    ax.annotate("", xy=(0.15, 0), xytext=(0.15, -dd), arrowprops=dict(arrowstyle="<->", color=K.zacht, lw=1.1))
    ax.text(0.25, -0.55, "$d$", color=K.tekst, fontsize=12)
    ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=150, theta2=180, color=K.rood, lw=1.3))
    ax.text(-0.85, 0.12, "$\\theta$", color=K.rood, fontsize=12)
    ax.text(0, -2.0 * dd - 0.3, "extra weg van de onderste straal: $2d\\sin\\theta$ (paars)", color=K.paars,
            fontsize=10.5, ha="center", va="top")
    return kader(fig)


def xrd_poederpatroon():
    """Berekend poederdiffractogram van koper (FCC, Cu Kα)."""
    fig, ax = figuur(6.6, 3.8)
    a, lam = 0.3615, 0.15406
    tt = np.linspace(30, 100, 3000)
    I = np.zeros_like(tt)
    pieken = [((1, 1, 1), 100), ((2, 0, 0), 46), ((2, 2, 0), 20), ((3, 1, 1), 17), ((2, 2, 2), 5)]
    for (h, k, l), Irel in pieken:
        dval = a / np.sqrt(h * h + k * k + l * l)
        t2 = 2 * np.degrees(np.arcsin(lam / (2 * dval)))
        I += Irel * np.exp(-0.5 * ((tt - t2) / 0.18) ** 2)
        ax.text(t2, Irel + 4, f"({h}{k}{l})", ha="center", color=K.tekst, fontsize=10)
    ax.plot(tt, I + 1.5, color=K.accent, lw=1.8)
    ax.set_xlim(30, 100)
    ax.set_ylim(0, 115)
    ax.set_xlabel("$2\\theta$ (°)")
    ax.set_ylabel("relatieve intensiteit")
    label(ax, 52, 80, "Cu, FCC\n$a$ = 0.3615 nm\n$\\lambda$ = 0.154 nm", K.zacht, fontsize=10)
    return kader(fig)


def cmc_sds():
    """Oppervlaktespanning van SDS-oplossingen tegen log c (schematisch, CMC = 8.2 mM)."""
    fig, ax = figuur(6.4, 4.2)
    cmc, g0, gc = 8.2e-3, 72.0, 36.0
    c = np.logspace(-5, -1, 300)
    # Szyszkowski-vorm onder de CMC, constant erboven
    B, a = 9.5, 2.0e-4
    g = g0 - B * np.log(1 + c / a)
    gcmc = g0 - B * np.log(1 + cmc / a)
    g = np.where(c < cmc, g, gcmc)
    ax.axvspan(cmc, 1e-1, color=K.vlak_accent, lw=0)
    ax.plot(c, g, color=K.blauw, lw=2.4)
    ax.axvline(cmc, color=K.accent, lw=1.2, ls="--")
    label(ax, cmc * 1.15, 66, "CMC\n8.2 mmol/L", K.accent, fontsize=10.5, va="top")
    label(ax, 1.3e-5, 69, "vrije moleculen\nadsorberen aan het\noppervlak", K.tekst, fontsize=10, va="top")
    label(ax, 1.3e-2, 45, "extra SDS vormt\nmicellen;\n$\\gamma$ blijft constant", K.tekst, fontsize=10, va="bottom")
    ax.set_xscale("log")
    ax.set_xlim(1e-5, 1e-1)
    ax.set_ylim(30, 75)
    ax.set_xlabel("concentratie SDS (mol/L)")
    ax.set_ylabel("oppervlaktespanning $\\gamma$ (mN/m)")
    return kader(fig)


def banden():
    """Bandenschema van geleider, halfgeleider en isolator met band gaps (Kittel)."""
    fig, ax = figuur(6.8, 4.2)
    stoffen = [("koper\n(geleider)", 0.0, K.oker), ("silicium\n(halfgeleider)", 1.12, K.blauw),
               ("diamant\n(isolator)", 5.5, K.paars)]
    for i, (nm, Eg, k) in enumerate(stoffen):
        x0 = i * 1.6
        if Eg == 0:
            ax.add_patch(Rectangle((x0, -3), 1, 3, color=k, alpha=0.85, lw=0))
            ax.add_patch(Rectangle((x0, 0), 1, 2.5, color=k, alpha=0.25, lw=0))
            label(ax, x0 + 0.5, 0.3, "gedeeltelijk\ngevuld", k, ha="center", va="bottom", fontsize=9.5)
        else:
            ax.add_patch(Rectangle((x0, -3), 1, 3, color=k, alpha=0.85, lw=0))
            ax.add_patch(Rectangle((x0, Eg), 1, 2.5, color=k, alpha=0.25, lw=0))
            ax.annotate("", xy=(x0 + 0.5, Eg), xytext=(x0 + 0.5, 0),
                        arrowprops=dict(arrowstyle="<->", color=K.tekst, lw=1.2))
            label(ax, x0 + 0.58, Eg / 2, f"$E_g$ = {Eg} eV", K.tekst, fontsize=10, va="center")
        label(ax, x0 + 0.5, -3.3, nm, k, ha="center", va="top", fontsize=10.5)
    label(ax, -0.1, -1.5, "valentieband\n(gevuld)", K.zacht, ha="right", va="center", fontsize=9.5)
    label(ax, -0.1, 6.5, "geleidingsband\n(leeg)", K.zacht, ha="right", va="center", fontsize=9.5)
    ax.set_xlim(-1.3, 4.3)
    ax.set_ylim(-4.6, 8.3)
    ax.axis("off")
    return kader(fig)
