"""Toestandsvergelijkingen om figuren met realistische data te tekenen.

Peng-Robinson voor afzonderlijke gassen, Lee-Kesler (eenvoudig fluïdum)
voor de algemene compressibiliteitskaart.
"""
import numpy as np


def brentq(f, a, b, tol=1e-12, n=200):
    """Eenvoudige bisectie (zonder scipy)."""
    fa = f(a)
    for _ in range(n):
        m = 0.5 * (a + b)
        fm = f(m)
        if np.sign(fm) == np.sign(fa):
            a, fa = m, fm
        else:
            b = m
        if abs(b - a) < tol * max(1.0, abs(m)):
            break
    return 0.5 * (a + b)

R = 8.314462618  # J/(mol K)

# Kritische gegevens: Tc [K], pc [Pa], acentrische factor
GASSEN = {
    "H2": (33.19, 13.13e5, -0.216),
    "N2": (126.2, 33.98e5, 0.037),
    "CH4": (190.56, 45.99e5, 0.011),
    "C2H6": (305.32, 48.72e5, 0.099),
    "C2H4": (282.34, 50.41e5, 0.087),
    "CO2": (304.13, 73.77e5, 0.225),
}


# ------------------------------------------------------------ Peng-Robinson
def _pr_ab(T, Tc, pc, w):
    k = 0.37464 + 1.54226 * w - 0.26992 * w**2
    alfa = (1 + k * (1 - np.sqrt(T / Tc))) ** 2
    a = 0.45724 * R**2 * Tc**2 / pc * alfa
    b = 0.07780 * R * Tc / pc
    return a, b


def pr_druk(Vm, T, gas):
    """Druk [Pa] bij molair volume Vm [m3/mol]."""
    a, b = _pr_ab(T, *GASSEN[gas])
    return R * T / (Vm - b) - a / (Vm**2 + 2 * b * Vm - b**2)


def _pr_Z_wortels(T, p, gas):
    a, b = _pr_ab(T, *GASSEN[gas])
    A = a * p / (R * T) ** 2
    B = b * p / (R * T)
    c = [1, -(1 - B), A - 3 * B**2 - 2 * B, -(A * B - B**2 - B**3)]
    z = np.roots(c)
    z = np.sort(z[np.abs(z.imag) < 1e-9].real)
    return z[z > B], A, B


def pr_Z(T, p, gas, fase="damp"):
    z, _, _ = _pr_Z_wortels(T, p, gas)
    return z[-1] if fase == "damp" else z[0]


def _ln_phi(z, A, B):
    s2 = np.sqrt(2)
    return z - 1 - np.log(z - B) - A / (2 * s2 * B) * np.log((z + (1 + s2) * B) / (z + (1 - s2) * B))


def pr_verzadiging(T, gas):
    """Dampdruk [Pa] en molaire volumes (vloeistof, damp) [m3/mol] via gelijke fugaciteit."""
    Tc, pc, w = GASSEN[gas]

    def f(p):
        z, A, B = _pr_Z_wortels(T, p, gas)
        if len(z) < 2:
            return np.nan
        return _ln_phi(z[0], A, B) - _ln_phi(z[-1], A, B)

    # drukgebied met drie wortels = tussen de spinodale punten van de isotherm
    _, b = _pr_ab(T, Tc, pc, w)
    V = np.geomspace(b * 1.001, b * 400, 20000)
    p = pr_druk(V, T, gas)
    d = np.diff(p)
    ext = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0] + 1
    p_lo, p_hi = max(p[ext[0]], 1e-6 * pc), p[ext[1]]
    eps = 1e-9 * (p_hi - p_lo)
    psat = brentq(f, p_lo + eps, p_hi - eps)
    z, _, _ = _pr_Z_wortels(T, psat, gas)
    return psat, z[0] * R * T / psat, z[-1] * R * T / psat


# ------------------------------------------------- Lee-Kesler (eenvoudig fluïdum)
_LK = dict(b1=0.1181193, b2=0.265728, b3=0.154790, b4=0.030323,
           c1=0.0236744, c2=0.0186984, c3=0.0, c4=0.042724,
           d1=0.155488e-4, d2=0.623689e-4, beta=0.65392, gamma=0.060167)


def lee_kesler_Z(Tr, pr):
    k = _LK
    B = k["b1"] - k["b2"] / Tr - k["b3"] / Tr**2 - k["b4"] / Tr**3
    C = k["c1"] - k["c2"] / Tr + k["c3"] / Tr**3
    D = k["d1"] + k["d2"] / Tr

    def Zv(V):
        return (1 + B / V + C / V**2 + D / V**5
                + k["c4"] / (Tr**3 * V**2) * (k["beta"] + k["gamma"] / V**2) * np.exp(-k["gamma"] / V**2))

    def f(V):
        return pr * V / Tr - Zv(V)

    Vs = np.geomspace(0.01, 1e4, 3000)
    fs = f(Vs)
    idx = np.where(np.sign(fs[:-1]) != np.sign(fs[1:]))[0]
    i = idx[-1]  # grootste volume = gasachtige wortel
    V = brentq(f, Vs[i], Vs[i + 1])
    return pr * V / Tr
