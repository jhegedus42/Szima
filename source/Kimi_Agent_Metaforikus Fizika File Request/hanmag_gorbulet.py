# -*- coding: utf-8 -*-
"""
HANMAG-GORBULET -- a kotodes geometriaja, merve.

A kerdes: a Hebb-kotes tenyleg gorbiti-e a geometriat?
Valasz, harom mert tenyben:

  1. KOTES NELKUL NINCS GEOMETRIA: a friss vilag par-grafja ures
     (Van Raamsdonk-torveny: az osszefonodas a terosszefugges ragasztoja).

  2. A STABILIZATOR-FONODAS NEM PAROS: a darab-kotesek utan a PPT-fele
     paros fonodasi graf URES marad -- a monogamia es a kod-struktura a
     korrelaciot tobbes/blokk-formaba tereli. Az assembly nem haromszog,
     hanem HIPEREL (GHZ-signatura: minden reszhalmaz S=1, par-fonodas 0).

  3. A GORBSEG A ZARODASOKBAN VAN: a K3 haromszog-anchor Ollivier-Ricci
     gorbsege +0.5; a vezetekek es fakeszetege 0. A Hebb-szabaly, amikor
     zaroeleket hoz letre, pozitiv-gorbsegu zsebet epit: az a sejtassembly.

Futtatas:  python3 hanmag_gorbulet.py
A vege:    GORBULET ELLENORIZVE
"""

import numpy as np
from itertools import combinations
from scipy.optimize import linprog
import hanmag_vilag as V


def ellenoriz(felt, uzenet):
    print(("    [OK] " if felt else "    [HIBA] ") + uzenet)
    if not felt:
        raise AssertionError(uzenet)


def banner(szoveg):
    print("\n" + "=" * 64)
    print(szoveg)
    print("=" * 64)


# ----------------------------------------------------------------------
# 1. KAPUK ES ALLAPOTVEKTOR (egzakt, a normalt projekcio modszerrel)
# ----------------------------------------------------------------------

def h_kapu(a, q):
    """Hadamard a q-n: X<->Z, Y->-Y."""
    for p in a.g:
        x, z = (p.x >> q) & 1, (p.z >> q) & 1
        p.s ^= (x & z)
        p.x = (p.x & ~(1 << q)) | (z << q)
        p.z = (p.z & ~(1 << q)) | (x << q)


def allapot_vektor(a, n=7):
    """|psi> a stabilizator-csoport osszegzesevel; onnormalizalo projekcio.

    psi = Sum_{g in <G>} g|0> / ||...|| -- a generatorok operatorkent,
    egymas utan, igy a fazisok egzaktak (nincs csoportszorzas-hiba).
    """
    psi = np.zeros(1 << n, dtype=complex)
    for idx in range(1 << len(a.g)):
        amp = np.zeros(1 << n, dtype=complex)
        amp[0] = 1.0
        for k in range(len(a.g)):
            if not (idx >> k) & 1:
                continue
            g = a.g[k]
            uj = np.zeros(1 << n, dtype=complex)
            for b in range(1 << n):
                if amp[b] == 0:
                    continue
                fazis = ((-1) ** (g.s ^ ((g.z & b).bit_count() % 2))
                         * (1j) ** ((g.x & g.z).bit_count() % 4))
                uj[b ^ g.x] += amp[b] * fazis
            amp = uj
        psi += amp
    return psi / np.linalg.norm(psi)


# ----------------------------------------------------------------------
# 2. PAROS FONODAS: redukalt suruseg + Peres-Horodecki (PPT)
# ----------------------------------------------------------------------

def rho_par(psi, n, x, y):
    """a (x,y) qubit-par redukalt surusegmatrixa.
    Figyelem: a reshape utan a q qubit az (n-1-q) tengely!"""
    t = np.moveaxis(psi.reshape([2] * n), [n - 1 - x, n - 1 - y], [0, 1])
    m = t.reshape(4, -1)
    return m @ m.conj().T


def ppt_min(rho):
    """a parcialis transzponalt legkisebb sajaterteke; fonott, ha < 0.
    A PT a b es b' tengelyek CSEREJE: transpose(0,3,2,1)."""
    pt = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    return float(np.linalg.eigvalsh((pt + pt.conj().T) / 2).min())


def par_graf(a, n=7):
    """PPT-fele paros fonodasi graf: el, ahol a redukalt par fonott."""
    psi = allapot_vektor(a, n)
    E = {}
    for x, y in combinations(range(n), 2):
        lam = ppt_min(rho_par(psi, n, x, y))
        if lam < -1e-9:
            E[(x, y)] = round(-lam, 3)
    return E


def blokk_elek(a, n=7):
    """blokk-vagas elek: a par-mint-egyseg fonodik a tobbiekkel (S < 2)."""
    E = {}
    for x, y in combinations(range(n), 2):
        s = a.vagas_entropia((1 << x) | (1 << y))
        if s < 1.999:
            E[(x, y)] = 2 - s
    return E


# ----------------------------------------------------------------------
# 3. GRAF-GORBOSEG: Forman- es Ollivier-Ricci
# ----------------------------------------------------------------------

def fok(E):
    d = {i: 0 for i in range(7)}
    for (a, b) in E:
        d[a] += 1
        d[b] += 1
    return d


def graf_tav(E):
    N = {i: set() for i in range(7)}
    for (a, b) in E:
        N[a].add(b)
        N[b].add(a)
    D = {}
    for s in range(7):
        dist = {s: 0}
        q = [s]
        for u in q:
            for w in N[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    q.append(w)
        for t in range(7):
            D[(s, t)] = dist.get(t, 10)
    return D


def forman(E):
    """Forman-Ricci: F(e) = 4 - deg(u) - deg(v)."""
    d = fok(E)
    return {e: 4 - d[e[0]] - d[e[1]] for e in E}


def ollivier(E):
    """Ollivier-Ricci: k(e) = 1 - W1(m_x, m_y)/d(x,y), egyenletes szomszed-mertekkel."""
    d = fok(E)
    D = graf_tav(E)
    N = {i: set() for i in range(7)}
    for (a, b) in E:
        N[a].add(b)
        N[b].add(a)
    kap = {}
    for (x, y) in E:
        px = {u: 1 / d[x] for u in N[x]}
        py = {u: 1 / d[y] for u in N[y]}
        sx, sy = sorted(px), sorted(py)
        nx, ny = len(sx), len(sy)
        c = [D[(i, j)] for i in sx for j in sy]
        Aeq, beq = [], []
        for i in range(nx):
            row = [0] * (nx * ny)
            for j in range(ny):
                row[i * ny + j] = 1
            Aeq.append(row)
            beq.append(px[sx[i]])
        for j in range(ny):
            row = [0] * (nx * ny)
            for i in range(nx):
                row[i * ny + j] = 1
            Aeq.append(row)
            beq.append(py[sy[j]])
        r = linprog(c, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
        kap[(x, y)] = round(1 - r.fun / D[(x, y)], 3)
    return kap


# ----------------------------------------------------------------------
# 4. KISERLETEK
# ----------------------------------------------------------------------

def kiserlet_sanity():
    banner("0. SANITY -- a merorud ellenorzese")
    R = np.zeros((4, 4), dtype=complex)
    R[0, 0] = R[3, 3] = R[0, 3] = R[3, 0] = 0.5
    ellenoriz(abs(ppt_min(R) + 0.5) < 1e-9, "kezi Bell: PPT min = -0.5")
    b = V.Allapot([V.Pauli(z=1 << q) for q in range(7)])
    h_kapu(b, 0)
    b.cnot(0, 1)
    lam = ppt_min(rho_par(allapot_vektor(b), 7, 0, 1))
    ellenoriz(abs(lam + 0.5) < 1e-9, "motor-Bell: PPT min = -0.5")


def kiserlet_nincs_geometria():
    banner("1. KOTES NELKUL NINCS GEOMETRIA (Van Raamsdonk)")
    v = V.epits_vilagot()
    ellenoriz(par_graf(v) == {}, "friss vilag: a PPT par-graf URES")
    ellenoriz(blokk_elek(v) == {}, "friss vilag: blokk-elek sincsenek")
    print("    -> a geometria nem adott: a kotodesek epitik.")


def kiserlet_nem_paros():
    banner("2. A STABILIZATOR-FONODAS NEM PAROS (monogamia, merve)")
    v = V.epits_vilagot()
    for k in range(3):
        if k:
            v.cnot(k - 1, k)
        v.permutal(V.SINGER7)
    print("    3 jelentesdarab bekotve (a vilag-kiserlet)")
    ellenoriz(par_graf(v) == {}, "a PPT par-graf a kotesek utan is URES")
    be = blokk_elek(v)
    ellenoriz(len(be) > 0, "a blokk-vagas graf nem ures: %s" % (be,))
    print("    -> a fonodas blokk/tobbes-formaban jon letre, nem parosan.")

    g = V.Allapot([V.Pauli(z=1 << q) for q in range(7)])
    h_kapu(g, 0)
    g.cnot(0, 1)
    g.cnot(0, 2)
    ellenoriz(par_graf(g) == {}, "GHZ: par-graf ures (monogamia)")
    S = lambda m: g.vagas_entropia(m)
    sig = all(S(1 << q) == 1 for q in range(3)) and \
          all(S((1 << i) | (1 << j)) == 1 for i, j in combinations(range(3), 2))
    ellenoriz(sig, "GHZ-signatura: minden reszhalmaz S=1, par-fonodas 0")
    print("    -> az ASSEMBLY a stabilizator-vilagban HIPEREL, nem haromszog.")


def kiserlet_anchork():
    banner("3. A GORBSEG A ZARODASOKBAN VAN (anchor-skala)")
    adat = [("haromszog K3", [(0, 1), (1, 2), (0, 2)], 0.5),
            ("ut P4", [(0, 1), (1, 2), (2, 3)], 0.0),
            ("csillag K1,3", [(0, 1), (0, 2), (0, 3)], 0.0),
            ("3 vezetek", [(0, 3), (1, 5), (2, 6)], 0.0)]
    for nev, ed, vart in adat:
        Ea = {e: 1 for e in ed}
        kap = ollivier(Ea)
        min_k = min(kap.values())
        print("    %-14s Ollivier %s" % (nev, kap))
        if vart > 0:
            ellenoriz(all(k > 0.01 for k in kap.values()),
                      "%s: minden el pozitiv gorbsegu" % nev)
        else:
            ellenoriz(all(k <= 0.01 for k in kap.values()),
                      "%s: nincs pozitiv gorbseg" % nev)
    print("    -> a zaroelek (K3) hordozzak a pozitiv gorbseget: k = +0.5.")


def kiserlet_itelet():
    banner("4. AZ ITELET")
    print("    a Hebb-szabaly a geometriat igy gorbiti:")
    print("      eloszor ELEK (vezetekek, k=0 -- feherallomany: a metrika)")
    print("      aztan ZARODASOK (hiperelek/klaszterek, k>0 -- szurkeallomany)")
    print("    a gepben a fonodasi hipergraf = a tanult geometria;")
    print("    a sziluett annak permutacio-invariens lenyomata.")
    print("    (irodalmi elozmeny: Forman-Ricci az fMRI-haookon -- Weber/Jost 2017;")
    print("     fizikai torveny: az osszefonodas = terosszefugges -- Van Raamsdonk 2010.)")


if __name__ == "__main__":
    kiserlet_sanity()
    kiserlet_nincs_geometria()
    kiserlet_nem_paros()
    kiserlet_anchork()
    kiserlet_itelet()
    print("\nGORBULET ELLENORIZVE")
