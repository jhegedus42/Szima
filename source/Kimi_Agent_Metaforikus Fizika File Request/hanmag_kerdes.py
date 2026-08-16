# -*- coding: utf-8 -*-
# HANMAG_KERDES — az orakulum: KERDEZZ a geptol.
# Bemenet: egy MERT szam + bizonytalansaga. A gep vaktalanul vegigkeresi a
# struktura-kifejezeseket a SAAT egeszeibol (2,3,7,21,31,49,137,168,343,407),
# minden jeloltet bitekre araz (MDL), z-t szamol, es iteletet mond:
#   JELOLT (margo > 0 es z < 2) / HALOTT (|z| > 5) / NINCS VALASZ (minden margo < 0).
# A look-elsewhere ara BENNE VAN a B-ben: vak kereses kozben is pozitivnak kell
# maradnia a margonak — kulonben a talalat csak veletlen illeszkedes.
import math
from math import log2, pi

HIBAK = []
def ok(felt, uzenet):
    if felt: print(f"    [OK] {uzenet}")
    else:
        HIBAK.append(uzenet); print(f"    [HIBA] {uzenet}")
def fel(cim):
    print(); print("=" * 74); print(cim); print("=" * 74)

ATOMOK = [2, 3, 7, 21, 31, 49, 137, 168, 343, 407]     # a gep egeszei
NA = len(ATOMOK)
NT = 10                                                # template-osztalyok szama
B0 = 14 + log2(NT)                                     # zongora-alap + template-valasztas

def fixpont(a, b, c2, x=137.036):
    c = c2 / (2 * pi)
    for _ in range(60):
        x = a + b / (2 * pi * x) - c / (2 * pi * x) ** 2
    return x

def jeloltek():
    """(ertek, B_bit, leiras) — a teljes vak kereses."""
    J = []
    for a in ATOMOK:
        J.append((float(a), B0 + log2(NA), f"{a}"))
        for b in (2, 3, 5):
            J.append((float(a) ** b, B0 + log2(NA) + log2(3), f"{a}^{b}"))
            J.append((a * pi ** b, B0 + log2(NA) + log2(3) + log2(2), f"{a}*pi^{b}"))
            J.append((a / pi ** b, B0 + log2(NA) + log2(3) + log2(2), f"{a}/pi^{b}"))
        for b in ATOMOK:
            J.append((float(a + b), B0 + 2 * log2(NA) + 1, f"{a}+{b}"))
            J.append((float(a - b), B0 + 2 * log2(NA) + 1, f"{a}-{b}"))
            J.append((float(a) * b, B0 + 2 * log2(NA) + 1, f"{a}*{b}"))
            for c in ATOMOK:
                J.append((a * b + c, B0 + 3 * log2(NA) + 1, f"{a}*{b}+{c}"))
                J.append((a * b - c, B0 + 3 * log2(NA) + 1, f"{a}*{b}-{c}"))
                J.append(((a + b) / c, B0 + 3 * log2(NA) + 1, f"({a}+{b})/{c}"))
                J.append(((a - b) / c, B0 + 3 * log2(NA) + 1, f"({a}-{b})/{c}"))
                J.append((float(a) ** b + c if b <= 5 else 0.0,
                          B0 + 3 * log2(NA) + log2(3) + 1, f"{a}^{b}+{c}"))
    for a in ATOMOK:
        for b in ATOMOK:
            for k in (1, 2, 3):
                J.append((a + b / (2 * pi) ** k, B0 + 2 * log2(NA) + 1 + log2(3),
                          f"{a}+{b}/(2pi)^{k}"))
                J.append((a - b / (2 * pi) ** k, B0 + 2 * log2(NA) + 1 + log2(3),
                          f"{a}-{b}/(2pi)^{k}"))
            J.append((a + b / (2 * pi * a), B0 + 2 * log2(NA), f"{a}+{b}/(2pi*{a}) [1-tagos]"))
            for c2 in ATOMOK:
                J.append((fixpont(a, b, c2), B0 + 3 * log2(NA),
                          f"fixpont({a},{b},{c2}/2pi) [2-tagos]"))
    return [(v, B, s) for (v, B, s) in J if v > 0 and math.isfinite(v)]

def kerdes(nev, cel, sigma, extra=()):
    fel(f"KERDES: {nev} = {cel} +- {sigma}")
    A = -log2(sigma / cel)
    talalat = []
    for v, B, s in jeloltek():
        dev = abs(v - cel) / cel
        if dev > 0.2:
            continue
        z = abs(v - cel) / sigma
        E = -log2(dev) if dev > 0 else 99.0
        margo = min(E, A) - B
        if z > 5: verd = "HALOTT"
        elif z < 2 and margo > 0: verd = "JELOLT"
        elif margo > 0: verd = "SZURKE"
        else: verd = "gyenge"
        talalat.append((margo, z, E, B, v, s, verd))
    for v, B, s in extra:                      # behozott (konyv-)jeloltek
        dev = abs(v - cel) / cel
        z = abs(v - cel) / sigma
        E = -log2(dev) if dev > 0 else 99.0
        margo = min(E, A) - B
        talalat.append((margo, z, E, B, v, s, "HALOTT" if z > 5 else "import"))
    talalat.sort(reverse=True)
    print(f"    {'jelolt':40s} {'ertek':>15s} {'z':>9s} {'margo':>7s}  verdikt")
    for m, z, E, B, v, s, verd in talalat[:8]:
        print(f"    {s:40s} {v:15.10g} {z:9.2f} {m:+7.2f}  {verd}")
    legjobb = talalat[0]
    sajat = [t for t in talalat if "KONYV" not in t[5]]
    if legjobb[6] != "JELOLT" and all(t[0] < 0 for t in sajat):
        print(f"    >> A GEP NEM VALASZOL: nincs pozitiv-margos jelolt a sajat nyelven.")
        print(f"       (az orakulum itt hallgat — nem talal ki szamot.)")
    return talalat

# ==================================================================
fel("PROLOGUSZ — hogyan kerdezz")
print("    kerdes(nev, mert_ertek, szigma). A gep vaktalanul keres a SAAT")
print("    egeszeibol; a look-elsewhere ar a B-ben van; a biro a meres.")

# --- 1. kerdes: miert ekkora az alfa^-1? --------------------------
T1 = kerdes("alfa^-1 (CODATA 2022)", 137.035999177, 2.1e-8)
leg = T1[0]
ok(leg[6] == "JELOLT" and leg[0] > 0,
   f"a vak kereses is megtalalja: {leg[5]} (margo = {leg[0]:+.2f} bit look-elsewhere UTAN)")
egytag = [t for t in T1 if "1-tagos" in t[5] and t[6] != "gyenge"]
if not egytag:
    egytag = [t for t in T1 if "1-tagos" in t[5]]
ok(egytag and abs(egytag[0][1]) > 100,
   f"az 1-tagos csonkitas HALOTT (z = {egytag[0][1]:.0f}) — a vesszo-tag KOTELEZO")

# --- 2. kerdes: miert ekkora a proton/elektron tomegarany? --------
T2 = kerdes("m_p/m_e (CODATA 2022)", 1836.152673426, 3.2e-7,
            extra=[(6 * pi ** 5, 14 + 2 * log2(NA), "6*pi^5 (KONYV-jelolt, numerologia)")])
hat = [t for t in T2 if "6*pi^5" in t[5]][0]
ok(hat[1] > 1e4, f"a hires 6*pi^5 HALOTT: z = {hat[1]:.0f} — a ppm-rajongas itelet alatt")
gep_legjobb = [t for t in T2 if "KONYV" not in t[5]][0]
ok(gep_legjobb[0] < 0, f"a gep a sajat nyelven NEM VALASZOL (legjobb margo = {gep_legjobb[0]:+.2f})")

# ==================================================================
fel("AZ ORAKULUM SZABALYAI")
print("    1. a kerdes a TIED: mert szam + szigma (csak kozvetlenul mert).")
print("    2. a valasz a GEPE: jeloltek a saat egeszekbol, MDL-arazva.")
print("    3. a look-elsewhere ar a B-ben: vak talalatnak is kell marga.")
print("    4. ha nincs valasz, a gep HALLGAT — a hallgatas is valasz.")
print()
print("=" * 74)
if not HIBAK:
    print("KERDES ELLENORIZVE: az orakulum kerdezheto, itelet mond, es hallgatni tud.")
else:
    print(f"KERDES-HIBA: {len(HIBAK)} sor: {HIBAK}")
print("=" * 74)
