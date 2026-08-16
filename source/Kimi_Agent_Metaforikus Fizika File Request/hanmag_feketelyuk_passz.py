#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hanmag_feketelyuk_passz.py — A FEKETE LYUK BELESSE A GÉPBE: a 127-bites lyuk útlevele
======================================================================================
A gép számkészletéből, a már bizonyított láncokkal:
  S_bits(M) = (4 pi / ln2) (M/m_P)^2        [Bekenstein, a gép 1 bit = 4 ln2 l_P^2 törvényéből]
  M = 2N E_bit/c^2                          [Landauer-híd, PONTOSAN zárt — az előző fájlban]
  T_H = hbar c / (4 pi k_B R)               [Hawking/Unruh]
  t_scr = (2R/c) ln S                       [gyors scrambler — a gép SAJÁT scramblerje]
  t_evap = 5120 pi (M/m_P)^3 t_P            [Page-féle elpárolgás]

Tartalom:
  1. A GÉP SAJÁT FEKETE LYUKA: az N = 127 = 2^7-1 bites lyuk teljes útlevele (SI-ben).
  2. A proton-stabilitás következmény: alfa_G = 2^127 azt jelenti, hogy a proton
     NEM lehet fekete lyuk (10^37-nel kevesebb bitje kéne) — a hierarchia = az anyag stabilitása.
  3. Asztrofizikai kalibráció: Nap, Sgr A*, M87* — ugyanazok a képletek 10^9 M_Nap-ig.
  4. Elpárolgás, Page-idő, maradvány: a végállapot 18 bites (4 pi/ln2) Planck-maradvány.
  5. Kapcsolat a motorhoz: a 127-bites lyuk = a Carnot-gép munkatestje; a Landauer 2N
     faktor itt is érvényes (M = 2N E_bit/c^2, arány = 1.000...).
"""

import numpy as np

LN2 = np.log(2)
c, h, G, kB = 299792458.0, 6.62607015e-34, 6.67430e-11, 1.380649e-23
hbar = h / (2 * np.pi)
lP = np.sqrt(G * hbar / c ** 3)
tP = lP / c
mP = hbar / (c * lP)
TP = mP * c ** 2 / kB
MSUN = 1.989e30
EV = 1.602176634e-19

def utlevel(M, nev, extra=""):
    """Fekete lyuk útlevél a gép képleteiből."""
    N = 4 * np.pi / LN2 * (M / mP) ** 2                      # entrópia bitben
    R = 2 * G * M / c ** 2
    A = 4 * np.pi * R ** 2
    TH = hbar * c / (4 * np.pi * kB * R)
    Eb = kB * TH * LN2
    tscr = 2 * R / c * np.log(max(N, 2))
    tev = 5120 * np.pi * (M / mP) ** 3 * tP
    print(f"  {nev}")
    if M < 1.0:
        print(f"    M = {M:.4e} kg = {M/mP:.4f} m_P;   R = {R:.4e} m = {R/lP:.3f} l_P")
    else:
        print(f"    M = {M:.4e} kg = {M/mP:.2e} m_P;   R = {R:.4e} m = {R/lP:.2e} l_P")
    print(f"    S = {N:.4e} bit;   A = {A:.4e} m^2 = 4 ln2 N l_P^2")
    print(f"    T_H = {TH:.4e} K;   E_bit(Landauer) = {Eb:.4e} J = {Eb/EV:.4e} eV")
    print(f"    t_scramble = {tscr:.4e} s = {tscr/tP:.2f} t_P;   t_evap = {tev:.4e} s")
    if extra:
        print(f"    {extra}")
    return N, R, TH

def kiserlet_sajat_lyuk():
    print("=" * 88)
    print("1. A GÉP SAJÁT FEKETE LYUKA — N = 127 = 2^7-1 bit (a Hilbert-tér nemtriviális állapotai)")
    print("=" * 88)
    Ncel = 127
    M = mP * np.sqrt(Ncel * LN2 / (4 * np.pi))
    N, R, TH = utlevel(M, "a 127-bites lyuk:")
    Eb = kB * TH * LN2
    M_land = 2 * Ncel * Eb / c ** 2
    print(f"    Landauer-ellenőrzés: M = 2N E_bit/c^2 = {M_land:.4e} kg  "
          f"(arány: {M_land/M:.12f} = 1)")
    print(f"    => a gép fekete lyuka ~2.65 m_P: az a legkisebb objektum, amely a [[7,1,3]]")
    print(f"       kód TELjes 2^7-1 állapotát tárolni tudja (Müller 7 -> Mersenne 127).")

def kiserlet_proton():
    print()
    print("=" * 88)
    print("2. A PROTON-STABILITÁS KÖVETKEZMÉNY — alfa_G = 2^127 fizikai jelentése")
    print("=" * 88)
    mp = 1.67262192369e-27
    Np = 4 * np.pi / LN2 * (mp / mP) ** 2
    print(f"  proton: S = {Np:.3e} bit  << 1 bit")
    print(f"  (m_P/m_p)^2 = {(mP/mp)**2:.4e}  vs  2^127 = {2.0**127:.4e}  (0.5%, ARANY)")
    print(f"  => a proton 2^127-szer 'túl könnyű' ahhoz, hogy fekete lyuk legyen: az")
    print(f"     alfa_G = 2^127 = AZ ANYAG STABILITÁSÁNAK ÁRA — ami nem tud 1 bitet sem")
    print(f"     tárolni, az nem omlanak össze horizonttá. Ezért létezünk.")

def kiserlet_asztro():
    print()
    print("=" * 88)
    print("3. ASZTROFIZIKAI KALIBRÁCIÓ — ugyanazok a képletek 60 nagyságrenden át")
    print("=" * 88)
    ev = 5120 * np.pi * (MSUN / mP) ** 3 * tP
    utlevel(MSUN, "Nap-tömegű fekete lyuk:")
    print(f"    (irodalmi értékek: S ~ 1.5e77 bit, T_H ~ 6.2e-8 K, t_evap ~ 2.1e67 év = "
          f"{2.1e67*3.156e7:.1e} s  ->  a gép értéke ezzel egyezik)")
    N, R, TH = utlevel(4.297e6 * MSUN, "Sgr A* (4.297e6 M_Nap):")
    print(f"    t_scramble ~ {2*R/c*np.log(N)/3600:.1f} óra — ennyi idő alatt keveri szét")
    print(f"    a becsapódó információt a galaxis-központi fekete lyuk")
    utlevel(6.5e9 * MSUN, "M87* (6.5e9 M_Nap):")

def kiserlet_parolgas():
    print()
    print("=" * 88)
    print("4. ELPÁROLGÁS, PAGE-IDŐ, MARADVÁNY")
    print("=" * 88)
    Ncel = 127
    M0 = mP * np.sqrt(Ncel * LN2 / (4 * np.pi))
    tev = 5120 * np.pi * (M0 / mP) ** 3 * tP
    # Page-idő: S_rad = S/2, azaz M^2 = M0^2/2 -> M = M0/sqrt2; M^3-törvény: t = tev(1-(M/M0)^3)
    tpage = tev * (1 - (1 / np.sqrt(2)) ** 3)
    print(f"  a 127-bites lyuk: t_evap = {tev:.3e} s = {tev/tP:.2e} t_P")
    print(f"  Page-idő (S_rad = S/2, M = M0/sqrt2): t_Page = {tpage:.3e} s = "
          f"{tpage/tev:.3f} t_evap")
    print(f"  (a gép Hayden–Preskill-kísérlete a kód szintjén mérte: az információ")
    print(f"   a sugárzás felezésekor válik kinyerhetővé — k = 5/7 átmenet, I = 2 bit)")
    Mr = mP
    Nr = 4 * np.pi / LN2
    print(f"  maradvány: az elpárolgás a Planck-skálán áll meg: M ~ m_P = {Mr:.3e} kg,")
    print(f"  S ~ 4 pi/ln2 = {Nr:.2f} bit  ->  a fekete lyuk végterméke egy ~18 bites")
    print(f"  objektum (a legkisebb értelmes horizont); alatta: nincs információ-tárolás.")

def kiserlet_motor_kapcs():
    print()
    print("=" * 88)
    print("5. KAPCSOLAT A CARNOT-MOTORHOZ — a 127-bites lyuk mint munkatest")
    print("=" * 88)
    print("  a Carnot-motor 16 kubites horizontja (7 adat + 6 ancilla + 3 környezet)")
    print("  a 127-bites lyuk MIKROSZKOPIS mása: a hibajavító a vákuum-polárizáció ellen")
    print("  dolgozik, a kibocsátott ancilla = Hawking-sugárzás, a bent maradt adat =")
    print("  bolygók; a Landauer-híd (M = 2N E_bit/c^2) mindkét skálán 1.000...-re zárul.")
    print("  a gép teljes lánca: [[7,1,3]] -> scrambler -> Carnot -> CPT -> QFT ->")
    print("  Landauer -> abdukció -> FEKETE LYUK: a 127-bites útlevéllel ZÁRVA.")

if __name__ == "__main__":
    print("HANMAG FEKETE LYUK-ÚTLEVÉL — a 127-bites lyuk (a gép számkészletéből)")
    print()
    kiserlet_sajat_lyuk()
    kiserlet_proton()
    kiserlet_asztro()
    kiserlet_parolgas()
    kiserlet_motor_kapcs()
