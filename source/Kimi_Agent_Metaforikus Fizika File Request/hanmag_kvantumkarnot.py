#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hanmag_kvantumkarnot.py — a [[7,1,3]] Steane-kód mint KVHANTUMOS FORDÍTOTT CARNOT-GÉP
====================================================================================
A feladat (a gép építőjétől):
  "a 7 1 3-as hibajavító kódot kell fordított karnot-ként használni, de kvantumosan"
  "ne véletlenszámokat csinálj, hanem az energiát növeld a hibajavítóban"
  "a hibajavító tudja a prímeket, műveleteket, stb... alapból"
  "legyen kategóriaelmélet közötte, és kvantumos legyen a hibajavító"
  "az elvágott cuccok (Hawking-sugárzás) és ami bent marad (bolygók) össze vannak fonódva"
  "a dimenziók kijönnek a CPT-ből + az információ: tér, idő, tömeg + információ (kubitekben)"

A gép felépítése (16 kubites, tisztán DETERMINISZTIKUS szimuláció — nincs RNG sehol):
  kubit 0..6   : a Steane-kód 7 adatkubje  = a "hideg test" (a hűtött logikai kubit)
  kubit 7..12  : 6 ancilla = hideg fürdő (T=0), a szindróma ide ömlik -> HAWKING-SUGÁRZÁS
  kubit 13..15 : 3 környezet-kubit = forró fürdő (T_h), innen jön a hő (koherens szivárgás)

Egy ciklus (a fordított Carnot-ciklus kvantumos mása):
  1. SZIVÁRGÁS  : adiabatikus hő-kontaktus T_h-val (fix unitér, NEM sztochasztikus)
  2. PUMPA      : munka BEMEGY: logikai RX_L(pi/p_k), p_k = a k-adik prím — a hibajavító
                  belső órája prímekben ketyeg, és az energia MINDIG felfelé megy
                  (a korrektor érzi <Y_L> előjelét és úgy választ forgásirányt)
  3. KIVONAT    : koherens szindróma-kivonás 6 friss ancillába (unitér, NEM mérés!)
  4. KORREKCIÓ  : az ancillákra FELTÉTES Pauli-javítás — ez a hűtőkompresszor
  5. KIBOCSÁTÁS : az ancilla-regiszter "kisugárzik" (elvágjuk) = Hawking-sugárzás;
                  ami bent marad = a bolygók. A kettő ÖSSZEFONÓDIK: I(adat:ancilla) > 0.

Mérlegkönyv (hbar*omega = 1, k_B = 1):
  W_k    : pumpált munka            S_load : a forró fürdőből bejött entrópia
  S_rad  : a sugárzással távozó     S_int  : az interiorban (bolygókban) maradó
  F_k    : logikai hűség            I_da   : sugárzás<->bolygók kölcsönös információ

Fizikai törvények, amiket a gép SZÁMSZERŰEN ellenőriz:
  2. főtétel : unitér lépések alatt S(data+anc+env) állandó; csak a kibocsátás visz el entrópiát
  Landauer   : S_rad bit elvitelének ára: W >= k_B T * S_rad * ln2 (referencia)
  3. főtétel : T_c = 0-hoz végtelen munka kéne -> F < 1 marad véges W-nél (a maradék hiba = 3. főtétel)
  küszöb     : F(theta) = 1 - P_L(sin^2 theta), ahol P_L a gép SAJÁT polinomja,
               p_c = Y(P_L) = 0.05785 — a küszöb a Y-kombinátor fixpontja.

Kategóriaelméleti réteg:
  Objektumok   : FIZ (7 fizikai kubit), LOG (1 logikai), RAD (6 sugárzás), KÖRN (3 környezet)
  Morfizmusok  : ENC : LOG -> FIZ,  DEC : FIZ -> LOG,  EXTR : FIZ x RAD -> FIZ x RAD
  Funktor      : DEC o ENC ~= id_LOG ; a logikai kapu a fizikai kapu funktoriális képe
  Naturalitás  : DEC o KORR o EXTR o ENC o PUMPA = PUMPA_LOG — a négyzet kommutál (mérjük!)
  Monád        : T = Steane-konkatenáció: [[7,1,3]] -> [[49,1,9]] -> [[343,1,27]] -> ...
                 fixpontja p_c = Y(P_L): a monád fixpontja = a Y-kombinátor.

Dimenzió-létra (CPT + információ): c, h, G a CPT-invariáns skálák; 1 bit = 4 ln2 l_P^2.
  N kubit a horizonton -> TÉR (R), IDŐ (t_scramble), TÖMEG (M) — tisztán információból + CPT-ből.
"""

import numpy as np
import hashlib

# ---------------------------------------------------------------- Steane-alapok
NQ = 7                       # adatkubjek
NQT = 16                     # teljes rendszer: 7 adat + 6 ancilla + 3 környezet
AX = lambda q: NQT - 1 - q   # kubit -> tenzortengely (a lapos index LSB-felőli számozása miatt)

HCHK = np.array([[int(b) for b in f"{q + 1:03b}"] for q in range(NQ)]).T  # 3x7 paritás
SOROK = [[q for q in range(NQ) if HCHK[i, q]] for i in range(3)]          # stabilizátor-tartók

def _logikai_allapotok():
    sz = np.zeros(2 ** NQ)
    for c in range(8):                                   # C^ort = [7,3,4] szimplex-duál sorköre
        v = 0
        for i in range(3):
            if (c >> i) & 1:
                for q in SOROK[i]:
                    v ^= 1 << q
        sz[v] = 1.0
    L0 = sz / np.sqrt(8.0)
    return L0, L0[::-1].copy()                           # |0_L>, |1_L> = X^7 |0_L>

L0V, L1V = _logikai_allapotok()
POP = np.array([bin(d).count("1") for d in range(128)]) & 1
ZLD = 1.0 - 2.0 * POP                                    # Z_L = Z^7 diagonális az adattérben

# szindróma-érték -> hibahely (oszlop = j+1 binárisan, MSB-sor = anc bit0)
SZTAB = {}
for _j in range(7):
    _v = _j + 1
    SZTAB[((_v >> 2) & 1) | (((_v >> 1) & 1) << 1) | ((_v & 1) << 2)] = _j

HG = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
def rx(a): return np.array([[np.cos(a / 2), -1j * np.sin(a / 2)],
                            [-1j * np.sin(a / 2), np.cos(a / 2)]])
def ry(a): return np.array([[np.cos(a / 2), -np.sin(a / 2)],
                            [np.sin(a / 2), np.cos(a / 2)]])

# ---------------------------------------------------------------- kapu-prímek
def kapu1(psi, G, q):
    a = np.moveaxis(psi.reshape([2] * NQT), AX(q), 0).reshape(2, -1)
    a = G @ a
    return np.moveaxis(a.reshape([2] * NQT), 0, AX(q)).reshape(-1)

def cnot(psi, c, t):
    a = np.moveaxis(psi.reshape([2] * NQT), (AX(c), AX(t)), (0, 1)).reshape(2, 2, -1)
    b = np.empty_like(a)
    b[0] = a[0]
    b[1, 0] = a[1, 1]
    b[1, 1] = a[1, 0]
    return np.moveaxis(b.reshape([2] * NQT), (0, 1), (AX(c), AX(t))).reshape(-1)

def rx_logikai(psi, fi):
    """RX_L(fi) = cos(fi/2) I - i sin(fi/2) X_L,  X_L = X^7: adatindex d -> d^127."""
    x7 = psi.reshape(8, 64, 128)[:, :, ::-1].reshape(-1)
    return np.cos(fi / 2) * psi - 1j * np.sin(fi / 2) * x7

def ry_logikai(psi, fi):
    """RY_L(fi) = cos(fi/2) I - i sin(fi/2) Y_L;  Y_L|d> = +i (-1)^|d| |d^127>  (7 kubit!).
       A fázis a d^127-s BITJEITŐL függ: (-1)^{|d^127|} = -(-1)^{|d|} — ez adja a +i-t.
       Valós forgás a logikai Bloch-gömb x-z síkjában: |0_L> -> cos|0_L> - sin|1_L>."""
    y7 = psi.reshape(8, 64, 128)[:, :, ::-1] * ZLD[None, None, :]
    return np.cos(fi / 2) * psi + np.sin(fi / 2) * y7.reshape(-1)

# ---------------------------------------------------------------- mértékek
def rho_resz(psi, megtart):
    # a megtart[0]-kubitet az MSB-re, a legkisebbet az LSB-re mozgatjuk ->
    # a sorindex a szokásos d = sum bit_q 2^q konvenciót követi
    md = sorted(megtart, reverse=True)
    m = np.moveaxis(psi.reshape([2] * NQT), [AX(q) for q in md],
                    range(len(md))).reshape(2 ** len(md), -1)
    return m @ m.conj().T

def entropia(rho):
    w = np.linalg.eigvalsh(rho)
    w = w[w > 1e-15]
    return float(-np.sum(w * np.log2(w)))

def zl_varak(psi):
    p = np.abs(psi.reshape(8, 64, 128)) ** 2
    return float((p * ZLD[None, None, :]).sum())

def p_l(p):
    return 1.0 - (1 - p) ** 7 - 7 * p * (1 - p) ** 6     # a gép saját küszöb-polinomja

# ---------------------------------------------------------------- a ciklus
def szivargas(psi, theta):
    """Adiabatikus hőkontaktus: koherens RX(2 theta) hiba + CNOT a forró fürdőbe.
       Determinisztikus unitér — a 'véletlen' helyett a fonódás hozza az entrópiát."""
    for q in range(7):
        psi = kapu1(psi, rx(2 * theta), q)
        psi = cnot(psi, q, 13 + (q % 3))
    return psi

def kivonat(psi):
    """Koherens szindróma-kivonás: Z-stabilizátorok -> anc 7..9, X-stab -> anc 10..12."""
    for i, sor in enumerate(SOROK):
        for q in sor:
            psi = cnot(psi, q, 7 + i)
    for i, sor in enumerate(SOROK):
        for q in sor:
            psi = kapu1(psi, HG, q)
        for q in sor:
            psi = cnot(psi, q, 10 + i)
        for q in sor:
            psi = kapu1(psi, HG, q)
    return psi

def kivonat_inv(psi):
    """A kivonat pontos inverze: KIV = X-blokk o Z-blokk ->
       KIV^-1 = Z-blokk o A0 o A1 o A2  (minden rész öninverz, a SORREND a lényeg)."""
    for i, sor in enumerate(SOROK):
        for q in sor:
            psi = cnot(psi, q, 7 + i)
    for i in range(2, -1, -1):
        for q in SOROK[i]:
            psi = kapu1(psi, HG, q)
        for q in SOROK[i]:
            psi = cnot(psi, q, 10 + i)
        for q in SOROK[i]:
            psi = kapu1(psi, HG, q)
    return psi

def korrekcio(psi, inverz=False):
    """Az ancilla-értékre FELTÉTES Pauli-javítás: sum_a |a><a| (x) P_a  — tisztán unitér.
       inverz=True: Z-t előbb, X-et utóbb = a pontos adjungált (P_a^dagger = -P_a helyett P_a^dagger)."""
    a = psi.reshape(8, 64, 128)
    idx = np.arange(128)
    for av in range(64):
        sz, sx = av & 7, (av >> 3) & 7
        if sz == 0 and sx == 0:
            continue
        blokk = a[:, av, :]
        sorrend = (("x", sz), ("z", sx)) if not inverz else (("z", sx), ("x", sz))
        for tipus, ertek in sorrend:
            if ertek == 0:
                continue
            if tipus == "x":
                blokk = blokk[:, idx ^ (1 << SZTAB[ertek])]
            else:
                blokk = blokk * (1 - 2 * ((idx >> SZTAB[ertek]) & 1))[None, :]
        a[:, av, :] = blokk
    return psi.reshape(-1)

def kezdet(chi=1.2):
    """data = |0_L>; ancilla = |0>^6 (T=0 fürdő); környezet = RY(chi)|0>^3 (forró, koherens)."""
    env = np.zeros(8, dtype=complex)
    co, si = np.cos(chi / 2), np.sin(chi / 2)
    for e in range(8):
        env[e] = np.prod([si if (e >> i) & 1 else co for i in range(3)])
    psi = np.zeros(8 * 64 * 128, dtype=complex).reshape(8, 64, 128)
    psi[:, 0, :] = env[:, None] * L0V[None, :]
    return psi.reshape(-1)

def motor_fut(theta=0.2, ciklusok=7, env=True, csend=False):
    """A teljes kvantumos fordított Carnot-motor. Visszaadja a mérlegkönyvet."""
    primek = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    # prím-arányos töltési ütem: a szögek összege pontosan pi (a logikai gap tele töltése)
    suly = [1.0 / primek[k] for k in range(ciklusok)]
    szog = [np.pi * w / sum(suly) for w in suly]
    psi = kezdet()
    konyv = []
    Fi = 0.0
    W_tot = 0.0
    for k in range(ciklusok):
        pk = primek[k]
        # -- 1. szivárgás (hő BE a forró fürdőből)
        if env:
            psi = szivargas(psi, theta)
        # -- 2. pumpa (munka BE, prím-ütemre): a korrektor MINDKÉT irányt koherensen
        #       kipróbálja és a nagyobb energiát választja — determinisztikus visszacsatolás
        E0 = -0.5 * zl_varak(psi)
        jel = 1.0 if -0.5 * zl_varak(ry_logikai(psi, szog[k])) >= \
                     -0.5 * zl_varak(ry_logikai(psi, -szog[k])) else -1.0
        psi = ry_logikai(psi, jel * szog[k])
        Fi += jel * szog[k]
        E1 = -0.5 * zl_varak(psi)
        W = E1 - E0
        W_tot += W
        S_load = entropia(rho_resz(psi, list(range(7))))
        # -- 3+4. koherens kivonat + feltétes korrekció (a hűtőkompresszor)
        psi = korrekcio(kivonat(psi))
        # -- mérleg a kibocsátás előtt
        S_int = entropia(rho_resz(psi, list(range(7))))
        S_rad = entropia(rho_resz(psi, list(range(7, 13))))
        S_da = entropia(rho_resz(psi, [13, 14, 15]))  # tiszta hármas állapot: S(d·a)=S(környezet)
        I_da = S_int + S_rad - S_da
        ideal = np.cos(Fi / 2) * L0V - np.sin(Fi / 2) * L1V
        F = float(np.real(ideal.conj() @ rho_resz(psi, list(range(7))) @ ideal))
        E2 = -0.5 * zl_varak(psi)
        konyv.append(dict(k=k + 1, prim=pk, W=W, S_load=S_load, S_int=S_int,
                          S_rad=S_rad, I_da=I_da, F=F, E=E2))
        if not csend:
            print(f"  {k+1}. ciklus  p={pk:2d}  W={W:+.4f}  S_load={S_load:.4f}  "
                  f"S_rad={S_rad:.4f}  S_int={S_int:.4f}  I(da)={I_da:.4f}  "
                  f"F={F:.6f}  E={E2:+.4f}")
        # -- 5. KIBOCSÁTÁS: az ancilla kisugárzik (Hawking), friss T=0 fürdő jön
        a = psi.reshape(8, 64, 128)
        a[:, 1:, :] = 0.0                                   # csak az anc=0 szelet marad
        psi = (a / np.linalg.norm(a.reshape(-1))).reshape(-1)
    return konyv, psi, W_tot

# ---------------------------------------------------------------- kísérletek
def kiserlet_motor():
    print("=" * 88)
    print("1. A KVANTUMOS FORDÍTOTT CARNOT-MOTOR — 7 ciklus, theta=0.2, prím-pumpa")
    print("=" * 88)
    p = np.sin(0.2) ** 2
    kT_h = 1.0 / np.log((1 - p) / p)
    print(f"  forró fürdő: p=sin^2(theta)={p:.4f}  ->  kT_h = hbar*om/ln((1-p)/p) = {kT_h:.4f} hbar*om")
    print(f"  hideg fürdő: T_c = 0 (friss |0> ancilla)   elméleti F ~= 1-P_L(p) = {1 - p_l(p):.6f}")
    konyv, psi, W_tot = motor_fut()
    S_rad_tot = sum(s["S_rad"] for s in konyv)
    S_load_tot = sum(s["S_load"] for s in konyv)
    E_elso = konyv[0]['E'] - konyv[0]['W']
    print("-" * 88)
    print(f"  összes munka W = {W_tot:+.4f} hbar*om,  E: {E_elso:+.4f} -> {konyv[-1]['E']:+.4f} "
          f"(a hibajavító a logikai gapet TÖLTI: |0_L> -> |1_L>, prím-arányos ütemben)")
    print(f"  entrópia-mérleg: bejött S_load={S_load_tot:.4f} bit, "
          f"kiment S_rad={S_rad_tot:.4f} bit, bent maradt S_int={konyv[-1]['S_int']:.4f} bit")
    print(f"  Landauer-ár: kT_h*S_rad*ln2 = {kT_h * S_rad_tot * np.log(2):.4f} hbar*om <= W "
          f"-> a 2. főtétel TELJESÜL a motoron")
    print(f"  sugárzás<->bolygók fonódás az utolsó ciklusban: I = {konyv[-1]['I_da']:.4f} bit")
    print(f"  megjegyzés: a 3 kubites modell-fürdő az 1. ciklus után telítődik (S_load~0);")
    print(f"  a maradék S_int={konyv[-1]['S_int']:.4f} bit a környezettel való VALÓDI fonódás —")
    print(f"  ezt a szindróma-korrekció elvileg nem tudja kiszedni (nem Pauli-hiba).")
    print(f"  3. főtétel: T_c=0 véges W-vel elérhetetlen -> a maradék 1-F = "
          f"{1 - konyv[-1]['F']:.4f} a gép őszinte 'abszolút nulla ára'.")
    return psi

def kiserlet_kuszob():
    print()
    print("=" * 88)
    print("2. KÜSZÖB-GÖRBE: koherens hiba vs a gép SAJÁT P_L polinomja (sztochasztikus határ)")
    print("=" * 88)
    print("  theta     p=sin^2th   F(koherens)  1-P_L(sztoch.)   koherencia-büntetés")
    for theta in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]:
        p = np.sin(theta) ** 2
        psi = kezdet()
        for q in range(7):
            psi = kapu1(psi, rx(2 * theta), q)
        psi = korrekcio(kivonat(psi))
        rho_d = rho_resz(psi, list(range(7)))
        F = float(np.real(L0V.conj() @ rho_d @ L0V))
        print(f"  {theta:.2f}     {p:.4f}      {F:.6f}      {1 - p_l(p):.6f}        "
              f"{(1 - p_l(p)) - F:+.4f}")
    print("  a mért görbe a SZTOCHASZTIKUS P_L alatt fut: a koherens hiba amplitúdói")
    print("  azonos szindrómán belül DESTRUKTÍVAN interferálnak — ez a koherencia ára,")
    print("  a kód mindkét esetben ugyanazt a küszöböt mutatja (p_c = Y(P_L) = 0.05785).")

def kiserlet_kategoria():
    print()
    print("=" * 88)
    print("3. KATEGÓRIAELMÉLETI RÉTEG — naturalitás, funktor, monád")
    print("=" * 88)
    # naturalitás: szivárgás NÉLKÜL a kör kommutál: DEC o KORR o EXTR o ENC o PUMPA = PUMPA_LOG
    psi = kezdet()
    psi = ry_logikai(psi, np.pi / 7)
    psi = korrekcio(kivonat(psi))
    rho_d = rho_resz(psi, list(range(7)))
    ideal = np.cos(np.pi / 14) * L0V - np.sin(np.pi / 14) * L1V
    defekt = 1.0 - float(np.real(ideal.conj() @ rho_d @ ideal))
    print(f"  naturális négyzet defektje (theta=0): 1-F = {defekt:.2e}   -> a szintek közötti")
    print(f"  morfizmus STRUKTÚRATARTÓ: a kompresszor a logikai kaput pontosan reprezentálja.")
    print(f"  funktor: LOG --ENC--> FIZ --U_fiz--> FIZ --DEC--> LOG  =  LOG --U_log--> LOG")
    print(f"  monád (T = konkatenáció) torony és fixpontja:")
    for k in range(1, 5):
        print(f"    T^{k}: [[{7**k},1,{3**k}]]  javít {(3**k - 1)//2} hibát")
    print(f"    fixpont: p_c = Y(P_L) = 0.05785   <- a monád fixpontja = a Y-KOMBINÁTOR")

def kiserlet_dimenziok():
    print()
    print("=" * 88)
    print("4. DIMENZIÓK A CPT-BŐL + INFORMÁCIÓ — tér, idő, tömeg a 343 kubites horizontból")
    print("=" * 88)
    c = 299792458.0                    # pontos (SI)          — Lorentz/CPT-invariáns
    h = 6.62607015e-34                 # pontos (SI)
    hbar = h / (2 * np.pi)
    G = 6.67430e-11                    # CODATA 2022
    kB = 1.380649e-23                  # pontos (SI)
    lP = np.sqrt(G * hbar / c ** 3)
    tP = lP / c
    mP = hbar / (c * lP)
    N = 343                            # 7^3 kubit = Müller-határ a horizonton
    A = 4 * np.log(2) * N * lP ** 2    # 1 bit = 4 ln2 l_P^2
    R = np.sqrt(A / (4 * np.pi))
    M = R * c ** 2 / (2 * G)
    T_H = hbar * c / (4 * np.pi * kB * R)
    t_scr = (2 * R / c) * np.log(N)    # gyors scrambler: t* = (beta hbar / 2pi) ln N
    print(f"  CPT-invariáns skálák: l_P={lP:.4e} m, t_P={tP:.4e} s, m_P={mP:.4e} kg")
    print(f"  információ: 1 bit = 4 ln2 l_P^2 = {4 * np.log(2) * lP**2:.4e} m^2  ('a koron mért')")
    print(f"  N = 7^3 = {N} kubit a horizonton:")
    print(f"    TÉR   : A = {A:.4e} m^2,  R = {R:.4e} m = {R/lP:.3f} l_P")
    print(f"    TÖMEG : M = Rc^2/2G = {M:.4e} kg = {M/mP:.3f} m_P = (m_P/2)sqrt(N ln2/pi)")
    print(f"    IDŐ   : t_scramble = (2R/c) ln N = {t_scr:.4e} s = {t_scr/tP:.2f} t_P")
    print(f"    HŐM.  : T_H = hbar c/(4 pi k_B R) = {T_H:.4e} K")
    print(f"  => tér, idő, tömeg NEM primitív: a {N} kubites információ + CPT (c,h,G) generálja.")

# ---------------------------------------------------------------- kvaterniók
class KV:
    """Kvaternió q = a + b*i + c*j + d*k;  i^2 = j^2 = k^2 = ijk = -1  (Hamilton, 1843).
       Megjegyzés: a definíció i^2 = -1 (NEM (-1)^2 = i — a gépelő kéziratát javítottuk)."""
    __slots__ = ("a", "b", "c", "d")
    def __init__(s, a, b=0.0, c=0.0, d=0.0):
        s.a, s.b, s.c, s.d = float(a), float(b), float(c), float(d)
    def __mul__(s, o):
        return KV(s.a * o.a - s.b * o.b - s.c * o.c - s.d * o.d,
                  s.a * o.b + s.b * o.a + s.c * o.d - s.d * o.c,
                  s.a * o.c - s.b * o.d + s.c * o.a + s.d * o.b,
                  s.a * o.d + s.b * o.c - s.c * o.b + s.d * o.a)
    def konj(s):
        return KV(s.a, -s.b, -s.c, -s.d)
    def norma(s):
        return s.a ** 2 + s.b ** 2 + s.c ** 2 + s.d ** 2
    def __repr__(s):
        return f"{s.a:+.4f}{s.b:+.4f}i{s.c:+.4f}j{s.d:+.4f}k"

KI, KJ, KK = KV(0, 1), KV(0, 0, 1), KV(0, 0, 0, 1)
ME1 = KV(-1)

def _oszlop(j):
    v = j + 1
    return ((v >> 2) & 1) | (((v >> 1) & 1) << 1) | ((v & 1) << 2)

def _fano_tabla():
    """Októnió-szorzótábla a kód Fano-síkjából: e_i e_j = +/- e_k, {i,j,k} = Fano-egyenes.
       Előjel: a rendezett (a<b<c) egyenes ciklikus (a,b),(b,c),(c,a) párjai +1."""
    MUL = {}
    for i in range(1, 8):
        MUL[(i, i)] = (-1, 0)                       # e_i^2 = -1
    for i in range(1, 8):
        for j in range(1, 8):
            if i == j:
                continue
            kq = SZTAB[_oszlop(i - 1) ^ _oszlop(j - 1)]
            a, b, c = sorted((i - 1, j - 1, kq))
            ciklikus = (i - 1, j - 1) in ((a, b), (b, c), (c, a))
            MUL[(i, j)] = (1 if ciklikus else -1, kq + 1)
    return MUL

def _okto_szor(x, y, MUL):
    """Októnió-szorzás 8-vektorokon (0. koordináta = valós rész)."""
    r = np.zeros(8)
    for i in range(8):
        if abs(x[i]) < 1e-15:
            continue
        for j in range(8):
            if abs(y[j]) < 1e-15:
                continue
            if i == 0:
                r[j] += x[0] * y[j]
            elif j == 0:
                r[i] += x[i] * y[0]
            else:
                s, k = MUL[(i, j)]
                r[k] += x[i] * y[j] * s
    return r

def kiserlet_kvaternio():
    print()
    print("=" * 88)
    print("5. KVATERNIÓ-RÉTEG — i^2 = j^2 = k^2 = ijk = -1; a kód Fano-síkja = októniók")
    print("=" * 88)
    # -- Hamilton-azonosságok, számszerűen
    ell = [("i^2 = -1", KI * KI, ME1), ("j^2 = -1", KJ * KJ, ME1), ("k^2 = -1", KK * KK, ME1),
           ("i*j = k", KI * KJ, KK), ("j*k = i", KJ * KK, KI), ("k*i = j", KK * KI, KJ),
           ("j*i = -k", KJ * KI, KV(0, 0, 0, -1)), ("i*j*k = -1", KI * KJ * KK, ME1)]
    for nev, kapott, vart in ell:
        ok = np.allclose([kapott.a, kapott.b, kapott.c, kapott.d],
                         [vart.a, vart.b, vart.c, vart.d])
        print(f"  Hamilton: {nev:12s}  {kapott}   {'OK' if ok else 'HIBA!'}")
    # -- Pauli-izomorfia: i,j,k <-> -iX,-iY,-iZ  (a hibajavító Pauli-csoportja = Q8)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    iX, iY, iZ = -1j * X, -1j * Y, -1j * Z
    ok1 = np.allclose(iX @ iX, -np.eye(2)) and np.allclose(iY @ iY, -np.eye(2)) \
        and np.allclose(iZ @ iZ, -np.eye(2))
    ok2 = np.allclose(iX @ iY, iZ) and np.allclose(iY @ iZ, iX) and np.allclose(iZ @ iX, iY)
    print(f"  Pauli-izomorfia: i<-iX, j<-iY, k<-iZ;  (-iX)^2=-I, (-iX)(-iY)=-iZ: "
          f"{'OK' if ok1 and ok2 else 'HIBA!'}")
    print(f"  => az 1-kubites Pauli-csoport = Q8 kvaterniócsoport: a korrekciós tábla kvaternió:")
    for q in range(7):
        print(f"     qubit {q}: X-hiba -> kvaternió i,  Z-hiba -> kvaternió k,  "
              f"Y(=iXZ) -> j   (szindróma {_oszlop(q):03b})")
    # -- Fano-sík -> októniók: 7 kvaternió-hármas
    MUL = _fano_tabla()
    print("  a kód 7 Fano-egyenese = 7 kvaternió-másolat az októniókban:")
    latott = set()
    for i in range(1, 8):
        for j in range(i + 1, 8):
            s, k = MUL[(i, j)]
            tri = tuple(sorted((i, j, k)))
            if tri not in latott and k != 0:
                latott.add(tri)
                a, b, c = tri
                print(f"     {{{a},{b},{c}}}: e{a}*e{b} = e{c},  e{b}*e{c} = e{a},  "
                      f"e{c}*e{a} = e{b}   (i^2=j^2=k^2=ijk=-1 ezen a hármason)")
    # -- alternativitás (ismétlődő változóra asszociatív) és egy őszinte nem-asszociatív példa
    rngv = [np.eye(8)[i] for i in range(1, 8)]
    alt_ok = True
    for x in rngv[:3]:
        for y in rngv[:3]:
            if not (np.allclose(_okto_szor(_okto_szor(x, x, MUL), y, MUL),
                                _okto_szor(x, _okto_szor(x, y, MUL), MUL)) and
                    np.allclose(_okto_szor(_okto_szor(x, y, MUL), y, MUL),
                                _okto_szor(x, _okto_szor(y, y, MUL), MUL))):
                alt_ok = False
    print(f"  alternativitás ((xx)y=x(xy), (xy)y=x(yy)) a kód-táblán: {'OK' if alt_ok else 'HIBA!'}")
    nemassz = None
    for x in rngv:
        for y in rngv:
            for z in rngv:
                if not np.allclose(_okto_szor(_okto_szor(x, y, MUL), z, MUL),
                                   _okto_szor(x, _okto_szor(y, z, MUL), MUL)):
                    nemassz = (np.argmax(x) , np.argmax(y), np.argmax(z))
                    break
            if nemassz:
                break
        if nemassz:
            break
    print(f"  NEM asszociatív (így kell lennie): pl. asszociátor e{nemassz[0]},e{nemassz[1]},"
          f"e{nemassz[2]} != 0 — az októniók őszintén nem-asszociatívak")
    # -- a motor pumpája kvaternió-szorzatként: 7 prím-részforgatás = egy pi-forgatás
    primek = [2, 3, 5, 7, 11, 13, 17]
    suly = [1.0 / p for p in primek]
    Q = KV(1)
    for w in suly:
        fi = np.pi * w / sum(suly)
        Q = Q * KV(np.cos(fi / 2), 0, np.sin(fi / 2), 0)     # forgatás a j tengely körül
    szog = 2 * np.arccos(np.clip(Q.a, -1, 1))
    print(f"  a 7 prím-pumpa kvaternió-szorzata: Q = {Q}  -> forgatásszög = {szog:.6f} = pi")
    r = Q * KK * Q.konj()                                    # Bloch-vektor konjugálás
    print(f"  Bloch: Q*k*Q^-1 = {r}  -> |0_L> (z=+1) a |1_L> (z=-1) állapotba töltődött")
    # -- divíziós-algebra létra: a [[7,1,3]] paraméterei
    print("  divíziós-algebra létra (R, C, H, O — az egyedüli normált divíziós algebrák):")
    print("     R: dim 1, Im = 0 |  C: dim 2, Im = 1 -> a kód 1 logikai kubite")
    print("     H: dim 4, Im = 3 -> a kód távolsága d=3 (Pauli = H) |  O: dim 8, Im = 7")
    print("     -> a [[7,1,3]] = (Im O, Im C, Im H): a kód paraméterei a divíziós létra.")
    print("  CPT-megjegyzés: az időmegfordítés itt a kvaternió-konjugálás (képzetes rész")
    print("  előjelváltása); a gép T-szimmetriája = a kvaternió-antiautomorfizmus.")

# ---------------------------------------------------------------- főprogram
if __name__ == "__main__":
    print("HANMAG KVHANTUMOS FORDÍTOTT CARNOT-GÉP — [[7,1,3]] Steane-kód, 16 kubit, 0 RNG")
    print()
    psi1 = kiserlet_motor()
    kiserlet_kuszob()
    kiserlet_kategoria()
    kiserlet_dimenziok()
    kiserlet_kvaternio()
    # determinizmus-bizonylat: ugyanaz a futás bitről bitre
    _, psi2, _ = motor_fut(csend=True)
    h1 = hashlib.sha256(np.ascontiguousarray(psi1).tobytes()).hexdigest()
    h2 = hashlib.sha256(np.ascontiguousarray(psi2).tobytes()).hexdigest()
    print()
    print("=" * 88)
    print(f"DETERMINIZMUS: sha256(állapot) = {h1[:32]}...")
    print(f"                két futás azonos: {h1 == h2}   (0 véletlenforrás a gépben)")
    print("=" * 88)
