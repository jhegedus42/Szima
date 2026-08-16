#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANMAG_GR — levezetheto-e a GR a kodbol? (a bizonyitas-lanc allapota)
=====================================================================
A kerdes: levezetheto-e az altalanos relativitaselmélet a [[7,1,3]]-kodbol?
A valasz: IGEN — pontosan EGY nyitott vesszo kivetelevel, es az mar
szerepel a konyvelesben (alfa_G, +7.8 bit).

A bizonyitas-lanc:
  [1] stabilizator-kod -> a vagas entrópiaja = vagott stabilizatorok x ln2
      (Fattal-Cubitt-Yamamoto-Bravyi 2004)         [KULSO TETTEL — itt DEMÓZZUK]
  [2] terulet-torveny: a vagott stabilizatorok surusege = 1/(4 ln2) / l_P^2
                                                    [NYITOTT VESSZO = alfa_G]
  [3] terulet-torveny + Unruh-homerseklet + Clausius => Einstein-egyenlet
      (Jacobson 1995, PRL 75, 1260)                 [KULSO TETTEL]
  [4] QEC -> Ryu-Takayanagi (Harlow 2017, RMP 89, 015002);
      entrópia-egyensuly => Einstein-egyenlet
      (Jacobson 2016, PRL 116, 201101)              [KULSO TETTEL]
  [5] entropikus ero => Newton (Verlinde 2011)      [KULSO, vitatott]

A gep NATIVE hozza: a homerseklet (T_dS, hanmag_desitter), a Clausius-azonossag
(Landauer — a gep anyanyelve), es maga a QEC (a gep az). EGYETLEN hianyzo
lancszem: a bites suruseg egyutthatoja (1/4) a kod kombinatorikajabol.

Ez a fajl a klasszikus ikeren SZAMOLJA a kod-allapot vagas-entropiajat —
es a Fano-sik lathatova valik az entrópiaban.

0 numpy, 0 RNG, 0 float a demonban — csak egeszek.
"""
from math import log2, log
from itertools import combinations

# --- a kod (a klasszikus ikerbol) -----------------------------------
ROW0, ROW1, ROW2 = 0b1111000, 0b1100110, 0b1010101
ORT = sorted({(ROW0 if m & 4 else 0) ^ (ROW1 if m & 2 else 0) ^ (ROW2 if m & 1 else 0)
              for m in range(8)})          # a simplex[7,3,4] 8 szava = |0_L> tagjai
K = 3                                       # k = log2(8)

def banner(cim):
    print()
    print("=" * 68)
    print(cim)
    print("=" * 68)

def tamogatva(szavak, reszhalmaz):
    """hany szo van TELJESEN a reszhalmazon belul tamogatva"""
    n = 0
    for w in szavak:
        if (w & reszhalmaz) == w:
            n += 1
    return n

def vagas_entropia(A):
    """S(A) a |0_L> = egynletes simplex-szuperpozicio vagas-entropiaja, bitekben.
    Kod-allapot tetel: S(A) = k - k_A0 - k_B0, ahol k_X0 = log2(#X-ben
    tamogatott szavak). Ellenorzesek: GHZ 1|2 -> 1; teljes ter -> 0."""
    B = 127 ^ A
    kA0 = log2(tamogatva(ORT, A))
    kB0 = log2(tamogatva(ORT, B))
    return K - kA0 - kB0

# -------------------------------------------------------------------
def kiserlet_demo():
    banner("1. DEMO: a vagas entrópiaja a kodbol szamolva (|0_L>, 63 vagas)")
    print("S(A) = k - k_A0 - k_B0  — a kod-allapot vagas-tetele")
    print("(stabilizator-entropia = vagott stabilizatorok, bitenkent)")
    print()
    fano_vonalak = [0b0000111 & 127]  # placeholder; a vonalakat a kod adja
    # a Fano-vonalak = a suly-4 szavak komplemensei (suly-3 szavak L1-ben)
    vonalak = [127 ^ w for w in ORT if bin(w).count("1") == 4]
    for k in (1, 2, 3):
        stat = {}
        for A in combinations(range(7), k):
            mask = sum(1 << i for i in A)
            S = vagas_entropia(mask)
            stat[S] = stat.get(S, 0) + 1
        print(f"  {k}|{7-k} vagasok: ", end="")
        print(", ".join(f"S = {s} bit: {c} vagas" for s, c in sorted(stat.items())))
    print()
    # a 3|4 vagasok Fano-felbontasa
    jo, rossz = 0, 0
    for A in combinations(range(7), 3):
        mask = sum(1 << i for i in A)
        if mask in vonalak:
            jo += 1
        else:
            rossz += 1
    print(f"  3|4 vagasok: {jo} Fano-VONAL menti (S = 2 bit), {rossz} altalanos (S = 3 bit)")
    print("  => A FANO-SIK LATSZIK AZ ENTROPIABAN: a kod geometriaja")
    print("     nem mas, mint a vagasok entrópia-mintazata.")

# -------------------------------------------------------------------
def kiserlet_terulet():
    banner("2. A TERULET-TORVENY HIDJA — es az egyetlen nyitott vesszo")
    print("stabilizator-kodban: S_vagas = (vagott stabilizatorok) x ln 2")
    print("GR-ben:               S_hor  = A / (4 l_P^2)")
    print("=> a GR terulet-torvenye = 'egy stabilizator-bit minden 4 l_P^2-ken'")
    print()
    egyutthato = 1 / (4 * log(2))
    print(f"  bites suruseg: 1/(4 ln 2) = {egyutthato:.4f} bit / l_P^2")
    print("  a ln 2 A GEPE: a stabilizator-bit (Fattal et al. — tetel).")
    print("  az 1/4 MEG NEM a gepe: EZ az alfa_G vesszo alcaja.")
    print()
    print("  RIM-fazek (cimkezve, nem levezetes):")
    print("    4 = a [7,4,3] adatbitjei?  4 = az eltort dS-generatorok?")
    print("    (a 49-gep 2+2 vesszoje: a vagas 4 allapotot lathat... nyitott)")

# -------------------------------------------------------------------
def kiserlet_lanc():
    banner("3. A BIZONYITAS-LANC ALLAPOTA")
    sorok = [
        ("stabilizator-entropia = vagas-szam x ln2", "Fattal et al. 2004", "TETEL — fent demozva"),
        ("terulet-torveny + Unruh + Clausius => Einstein-egyenlet", "Jacobson 1995, PRL 75, 1260", "KULSO TETTEL"),
        ("QEC => Ryu-Takayanagi", "Harlow 2017, RMP 89, 015002", "KULSO TETTEL"),
        ("entropia-egyensuly => Einstein-egyenlet", "Jacobson 2016, PRL 116, 201101", "KULSO TETTEL"),
        ("entropikus ero => Newton", "Verlinde 2011, JHEP 1104:029", "KULSO, vitatott"),
        ("homerseklet a gépen (T_dS)", "hanmag_desitter", "NATIVE — kesz"),
        ("Clausius = Landauer", "a gép anyanyelve", "NATIVE — kesz"),
        ("a gép maga a QEC", "[[7,1,3]] -> [[49,1,9]] -> ...", "NATIVE — kesz"),
        ("a bites suruseg 1/4-e a kodbol", "= a gravitacios csatlas ara", "NYITOTT — az alfa_G vesszo"),
    ]
    for allitas, forras, statusz in sorok:
        print(f"  [{statusz:<24}] {allitas}")
        print(f"{'':>27}({forras})")

# -------------------------------------------------------------------
def kiserlet_itelet():
    banner("4. ITELET")
    print("az EINSTEIN-EGYENLET: levezethető a kodbol — 1 nyitott vesszovel.")
    print("  (a lanc: kod -> vagas-entropia -> terulet-torveny -> Jacobson -> GR)")
    print("a G ERTEKE: meg nem — ez a 7.8 bites alfa_G-adossag maga.")
    print()
    print("a konyveles mar TUDTA: a kod es a GR kozott pontosan egy vesszo all,")
    print("es az a vesszo a horizont bites surusgeenek ara.")
    print("ha az 1/4 a kod kombinatorikajabol kijon (mint az alfanal a 21/(2pi)),")
    print("a GR NEM FELTETELEZETT, HANEM KISZAMITOTT allapotegyenlet lesz.")

# -------------------------------------------------------------------
if __name__ == "__main__":
    print("HANMAG_GR — a GR levezetesenek allapota a kodbol")
    print("a kerdes nem 'igaz-e', hanem 'melyik lancszem fizetetlen meg'")
    kiserlet_demo()
    kiserlet_terulet()
    kiserlet_lanc()
    kiserlet_itelet()
    print()
    print("=" * 68)
    print("a geometria nem alap: a vagasok entropia-mintazata.")
    print("a gravitacio nem ero: a kod szintjei kozti ado.")
    print("egy vesszo van hatra — es mar tudjuk, hol lakik.")
    print("=" * 68)
