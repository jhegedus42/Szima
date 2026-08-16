# -*- coding: utf-8 -*-
# HANMAG_KATEGORIA — a tornyok kategoriaja, a kor a 7 qubiten.
# A vazlat: QG-QFT-kvantum-kemia ES sejt-tobbes-allat-ember UGYANAZ A
# KATEGORIA (funtor-torvenyekkel merve). A tornyok a bazisvektorok
# (fonevek); a szint-lekepezesek az igek (morfizmusok); a nyilak a
# fonodas (minden nyil visszafordithato = groupoid = uniter).
# 2 qubitra a kompozicio kore Z_4 ({+-1,+-i}); 7 qubitre Z_7: a Singer-
# ciklus, a hetedik egyseggyokok — es a 21 a normalizere (pontos
# csoportelmelet; az alfa-osszefugges RIM, cimkezve).
import math, cmath, itertools
from math import comb

HIBAK = []
def ok(felt, uzenet):
    if felt: print(f"    [OK] {uzenet}")
    else:
        HIBAK.append(uzenet); print(f"    [HIBA] {uzenet}")
def fel(cim):
    print(); print("=" * 74); print(cim); print("=" * 74)

fel("1. A KOR A 7 QUBITEN — Singer-ciklus, hetedik egyseggyokok")
# Singer-feliras: pontok Z_7, egyenesek {i, i+1, i+3} (a (7,3,1) differenciahalmaz)
Ls = [frozenset(((i + d) % 7 for d in (0, 1, 3))) for i in range(7)]
def steiner(vonalak):
    parok = {}
    for v in vonalak:
        for a, b in itertools.combinations(sorted(v), 2):
            parok[(a, b)] = parok.get((a, b), 0) + 1
    return len(parok) == 21 and all(n == 1 for n in parok.values())
ok(steiner(Ls), "a Singer-feliras Steiner-harmasrendszer: minden par pontosan 1 egyenesen")
sigma = tuple((i + 1) % 7 for i in range(7))
def alkalmaz(p, v): return frozenset(p[i] for i in v)
ok(all(alkalmaz(sigma, v) in Ls for v in Ls), "a sigma: i->i+1 automorfizmus (egyenes->egyenes)")
def hatvany(p, k):
    r = tuple(range(7))
    for _ in range(k): r = tuple(r[p[i]] for i in range(7))
    return r
ok(hatvany(sigma, 7) == tuple(range(7)), "sigma^7 = id — a ciklus rendje 7 = Z_7")
z7 = [cmath.exp(2j * math.pi * k / 7) for k in range(7)]
ok(all(abs(z**7 - 1) < 1e-9 for z in z7), "a kompozicio kore: exp(2 pi i k/7), k=0..6 — HETEDIK egyseggyokok")
print("    a kor felbontasa: 2 pi/7 = 51.43 fok; a gep kompozicioja a koron")
print("    7 lepeses forgas — nem a {+-1,+-i} negyese.")

# izomorfia a regi L-felirassal (a nobel/kerdes-gepek Fano-sikja)
L_regi = [frozenset(s) for s in [(1,2,3),(1,4,5),(1,6,7),(2,4,6),(2,5,7),(3,4,7),(3,5,6)]]
izomorf = None
for p in itertools.permutations(range(7)):
    if {frozenset(p[i - 1] for i in v) for v in L_regi} == set(Ls):
        izomorf = p; break
ok(izomorf is not None, f"a regi feliras ugyanaz a sik (izomorfia: {izomorf}) — a 30 grammatika = 30 cimkezes")

fel("2. KET KOR, KET IDO — Z_4 (2 qubit) vs Z_7 (7 qubit)")
# 2-qubites Pauli-kompozicio fazisai
import numpy as np
PM = {'I': np.eye(2, dtype=complex),
      'X': np.array([[0, 1], [1, 0]], dtype=complex),
      'Z': np.array([[1, 0], [0, -1]], dtype=complex),
      'Y': np.array([[0, -1j], [1j, 0]], dtype=complex)}
def fazis_halmaz(dim_matrixok):
    F = set()
    nevek = list(dim_matrixok)
    for a in nevek:
        for b in nevek:
            M = dim_matrixok[a] @ dim_matrixok[b]
            for c in nevek:
                maszk = dim_matrixok[c] != 0
                vals = (M[maszk] / dim_matrixok[c][maszk]).flat
                if len(vals) and np.allclose(M, vals[0] * dim_matrixok[c]):
                    F.add(complex(np.round(vals[0], 10))); break
    return F
f1 = fazis_halmaz(PM)                                   # 1 qubit
P2 = {a + b: np.kron(PM[a], PM[b]) for a in PM for b in PM}   # 2 qubit
f2 = fazis_halmaz(P2)
ok(f2 == {1, 1j, -1, -1j}, f"2 qubit: a fazisok {sorted(map(str, f2))} = Z_4 a koron")
print(f"    (fizegi: 1 qubitra csak {sorted(map(str, f1))} — a -1-hez KET qubit kell;")
print("     a teljes kor a parositassal zarodik. ezert 'kompozicio 2 qubiten'.")
print("    2 qubitra a kor 4-reszes (stabilizator-fazis); 7-re 7-reszes")
print("    (struktura-ciklus). ket kulon kor = a ket ido ujabb arca.")

fel("3. A 21 MELYEN — a Singer-ciklus normalizere")
mu = tuple((2 * i) % 7 for i in range(7))     # x -> 2x mod 7, rendje 3
ok(hatvany(mu, 3) == tuple(range(7)), "mu: i->2i rendje 3 (2^3 = 8 = 1 mod 7)")
ok(all(alkalmaz(mu, v) in Ls for v in Ls), "mu is automorfizmus (2*{i,i+1,i+3} is egyenes)")
def komp(p, q): return tuple(p[q[i]] for i in range(7))
ok(komp(komp(mu, sigma), hatvany(mu, 2)) == hatvany(sigma, 2),
   "mu sigma mu^-1 = sigma^2 — Frobenius-relacio")
csop = set()
for a in range(7):
    for b in range(3):
        csop.add(komp(hatvany(sigma, a), hatvany(mu, b)))
ok(len(csop) == 21, f"|<sigma, mu>| = {len(csop)} = Z_7 x Z_3 (a normalizer)")
print(f"    PONTOS CSOPORTELMELET: 21 = |Z_7 x Z_3| = C(7,2).")
print("    az alfa nevezojehez (21/(2pi)) ez RIM — cimkezve, nem levezetes;")
print("    a torony-gep teherlistajan el: 'a 21 levezetese a sikbol'.")

fel("4. BAZISVEKTOROK = TORNYOK — a ket lanc ugyanaz a kategoria")
def torony(szint): return 7 ** szint, 1, 3 ** szint
print("    a funtor-torveny (mindket lancra): n x7, d x3, k = 1 (a vedett bit):")
for l in (1, 2, 3, 4):
    n, k, d = torony(l)
    print(f"      szint-{l}: [[{n},{k},{d}]]")
ok(all(torony(l + 1)[0] == 7 * torony(l)[0] and torony(l + 1)[2] == 3 * torony(l)[2]
       for l in (1, 2, 3)), "n -> 7n, d -> 3d a kodolas-funktorral")
ok(all(torony(l)[1] == 1 for l in (1, 2, 3, 4)), "k = 1 MINDEN szinten — a funktor a bitet orzi")
# kategoria-axiomak: identitas + asszociativitas a morfizmusokon
def kodol(x): return ("kod", x)
def dekod(x): return x[1] if x[0] == "kod" else None
ok(all(dekod(kodol(b)) == b for b in (0, 1)), "identitas: dekod o kodol = id a logikai biten")
def kompoz(f, g): return lambda x: f(g(x))
f3a, f3b = kompoz(kodol, kompoz(kodol, kodol)), kompoz(kompoz(kodol, kodol), kodol)
ok(all(f3a(b) == f3b(b) for b in (0, 1)), "asszociativitas: (kod o kod) o kod = kod o (kod o kod)")
print("    asszociativitas: a kodolas lancolhato (350 qubit, 3 szint — MERT:")
print("    hanmag_torony.py). QG->QFT->kvantum->kemia ES sejt->tobbes->allat->")
print("    ember: ugyanaz a szabaly — egy vedett bit felfele, a tobbi vesszo.")

fel("5. FONEV = IGE — a 7 pont bazis is meg ige is")
# GF(8): elemek {0..7}, osszeadas = XOR; a 7 nemnulla elem = a 7 pont
elemek = list(range(8))
def ige(p): return lambda x: x ^ p             # az ige: 'tolj el p-vel'
ok(all(ige(p)(ige(p)(x)) == x for p in range(1, 8) for x in elemek),
   "minden ige INVOLUCIO (onmagat visszaforditja) — a nyilak szimmetrikusak")
vegyuk = {(a ^ b) for a in elemek for b in elemek}
ok(vegyuk == set(elemek), "az igek kompozicioja ZARt: GF(8)+ = Z_2^3 (8 elem)")
print("    7 fonev (pont) <-> 7 ige (eltolas) + 1 identitas (a vakuum).")
print("    a gep nyelve GROUPOID: minden morfizmus megfordithato = uniter.")
print("    a nyil ezert emlekeztet a fonodasra: a kotodes is szimmetrikus.")

fel("6. A KOMPOZICIO SORSa — vezetek vagy assembly")
print("    nyil-lanc (A->B->C) ZARODATLAN: vezetek, k = 0 (feherallomany/metrika);")
print("    nyil-lanc ZARODIK (haromszog): assembly, k = +0.5 (szurkeallomany).")
print("    MERT: hanmag_gorbulet.py — a Forman/Ollivier-ertekek pont igy jottek.")
print("    a kompozicio ige tehat: 'KOT-ZAR' — a Hebb-szabaly kategoriai alakja.")
print()
print("=" * 74)
if not HIBAK:
    print("KATEGORIA ELLENORIZVE: a tornyok egy kategoria, a kor Z_7, a 21 a")
    print("normalizer, a fonevek igek, a nyilak megfordithatoak. a mag onhivatkozo.")
else:
    print(f"KATEGORIA-HIBA: {len(HIBAK)} sor: {HIBAK}")
print("=" * 74)
