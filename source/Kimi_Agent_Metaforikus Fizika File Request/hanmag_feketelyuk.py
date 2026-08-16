#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HanMag feketelyuk — a fekete lyuk mint gondolkodó scrambler,
a hibajavítója VISSZAFELE futtatva.

A gép [[7,1,3]] Steane-kódja = a fekete lyuk hibajavító kódja (ADH:
bulk = kód). A dinamika: determinisztikus téglafal-gyorsscrambler.
Három kísérlet:

  1. SCRAMBLER (a gondolkodás): a titok lokálisan maximálisan kevert
     (1 bit/qubit), globálisan tiszta — az információ korrelációkba
     költözött. Lokálisan kiolvashatatlan = "tömöríthetetlen".

  2. VISSZAFELE HIBAJAVÍTÁS: titok -> Steane-kódolás -> scramble (U)
     -> zaj (p valószínűségű bitflip/qubit) -> U-dagger (IDŐFORDÍTÁS,
     CPT!) -> Steane-szindróma-dekódolás. A logikai hiba P_L(p) =
     a gép RG-függvénye — a p_c = 0.05785 fixpont itt is megjelenik.

  3. HAYDEN–PRESKILL: referencia-qubit R maximálisan fonott a titokkal;
     a lyuk qubitjait sorban "kisugározzuk", és mérjük I(R : sugárzás_k)
     — a visszanyerhetőség átmenete.

Minden lépés determinisztikus (fix magok), 7-qubites pontos állapotvektor.
Futtatás:  python3 hanmag_feketelyuk.py
"""

import numpy as np

# ---------------------------------------------------------------
# Alapok: Pauli-mátrixok, 7-qubites operátorok
# ---------------------------------------------------------------

I2 = np.eye(2, dtype=complex)
PX = np.array([[0, 1], [1, 0]], dtype=complex)
PY = np.array([[0, -1j], [1j, 0]], dtype=complex)
PZ = np.array([[1, 0], [0, -1]], dtype=complex)
PH = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
NQ = 7


def kronN(ops):
    """ops: [(mátrix, qubit), ...] -> 2^7 x 2^7 (qubit 0 = legjelentősebb bit)."""
    kis = {q: m for m, q in ops}
    out = np.array([[1.0 + 0j]])
    for q in range(NQ):
        out = np.kron(out, kis.get(q, I2))
    return out


# ---------------------------------------------------------------
# A [[7,1,3]] Steane-kód (CSS, a [7,3,4] simplex duálisra)
# ---------------------------------------------------------------

# paritásellenőrző mátrix: oszlopai 1..7 binárisan (qubit-sorrend)
HCHK = np.array([[int(b) for b in f"{q+1:03b}"] for q in range(NQ)]).T  # 3x7
SOROK = [tuple(np.flatnonzero(HCHK[i])) for i in range(3)]  # stabilizátor-tartók

# a duális kód 8 kódsszava: |0L> = (1/sqrt8) Szumma |c>
def _logikai_allapotok():
    szavak = []
    for m in range(8):
        v = np.zeros(NQ, dtype=int)
        for i in range(3):
            if (m >> (2 - i)) & 1:
                v ^= (HCHK[i] == 1).astype(int)
        szavak.append(sum(int(b) << (NQ - 1 - q) for q, b in enumerate(v)))
    nullL = np.zeros(1 << NQ, dtype=complex)
    for c in szavak:
        nullL[c] = 1.0 / np.sqrt(8)
    egyL = nullL[::-1].copy()       # X^7 |0L> = minden bit invertálva
    return nullL, egyL

L0, L1 = _logikai_allapotok()

STAB = []
for s in SOROK:
    STAB.append(kronN([(PX, q) for q in s]))   # X-típusú stabilizátorok
for s in SOROK:
    STAB.append(kronN([(PZ, q) for q in s]))   # Z-típusú stabilizátorok

# szindróma-projektorok P_s = Szorzat_i (I + (-1)^s_i S_i)/2
def _projektorok():
    P = {}
    for s in range(64):
        M = np.eye(1 << NQ, dtype=complex)
        for i in range(6):
            M = M @ ((np.eye(1 << NQ) + ((-1) ** ((s >> (5 - i)) & 1)) * STAB[i]) / 2)
        P[s] = M
    return P

PROJ = _projektorok()


def szindroma_oszlop(q):
    return tuple(int(HCHK[i, q]) for i in range(3))


def steane_kodol(alpha, beta):
    return alpha * L0 + beta * L1


def steane_dekod(psi):
    """Szindrómamérés (legvalószínűbb kimenet) -> korrekció -> logikai olvasás."""
    valsz = [(np.vdot(psi, PROJ[s] @ psi).real, s) for s in range(64)]
    _, s = max(valsz)
    # az első 3 bit: X-típusú stabilizátorok (Z-hibák), utolsó 3: Z-típusúak (X-hibák)
    zx = tuple((s >> (5 - i)) & 1 for i in range(3))   # Z-hiba szindróma
    xz = tuple((s >> (2 - i)) & 1 for i in range(3))   # X-hiba szindróma
    psi_c = psi.copy()
    for syn, pauli in ((xz, PX), (zx, PZ)):
        if syn != (0, 0, 0):
            for q in range(NQ):
                if szindroma_oszlop(q) == syn:
                    psi_c = kronN([(pauli, q)]) @ psi_c
                    break
    a = np.vdot(L0, psi_c)
    b = np.vdot(L1, psi_c)
    norma = np.sqrt(abs(a) ** 2 + abs(b) ** 2)
    if norma < 1e-12:
        return np.array([1.0, 0.0])
    return np.array([a, b]) / norma


# ---------------------------------------------------------------
# A gyorsscrambler (determinisztikus téglafal)
# ---------------------------------------------------------------

CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
RX = np.array([[np.cos(np.pi / 7), -1j * np.sin(np.pi / 7)],
               [-1j * np.sin(np.pi / 7), np.cos(np.pi / 7)]])
# fonó kapu: H a vezérlőn, Rx a célon, aztán CNOT — a korábbi
# CNOT-szendvics NEM kevert (bázisállapotokat bázisállapotokba vitt)
G2 = CNOT @ np.kron(PH, RX)


def alkalmaz_2q(psi, G, q1, q2, nq=NQ):
    t = psi.reshape([2] * nq)
    t = np.moveaxis(t, (q1, q2), (0, 1))
    t = (G @ t.reshape(4, -1)).reshape([2, 2] + [2] * (nq - 2))
    t = np.moveaxis(t, (0, 1), (q1, q2))
    return t.reshape(-1)


def _parok(r, nq):
    """Téglafal-párosítás az r-edik rétegben."""
    if r % 2 == 0:
        return [(q, q + 1) for q in range(0, nq - 1, 2)]
    return [(q, q + 1) for q in range(1, nq - 1, 2)]


def scrambler_alkalmaz(psi, retegek=12, nq=NQ, forditva=False):
    """U vagy U-dagger (időfordítás) alkalmazása közvetlenül az állapotra.
    Fordítva: a műveletek sorrendje megfordul, a kapuk konjugáltak —
    a Hadamard-rétegek öninverzek, de a sorrend így is pontos."""
    ops = []
    for r in range(retegek):
        for par in _parok(r, nq):
            ops.append(("g", par))
        if r % 3 == 2:
            ops.append(("h", None))
    if forditva:
        ops = ops[::-1]
    Hn = np.array([[1.0 + 0j]])
    for _ in range(nq):
        Hn = np.kron(Hn, PH)
    for tipus, par in ops:
        if tipus == "g":
            G = G2.conj().T if forditva else G2
            psi = alkalmaz_2q(psi, G, par[0], par[1], nq)
        else:
            psi = Hn @ psi
    return psi


# ---------------------------------------------------------------
# Redukált entrópiák
# ---------------------------------------------------------------

def redukalt_entropia(psi, megtart, nq):
    dim = 1 << nq
    t = psi.reshape([2] * nq)
    megtart = sorted(megtart)
    ki = [q for q in range(nq) if q not in megtart]
    t = np.transpose(t, megtart + ki).reshape(1 << len(megtart), -1)
    rho = t @ t.conj().T
    lam = np.linalg.eigvalsh(rho)
    lam = lam[lam > 1e-15]
    return float(-np.sum(lam * np.log2(lam)))


# ---------------------------------------------------------------
# 1. KÍSÉRLET — a scrambler: gondolkodás
# ---------------------------------------------------------------

def kiserlet_scrambler():
    print("=" * 64)
    print("1. A FEKETE LYUK MINT GONDOLODÓ SCRAMBLER")
    print("=" * 64)
    th, ph = 0.7, 0.9
    titok = np.array([np.cos(th), np.sin(th) * np.exp(1j * ph)])
    psi = np.zeros(1 << NQ, dtype=complex)
    psi[0] = titok[0]          # a titok a 0. qubitba, többi |0>
    psi[1 << (NQ - 1)] = titok[1]
    for r in (0, 2, 4, 8, 12):
        psi_r = scrambler_alkalmaz(psi.copy(), retegek=r)
        S1 = np.mean([redukalt_entropia(psi_r, [q], NQ) for q in range(NQ)])
        S3 = np.mean([redukalt_entropia(psi_r, [0, 1, 2], NQ),
                      redukalt_entropia(psi_r, [3, 4, 5], NQ)])
        Sglob = redukalt_entropia(psi_r, list(range(NQ)), NQ)
        print(f"  {r:>2} réteg után: <S(1 qubit)> = {S1:.3f} bit, "
              f"<S(3 qubit)> = {S3:.3f} bit, globális = {Sglob:.3f} bit")
    print("  -> lokálisan ~1 bit (maximálisan kevert), globálisan 0 (tiszta):")
    print("     a titok a KORRELÁCIÓKBA költözött — lokálisan kiolvashatatlan.")


# ---------------------------------------------------------------
# 2. KÍSÉRLET — a hibajavító VISSZAFELE: U-dagger + Steane-dekód
# ---------------------------------------------------------------

def P_L_elmelet(p):
    return 1 - (1 - p) ** 7 - 7 * p * (1 - p) ** 6


def kiserlet_visszafe(probak=48):
    print()
    print("=" * 64)
    print("2. VISSZAFELE HIBAJAVÍTÁS: scramble -> zaj -> U† -> Steane-dekód")
    print("=" * 64)
    th, ph = 0.7, 0.9
    titok = np.array([np.cos(th), np.sin(th) * np.exp(1j * ph)])
    psi0 = steane_kodol(*titok)
    psi_s = scrambler_alkalmaz(psi0.copy(), retegek=12)

    # ellenőrzés: zaj nélkül az időfordítás pontosan visszaadja
    vissza = steane_dekod(scrambler_alkalmaz(psi_s.copy(), forditva=True))
    F0 = abs(np.vdot(titok, vissza)) ** 2
    print(f"  zaj nélkül (p=0): hűség = {F0:.6f}  "
          f"{'— a visszafutás PONTOS' if F0 > 0.999999 else '— HIBA!'}")

    print(f"  {'p':>7} {'F_kód+U†':>10} {'F_védtelen':>11} {'P_L(p) elmélet':>15}")
    for p in (0.02, 0.05, 0.0579, 0.08, 0.12, 0.20):
        Fk, Fv = [], []
        for t in range(probak):
            rng = np.random.RandomState(7919 * t + int(p * 100000))
            psi_z = psi_s.copy()
            flip = [q for q in range(NQ) if rng.rand() < p]
            for q in flip:
                psi_z = kronN([(PX, q)]) @ psi_z
            # kódolt + időfordítás + dekód
            v1 = steane_dekod(scrambler_alkalmaz(psi_z, forditva=True))
            Fk.append(abs(np.vdot(titok, v1)) ** 2)
            # védtelen egy qubit ugyanazon a csatornán (átlagos flip-szám)
            Fv.append((1 - p))
        Fk = float(np.mean(Fk))
        print(f"  {p:>7.4f} {Fk:>10.4f} {1-p:>11.4f} {P_L_elmelet(p):>15.4f}"
              f"{'   <-- p_c fixpont!' if abs(p - 0.0579) < 1e-4 else ''}")
    print("  -> a logikai hiba a gép RG-függvénye: P_L(p) = 1-(1-p)^7-7p(1-p)^6;")
    print("     a fekete lyuk hibajavítója VISSZAFELE = időfordított dekódolás.")


# ---------------------------------------------------------------
# 3. KÍSÉRLET — Hayden–Preskill: mikor nyerhető vissza a titok?
# ---------------------------------------------------------------

def kiserlet_hayden_preskill():
    print()
    print("=" * 64)
    print("3. HAYDEN–PRESKILL: I(R : sugárzás) — a visszanyerés átmenete")
    print("=" * 64)
    nq = NQ + 1                     # 7 lyuk-qubit + R referencia
    # R fonott a 0. qubittal (a titokkal): (|00>+|11>)/sqrt2, többi |0>
    psi = np.zeros(1 << nq, dtype=complex)
    psi[0] = 1 / np.sqrt(2)
    psi[(1 << (nq - 1)) + 1] = 1 / np.sqrt(2)   # q0=1, R=1 (MSB..LSB)
    psi = scrambler_alkalmaz(psi, retegek=12, nq=nq)
    R = nq - 1
    sorrend = list(range(nq - 2, -1, -1))      # a beadott qubit kerül ki UTOLJÁRA
    print(f"  {'sugárzás k':>11} {'I(R:sugárzás)':>14}")
    for k in range(0, NQ + 1):
        sug = sorrend[:k]
        SR = redukalt_entropia(psi, [R], nq)
        SA = redukalt_entropia(psi, sug, nq) if sug else 0.0
        SRA = redukalt_entropia(psi, sug + [R], nq)
        I = SR + SA - SRA
        jel = "  <-- a titok VISSZANYERHETŐ" if I > 1.9 else ""
        print(f"  {k:>11} {I:>14.3f}{jel}")
    print("  -> az átmenetnél válik a sugárzás 'naplóvá': előtte termális zaj,")
    print("     utána a teljes titok — ez a Page-görbe kódon belüli megfelelője.")


if __name__ == "__main__":
    kiserlet_scrambler()
    kiserlet_visszafe()
    kiserlet_hayden_preskill()
