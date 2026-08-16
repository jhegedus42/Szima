#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hanmag_landauer.py — DIMENZIÓK A LANDAUERBŐL + A 137 ZONGORAHANGOLÁSA
=====================================================================
Az építő kérdései:
  "dimenziók = Landauerből jönnek => mennyi energia egy bit?"
  "a 137 tökéletes részéhez meg kell a zongorahangolás, a körön (fázison) ott van
   valami C a CPT-ből, színek, hangok, 3-as szám, 5-ös szám"

1. LANDAUER: 1 bit törlése T hőmérsékleten >= k_B T ln2 munka — ez a bit->energia híd.
   A horizonton a híd ÖSSZEZÁR: a 343 kubites fekete lyuk tömege PONTOSAN
   M c^2 = 2N . k_B T_H ln2  (a 2-es faktor: E = T S / 2, mert S ~ E^2; másképp:
   a Bogoliubov-pár KÉT oldala fizet minden bitért — belső + külső módus).
   Dimenzió-létra Landauerből: N bit -> terület -> R -> T_H -> E_bit -> M -> t.

2. ZONGORAHANGOLÁS: alfa^-1 = 137.035999084. Az egész rész a kód: 2^7 + 3^2 = 137.
   A törtrész = a fáziskör (az U(1)-mértékcsoport!) hangolási hibája:
   a zongorán a tiszta kvint (3:2) nem zárja a kört (Pythagoraszi komma 3^12/2^19),
   az 5-limit sem (szintonikus komma 81/80) — a fizikában a vákuum-polárizáció
   (radiatív korrekció) detunálja a fázist. A gép a SAJÁT Y-fixpontjával próbálja:
   delta = T* ln2 / 2^4. A döntés a szokásos MDL + 2000-as véletlen-kontroll — őszintén.
   "3-as szám, 5-ös szám": a dúr-triad 4:5:6 (C-E-G) prímtára {2,3,5} = az 5-limit;
   a 3 szín (SU(3)) és a 3 hang (triad) a CPT C-műveletének két arca.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hanmag_codata import kifejezes_ter, elorendez, legjobb

LN2 = np.log(2)

# ---------------------------------------------------------------- 1. Landauer
def kiserlet_landauer():
    print("=" * 88)
    print("1. MENNYI ENERGIA EGY BIT? — E_bit = k_B T ln2, és a dimenzió-létra Landauerből")
    print("=" * 88)
    c, h, G, kB = 299792458.0, 6.62607015e-34, 6.67430e-11, 1.380649e-23
    hbar = h / (2 * np.pi)
    lP = np.sqrt(G * hbar / c ** 3)
    mP = hbar / (c * lP)
    TP = mP * c ** 2 / kB
    eV = 1.602176634e-19

    def ebit(T):
        return kB * T * LN2

    print(f"  Landauer: 1 bit törlése T-n >= k_B T ln2 (SZIGORÚ fizikai határ, nem becslés)")
    for nev, T in [("kozmikus háttér, 2.725 K", 2.725),
                   ("szobahőmérséklet, 300 K", 300.0),
                   ("Planck-hőmérséklet", TP)]:
        E = ebit(T)
        print(f"    {nev:28s}: E_bit = {E:.3e} J = {E/eV:.3e} eV")
    # a gép horizontja (343 kubit)
    N = 343
    A = 4 * LN2 * N * lP ** 2
    R = np.sqrt(A / (4 * np.pi))
    TH = hbar * c / (4 * np.pi * kB * R)
    Eb = ebit(TH)
    M_land = 2 * N * Eb / c ** 2
    M_geom = R * c ** 2 / (2 * G)
    print(f"  a gép 343 kubites horizontja (T_H = {TH:.4e} K):")
    print(f"    E_bit(T_H) = {Eb:.4e} J = {Eb/eV:.4e} eV = {Eb/(mP*c**2):.4f} m_P c^2")
    print(f"    M = 2N E_bit/c^2 = {M_land:.4e} kg  vs  M = Rc^2/2G = {M_geom:.4e} kg")
    print(f"    arány = {M_land/M_geom:.12f}   <- PONTOSAN 1: a Landauer-híd ÖSSZEZÁR")
    print(f"    (a 2-es faktor: dE = T dS és S ~ E^2 -> E = T S/2; vagy másképp:")
    print(f"     minden bit KÉT móduson oszlik meg — belső + külső, a Bogoliubov-pár.)")
    print(f"  DIMENZIÓ-LÉTRA LANDAUERBŐL (N bit + c, h, G — semmi más):")
    print(f"    N = 343 bit  ->  A = 4ln2 N l_P^2 = {A:.3e} m^2   [tér: a bit FELÜLET]")
    print(f"                 ->  R = sqrt(A/4pi) = {R:.3e} m     [hossz]")
    print(f"                 ->  T_H = hbar c/4pi k_B R = {TH:.3e} K  [hőmérséklet]")
    print(f"                 ->  E_bit = k_B T_H ln2 = {Eb:.3e} J  [energia: LANDAUER]")
    print(f"                 ->  M = 2N E_bit/c^2 = {M_land:.3e} kg  [tömeg]")
    print(f"                 ->  t = R/c = {R/c:.3e} s            [idő]")
    print(f"    => tér, idő, tömeg, energia: mind az N bit Landauer-árából + CPT-skálákból.")

# ---------------------------------------------------------------- 2. zongorahangolás
def kiserlet_hangolas():
    print()
    print("=" * 88)
    print("2. A 137 ZONGORAHANGOLÁSA — a fáziskör (U(1)) komma-hibája")
    print("=" * 88)
    # a körhangolás klasszikus kommái
    pyth = 3 ** 12 / 2 ** 19
    synt = 3 ** 4 / (2 ** 4 * 5)
    diesis = 2 ** 7 / 5 ** 3
    print(f"  Pythagoraszi komma: (3/2)^12/2^7 = 3^12/2^19 = {pyth:.6f}  (a kvintkör nem zárul!)")
    print(f"  szintonikus komma:  3^4/(2^4.5) = 81/80 = {synt:.6f}  (az 5-limit hibája — '5-ös szám')")
    print(f"  nagy diesis:        2^7/5^3 = 128/125 = {diesis:.6f}")
    print(f"  a gép 7-es gyűrűje: (3/2)^7/2^4 = {3**7/2**11:.6f}  (a 7-kvintes kör hibája)")
    print(f"  12-TET kvint: 2^(7/12) = {2**(7/12):.6f} vs 3/2 = 1.5  (hiba {(2**(7/12)/1.5-1)*100:+.3f}%)")
    print(f"  7-TET kvint:  2^(4/7)  = {2**(4/7):.6f} vs 3/2 = 1.5  (hiba {(2**(4/7)/1.5-1)*100:+.3f}%)")
    print(f"  dúr-triad C-E-G = 4:5:6 = 2^2 : 5 : 2.3  -> a prímtár {{2,3,5}} = az 5-limit;")
    print(f"  a 3 szín (SU(3)c) és a 3 hang (triad): a CPT C-műveletének két arca.")

    ALFA = 137.035999084
    egesz = 2 ** 7 + 3 ** 2
    delta_cel = ALFA - egesz
    print(f"\n  alfa^-1 = {ALFA};  egész rész a kód: 2^7+3^2 = {egesz};  "
          f"hangolandó törtrész: delta = {delta_cel:.7f}")
    # delta-jelöltek a körhangolás és a gép fixpontjai közül
    jeloltek = []
    for p in [3, 5, 7]:
        for j in range(0, 6):
            jeloltek.append((1 / (p * 2 ** j * LN2), f"1/({p}*2^{j}*ln2)"))
    for nev, komma in [("pyth", pyth), ("synt", synt), ("diesis", diesis)]:
        for k in [1, 2, 3]:
            jeloltek.append((k * np.log(komma), f"{k}*ln({nev})"))
    Ts, pc = 0.83, 0.05785                              # a gép Y-fixpontjai (S1-modell)
    for j in range(2, 6):
        jeloltek.append((Ts * LN2 / 2 ** j, f"T*ln2/2^{j}"))
        jeloltek.append((pc * LN2 / 2 ** j, f"p_c*ln2/2^{j}"))
    jeloltek.append((np.log(1.5 / 2 ** (7 / 12)), "ln(kvint/12-TET)"))
    jeloltek.append((np.log(1.5 / 2 ** (4 / 7)), "ln(kvint/7-TET)"))
    jeloltek.append((1 / (40 * LN2), "1/(40*ln2)"))
    jeloltek.sort(key=lambda t: abs(t[0] - delta_cel))
    print(f"  legjobb delta-jelöltek:")
    for d, nev in jeloltek[:4]:
        ppm = abs(egesz + d - ALFA) / ALFA * 1e6
        print(f"    {nev:<16} delta = {d:.7f}  ->  alfa^-1 = {egesz + d:.7f}  ({ppm:.2f} ppm)")

    # őszinte MDL + kontroll a teljes kifejezés-téren + a kompozit alfa-alakokkal
    ter = kifejezes_ter()
    for d, nev in jeloltek:
        koltseg = 12 + 18 if "T*" in nev else 12 + 14     # 2^7+3^2 alap + delta-ár
        ter.append((egesz + d, f"2^7+3^2+{nev}", koltseg))
    lv, rend = elorendez(ter)
    (v, sz, k), d = legjobb(ALFA, ter, lv, rend)
    rng = np.random.RandomState(137)
    talal = 0
    for Ta in ALFA * np.exp(rng.uniform(-1, 1, 2000)):
        _, da = legjobb(Ta, ter, lv, rend)
        if da <= d:
            talal += 1
    p = talal / 2000
    ppm = abs(v - ALFA) / ALFA * 1e6
    it = "ARANY" if p < 0.01 else ("EZÜST" if p < 0.05 else ("BRONZ" if p < 0.15 else "elutasítva"))
    print(f"\n  a teljes tér ({len(ter)} alak) legjobbja az alfa^-1-re:")
    print(f"    {sz} = {v:.7f}   ({ppm:.3f} ppm, költség {k} bit)")
    print(f"    véletlen-kontroll (2000 ál-cél): p = {p:.4f}  ->  ítélet: {it}")
    print(f"  fizikai olvasat: a 137 egésze a KÓD (2^7+3^2 = Im O + a Gauss-sztori);")
    print(f"  a törtrész a fáziskör HANGOLÁSI HIBÁJA — a vákuum-polárizáció detunálása,")
    print(f"  amit a gép a SAJÁT T* = Y(dC/dT) fixpontjából ad (gép-belső mérték, nem CODATA).")

if __name__ == "__main__":
    print("HANMAG LANDAUER-DIMENZIÓK + A 137 ZONGORAHANGOLÁSA (0 RNG a fizikában)")
    print()
    kiserlet_landauer()
    kiserlet_hangolas()
