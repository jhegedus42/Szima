#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANMAG_DESITTER — a gravitacios szarny elso gepe: SO(4,1) es a horizont
========================================================================
A Georgi-konyv az anyag-algebraikat adta (G2 = 7, SO(10) = 16, E6 = 27).
A gravitacio masik csalad: a TERIDO-algebrak. A gep legjobb sora
(rho_Lambda, 0.24 szigma) de Sitter-horizont-termodinamika — a de Sitter
csoport: SO(4,1).

MacDowell-Mansouri: a GR + Lambda az SO(4,1) gauge-elmelete, SO(3,1)-re
törve. A gep nyelven: A GRAVITACIO = A dS->LORENTZ REDUKCIO VESSZOJE —
egy szint-hatar ado, pontosan a 2+2-fajta.

Ez a gep ELRENDEZI az algebrat es KISZAMOLJA a horizont szamait a MERT
H0-bol. Levezetes meg nincs — a hazi feladat a 4 eltort generator aranak
gepi kiszamitasa.

0 RNG, 0 numpy — csak egeszek, pi, es a mert H0.
"""
from math import pi, log2, sqrt

def banner(cim):
    print()
    print("=" * 68)
    print(cim)
    print("=" * 68)

# --- SI pontos es mert ertekek --------------------------------------
C = 299792458.0                      # m/s (pontos)
HBAR = 1.054571817e-34               # J s
KB = 1.380649e-23                    # J/K (pontos)
G = 6.67430e-11                      # m^3 kg^-1 s^-2 (mert, 22 ppm)
MPC = 3.0856775814913673e22          # m
H0 = 67.4e3 / MPC                    # s^-1   (mert: Planck-piano)
L_P = sqrt(G * HBAR / C ** 3)        # Planck-hossz
T_P = HBAR / (L_P * KB) / C * C      # Planck-homerseklet... T_P = m_P c^2/k_B
M_P = sqrt(HBAR * C / G)
T_P = M_P * C * C / KB

# -------------------------------------------------------------------
def kiserlet_algebra():
    banner("1. AZ ALGEBRA: SO(4,1) = 10 = 6 + 4")
    dim = lambda n: n * (n - 1) // 2
    print(f"SO(4,1) dim = {dim(5)}   (de Sitter-csoport)")
    print(f"SO(3,1) dim = {dim(4)} = 3 forgas + 3 boost   (Lorentz-csoport)")
    print(f"eltort (tort) generatorok: {dim(5) - dim(4)} = a hiperboloid-transzlaciok")
    print()
    print("a gep nyelven: a Lorentz-reszcsoport a KOD, a 4 eltort irany")
    print("a VESSZO — a gravitacios csatlas ara itt lakik.")
    print()
    print("FIGYELEM: SO(4,1) != SO(10)! az elso a TERIDO (horizont),")
    print("a masodik az ANYAG (16-os spinor). a gep mindkettot szamolja,")
    print("de nem keveri — a ket vesszo kulon szamlara megy.")
    print()
    print("RIM (cimkezve): a Lorentz-algebra 6 = a szint-1 stabilizatorok;")
    print("a tort iranyok 4 = az adatbitek. rim, nem levezetes.")

# -------------------------------------------------------------------
def kiserlet_horizont():
    banner("2. A HORIZONT SZAMAI (mert H0 = 67.4 km/s/Mpc-bol)")
    H = H0
    R = C / H
    A = 4 * pi * R * R
    S_nat = A / (4 * L_P ** 2)              # entrópia, nat
    S_bit = S_nat / log2(2.718281828459045) # bit = nat / ln 2
    T_dS = HBAR * H / (2 * pi * KB)         # Gibbons-Hawking homerseklet
    print(f"de Sitter-sugar:  R = c/H0 = {R:.4e} m = {R / L_P:.3e} l_P")
    print(f"horizont-felulet: A = {A:.4e} l_P^2")
    print(f"S_dS = A/4 = {S_nat:.3e} nat = {S_bit:.3e} bit")
    print(f"  -> log2(S_bit) = {log2(S_bit):.2f}   (a gep szama: 407 = 7^3 + 2^6)")
    print(f"T_dS = hbar H / (2 pi k_B) = {T_dS:.3e} K")
    print()
    T_CMB = 2.7255
    r = T_CMB / T_dS
    print(f"T_CMB / T_dS = {r:.3e} = 2^{log2(r):.1f}   RIM: ~ 2^100")
    print(f"a horizont bites surusege: 1 bit / {4 * 0.6931:.3f} l_P^2 (Bekenstein-Hawking)")

# -------------------------------------------------------------------
def kiserlet_masodik_ido():
    banner("3. A MASODIK IDO KOZMIKUS ARA")
    T_dS = HBAR * H0 / (2 * pi * KB)
    print(f"a masodik ido = homerseklet. a kozmikus koho: T_dS = {T_dS:.2e} K")
    print("az elso ido a fazist szamolja (a CMB-fotonok oraja),")
    print("a masodik ido a horizont torlesenek ara (Gibbons-Hawking).")
    print()
    Om = 0.6889
    from math import log
    print(f"Omega_Lambda = {Om} vs ln 2 = {log(2):.4f}  ->  a gep a ln2-atkelo")
    print("elott all (z* = -0.0065): a horizont-bitek aranya MOST lepi at a")
    print("felezo pontot. a kozmikus Page-ido (Omega = 0.5) mar elmult (z ~ 0.33).")

# -------------------------------------------------------------------
def kiserlet_mm():
    banner("4. MacDOWELL-MANSOURI: A VESSZO ALAKJA")
    print("az SO(4,1)-kapcsolat felbomlik: W = (omega, e) — Lorentz-resz + tetrad.")
    print("a gorbulet: F = R + e e / l^2.")
    print("a hatas: S ~ integral eps F F = Einstein-Hilbert + Lambda-tag + Euler.")
    print("a Lambda-tag a 4 ELTORT irany szorzatabol jon (e e e e / l^4) —")
    print("a gravitacio ara SZOROSAN a vesszo iranyaiban lakik.")
    print()
    print("A HAZI FELADAT (a genomba irva): az SO(4,1) unitaris reprezentacioi")
    print("a gepen — a horizont Hilbert-terenek spektruma — es a 4 eltort")
    print("generator aranak kiszamitasa, mint szint-hatar ado (2+2-szeru).")
    print("olvasmany a polcon: ER=EPR (1306.0533) — a vagas = osszefonodas.")

# -------------------------------------------------------------------
if __name__ == "__main__":
    print("HANMAG_DESITTER — a gravitacios szarny elso gepe")
    print("SO(4,1) = 10 = 6 + 4: a gravitacio a de Sitter-algebra vesszoje")
    kiserlet_algebra()
    kiserlet_horizont()
    kiserlet_masodik_ido()
    kiserlet_mm()
    print()
    print("=" * 68)
    print("az anyag-algebra bepolcsozva (G2, SO(10), E6);")
    print("a terido-algebra kicsomagolva (SO(4,1) = 6 + 4);")
    print("a szamla nyitva: 4 eltort generator — az ar a gepen fizetendo.")
    print("=" * 68)
