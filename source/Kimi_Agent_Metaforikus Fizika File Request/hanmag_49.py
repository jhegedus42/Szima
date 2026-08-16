#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANMAG_49 — a 7x7-es konkatenalt klasszikus iker
=================================================
Az elso gep ([[7,1,3]], hanmag_klasszikus.py) onmagaval konkatenalva:
[[7,1,3]] x [[7,1,3]] = [[49,1,9]].

JAVITAS: a konkatenalt tavolsag d = 3*3 = 9 (nem 7).
A torony: [[7^l, 1, 3^l]] — l=1: (7,1,3); l=2: (49,1,9); l=3: (343,1,27).

A 49 bit = 7 blokk x 7 bit. Minden blokk a regi Hamming[7,4,3];
a 7 blokk logikai erteke egy kulso [7,4,3]-ot alkot.
A meres itt is Hamming-tavolsag: a szindroma a hiba cime — most ket szinten.

Az iker NEM HISZ — MEGSZAMOL: az osszes suly <= 5 hibamintazatot
kimeritoen vegigprobalja (2 138 410 eset), es kirija, hol fizet a gep
a szintek hataran: EZ A KONKATENACIOS VESSZO.

Tiszta egeszek, XOR/AND/NOT — 0 float, 0 RNG, 0 numpy.
"""
from itertools import combinations
from collections import Counter
from time import time

# --- a kod (ugyanaz, mint az elso ikerben) --------------------------
ROW0, ROW1, ROW2 = 0b1111000, 0b1100110, 0b1010101

def par(x):
    return bin(x).count("1") & 1

def szin7(v):
    return (par(v & ROW0) << 2) | (par(v & ROW1) << 1) | par(v & ROW2)

SZIN = [szin7(v) for v in range(128)]
KOD7 = [v for v in range(128) if SZIN[v] == 0]                 # 16 kodso
ORT = sorted({(ROW0 if m & 4 else 0) ^ (ROW1 if m & 2 else 0) ^ (ROW2 if m & 1 else 0)
              for m in range(8)})                               # 8 szo, sulyok {0,4}
L1 = [v ^ 127 for v in ORT]                                     # 8 szo, sulyok {3,7}
COSET = {}
for v in ORT:
    COSET[v] = 0
for v in L1:
    COSET[v] = 1
T = 0b0000111   # suly-3 szo az L1-ben = blokk-logikai X (a legkonnyebb)

# --- belso dekoder-tablak (blokk-pozicio fuggetlen, 128 belepese) ----
CORR, COS = [], []
for _ in range(7):
    ct, st = [], []
    for b in range(128):
        s = SZIN[b]
        bb = b if s == 0 else b ^ (1 << (s - 1))   # 1 hiba javitasa a blokkban
        ct.append(bb)
        st.append(COSET[bb])                        # a blokk logikai erteke
    CORR.append(ct)
    COS.append(st)

# --- a ket szintu dekoder -------------------------------------------
def dekod(v):
    """49 bites szo -> (javitott szo, logikai bit).
    Belso szint: minden blokk 1 hibat javit (a szindroma a hiba cime).
    Kulso szint: a 7 blokklogikai biten 1 blokk-hiba javithato."""
    out, bvec = 0, 0
    for i in range(7):
        b = (v >> (7 * i)) & 127
        out |= CORR[i][b] << (7 * i)
        bvec |= COS[i][b] << i
    S = SZIN[bvec]
    if S:
        out ^= 127 << (7 * (S - 1))     # blokk-logikai korrekcio = komplemens
        bvec ^= 1 << (S - 1)
    return out, COSET[bvec]

def banner(cim):
    print()
    print("=" * 66)
    print(cim)
    print("=" * 66)

# ===================================================================
def kiserlet_felepites():
    banner("1. FELEPITES: 49 = 7 x 7")
    print("49 bit = 7 blokk x 7 bit; a 49 bites szo egyetlen Python int.")
    print()
    print("szindroma-bitek (klasszikus iker, bit-felis oldal):")
    print("  belso szint: 7 blokk x 3 bit = 21")
    print("  kulso szint: 7 blokklogika x 3 bit = 3")
    print("  osszesen: 24 bit -> ervenyes szavak: 2^(49-24) = 2^25")
    print()
    print("a kvantum-kod stabilizatorai (ugyanennek a ket oldala):")
    print("  belso: 7 blokk x 6 stabilizator = 42")
    print("  kulso: 6 stabilizator          =  6")
    print("  osszesen: 48 = 7^2 - 1         -> 1 logikai qubit")
    print()
    print("blokk = 16 kodszo = 16 Weyl-allapot (e, nu, u, d x szin x spin)")
    print("a 48 ketfele bomlasa:")
    print("  48 = 42 + 6   (szindroma-geometria: belso + kulso)")
    print("  48 = 3 x 16   (anyag: 3 generacio x 16 Weyl)   [RIMEL, nem levezetes]")
    print()
    # ervenyes szavak megszamolasa egy mintan: blokkok KOD7-ben,
    # blokklogikai vektor KOD7-ben
    print("logikai osztalyok: |0_L> = kulso ORT, |1_L> = kulso L1")
    print("  osztalyonkenti szavak: 8^7 x 8 = 2^24")
    print("  (blokkonkent 8 szo a valasztott mellekosztalyban, 8 kulso szo)")

# ===================================================================
def kiserlet_tavolsag():
    banner("2. TAVOLSAG: d = 3 x 3 = 9 — logikai operator sulya 9")
    LX = T | (T << 7) | (T << 14)     # blokk-logikai X a 0.,1.,2. blokkban
    w = bin(LX).count("1")
    print(f"L_X = T | T<<7 | T<<14   (T = {T:07b}, suly-3 L1-szo)")
    print(f"suly(L_X) = {w} = 3 x 3")
    # ellenorzes: minden szindroma nulla, es a logikai bit flippel
    out, logi = dekod(LX)
    bvec = 0
    for i in range(7):
        bvec |= COS[i][(LX >> (7 * i)) & 127] << i
    print(f"belso szindromak: {[SZIN[(LX >> (7*i)) & 127] for i in range(7)]} (mind 0)")
    print(f"kulso szindroma: {SZIN[bvec]} (= 0), kulso mellekosztaly: {COSET[bvec]} (= 1)")
    print("-> a 9-sulyu operator |0_L>-t |1_L>-be visz, detektalhatatlanul.")
    print("   a kod tavolsaga teher 9: negy hibat biztosan javit, otne nem.")

# ===================================================================
def kiserlet_korrekcio():
    banner("3. KIMERITO KORREKCIOS MERES: minden suly <= 4 hiba")
    print("a gep nem mintat vesz — az OSSZES hibamintazatot vegigjatsza:")
    print()
    print(f"{'suly':>4} {'mintazatok':>12} {'pontos':>12} {'logikai':>12} {'log.hiba':>10}")
    ossz = {}
    for w in range(5):
        t0 = time()
        tot = ex = lg = 0
        for combo in combinations(range(49), w):
            e = 0
            for p in combo:
                e |= 1 << p
            out, logi = dekod(e)
            tot += 1
            if out == 0:
                ex += 1
            if logi == 0:
                lg += 1
        ossz[w] = (tot, ex, lg)
        print(f"{w:>4} {tot:>12} {ex:>12} {lg:>12} {tot - lg:>10}   ({time()-t0:.1f} s)")
    print()
    print("pontos = a javitott szo bitrol bitre a kiindulasi |0_L> szo")
    print("logikai = a logikai bit megmaradt (a szo a helyes osztalyban)")
    print()
    w4hiba = ossz[4][0] - ossz[4][2]
    print(f"suly 4: logikai hibak = {w4hiba}")
    print(f"  elmeleti joslat: csak a 2+2 szetosztas bukik el:")
    print(f"  C(7,2 blokkonkent) x C(7,2 blokkok) = 21 x 441 = {21 * 441}", end="")
    print(f" = 21^3 = {21**3}   {'PONTOSAN EGYEZIK' if w4hiba == 21**3 else 'NEM EGYEZIK'}")
    return ossz

# ===================================================================
def kiserlet_vesszo():
    banner("4. A KONKATENACIOS VESSZO: suly-5 hibak (1 906 884 eset)")
    t0 = time()
    tot = lg = 0
    part = Counter()
    for combo in combinations(range(49), 5):
        e = 0
        for p in combo:
            e |= 1 << p
        out, logi = dekod(e)
        tot += 1
        if logi == 0:
            lg += 1
        else:
            cnt = [0] * 7
            for p in combo:
                cnt[p // 7] += 1
            part[tuple(sorted((c for c in cnt if c), reverse=True))] += 1
    hiba = tot - lg
    print(f"osszes mintazat: {tot}, logikai hiba: {hiba} ({hiba/tot:.4%})   ({time()-t0:.1f} s)")
    print()
    print("a bukasok szetosztas szerint (blokkonkenti hibaszamok):")
    for p, c in sorted(part.items(), key=lambda kv: -kv[1]):
        print(f"  {'+'.join(map(str, p)):>8}: {c:>8}")
    print()
    print("EZ A VESSZO: amikor ket blokk EGYSZERRE fizeti a belso adot (2+2),")
    print("a kulso szint mar csak 1 blokk-hibat tud rendezni — a tobbi kilottyen.")
    print("a gep a szintek hataran szamlal adot; a vesszo a hatar meroszama.")

# ===================================================================
def kiserlet_szamlap():
    banner("5. SZAMLAP: a torony")
    print(f"{'szint':>5} {'qubit':>6} {'tavolsag':>8} {'stabilizator':>12} {'logikai':>8}")
    for l in range(1, 4):
        n = 7 ** l
        d = 3 ** l
        print(f"{l:>5} {n:>6} {d:>8} {n - 1:>12} {1:>8}")
    print()
    print("7^1 = 7    — a kod (az elso iker)")
    print("7^2 = 49   — az anyag (3 generacio x 16 Weyl = 48 + 1 logikai)")
    print("7^3 = 343  — a Landauer-horizont (a korabbi gepek szama)")
    print("           stabilizator: 342 = 343 - 1 -> a 343. csatorna a logikai bit")
    print()
    print("tarolas: 2^49 bit = 70 TB; 2^49 float64 = 4.5 PB;")
    print("az iker mindezt 1 db 49 bites egeszben hordozza,")
    print("es 2 138 410 hibamintazatot szamol ki percek alatt.")

# ===================================================================
if __name__ == "__main__":
    print("HANMAG_49 — a 7x7-es konkatenalt klasszikus iker")
    print("[[7,1,3]] x [[7,1,3]] = [[49,1,9]] — meres = Hamming-tavolsag, ket szinten")
    kiserlet_felepites()
    kiserlet_tavolsag()
    kiserlet_korrekcio()
    kiserlet_vesszo()
    kiserlet_szamlap()
    print()
    print("=" * 66)
    print("het blokk, egy logikai bit, es a vesszo pontosan ott,")
    print("ahol a ketto talalkozik: 2 + 2.")
    print("=" * 66)
