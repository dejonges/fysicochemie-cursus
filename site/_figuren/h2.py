"""Figuren hoofdstuk 2 – De moleculaire oorsprong van chemische energie."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Circle, FancyArrowPatch

from huisstijl import K, figuur, kader, label, pijl, achter, schema, toon  # noqa: F401

h = 6.62607015e-34
c = 2.99792458e8
kB = 1.380649e-23
NA = 6.02214076e23
eV = 1.602176634e-19


def _golflengte_kleur(nm):
    """Benaderende RGB-kleur van zichtbaar licht (380-750 nm)."""
    w = nm
    if 380 <= w < 440:
        r, g, b = -(w - 440) / 60, 0.0, 1.0
    elif w < 490:
        r, g, b = 0.0, (w - 440) / 50, 1.0
    elif w < 510:
        r, g, b = 0.0, 1.0, -(w - 510) / 20
    elif w < 580:
        r, g, b = (w - 510) / 70, 1.0, 0.0
    elif w < 645:
        r, g, b = 1.0, -(w - 645) / 65, 0.0
    elif w <= 750:
        r, g, b = 1.0, 0.0, 0.0
    else:
        r, g, b = 0.5, 0.5, 0.5
    f = 0.35 + 0.65 * (min(w - 380, 750 - w, 40) / 40) if 380 <= w <= 750 else 1
    return (r * f, g * f, b * f)


def _regenboog(ax, x0, x1, y0, y1, alfa=1.0, n=200):
    lam = np.linspace(380, 750, n)
    img = np.array([[_golflengte_kleur(l) for l in lam]])
    ax.imshow(img, extent=(x0, x1, y0, y1), aspect="auto", alpha=alfa, zorder=0)


# ------------------------------------------------------- ultravioletcatastrofe
def uv_catastrofe():
    fig, ax = figuur(6.8, 4.5)
    lam = np.linspace(30, 3000, 800) * 1e-9

    def planck(T):
        return 2 * h * c**2 / lam**5 / np.expm1(h * c / (lam * kB * T))

    norm = planck(5000).max()  # maximum bij 5000 K = 1
    rj = 2 * c * kB * 5000 / lam**4 / norm
    _regenboog(ax, 380, 750, 0, 0.035, alfa=0.85)
    label(ax, 565, 0.055, "zichtbaar", K.zacht, ha="center", fontsize=10)
    for T, k in [(3000, K.rood), (4000, K.oker), (5000, K.blauw)]:
        B = planck(T) / norm
        ax.plot(lam * 1e9, B, color=k)
        i = np.argmax(B)
        label(ax, lam[i] * 1e9 + 60, B[i] + 0.025, f"{T} K", k, fontsize=11)
    ax.plot(lam * 1e9, rj, color=K.tekst, lw=2.2)
    label(ax, 1480, 1.0, "klassieke theorie\n(Rayleigh-Jeans, 5000 K)", K.tekst, fontsize=11)
    label(ax, 2950, 0.73, "wet van Planck", K.blauw, ha="right", fontsize=11)
    pijl(ax, (2280, 0.705), (900, 0.476), K.blauw, lw=1.2)
    ax.set_xlim(0, 3000)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel(r"golflengte $\lambda$ (nm)")
    ax.set_ylabel("uitgestraalde intensiteit\n(relatief, maximum bij 5000 K = 1)")
    return kader(fig)


# ----------------------------------------------------------- foto-elektrisch effect
def foto_elektrisch():
    fig, ax = figuur(6.4, 4.3)
    schema(fig, ax)
    ax.set_aspect("auto")
    Phi, Ek = 4.0, 2.6
    ax.fill_between([1.4, 8.2], Phi, Phi + Ek + 0.9, color=K.vlak_accent, lw=0, zorder=0)
    for y, t in [(0, "gebonden elektron in het metaal"), (Phi, "vrij elektron in rust"),
                 (Phi + Ek, "uitgestoten foto-elektron")]:
        ax.plot([1.4, 8.2], [y, y], color=K.as_, lw=1.8)
        label(ax, 8.4, y, t, K.tekst, va="center", fontsize=11.5)
    label(ax, 6.0, Phi + Ek + 0.5, "vrije elektronen", K.accent, ha="center", fontsize=10.5, style="italic")
    # foton
    x = 2.6
    pijl(ax, (x, 0), (x, Phi + Ek), K.paars, lw=2.2)
    label(ax, x - 0.25, (Phi + Ek) / 2, r"$h\nu$", K.paars, ha="right", va="center", fontsize=15)
    x = 4.2
    pijl(ax, (x, 0), (x, Phi), K.oker, lw=2.2)
    label(ax, x + 0.2, Phi / 2, r"$\Phi$" + "\nwerkfunctie", K.oker, va="center", fontsize=12)
    pijl(ax, (x, Phi), (x, Phi + Ek), K.groen, lw=2.2)
    label(ax, x + 0.2, Phi + Ek / 2, r"$E_k$" + "\nkinetische energie", K.groen, va="center", fontsize=12)
    # energie-as
    pijl(ax, (0.7, -0.3), (0.7, 7.6), K.as_, lw=1.4)
    label(ax, 0.45, 3.6, "energie $E$", K.tekst, rotation=90, ha="center", va="center")
    ax.set_xlim(0.2, 13.4)
    ax.set_ylim(-0.6, 7.9)
    return kader(fig)


# ------------------------------------------------------------------ model van Bohr
def bohr():
    fig, ax = figuur(5.6, 4.6)
    schema(fig, ax)
    for n, r in [(1, 1.0), (2, 2.0), (3, 3.0)]:
        ax.add_patch(Circle((0, 0), r, fill=False, ec=K.zacht, lw=1.4, ls=(0, (3, 3))))
        label(ax, -0.15, r + 0.12, f"$n$ = {n}", K.accent, ha="right", fontsize=12)
    ax.add_patch(Circle((0, 0), 0.22, color=K.rood, zorder=3))
    label(ax, 0.3, -0.45, "+$Ze$", K.rood, fontsize=13)
    a3, a2 = np.radians(35), np.radians(18)
    p3 = (3 * np.cos(a3), 3 * np.sin(a3))
    p2 = (2 * np.cos(a2), 2 * np.sin(a2))
    for p in (p3, p2):
        ax.add_patch(Circle(p, 0.13, color=K.blauw, zorder=4))
    ax.add_patch(FancyArrowPatch(p3, p2, arrowstyle="-|>", mutation_scale=14, color=K.blauw, lw=1.8,
                                 shrinkA=6, shrinkB=6, connectionstyle="arc3,rad=0.25", zorder=5))
    label(ax, 2.72, 2.05, "elektron valt\nnaar lager niveau", K.blauw, fontsize=10.5, ha="left")
    # foton als golfje
    x = np.linspace(0, 1.8, 200)
    y = 0.16 * np.sin(2 * np.pi * x / 0.3)
    x0, y0 = 2.35, 0.55
    ax.plot(x0 + x, y0 + y, color=K.oker, lw=2)
    pijl(ax, (x0 + 1.75, y0), (x0 + 2.15, y0), K.oker, lw=2)
    label(ax, x0 + 1.3, y0 + 0.3, "foton wordt\nuitgezonden", K.oker, ha="center", va="bottom", fontsize=10.5)
    label(ax, x0 + 1.1, y0 - 0.85, r"$\Delta E = h\nu$", K.oker, ha="center", fontsize=14)
    ax.set_xlim(-3.3, 4.7)
    ax.set_ylim(-3.3, 3.5)
    return kader(fig)


# ---------------------------------------------------------------------- orbitalen
def _Y(naam, th, ph):
    st, ct = np.sin(th), np.cos(th)
    return {
        "s": np.ones_like(th),
        "p_z": ct, "p_x": st * np.cos(ph), "p_y": st * np.sin(ph),
        "d_{z^2}": 3 * ct**2 - 1, "d_{xz}": st * ct * np.cos(ph), "d_{yz}": st * ct * np.sin(ph),
        "d_{xy}": st**2 * np.sin(2 * ph), "d_{x^2-y^2}": st**2 * np.cos(2 * ph),
    }[naam]


def orbitalen():
    rijen = [["s"], ["p_x", "p_y", "p_z"], ["d_{xy}", "d_{xz}", "d_{yz}", "d_{x^2-y^2}", "d_{z^2}"]]
    fig = plt.figure(figsize=(8.4, 5.6))
    fig.get_layout_engine().set(w_pad=0.05, h_pad=0.05)
    gs = fig.add_gridspec(3, 10)
    th, ph = np.meshgrid(np.linspace(0, np.pi, 70), np.linspace(0, 2 * np.pi, 110))
    plus, min_ = np.array(to_rgb(K.accent)), np.array(to_rgb(K.oker))
    for i, rij in enumerate(rijen):
        n = len(rij)
        start = 5 - n
        for j, naam in enumerate(rij):
            ax = fig.add_subplot(gs[i, start + 2 * j:start + 2 * j + 2], projection="3d")
            Y = _Y(naam, th, ph)
            r = np.abs(Y) / np.abs(Y).max()
            X, Yc, Z = r * np.sin(th) * np.cos(ph), r * np.sin(th) * np.sin(ph), r * np.cos(th)
            basis = np.where((Y >= 0)[..., None], plus, min_)
            # eenvoudige belichting op basis van de normaal ~ positie
            nrm = np.stack([X, Yc, Z], -1)
            nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True) + 1e-9
            lv = np.array([-0.5, -0.6, 0.8]); lv /= np.linalg.norm(lv)
            hel = 0.55 + 0.45 * np.clip(nrm @ lv, 0, 1)
            kleur = np.clip(basis * hel[..., None] + 0.12 * (1 - hel[..., None]), 0, 1)
            ax.plot_surface(X, Yc, Z, facecolors=kleur, rstride=1, cstride=1, linewidth=0,
                            antialiased=False, shade=False, rasterized=True)
            ax.set_box_aspect((1, 1, 1))
            lim = 0.75
            ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
            ax.view_init(elev=22, azim=35)
            ax.set_axis_off()
            ax.patch.set_alpha(0)
            ax.text2D(0.5, -0.02, f"${naam}$", transform=ax.transAxes, ha="center",
                      color=K.tekst, fontsize=12)
    fig.text(0.04, 0.84, "$\\ell = 0$", color=K.zacht, fontsize=12)
    fig.text(0.04, 0.51, "$\\ell = 1$", color=K.zacht, fontsize=12)
    fig.text(0.04, 0.18, "$\\ell = 2$", color=K.zacht, fontsize=12)
    fig.text(0.97, 0.84, "■ positief", color=K.accent, ha="right", fontsize=11)
    fig.text(0.97, 0.78, "■ negatief", color=K.oker, ha="right", fontsize=11)
    fig.text(0.97, 0.72, "teken van de golffunctie", color=K.zacht, ha="right", fontsize=10)
    return kader(fig)


# ------------------------------------------------------- waterstofspectrum + overgangen
SERIES = [(1, "Lyman"), (2, "Balmer"), (3, "Paschen")]


def waterstof():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.4, 6.6), height_ratios=[1, 3.1])
    fig.get_layout_engine().set(w_pad=0.18, h_pad=0.12)
    kl = {1: K.paars, 2: K.accent, 3: K.rood}
    RH = 1.0967758e7  # m-1

    # bovenaan: lijnenspectrum (logaritmische golflengte-as)
    a1.set_xscale("log")
    a1.axvspan(380, 750, color=K.vlak_grijs, lw=0, zorder=0)
    for nl, naam in SERIES:
        lams = [1e9 / (RH * (1 / nl**2 - 1 / nh**2)) for nh in range(nl + 1, nl + 9)]
        for l in lams:
            kleur = _golflengte_kleur(l) if 380 <= l <= 750 else kl[nl]
            a1.plot([l, l], [0, 1], color=kleur, lw=1.8)
        a1.text(np.sqrt(min(lams) * max(lams)), 1.12, naam, color=kl[nl], ha="center", fontsize=11.5)
    a1.set_xlim(85, 2000)
    a1.set_ylim(0, 1.5)
    a1.set_yticks([])
    a1.spines["left"].set_visible(False)
    a1.set_xticks([100, 200, 500, 1000, 2000], ["100", "200", "500", "1000", "2000"])
    a1.set_xlabel(r"golflengte $\lambda$ (nm)", labelpad=2)

    # onderaan: energieniveaus en overgangen
    E = lambda n: -13.6057 / n**2
    for n in range(1, 7):
        a2.plot([0, 10], [E(n), E(n)], color=K.as_, lw=1.4)
        if n <= 4:
            a2.text(-0.2, E(n), f"$n$ = {n}", ha="right", va="center", fontsize=10.5, color=K.tekst)
        if n <= 3:
            a2.text(10.2, E(n), f"{E(n):.2f} eV", va="center", fontsize=10.5, color=K.zacht)
    a2.plot([0, 10], [0, 0], color=K.as_, lw=1.4, ls=(0, (4, 3)))
    a2.text(-0.2, 0, r"$n = \infty$", ha="right", va="center", fontsize=10.5)
    a2.text(10.2, 0, "0 eV (geïoniseerd)", va="center", fontsize=10.5, color=K.zacht)
    x0 = {1: 0.6, 2: 4.6, 3: 7.7}
    for nl, naam in SERIES:
        for i, nh in enumerate(range(nl + 1, 7)):
            x = x0[nl] + 0.42 * i
            a2.annotate("", xy=(x, E(nl)), xytext=(x, E(nh)),
                        arrowprops=dict(arrowstyle="-|>", color=kl[nl], lw=1.6, shrinkA=0, shrinkB=0,
                                        mutation_scale=11))
        tekst = f"{naam} (naar $n$ = {nl})" if nl == 3 else f"{naam}\n(naar $n$ = {nl})"
        a2.text(x0[nl] + 0.21 * (6 - nl - 1), E(nl) - 0.45, tekst,
                color=kl[nl], ha="center", va="top", fontsize=10.5 if nl == 3 else 11)
    a2.set_xlim(-1.6, 13.2)
    a2.set_ylim(-15.4, 0.8)
    a2.set_xticks([])
    a2.spines["bottom"].set_visible(False)
    a2.set_ylabel("energie $E_n$ (eV)")
    return kader(fig)


# ---------------------------------------------------------------- molecuulorbitalen
def molecuulorbitalen():
    fig, assen = plt.subplots(1, 2, figsize=(8.4, 4.4))
    for ax, (titel, n_el, orde) in zip(assen, [(r"H$_2$", 2, "1"), (r"He$_2$", 4, "0")]):
        schema(fig, ax)
        ax.set_aspect("auto")
        yA, yb, ya = 0.0, -1.3, 1.6
        for xs, y in [((0, 1.1), yA), ((3.9, 5.0), yA), ((1.95, 3.05), yb), ((1.95, 3.05), ya)]:
            ax.plot(xs, [y, y], color=K.tekst, lw=2.4, solid_capstyle="butt")
        for x1, x2, y in [(1.1, 1.95, yb), (1.1, 1.95, ya), (3.9, 3.05, yb), (3.9, 3.05, ya)]:
            ax.plot([x1, x2], [yA, y], color=K.zacht, lw=1.1, ls=(0, (3, 3)))
        label(ax, 2.5, yb - 0.62, r"$\sigma_{1s}$  bindend", K.accent, ha="center")
        label(ax, 2.5, ya + 0.45, r"$\sigma^*_{1s}$  antibindend", K.rood, ha="center")

        def elektronen(xm, y, n):
            dx = 0.14
            for i in range(n):
                x = xm - dx if i == 0 else xm + dx
                y0, y1 = (y - 0.32, y + 0.32) if i == 0 else (y + 0.32, y - 0.32)
                ax.annotate("", xy=(x, y1), xytext=(x, y0),
                            arrowprops=dict(arrowstyle="-|>", color=K.blauw, lw=1.6, mutation_scale=11,
                                            shrinkA=0, shrinkB=0))

        per_atoom = n_el // 2
        elektronen(0.55, yA, per_atoom)
        elektronen(4.45, yA, per_atoom)
        elektronen(2.5, yb, 2)
        if n_el > 2:
            elektronen(2.5, ya, 2)
        label(ax, 2.5, 2.55, titel, K.tekst, ha="center", fontsize=15)
        label(ax, 0.55, -0.8, "1$s$\natoom A", K.zacht, ha="center", fontsize=10.5)
        label(ax, 4.45, -0.8, "1$s$\natoom B", K.zacht, ha="center", fontsize=10.5)
        label(ax, 2.5, -2.55, f"bindingsorde = {orde}", K.paars, ha="center", fontsize=12,
              bbox=dict(boxstyle="round,pad=0.35", fc=K.vlak_paars, ec="none"))
        ax.set_xlim(-0.6, 5.6)
        ax.set_ylim(-3.0, 2.9)
    ax = assen[0]
    pijl(ax, (-0.45, -2.2), (-0.45, 2.3), K.as_, lw=1.3)
    label(ax, -0.62, 0, "energie", K.tekst, rotation=90, ha="center", va="center", fontsize=11)
    return kader(fig)


# ================================================================ VOORSTELLEN
def ek_frequentie():
    """Kinetische energie van foto-elektronen vs. frequentie voor twee metalen."""
    fig, ax = figuur(6.8, 4.5)
    nu = np.linspace(0, 16, 300)  # 1e14 Hz
    hE = h * 1e14 / eV  # eV per 1e14 Hz
    ax.axvspan(4.0, 7.9, color=K.vlak_grijs, lw=0, zorder=0)
    _regenboog(ax, 4.0, 7.9, -0.25, -0.05)
    label(ax, 5.95, 4.55, "zichtbaar licht", K.zacht, ha="center", fontsize=10.5)
    for naam, Phi, k in [("natrium", 2.30, K.accent), ("koper", 4.70, K.rood)]:
        nu0 = Phi / hE
        m = nu >= nu0
        ax.plot(nu[m], hE * nu[m] - Phi, color=k)
        ax.plot(nu[~m], 0 * nu[~m], color=k, lw=2.6, alpha=0.35)
        ax.plot(nu0, 0, "o", color=k, zorder=5)
        label(ax, nu0, -0.55, rf"$\nu_0$ = {nu0:.1f}", k, ha="center", fontsize=10.5)
        label(ax, 15.8, hE * 15.8 - Phi + 0.12, f"{naam}\n$\\Phi$ = {Phi:.2f} eV", k,
              ha="right", va="bottom", fontsize=11)
    label(ax, 9.6, 1.2, r"helling = $h$" + "\n(voor elk metaal dezelfde)", K.tekst, fontsize=11)
    label(ax, 0.3, 3.3, "onder de drempel $\\nu_0$:\ngeen elektronen,\nhoe fel het licht ook is",
          K.zacht, fontsize=10.5, style="italic")
    ax.set_xlim(0, 16)
    ax.set_ylim(-0.8, 5)
    ax.axhline(0, color=K.as_, lw=0.8)
    ax.set_xlabel(r"frequentie van het licht $\nu$ ($10^{14}$ Hz)")
    ax.set_ylabel(r"kinetische energie $E_k$ (eV)")
    return kader(fig)


def spectrum_bindingen():
    """Energie van een mol fotonen over het spectrum, vergeleken met bindingsenergieën."""
    fig, ax = figuur(7.6, 4.9)
    lam = np.geomspace(50, 1e9, 400)  # nm
    E = h * c / (lam * 1e-9) * NA / 1000  # kJ/mol
    gebieden = [(50, 380, "UV", K.vlak_paars), (750, 1e6, "infrarood", K.vlak_rood),
                (1e6, 1e9, "microgolf", K.vlak_oker)]
    for a, b, t, k in gebieden:
        ax.axvspan(a, b, color=k, lw=0, zorder=0)
        label(ax, np.sqrt(a * b), 15000, t, K.zacht, ha="center", va="top", fontsize=10.5)
    _regenboog(ax, 380, 750, 1e-4, 3e4, alfa=0.35)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot(lam, E, color=K.tekst, lw=2.6, zorder=4)
    for t, e, va, x in [("N≡N  945", 945, "bottom", 3e5), ("O–H  463", 463, "bottom", 3e7),
                        ("C–C  348", 348, "top", 3e6)]:
        ax.axhline(e, color=K.accent, lw=1.1, ls=(0, (4, 3)), zorder=2)
        label(ax, x, e * (1.08 if va == "bottom" else 0.92), t, K.accent, ha="center", va=va, fontsize=10.5)
    RT = 8.314e-3 * 298
    ax.axhline(RT, color=K.rood, lw=1.1, ls=(0, (4, 3)))
    label(ax, 8e8, RT * 1.12, r"$RT$ bij 25 °C = 2.5", K.rood, ha="right", va="bottom", fontsize=10.5)
    ax.plot(1.22e8, h * c / 0.122 * NA / 1000, "o", color=K.oker, zorder=5)
    label(ax, 1.22e8, h * c / 0.122 * NA / 1000 * 2.2, "magnetron\n(12 cm)", K.oker, ha="center",
          va="bottom", fontsize=10)
    label(ax, 900, 0.3, "← UV breekt C–C-bindingen:\n    zonnebrand, vergeelde kunststof", K.paars,
          fontsize=10.5, va="center")
    label(ax, 4e4, 110, "IR en microgolven:\nmoleculen trillen en\ndraaien sneller (opwarmen),\nbindingen blijven heel",
          K.rood, fontsize=10.5, va="top")
    ax.set_xlim(50, 1e9)
    ax.set_ylim(1e-4, 30000)
    ax.set_xlabel(r"golflengte $\lambda$ (nm)")
    ax.set_ylabel("energie per mol fotonen (kJ mol$^{-1}$)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:g}"))
    return kader(fig)


def morse_h2():
    """Potentiële energie van H2 in functie van de kernafstand (Morse) met trillingsniveaus."""
    fig, ax = figuur(6.8, 4.6)
    De, re, a = 458.0, 74.1, 0.01935  # kJ/mol, pm, 1/pm
    r = np.linspace(38, 330, 600)
    V = De * (1 - np.exp(-a * (r - re))) ** 2 - De
    ax.plot(r, V, color=K.accent, zorder=4)
    we = 52.6  # kJ/mol (4401 cm-1)
    for v in range(6):
        Ev = we * (v + 0.5) - we**2 * (v + 0.5) ** 2 / (4 * De) - De
        r1 = re - np.log(1 + np.sqrt((Ev + De) / De)) / a
        r2 = re - np.log(1 - np.sqrt((Ev + De) / De)) / a
        ax.plot([r1, r2], [Ev, Ev], color=K.blauw, lw=1.3, zorder=3)
    E0 = we * 0.5 - we**2 * 0.25 / (4 * De) - De
    ax.axhline(0, color=K.zacht, lw=1.1, ls=(0, (4, 3)))
    label(ax, 325, 12, "twee losse H-atomen", K.zacht, ha="right", fontsize=10.5)
    ax.plot([re, re], [-De, 40], color=K.zacht, lw=1.0, ls=(0, (1.5, 2.5)))
    label(ax, re + 3, 55, r"$r_e$ = 74 pm" + "\nbindingslengte", K.tekst, fontsize=10.5)
    pijl(ax, (305, 0), (305, -De), K.rood, lw=1.4, stijl="<|-|>")
    label(ax, 298, -380, r"$D_e$ = 458 kJ mol$^{-1}$", K.rood, ha="right", va="center", fontsize=11)
    pijl(ax, (180, 0), (180, E0), K.oker, lw=1.4, stijl="<|-|>")
    label(ax, 185, -235, r"$D_0$ = 432 kJ mol$^{-1}$" + "\n(nodig om te breken)", K.oker,
          va="center", fontsize=10.5)
    label(ax, 128, -330, "trillingsniveaus", K.blauw, fontsize=10.5)
    label(ax, 44, 260, "kernen te dicht:\nsterke afstoting", K.tekst, fontsize=10.5)
    ax.set_xlim(30, 330)
    ax.set_ylim(-500, 330)
    ax.set_xlabel("afstand tussen de kernen $r$ (pm)")
    ax.set_ylabel(r"potentiële energie (kJ mol$^{-1}$)")
    return kader(fig)


# ================================================================ CASE: CO2 EN HET BROEIKASEFFECT
_C2 = h * c / kB * 100  # tweede stralingsconstante in cm K


def _planck(lam_um, T):
    """Wet van Planck: uitgestraald vermogen per golflengte-eenheid (willekeurige eenheid)."""
    lam = lam_um * 1e-6
    x = h * c / (lam * kB * T)
    with np.errstate(over="ignore"):
        return lam**-5 / np.expm1(x)


def zon_aarde_spectrum():
    """Straling van de zon (5800 K) en van de aarde (15 °C), met de absorptiebanden van CO2."""
    fig, ax = figuur(7.4, 4.6)
    lam = np.geomspace(0.1, 100, 800)
    for T, naam, k, x, y in [(5772, "zon\n(5800 K)", K.oker, 0.27, 0.80),
                             (288, "aarde\n(15 °C)", K.rood, 32, 0.80)]:
        B = _planck(lam, T)
        B = B / B.max()
        ax.fill_between(lam, B, color=k, alpha=0.18, lw=0)
        ax.plot(lam, B, color=k)
        label(ax, x, y, naam, k, ha="center", fontsize=11.5)
        lmax = 2897.8 / T
        ax.plot([lmax, lmax], [0, 1.0], color=k, lw=1.0, ls=(0, (2, 2)))
        label(ax, lmax, 1.03, rf"$\lambda_{{\max}}$ = {lmax:.1f} µm" if lmax > 1 else
              rf"$\lambda_{{\max}}$ = {lmax:.2f} µm", k, ha="center", va="bottom", fontsize=10.5)
    _regenboog(ax, 0.38, 0.75, -0.075, -0.02)
    for a, b, t in [(4.2, 4.45, "4.3 µm"), (13.5, 17.0, "15 µm")]:
        ax.axvspan(a, b, color=K.accent, alpha=0.28, lw=0, zorder=1)
        label(ax, np.sqrt(a * b), 1.20, t, K.accent, ha="center", va="bottom", fontsize=10.5)
    label(ax, 8.0, 1.36, r"absorptie door CO$_2$", K.accent, ha="center", va="bottom", fontsize=11)
    ax.set_xscale("log")
    ax.set_xlim(0.1, 100)
    ax.set_ylim(-0.09, 1.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:g}"))
    ax.set_xlabel(r"golflengte $\lambda$ (µm)")
    ax.set_ylabel("uitgestraald vermogen\n(elk geschaald op zijn maximum)")
    return kader(fig)


def ndir_sensor():
    """Principe van een CO2-meter: infrarood licht door een gascel, filter bij 4.26 µm, detector."""
    fig, ax = figuur(7.6, 2.9)
    schema(fig, ax)
    # lamp
    ax.add_patch(Circle((0.6, 1.0), 0.35, fc=K.vlak_rood, ec=K.rood, lw=1.6))
    label(ax, 0.6, 0.35, "IR-lamp", K.rood, ha="center", va="top", fontsize=10.5)
    # gascel
    ax.add_patch(plt.Rectangle((1.5, 0.45), 4.0, 1.1, fc=K.vlak_accent, ec=K.accent, lw=1.6))
    label(ax, 3.5, 0.35, "gascel met lucht uit de klas", K.accent, ha="center", va="top", fontsize=10.5)
    rng = np.random.default_rng(3)
    for x, y in zip(rng.uniform(1.75, 5.25, 26), rng.uniform(0.6, 1.4, 26)):
        ax.add_patch(Circle((x, y), 0.035, fc=K.zacht, ec="none"))
    for x, y in [(2.3, 1.22), (3.3, 0.72), (4.4, 1.15)]:
        ax.add_patch(Circle((x, y), 0.05, fc=K.tekst, ec="none"))
        ax.add_patch(Circle((x - 0.11, y), 0.055, fc=K.rood, ec="none"))
        ax.add_patch(Circle((x + 0.11, y), 0.055, fc=K.rood, ec="none"))
    label(ax, 4.4, 1.32, r"CO$_2$", K.tekst, ha="center", va="bottom", fontsize=10)
    # stralen
    for y, a in [(0.85, 1.0), (1.0, 1.0), (1.15, 1.0)]:
        pijl(ax, (0.98, y), (1.5, y), K.rood, lw=1.4)
    for y, lw in [(0.85, 1.0), (1.15, 1.0)]:
        pijl(ax, (5.5, y), (6.05, y), K.rood, lw=lw)
    # filter
    ax.add_patch(plt.Rectangle((6.1, 0.55), 0.14, 0.9, fc=K.vlak_oker, ec=K.oker, lw=1.6))
    label(ax, 6.17, 1.55, "filter\n4.26 µm", K.oker, ha="center", va="bottom", fontsize=10.5)
    pijl(ax, (6.26, 1.0), (6.85, 1.0), K.rood, lw=1.0)
    # detector
    ax.add_patch(plt.Rectangle((6.9, 0.7), 0.45, 0.6, fc=K.vlak_paars, ec=K.paars, lw=1.6))
    label(ax, 7.12, 0.6, "detector", K.paars, ha="center", va="top", fontsize=10.5)
    label(ax, 3.5, 1.68, "hoe meer CO$_2$, hoe minder licht van 4.26 µm de detector bereikt",
          K.tekst, ha="center", va="bottom", fontsize=10.5)
    ax.set_xlim(0.1, 7.6)
    ax.set_ylim(-0.05, 2.05)
    return kader(fig)


def mo_stikstof():
    """Molecuulorbitaaldiagram van N2 (valentie-elektronen): bindingsorde 3."""
    fig, ax = figuur(7.0, 5.6)
    schema(fig, ax)
    ax.set_aspect("auto")
    xa, xb, xm = (0.0, 1.1), (4.9, 6.0), (2.35, 3.65)
    y2s, y2p = -2.2, 0.6
    mo = [("σ2s", -2.9, 1, K.accent), ("σ*2s", -1.5, 1, K.rood), ("π2p", -0.1, 2, K.accent),
          ("σ2p", 0.35, 1, K.accent), ("π*2p", 1.5, 2, K.rood), ("σ*2p", 2.4, 1, K.rood)]
    bezetting = {"σ2s": 2, "σ*2s": 2, "π2p": 4, "σ2p": 2, "π*2p": 0, "σ*2p": 0}

    def niveau(x0, x1, y, n, k=K.tekst):
        if n == 1:
            ax.plot([x0, x1], [y, y], color=k, lw=2.4, solid_capstyle="butt")
            return [(x0 + x1) / 2]
        w = (x1 - x0 - 0.15) / 2
        ax.plot([x0, x0 + w], [y, y], color=k, lw=2.4, solid_capstyle="butt")
        ax.plot([x1 - w, x1], [y, y], color=k, lw=2.4, solid_capstyle="butt")
        return [x0 + w / 2, x1 - w / 2]

    def pijltjes(xm_, y, n):
        for i in range(n):
            dx = -0.09 if i == 0 else 0.09
            y0, y1 = (y - 0.22, y + 0.22) if i == 0 else (y + 0.22, y - 0.22)
            ax.annotate("", xy=(xm_ + dx, y1), xytext=(xm_ + dx, y0),
                        arrowprops=dict(arrowstyle="-|>", color=K.blauw, lw=1.4, mutation_scale=9,
                                        shrinkA=0, shrinkB=0))

    for xs in (xa, xb):
        c0 = niveau(*xs, y2s, 1)
        pijltjes(c0[0], y2s, 2)
        w = (xs[1] - xs[0]) / 3
        for j in range(3):
            xx = (xs[0] + j * w + 0.04, xs[0] + (j + 1) * w - 0.04)
            ax.plot(xx, [y2p, y2p], color=K.tekst, lw=2.4, solid_capstyle="butt")
            pijltjes((xx[0] + xx[1]) / 2, y2p, 1)
    label(ax, 0.55, y2s - 0.45, "2$s$", K.zacht, ha="center", va="top", fontsize=10.5)
    label(ax, 0.55, y2p - 0.42, "2$p$", K.zacht, ha="center", va="top", fontsize=10.5)
    label(ax, 5.45, y2s - 0.45, "2$s$", K.zacht, ha="center", va="top", fontsize=10.5)
    label(ax, 5.45, y2p - 0.42, "2$p$", K.zacht, ha="center", va="top", fontsize=10.5)
    for naam, y, n, k in mo:
        xs = niveau(*xm, y, n, k)
        e = bezetting[naam]
        if n == 1:
            pijltjes(xs[0], y, e)
        else:
            for x in xs:
                pijltjes(x, y, e // 2)
        label(ax, xm[1] + 0.12, y, naam, k, va="center", fontsize=11)
    for y_at, ys in [(y2s, [-2.9, -1.5]), (y2p, [-0.1, 0.35, 1.5, 2.4])]:
        for y in ys:
            ax.plot([xa[1], xm[0]], [y_at, y], color=K.zacht, lw=0.9, ls=(0, (3, 3)))
            ax.plot([xb[0], xm[1]], [y_at, y], color=K.zacht, lw=0.9, ls=(0, (3, 3)))
    label(ax, 0.55, 3.0, "N", K.tekst, ha="center", fontsize=14)
    label(ax, 5.45, 3.0, "N", K.tekst, ha="center", fontsize=14)
    label(ax, 3.0, 3.0, r"N$_2$", K.tekst, ha="center", fontsize=14)
    label(ax, 3.0, -3.75, "bindingsorde = (8 − 2)/2 = 3", K.paars, ha="center", fontsize=12,
          bbox=dict(boxstyle="round,pad=0.35", fc=K.vlak_paars, ec="none"))
    pijl(ax, (-0.45, -3.3), (-0.45, 2.8), K.as_, lw=1.3)
    label(ax, -0.62, -0.2, "energie", K.tekst, rotation=90, ha="center", va="center", fontsize=11)
    ax.set_xlim(-0.8, 6.3)
    ax.set_ylim(-4.2, 3.4)
    return kader(fig)


def trillingen_co2():
    """De drie trillingen van CO2 en de trilling van N2: welke veranderen het dipoolmoment?"""
    fig, assen = plt.subplots(1, 4, figsize=(9.6, 3.6))
    gevallen = [
        (r"N$_2$", "strek", 2330, False, "dipool blijft 0"),
        (r"CO$_2$", "symmetrische strek", 1333, False, "dipool blijft 0"),
        (r"CO$_2$", "buiging", 667, True, "dipool verandert"),
        (r"CO$_2$", "asymmetrische strek", 2349, True, "dipool verandert"),
    ]
    for ax, (mol, naam, nu, actief, dip) in zip(assen, gevallen):
        schema(fig, ax)
        if mol == r"N$_2$":
            atomen = [(-0.45, 0, K.blauw, 0.22), (0.45, 0, K.blauw, 0.22)]
            pijlen = [((-0.45, 0), (-0.85, 0)), ((0.45, 0), (0.85, 0))]
        elif naam == "symmetrische strek":
            atomen = [(-0.75, 0, K.rood, 0.2), (0, 0, K.tekst, 0.17), (0.75, 0, K.rood, 0.2)]
            pijlen = [((-0.75, 0), (-1.12, 0)), ((0.75, 0), (1.12, 0))]
        elif naam == "buiging":
            atomen = [(-0.75, 0, K.rood, 0.2), (0, 0, K.tekst, 0.17), (0.75, 0, K.rood, 0.2)]
            pijlen = [((-0.75, 0), (-0.75, 0.4)), ((0.75, 0), (0.75, 0.4)), ((0, 0), (0, -0.4))]
        else:
            atomen = [(-0.75, 0, K.rood, 0.2), (0, 0, K.tekst, 0.17), (0.75, 0, K.rood, 0.2)]
            pijlen = [((-0.75, 0), (-0.4, 0)), ((0.75, 0), (1.1, 0)), ((0, 0), (-0.38, -0.0))]
        x = [a[0] for a in atomen]
        ax.plot([min(x), max(x)], [0, 0], color=K.zacht, lw=3, zorder=1)
        for xx, yy, k, r in atomen:
            ax.add_patch(Circle((xx, yy), r, fc=k, ec="none", zorder=3))
        for van, naar in pijlen:
            if naam == "asymmetrische strek" and van == (0, 0):
                pijl(ax, (0, 0.33), (-0.4, 0.33), K.groen, lw=2.0)
                continue
            pijl(ax, van, naar, K.groen, lw=2.0, zorder=4)
        label(ax, 0, 1.05, mol, K.tekst, ha="center", fontsize=13)
        label(ax, 0, 0.78, naam, K.zacht, ha="center", fontsize=10.5)
        label(ax, 0, -0.72, rf"{nu} cm$^{{-1}}$  ({1e4 / nu:.1f} µm)", K.tekst, ha="center", fontsize=10.5)
        k = K.accent if actief else K.rood
        label(ax, 0, -1.02, dip, k, ha="center", fontsize=10.5)
        label(ax, 0, -1.34, "IR-actief" if actief else "IR-inactief", k, ha="center", fontsize=12,
              fontweight="bold")
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.55, 1.3)
    return kader(fig)


def cp_co2_n2():
    """Warmtecapaciteit van N2 en CO2: model met gekwantiseerde trillingen tegenover metingen."""
    fig, ax = figuur(6.8, 4.5)
    R = 8.314
    T = np.linspace(100, 1500, 400)

    def cv_vib(nu, T):
        x = _C2 * nu / T
        return x**2 * np.exp(x) / np.expm1(x) ** 2

    cp_n2 = R * (3.5 + cv_vib(2330, T))
    cp_co2 = R * (3.5 + cv_vib(1333, T) + 2 * cv_vib(667, T) + cv_vib(2349, T))
    for cp, k, naam, ywaarde in [(cp_n2, K.blauw, r"N$_2$", 31.5), (cp_co2, K.rood, r"CO$_2$", 51)]:
        ax.plot(T, cp, color=k)
    # metingen (correlaties tabel H1, NIST, 300-1000 K)
    Tm = np.array([300, 400, 500, 600, 700, 800, 900, 1000])
    for (a, b, cc), k in [((28.5, 3.6e-4, 4.00e-6), K.blauw), ((23.9, 5.21e-2, -2.20e-5), K.rood)]:
        ax.plot(Tm, a + b * Tm + cc * Tm**2, "o", color=k, ms=6, mfc=K.achtergrond, mew=1.6, zorder=5)
    label(ax, 1480, 34.8, r"N$_2$", K.blauw, ha="right", fontsize=12)
    label(ax, 1480, 56.5, r"CO$_2$", K.rood, ha="right", fontsize=12)
    ax.axhline(3.5 * R, color=K.zacht, lw=1.0, ls=(0, (4, 3)))
    label(ax, 110, 3.5 * R - 0.6, r"$\frac{7}{2}R$: enkel translatie en rotatie", K.zacht, va="top", fontsize=10.5)
    label(ax, 560, 42.5, "lijnen: model met gekwantiseerde trillingen\nbolletjes: metingen (NIST)",
          K.tekst, fontsize=10.5, va="top")
    ax.set_xlim(100, 1500)
    ax.set_ylim(26, 60)
    ax.set_xlabel(r"temperatuur $T$ (K)")
    ax.set_ylabel(r"$C_{p,\mathrm{m}}$ (J mol$^{-1}$ K$^{-1}$)")
    return kader(fig)
