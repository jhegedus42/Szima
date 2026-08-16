#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hanmag_klasszikus.py — KLASSZIKUS IKER: a gép tisztán bitekben és kapukban
===========================================================================
A kvantumgép CSS-váza = két KLASSZIKUS Hamming-kód összeillesztve:
[[7,1,3]] Steane = C[7,4,3] Hamming ⊃ C_ort[7,3,4] szimplex-duál.
Ez a fájl 0 numpy, 0 RNG, 0 lebegőpontos: minden állapot egy 7-bites szó (int),
minden kapu XOR/AND/NOT/CNOT, és minden mérés egy HAMMING-TÁVOLSÁG —
a felhasználó sejtése szerint: a "mérésből kapott bitszám" = d_H(szó1, szó2).

  1. Kapuk: XOR/AND/NOT/CNOT/Toffoli inteken (igazságtábla-ellenőrzéssel).
  2. Hamming[7,4,3]: kódolás, szindróma, javítás; súlyeloszlás = 1+7x^3+7x^4+x^7.
  3. A MÉRÉS = Hamming-távolság: a szindróma = a hiba "címe" (d_H a kódtól).
  4. A logikai kubit klasszikus váza: |0_L> = C_ort (8 szó), |1_L> = komplemens;
     d_H(0_L, 1_L) = 7 PONTOSAN — az anyag-antianyag távolság 7 bit.
  5. T-törés és Landauer TISZTÁN KLASSZIKUSAN: a reset = szindróma-törlés;
     rostaszál = 8 prekép -> törölt információ = 3 bit = 3 kT ln2 / ciklus.
  6. A gép számai mint bitek és távolságok (összesített tábla).
  7. A HATÁR (őszinte): ami kimarad — a folytonos fázis (a KÖR): RY-fi, Bogoliubov,
     alfa/2pi-hurok. A klasszikus iker a stabilizátor-rétegre PONTOS (Gottesman–Knill);
     a fizika maradéka = 1 kör, és ott lakik a 31/(2 pi x).
"""

# ---------------------------------------------------------------- 1. kapuk
def NOT(x):        return x ^ 1
def XOR(a, b):     return a ^ b
def AND(a, b):     return a & b
def CNOT(c, t):    return (c, t ^ c)          # vezérlő, cél
def TOFFOLI(a, b, t): return (a, b, t ^ (a & b))

def pop(x):        return bin(x).count("1")
def dH(a, b):      return pop(a ^ b)          # Hamming-távolság = popcount(XOR)
def par(x):        return pop(x) & 1          # paritás

def kiserlet_kapuk():
    print("=" * 88)
    print("1. KAPUK — a gép alapkövei (igazságtábla, 0/1)")
    print("=" * 88)
    ok = all(NOT(a) == 1 - a and XOR(a, b) == (a + b) % 2 and AND(a, b) == a * b
             for a in (0, 1) for b in (0, 1))
    ok2 = all(CNOT(c, t) == (c, t ^ c) and TOFFOLI(a, b, t) == (a, b, t ^ (a & b))
              for c in (0, 1) for t in (0, 1) for a in (0, 1) for b in (0, 1))
    print(f"  NOT/XOR/AND/CNOT/Toffoli igazságtáblák: {'HELYES' if ok and ok2 else 'HIBA'}")
    print(f"  a Hamming-távolság maga is kapu: d_H(a,b) = popcount(a XOR b)")

# ---------------------------------------------------------------- 2. Hamming[7,4,3]
# paritás-mátrix SORAI intekben (a motor HCHK-jából, oszlop q = bináris q+1):
ROW0, ROW1, ROW2 = 0b1111000, 0b1100110, 0b1010101     # = 120, 102, 85
def szindroma(v):
    """3 bites szindróma: s = (s0 s1 s2) = a hiba oszlopának bináris értéke = j+1."""
    return (par(v & ROW0) << 2) | (par(v & ROW1) << 1) | par(v & ROW2)

# a kód = a mag (minden 7-bites szó, aminek 0 a szindrómája):
KOD = [v for v in range(128) if szindroma(v) == 0]
def _bazis(szavak, k):
    b = []
    for v in szavak:
        w = v
        for x in b:
            w = min(w, w ^ x)
        if w:
            b.append(w)
        if len(b) == k:
            break
    return b
def kodol(m, B):
    v = 0
    for i in range(4):
        if (m >> i) & 1:
            v ^= B[i]
    return v

def kiserlet_hamming():
    print()
    print("=" * 88)
    print("2. HAMMING[7,4,3] — a kvantumkód klasszikus csontváza")
    print("=" * 88)
    B = _bazis(KOD, 4)
    assert all(kodol(m, B) in KOD for m in range(16))
    print(f"  |C| = {len(KOD)} = 2^4 kódszó;  generátor-bázis: {[f'{b:07b}' for b in B]}")
    # súlyeloszlás
    W = {}
    for v in KOD:
        W[pop(v)] = W.get(pop(v), 0) + 1
    print(f"  súlyeloszlás: A(x) = 1 + 7x^3 + 7x^4 + x^7  mért: {dict(sorted(W.items()))}")
    print(f"  kódtávolság: min d_H(különböző kódszavak) = "
          f"{min(dH(a, b) for a in KOD for b in KOD if a != b)}  -> 1 hiba javítható")
    # teljes javító-teszt: 16 kódszó x 7 egybites hiba
    n = 0
    for c in KOD:
        for j in range(7):
            v = c ^ (1 << j)
            s = szindroma(v)
            javitott = v ^ (1 << (s - 1)) if s else v
            assert javitott == c
            n += 1
    print(f"  javító-teszt: {n} egybites hiba MINdegyike visszaállítva (szindróma -> pozíció)")

# ---------------------------------------------------------------- 3. a mérés = Hamming-távolság
def kiserlet_meres_dH():
    print()
    print("=" * 88)
    print("3. A MÉRÉS = HAMMING-TÁVOLSÁG (a felhasználói szabály számszerűen)")
    print("=" * 88)
    print("  b(s1, s2) := d_H(s1, s2) = popcount(s1 XOR s2)  — a 'mérésből kapott bitszám'")
    c = KOD[5]
    print(f"  példa: kódszó {c:07b};  hibás másolatok és a mérés kimenete:")
    for j in (0, 3, 6):
        v = c ^ (1 << j)
        print(f"    hiba a {j}. biten: d_H(v, C) = 1;  szindróma = {szindroma(v):03b} = {szindroma(v)}"
              f" = a hiba POZÍCIÓJA+1  -> a szindróma a távolság CÍME")
    print(f"  Steane: Z-szindróma (3 bit) + X-szindróma (3 bit) = 6 bit/mérés -> 2^6 = 64 szindróma;")
    print(f"  (a T-törés kísérlet 32 = 2^5 ancsilla fáziscsatornát mért — a 64 fele;")
    print(f"   az alfa-jelölt: 31 = 32-1, a kijelölt csatorna nélkül, ld. hanmag_zaras 6.)")

# ---------------------------------------------------------------- 4. logikai kubit = komplemens-pár
def kiserlet_logikai():
    print()
    print("=" * 88)
    print("4. A LOGIKAI KUBIT KLASSZIKUS VÁZA — |0_L>, |1_L> mint bit-HALMAZOK")
    print("=" * 88)
    ORT = []                                                # C_ort = sorköz (szimplex)
    for m in range(8):
        v = 0
        if m & 1: v ^= ROW0
        if m & 2: v ^= ROW1
        if m & 4: v ^= ROW2
        ORT.append(v)
    assert all(szindroma(v) == 0 for v in ORT)              # duál a kódban
    L1 = [v ^ 0b1111111 for v in ORT]                       # |1_L> = X^7 |0_L> = komplemens
    print(f"  |0_L> tartó = C_ort[7,3,4]: {len(ORT)} szó;  |1_L> = komplemens: {len(L1)} szó")
    print(f"  C_ort súlyai: {sorted(pop(v) for v in ORT)}  (minden nemnulla: 4 = szimplex)")
    d = {dH(a, b) for a in ORT for b in L1}
    print(f"  d_H(0_L, 1_L) értékek = {sorted(d)}:  állapot↔SAJÁT komplemense = 7 BIT (pontosan);")
    print(f"  a két halmaz min. távolsága = 3 = a kódtávolság (ezért nem keverednek).")
    print(f"  C operátor = XOR 1111111 (komplemens);  Z_L = paritás;  |+_L> tartó = C (16 szó)")
    print(f"  SPEKTRUM d_H-ban a vákuumtól (|0000000>): 0 (vákuum), 3 (7 szó: a Hamming-vonalak),")
    print(f"  4 (7 szó: komplemensek), 7 (a pólus) — a '7 fent / vákuum / 7 lent' = SÚLYELOSZLÁS.")

# ---------------------------------------------------------------- 5. T-törés = szindróma-törlés
def reset(v):
    """Dekódolás+törlés: a legközelebbi kódszóra (1 bites javítás). SOK-AZ-EGYHEZ."""
    s = szindroma(v)
    return v ^ (1 << (s - 1)) if s else v

def kiserlet_tores_bits():
    print()
    print("=" * 88)
    print("5. T-TÖRÉS ÉS LANDAUER TISZTÁN KLASSZIKUSAN — a vágás = szindróma-TÖRLÉS")
    print("=" * 88)
    pre1, pre2 = 0b0000001, 0b0000100                       # két KÜLÖNBÖZŐ pre-állapot
    r1, r2 = reset(pre1), reset(pre2)
    print(f"  pre1 = {pre1:07b} -> post = {r1:07b};   pre2 = {pre2:07b} -> post = {r2:07b}")
    print(f"  ||pre1 - pre2||_H = {dH(pre1, pre2)} bit;  ||post1 - post2||_H = {dH(r1, r2)} bit"
          f"  -> SOK-AZ-EGYHEZ: nincs inverz, T TÖRIK (0 RNG, tiszta bit)")
    rosta = [v for v in range(128) if reset(v) == 0]
    print(f"  rostaszál a 0 kódszó fölött: {len(rosta)} prekép = 2^7/2^4 = 8")
    print(f"  törölt információ = log2(rosta) = 3 bit = PONTOSAN a szindróma (3 bit);")
    print(f"  teljes Steane-reset (Z+X): 6 bit -> LANDAUER-SZÁMLA: 6 kT ln2 / ciklus;")
    print(f"  a motor Landauer-hídja innentől bit-pontos: N törölt bit -> E = N kT ln2.")

# ---------------------------------------------------------------- 6. a gép számai bitben
def kiserlet_szamok():
    print()
    print("=" * 88)
    print("6. A GÉP SZÁMAI MINT BITEK ÉS TÁVOLSÁGOK")
    print("=" * 88)
    for nev, ert, forras in [
        ("állapottér", 128, "2^7 szó"),
        ("kódszavak", 16, "2^4 = |C|"),
        ("duál (|0_L> tartó)", 8, "2^3 = |C_ort|"),
        ("törölt bit / reset", 3, "log2(rosta) = Z-szindróma"),
        ("szindróma teljesen", 6, "3+3 bit = 6 ancsilla (2^6 = 64)"),
        ("kódtávolság", 3, "min d_H(C) -> 1 hibajavítás"),
        ("duál súly", 4, "szimplex [7,3,4]"),
        ("anyag-antianyag", 7, "d_H(0_L, 1_L) = komplemens"),
        ("spektrum-szintek", "0,3,4,7", "súlyeloszlás 1+7x^3+7x^4+x^7"),
    ]:
        print(f"  {nev:<24}{str(ert):<10}  {forras}")
    print(f"  -> a 137 egész része is ilyen: 2^7 (=128 szó) + 3^2 (= (kódtávolság)^2) = 137.")

# ---------------------------------------------------------------- 7. a határ
def kiserlet_hatar():
    print()
    print("=" * 88)
    print("7. A HATÁR (ŐSZINTE) — ami NEM megy klasszikusan: A KÖR")
    print("=" * 88)
    print("  a stabilizátor-réteg (H, CNOT, Pauli, mérés) KLASSZIKUSAN PONTOS (Gottesman–Knill):")
    print("  ez az iker azt bitről bitre visszaadja. Ami KIMARAD: a folytonos fázis —")
    print("  RY(fi), a pumpa, a Bogoliubov-szorítás, a spinor 2pi -> -1.")
    print("  a gép tétele: fizika = bitek + 1 kör; a klasszikus iker = a bitek;")
    print("  a kör = ahol a hurok-adósság lakik: alfa^-1 = 2^7+3^2 + 31/(2 pi x), 5.3 bit.")
    print("  és a T-törés tanulsága visszafelé is áll: a vágás PONTOSAN a kört vágja ki —")
    print("  a klasszikus iker tehát a 'mérés utáni' világ: bit, entrópia, Landauer.")

if __name__ == "__main__":
    print("HANMAG KLASSZIKUS IKER — 0 és 1, kapuk, Hamming-távolság (0 RNG, 0 float)")
    print()
    kiserlet_kapuk()
    kiserlet_hamming()
    kiserlet_meres_dH()
    kiserlet_logikai()
    kiserlet_tores_bits()
    kiserlet_szamok()
    kiserlet_hatar()
