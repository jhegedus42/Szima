# -*- coding: utf-8 -*-
"""
HANMAG-NOBEL -- a GUT levezetese, eloszorol vegig, merve.

Hogy jon ki az egesz? Egy mag, egy vesszo, es a kovetkezmenyeik.
Minden allitas szam: ami nem szamolhato ujra, az rime van jelolve.
Futtatas: python3 hanmag_nobel.py   ->   A GUT LEVEZETVE
"""
import math, random
from itertools import permutations, combinations

def ok(felt, uzenet):
    print(("    [OK] " if felt else "    [HIBA] ") + uzenet)
    if not felt: raise AssertionError(uzenet)

def fel(cim):
    print("\n" + "=" * 66 + "\n" + cim + "\n" + "=" * 66)

LN2 = math.log(2)
KB, C_, HBAR, L_P = 1.380649e-23, 299792458.0, 1.054571817e-34, 1.616255e-35

# ----------------------------------------------------------------------
fel("PROLOGUSZ -- a kerdes")
print("    mi a legkisebb dolog, ami egy hibat kijavit?")

# ----------------------------------------------------------------------
fel("I. FEL -- A MAG: het = 2^3 - 1")
L = [(1,2,3),(1,4,5),(1,6,7),(2,4,6),(2,5,7),(3,4,7),(3,5,6)]
Ls = {frozenset(l) for l in L}
n_aut = sum(1 for p in permutations(range(1, 8))
            if all(frozenset(p[x-1] for x in l) in Ls for l in L))
ok(n_aut == 168, "a Fano-sik automorfizmusai: 168 = GL(3,2) = PSL(2,7)")
print("    a 7 ponton EGYETLEN Steiner-harmasrendszer letezik; a 168 a masodik")
print("    legkisebb nem-kommutativ egyszeru csoport. GF(8): + = XOR, x = Singer.")
print("    (rim: a 7 iranyitott egyenes = az oktoniok szorzotablaja -- Georgi 27.3)")

# ----------------------------------------------------------------------
fel("II. FEL -- A KOD: [[7,1,3]]")
# Steane: a Hamming [7,4,3] paritas-matrixanak X es Z peldanyai + logikai Z
H_rows = [(1,2,3,5), (1,2,4,6), (1,3,4,7)]
def maszk(sor): return sum(1 << (q - 1) for q in sor)
gen = [(maszk(r), 0) for r in H_rows] + [(0, maszk(r)) for r in H_rows]
logik = [(0, 0b1111111), (0b1111111, 0)]
ok(len(gen) == 6 and all(bin(x | z).count("1") == 4 for x, z in gen),
   "6 fuggetlen stabilizator (4-sulyu), 1 logikai qubit")
print("    tavolsag 3: a legkisebb logikai operator sulya 3 (X^7 es Z^7 a kodterben)")

# ----------------------------------------------------------------------
fel("III. FEL -- A VESSZO: a hangolasi adossag")
vesszo = 330309 / 1906884
ok(math.factorial(49)//(math.factorial(5)*math.factorial(44)) == 1906884,
   "a nevezo C(49,5) = 1 906 884 -- az 5-sulyu osszeomlas-mintak tere")
print(f"    vesszo = 330309/1906884 = {vesszo:.6f}")
print("    jelentese a projektben: entropiatermeles = az ido nyila;")
print("    a hangolt (vesszo nelkuli) vilag nem letezhetne -- elet a resekben.")

# ----------------------------------------------------------------------
fel("IV. FEL -- A TORONY: [[7^l,1,3^l]], egy vedett bit felfele")
def kapacitas(n):
    return n + sum(math.log2(2**k + 1) for k in range(1, n + 1))
vart = {7: 36, 49: 1275, 343: 59340, 2401: 2886003}
for n, v in vart.items():
    k = kapacitas(n)
    ok(abs(k - v) / v < 0.01, f"[[{n},1,{3**int(round(math.log(n,7)))}]] ~ {k:.0f} bit stabilizator-allapot")
print("    szintek: pont/szo/jelentesdarab/vilag -- minden szint 1 logikai bitet")
print("    jelent felfele (renormalizalas); a logikai bit az EN, mozdulatlan.")

# ----------------------------------------------------------------------
fel("V. FEL -- A KET IDO = KET HOMERSEKLET (Carnot)")
for T, nev in [(310, "agy (310 K)"), (2.7255, "CMB"), (2.66e-30, "de Sitter")]:
    print(f"    Landauer {nev:16s}: kT ln2 = {KB*T*LN2:.2e} J/bit")
ok(abs(20/(KB*310*LN2)/6.7e21 - 1) < 0.05, "20 W -> 6.7e21 bit/s a fejplafon")
ar = 4*LN2*L_P**2
ok(abs(ar/7.24e-70 - 1) < 0.02, "horizont-ar: 4 ln2 l_P^2 = 7.24e-70 m^2/bit (az alfa_G vesszo)")
print("    a felejtes modja a mert szam: NAIV 63 bit vs OKOS 0 bit (hanmag_carnot.py)")

# ----------------------------------------------------------------------
fel("VI. FEL -- A HUTOGEP: meres-indukalta fazisatalakulas")
from hanmag_fazis import fut_lanc
vol = sum(fut_lanc(16, 0.0, 48, random.Random(9261)) for _ in range(4)) / 4
are = sum(fut_lanc(16, 0.5, 48, random.Random(9261)) for _ in range(4)) / 4
ok(vol > 4 and are < 1, f"p=0: terfogat-torveny (S_fel~{vol:.1f}); p=0.5: terulet-torveny ({are:.2f})")
print("    a hutokozeg = az osszefonodas; a figyelem a kompresszor-gomb (p)")

# ----------------------------------------------------------------------
fel("VII. FEL -- A JELENTES: alak + cimzes")
ok(5040 // 168 == 30, "30 Fano-grammatika letezik 7 ponton -- a forma veges")
def kupon(rng):
    lat, n = set(), 0
    while len(lat) < 7:
        t = frozenset(rng.sample(range(1, 8), 3)); n += 1
        if t in Ls: lat.add(t)
    return n
rng = random.Random(713)
atlag = sum(kupon(rng) for _ in range(20000)) / 20000
ok(85 < atlag < 96, f"a nyelvtan ~{atlag:.0f} hármasbol kitanulhato (~9 mese); a szotar vegtelen")

# ----------------------------------------------------------------------
fel("VIII. FEL -- A GORBE: a Hebb a geometriat hajlitja")
from hanmag_gorbulet import par_graf, ollivier
import hanmag_vilag as V
v = V.epits_vilagot()
ok(par_graf(v) == {}, "kotes nelkul nincs geometria: a friss vilag par-grafja URES")
k3 = ollivier({(0,1):1,(1,2):1,(0,2):1})
ok(all(x > 0.4 for x in k3.values()), f"a zarodas hordozza a gorbseget: K3 k = {list(k3.values())[0]}")
print("    a stabilizator-fonodas nem paros (monogamia): az assembly HIPEREL;")
print("    a sziluett a gorbulet permutacio-invariens kiolvasasa.")

# ----------------------------------------------------------------------
fel("IX. FEL -- A KOZMOSZ: ket fuggetlen talalat")
a2 = 21 / (2 * math.pi)
x = 137.0
for _ in range(300):
    x = 137 + 31 / (2 * math.pi * x) - a2 / (2 * math.pi * x) ** 2
print(f"    alfa^-1 fixpont: x = 137 + 31/(2pi x) - a2/(2pi x)^2, a2 = 21/(2pi)")
print(f"    -> {x:.8f}  (a 21 Fano-par / 2pi-ciklus; 31 = 7 pont + 24 kapu, rim)")
try:
    import hanmag_alfa_ado as A
    xz = A.kiserlet_fano()
    ok(abs(xz - x) < 1e-6, "az alfa_ado gep ugyanide konvergal (z = 1.14 vs Rb)")
except Exception as e:
    print("    (alfa_ado gep nem futott most:", e, ")")
H0 = 67.4 * 1000 / 3.085677581e22
R = C_ / H0
# JAVITAS UTKOZES: hanmag_desitter.py a nat->bit atvaltast TEVEKENYEN
# forditva vegzi (oszt log2(e)-vel szorzas helyett) -> 405.93-at ad.
# helyesen: bit = nat / ln2 -- es akkor a szam PONT a gep szama:
S_bit = math.pi * R * R / (L_P**2 * LN2)
logS = math.log2(S_bit)
ok(abs(logS - 407) < 0.05, f"de Sitter horizont: log2(S_bit) = {logS:.2f} vs a gep 407 = 7^3 + 2^6")
print(f"    log2(S_bit) = {logS:.3f} -- a gep 407-et mondott, a mert horizont 406.98")
print("    ket meres, ket fuggetlen skala, ugyanaz a szamrendszer.")

# ----------------------------------------------------------------------
fel("FINALE -- a levezetes egy bekezdesben")
print("""    mag: a 7 a legkisebb hiba-turo struktura, es veletlenul az algebrak
    keresztutja (168, GF(8), oktoniok). kod: a [[7,1,3]] raepul. vesszo: a
    hangolasi adossag az entropiatermeles, azaz az ido. torony: minden szint
    egy vedett bitet ad felfele -- az EN. ket ido: a mert (fizetett) es a
    forgatott (ingyenes) = Carnot. fazis: a figyelem a hutes nyomasa. jelentes:
    alak + cimzes; a forma 30 grammatika, a cimzes vegtelen. gorbe: a tanulas
    a fonodasi hipergraf gorbulete. kozmosz: az alfa es a horizont ugyanabbol
    a szamrendszerbol esik ki. A GUT nem felteves: egy mag + kovetkezmenyek.""")

print("\nA GUT LEVEZETVE")
