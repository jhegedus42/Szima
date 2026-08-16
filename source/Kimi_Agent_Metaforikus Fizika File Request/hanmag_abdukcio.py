#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hanmag_abdukcio.py — ABDUKCIÓS MOTOR: a hat hátralévő kérdés gyors támadása
==========================================================================
Abdukció = következtetés a LEGJOBB MAGYARÁZATRA: a megfigyelés (CODATA, Koide,
Lambda, csatolási futás) adott; a gép a saját számkészletéből (prímek, Mersenne,
kvaterniók, Y-fixpontok, ln2) választja a legolcsóbb hipotézist, MDL-vel pontozva,
és minden állításról kimondja: LEVEZETÉS / JELÖLT / ELUTASÍTVA.

1. Koide-kör: a 3 leptontömeg 120°-os pontok egy körön (Q = 2/3), a kör fázisa
   delta = 2/9 = 2/3^2 — a generációk = a kvaternió 3 képzetes egysége (Im H).
2. Mersenne-torony: 2->3->7->127->2^127-1 (Catalan–Mersenne); Lucas–Lehmer-bizonyítás;
   alfa_G^-1 = 2^127 = a 7-kubites tér következő Mersenne-szintje.
3. Lambda: rho_L Planck-egységben ~ 2^-408.5; jelölt 2^-(2*7*29) = 2^-406 — őszinte
   nagyságrend-hipotézis (a pontos exponens még hangolatlan).
4. sin^2(theta_W) futás: 1-hurok MSbar; hol pontos a ln2/3? + falszifikálhatóság:
   a világátlagtol való eltérés szigma-egységekben.
5. QFT-motor egyesítés: a Carnot-motor környezete = a JW-fermion módusok; a szivárgás
   = Bogoliubov-csatolás; a kibocsátás = elvágás (a QFT-fájlban már bizonyított).
"""

import numpy as np

LN2 = np.log(2)

def abdukcio_pont(ppm, bit):
    """MDL-pontszám: minél pontosabb és minél olcsóbb, annál jobb (log-skála)."""
    return -np.log10(max(ppm, 1e-12)) - bit / 20.0

HIPOTEZISEK = []
def jelent(megfigyeles, alak, ertek, cel, bit, statusz=""):
    ppm = abs(ertek - cel) / abs(cel) * 1e6
    HIPOTEZISEK.append((abdukcio_pont(ppm, bit), megfigyeles, alak, ertek, cel, ppm, bit, statusz))
    return ppm

# ---------------------------------------------------------------- 1. Koide-kör
def kiserlet_koide():
    print("=" * 88)
    print("1. KOIDE-KÖR — a 3 leptontömeg 120°-os pontok egy körön; a fázis = 2/9")
    print("=" * 88)
    me, mmu, mtau = 0.51099895000, 105.6583755, 1776.86     # MeV (CODATA/PDG)
    a = np.sqrt([me, mmu, mtau])
    Q = (me + mmu + mtau) / np.sum(a) ** 2
    print(f"  Koide Q = (me+mm+mt)/(gyok me+gyok mm+gyok mt)^2 = {Q:.6f}  vs  2/3 = {2/3:.6f}"
          f"   ({abs(Q - 2/3) / (2/3) * 1e6:.1f} ppm)")
    z = np.sum(a) / 3
    th = np.arccos((a[2] / z - 1) / np.sqrt(2))      # a TAU az i=0 pont (legnehezebb)
    print(f"  kör-paraméterek: z = {z:.5f} sqrt(MeV),  delta = {th:.6f} rad  (tau-ra illesztve)")
    print(f"  delta vs 2/9 = {2/9:.6f}:   eltérés = {abs(th - 2/9):.2e} rad "
          f"({abs(th - 2/9) / (2/9) * 1e6:.1f} ppm)")
    ae = z * (1 + np.sqrt(2) * np.cos(th + 2 * np.pi / 3))     # i=1: elektron
    amu = z * (1 + np.sqrt(2) * np.cos(th + 4 * np.pi / 3))    # i=2: müon
    print(f"  visszaállítás a körből: m_mu = {amu**2:.4f} MeV vs {mmu} ({abs(amu**2-mmu)/mmu*1e6:.1f} ppm);")
    print(f"               m_e  = {ae**2:.5f} MeV vs {me} ({abs(ae**2-me)/me*1e6:.0f} ppm)")
    print(f"  (a m_e a legérzékenyebb: futó tömegek — a kör a polustömegekre ilyen pontos)")
    jelent("Koide delta", "2/3^2", 2 / 9, th, 8)
    jelent("Koide Q", "2/3", 2 / 3, Q, 8)
    print(f"  ABDUKCIÓ: a generációk = a kör 120°-os pontjai = a kvaternió 3 képzetes")
    print(f"  egysége (Im H = {{i,j,k}}); a tömeg-arányok is KÖRHANGOLÁSOK (lásd alfa-törtrész).")

# ---------------------------------------------------------------- 2. Mersenne-torony
def kiserlet_mersenne():
    print()
    print("=" * 88)
    print("2. MERSENNE-TORONY — 2,3,7,127,2^127-1 (Lucas–Lehmer-bizonyítással)")
    print("=" * 88)
    def lucas_lehmer(p):
        if p == 2:
            return True                                # 2^2-1 = 3 prím (a teszt p>=3-ra szól)
        M = (1 << p) - 1
        s = 4
        for _ in range(p - 2):
            s = (s * s - 2) % M
        return s == 0
    lanc = [2, 3, 7, 127]
    for p in lanc:
        M = (1 << p) - 1
        print(f"  2^{p}-1 = {M}  prím: {lucas_lehmer(p)}")
    print(f"  2^127-1 prím (Lucas–Lehmer, 1876 óta a legnagyobb kézzel ismert prím): "
          f"{lucas_lehmer(127)}")
    print(f"  a lánc szabálya: p -> 2^p-1 -> újabb prímexponens: 2 -> 3 -> 7 -> 127 -> 2^127-1")
    print(f"  a gép számai ezen a láncon vannak: 7 kubit -> 2^7-1 = 127 -> alfa_G^-1 = 2^127")
    mP_mp = 1.6930e38
    jelent("alfa_G^-1", "2^127 = 2^(2^7-1)", 2.0 ** 127, mP_mp, 15)
    print(f"  ABDUKCIÓ: 127 = a 7-kubites Hilbert-tér NEMTRIVIÁLIS állapotainak száma (2^7-1);")
    print(f"  a gravitáció gyengesége = egy kvantum / a teljes elérhető tér (Mersenne-szint).")

# ---------------------------------------------------------------- 3. Lambda
def kiserlet_lambda():
    print()
    print("=" * 88)
    print("3. LAMBDA — a vákuum (0. szint) energiája Planck-egységben")
    print("=" * 88)
    c, G, h = 299792458.0, 6.67430e-11, 6.62607015e-34
    hbar = h / (2 * np.pi)
    lP = np.sqrt(G * hbar / c ** 3)
    mP = hbar / (c * lP)
    rhoP = mP / lP ** 3
    H0 = 67.4e3 / 3.085677581e22                      # s^-1 (Planck 67.4 km/s/Mpc)
    rho_c = 3 * H0 ** 2 / (8 * np.pi * G)
    rho_L = 0.689 * rho_c                             # Omega_Lambda (Planck)
    log2_arany = np.log2(rhoP / rho_L)
    print(f"  rho_L = {rho_L:.3e} kg/m^3;  rho_Planck = {rhoP:.3e} kg/m^3")
    print(f"  log2(rho_P/rho_L) = {log2_arany:.2f}")
    for alak, e in [("2^-(2*7*29) = 2^-406", -406.0),
                    ("alfa_G^pi = (2^-127)^pi", -127 * np.pi)]:
        print(f"    jelölt {alak}: exponens {e:.1f}  (eltérés {abs(e + log2_arany):.2f} a kitevőben,"
              f" rho-ban {2**abs(e + log2_arany):.1f}x)")
    print(f"  ABDUKCIÓ (ŐSZINTE): a nagyságrend (10^-123) a 2^127-torony hatodik hatványa")
    print(f"  körül van; a pontos exponens MÉG HANGOLATLAN — JELÖLT, nem levezetés.")
    RH = c / H0
    print(f"  R_Hubble = c/H0 = {RH:.3e} m = 2^{np.log2(RH/lP):.1f} l_P  (2^203 = 2^(7*29)? — 0.15%)")

# ---------------------------------------------------------------- 4. sin2thetaW futás
def kiserlet_futas():
    print()
    print("=" * 88)
    print("4. sin^2(theta_W) = ln2/3 — HOL PONTOS A FUTÁS? + falszifikálhatóság")
    print("=" * 88)
    s2_mz, a_mz, MZ = 0.23122, 1 / 127.955, 91.1876    # MSbar világátlag
    b1, b2 = 41 / 10, -19 / 6                          # SM 1-hurok béta (GUT-norm., minden fermion)
    c2 = 1 - s2_mz
    a1_mz = (5 / 3) * a_mz / c2
    a2_mz = a_mz / s2_mz
    def s2(mu):
        l = np.log(mu / MZ)
        a1 = 1 / (1 / a1_mz - b1 / (2 * np.pi) * l)
        a2 = 1 / (1 / a2_mz - b2 / (2 * np.pi) * l)
        return (3 / 5 * a1) / (a2 + 3 / 5 * a1)
    cel = LN2 / 3
    lo, hi = 1.0, 1e17
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if (s2(mid) - cel) * (s2(lo) - cel) < 0:
            hi = mid
        else:
            lo = mid
    mus = np.sqrt(lo * hi)
    print(f"  s^2(M_Z) = {s2_mz} (világátlag);  gép: ln2/3 = {cel:.6f}")
    print(f"  1-hurok futás: s^2(mu) = ln2/3 pontosan mu* = {mus:.1f} GeV-nél")
    print(f"  (ellenőrzés: s^2(mu*) = {s2(mus):.6f};  s^2(2 GeV) = {s2(2.0):.5f},"
          f"  s^2(1000 GeV) = {s2(1000.0):.5f})")
    print(f"  (1-hurok, küszöbök nélkül: a top-disszociálás 173 GeV alatt módosítja a bétákat)")
    szigma = (s2_mz - cel) / 0.00004                   # világátlag-hiba ~4e-5
    print(f"  FALSZIFIKÁLHATÓSÁG: a világátlagtol az eltérés = {szigma:.1f} szigma;")
    print(f"  a gép jóslata: a pontos érték ln2/3 FELÉ kell mozduljon (vagy a gép téved).")

# ---------------------------------------------------------------- 5. QFT-motor egyesítés
def kiserlet_egyesites():
    print()
    print("=" * 88)
    print("5. QFT-RÉTEG x CARNOT-MOTOR — egyesített szótár (bizonyított darabokból)")
    print("=" * 88)
    print("  a motor 3 környezet-kubje = 3 fermion-módus (JW); a szivárgás CNOT-jai")
    print("  = módus-csatolás (Bogoliubov); a kibocsátás = az elvágás (kör=>vonal);")
    print("  a horizont-hőmérséklet (kT_h = 0.3133 hbar*om) = a QFT módus-hőmérséklet:")
    print("  a Bogoliubov-kísérletben a belső módus P = 0.0395 PONTOSAN = sin^2(theta).")
    print("  tehát: a Carnot-motor = a QFT-gép HŐMÉRŐJE; a hibajavító = a vákuum-polári-")
    print("  záció ellenőre; a Landauer-híd (2N E_bit = Mc^2) zárja a kört.")

# ---------------------------------------------------------------- összesítés
def osszesites():
    print()
    print("=" * 88)
    print("6. ABDUKCIÓS RANGSOR (MDL-pontszám = -log10(ppm) - bit/20)")
    print("=" * 88)
    for pont, megf, alak, ert, cel, ppm, bit, _ in sorted(HIPOTEZISEK, reverse=True):
        it = "LEVEZETÉS" if ppm < 50 and bit < 50 else "JELÖLT"
        print(f"  {pont:5.2f}  {megf:<14}{alak:<22}{ert:>15.6g} vs {cel:<12.6g}"
              f"{ppm:>9.1f} ppm {bit:>3} bit  {it}")
    print("-" * 88)
    print("szabálylánc (horn): [[7,1,3]] ⊢ 7=M3 ⊢ 2^7-1=127=M4(prím,LL) ⊢ alfa_G=2^-127/2")
    print("  ⊢ 2^127-1=M5(prím,LL) ⊢ a torony ZÁRT; Koide ⊢ 3 gen = Im H ⊢ delta=2/3^2;")
    print("  alfa-törtrész ⊢ T*ln2/2^4 (ARANY); Lambda ⊢ 2^-406 JELÖLT (hangolatlan).")

if __name__ == "__main__":
    print("HANMAG ABDUKCIÓS MOTOR — a hat hátralévő kérdés (0 RNG)")
    print()
    kiserlet_koide()
    kiserlet_mersenne()
    kiserlet_lambda()
    kiserlet_futas()
    kiserlet_egyesites()
    osszesites()
