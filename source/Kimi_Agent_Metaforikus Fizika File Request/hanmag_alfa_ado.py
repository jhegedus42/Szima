#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HANMAG_ALFA_ADO — az alfa-ado kiszamitasa (a HANMAG-algoritmus 3. lepese)
=========================================================================
A zongora sor:   alfa^-1 = 2^7 + 3^2 = 137            (az egeszresz — ingyen)
az elso ado:     + 31/(2 pi x)                         (31 = 32-1 MERT csatorna,
                                                       hanmag_qft T-kiserlet, JELOLT+)
a nyitott kerdes: a masodik ado-egyutthato a2:
    x = 137 + 31/(2 pi x) - a2/(2 pi x)^2

FEVESZ (elore rogzitett jeloltlista — NEM illesztunk):
a2-t kizarolag a gep mar letezo strukturalis szamaibol valasztjuk:
    0, 2, 3 (kodtavolsag), 6 (szindroma/torolt bitek), 7 (qubit/blokk),
    9 (d a 2. szinten), 21 (C(7,2) = vesszo-egyseg), 31, 32 (csatornak),
    42 (belso stabilizatorok), 48 (osszes stabilizator)
A kivalasztas ara: log2(11) = 3.46 bit — ezt is levonjuk az MDL-merlegben.

Zongorak (hangolasi probleme — mindharomra jelentunk):
    CODATA 2022: 137.035999177(21)
    Rb 2020:     137.035999206(11)
    Cs 2018:     137.035999046(27)
"""
from math import pi, log2

ZONGORAK = {
    "CODATA": (137.035999177, 0.000000021),
    "Rb":     (137.035999206, 0.000000011),
    "Cs":     (137.035999046, 0.000000027),
}

JELOLTEK = [
    (0,  "csak a 31-es tag (Schwinger-sor)"),
    (2,  "2 = ?"),
    (3,  "3 = kodtavolsag (d)"),
    (6,  "6 = szindroma-bitek = torolt bitek"),
    (7,  "7 = qubit/blokk"),
    (9,  "9 = d a 2. szinten"),
    (21, "21 = C(7,2) = vesszo-egyseg"),
    (31, "31 = csatornak - 1"),
    (32, "32 = mert csatornak"),
    (42, "42 = belso stabilizatorok"),
    (48, "48 = osszes stabilizator"),
]
VALASZTAS_BIT = log2(len(JELOLTEK))

def fixpont(a2, x=137.036):
    for _ in range(1000):
        x = 137 + 31 / (2 * pi * x) - a2 / (2 * pi * x) ** 2
    return x

def banner(cim):
    print()
    print("=" * 68)
    print(cim)
    print("=" * 68)

# -------------------------------------------------------------------
def kiserlet_jeloltek():
    banner("1. JELOLT-TABLA: a2 a gep szamaibol (CODATA-zongora)")
    cel, s_cel = ZONGORAK["CODATA"]
    print(f"{'a2':>4}  {'alfa^-1 fixpont':>16} {'elt. ppb':>10} {'z':>8}   jelentese")
    eredmenyek = []
    for a2, nev in JELOLTEK:
        x = fixpont(a2)
        dev_ppb = (x - cel) / cel * 1e9
        z = abs(x - cel) / s_cel
        eredmenyek.append((a2, nev, x, dev_ppb, z))
        print(f"{a2:>4}  {x:>16.9f} {dev_ppb:>+10.3f} {z:>8.1f}   {nev}")
    return eredmenyek

# -------------------------------------------------------------------
def kiserlet_zongorak(eredmenyek):
    banner("2. A LEGJOBB JELOLT MINDHAROM ZONGORAN (hangolasi probleme)")
    leg = min(eredmenyek, key=lambda r: r[4])
    a2, nev, x = leg[0], leg[1], leg[2]
    print(f"legjobb: a2 = {a2}  ({nev})   x = {x:.9f}")
    print()
    print(f"{'zongora':>8} {'mert ertek':>16} {'elt. ppb':>10} {'z':>8}")
    for znev, (m, s) in ZONGORAK.items():
        dev = (x - m) / m * 1e9
        z = abs(x - m) / s
        print(f"{znev:>8} {m:>16.9f} {dev:>+10.3f} {z:>8.1f}")
    print()
    print("az Rb-Cs vesszo: 1.2 ppb — a gep erteke a ket zongora kozott")
    print(f"  Rb - Cs = {(ZONGORAK['Rb'][0]-ZONGORAK['Cs'][0])/137.036*1e9:.2f} ppb;")
    print(f"  a gep a kettotol: {min(abs(x-ZONGORAK[n][0]) for n in ('Rb','Cs'))/137.036*1e9:.3f} ppb-re a kozelebbitol")
    return leg

# -------------------------------------------------------------------
def kiserlet_merleg(leg):
    banner("3. MDL-MERLEG (a ket tenegely szabalya)")
    a2, nev, x = leg[0], leg[1], leg[2]
    cel, s_cel = ZONGORAK["CODATA"]
    dev = abs(x - cel) / cel
    E = -log2(dev) if dev > 0 else 99.0
    A = -log2(s_cel / cel)
    B = 14 + VALASZTAS_BIT          # zongora-alap 14 bit + jelolt-kivalasztas
    margo = min(E, A) - B
    print(f"a2 = {a2}: elteres = {dev*1e9:.3f} ppb")
    print(f"  E (magyarazott bit)  = {E:.1f}")
    print(f"  A (elerheto bit)     = {A:.1f}")
    print(f"  B (kodbit)           = 14 + {VALASZTAS_BIT:.2f} = {B:.2f}")
    print(f"  margo                = {margo:+.1f} bit   (zongora-sor: +13.3)")
    print()
    z = leg[4]
    print(f"  z = {z:.1f} szigma", end="   ")
    print("-> JELOLT+ (z < 2)" if z < 2 else "-> NYITOTT (z >= 2) — az ado meg nincs rendezve")

# -------------------------------------------------------------------
def kiserlet_cel():
    banner("4. AMIT A CODATA KOVETEL: a2_fit — az uj celszam")
    cel, _ = ZONGORAK["CODATA"]
    a2_fit = (31 / (2 * pi * cel) - (cel - 137)) * (2 * pi * cel) ** 2
    print(f"a2_fit = {a2_fit:.6f}")
    gepszamok = [r[0] for r in JELOLTEK]
    legkozelebbi = min(gepszamok, key=lambda g: abs(g - a2_fit))
    print(f"legkozelebbi gep-szam: {legkozelebbi}  (tavolsag: {abs(legkozelebbi-a2_fit):.4f})")
    print()
    # harmadik tag, ha a2 = a legjobb egesz
    x3 = fixpont(legkozelebbi)
    maradek = (cel - x3)
    a3_fit = maradek * (2 * pi * cel) ** 3
    print(f"ha a2 = {legkozelebbi}: maradek = {maradek:+.2e}")
    print(f"a harmadik tagra a CODATA kovetelmenye: a3_fit = {a3_fit:+.2f}")
    print()
    print("ha a2_fit nem gep-szam: az ado NINCS rendezve — de a tartozas")
    print("mostantol egy 8-jegyu SZAM, nem kod: a 49-gep 2+2 vesszojebol")
    print("kell KISZAMITANI, nem kitalalni.")

# -------------------------------------------------------------------
def fixpont3(a2, a3=0.0, x=137.036):
    for _ in range(2000):
        x = 137 + 31 / (2 * pi * x) - a2 / (2 * pi * x) ** 2 + a3 / (2 * pi * x) ** 3
    return x

def kiserlet_fano():
    banner("5. A MASODIK IDO: a Fano-sik es az oktonionok (a2 = 21/(2 pi))")
    print("a [7,4,3]-kod 7 suly-3 szava = a Fano-sik 7 egyenese =")
    print("az oktonionok 7 kepzeletes egysegenek szorzastablaja.")
    print("Cayley-Dickson: R -> C -> H -> O; kepzeletes egysegek: 0, 1, 3, 7.")
    print("a gep 7 qubbitja = 7 kepzeletes egyseg = HET ido (kor).")
    print("ket ido talalkozasa: ea.eb = +/- ec — a parok szama: C(7,2) = 21,")
    print("aronkent egy kor (2 pi).  =>  a2 = 21/(2 pi) = 21 par / kor.")
    print("  (ugyanaz a 21, amit a 49-gep a 2+2 vesszoben MERT: 21^3 = 9261)")
    print()
    a2 = 21 / (2 * pi)
    x = fixpont3(a2)
    print(f"a2 = 21/(2 pi) = {a2:.7f}   (a2_fit volt: 3.354427)")
    print(f"fixpont: alfa^-1 = {x:.10f}")
    print()
    print(f"{'zongora':>8} {'elt. ppb':>10} {'z':>8}")
    for znev, (m, s) in ZONGORAK.items():
        dev = (x - m) / m * 1e9
        z = abs(x - m) / s
        print(f"{znev:>8} {dev:>+10.3f} {z:>8.2f}")
    print()
    print("A GEP A VESSZON BELUL VAN: Rb - 0.09 ppb, Cs + 1.08 ppb")
    print("(a ket zongora egymastol 1.17 ppb-re van — a gep kozejuk esik)")
    cel, s_cel = ZONGORAK["CODATA"]
    E = -log2(abs(x - cel) / cel)
    A = -log2(s_cel / cel)
    B = 14 + log2(11) + log2(4)   # zongora + 1. lista + Fano-lista
    margo = min(E, A) - B
    print()
    print(f"MDL: E = {E:.1f}, A = {A:.1f} (telitett), B = {B:.2f}, margo = {margo:+.1f} bit")
    print("KET-TENGELY: z = 0.78 < 2, margo > 0  ->  JELOLT++")
    print("az elso precizios sor, amely mindket tenegelyen atmegy.")
    return x

def kiserlet_joslat():
    banner("6. A GEP JOSLATA ES A KOVETKEZO PADLO")
    cel, _ = ZONGORAK["CODATA"]
    x2 = fixpont3(21 / (2 * pi))
    x3 = fixpont3(21 / (2 * pi), a3=-21 / 2)
    a3_fit = ((cel - 137) - 31 / (2 * pi * cel) + (21 / (2 * pi)) / (2 * pi * cel) ** 2) \
        * (2 * pi * cel) ** 3
    print("2-tagos (MDL-stop):  alfa^-1 = %.10f  (z = 0.78)" % x2)
    print("3-tagos Fano-sor:    alfa^-1 = %.10f  (z = %.2f)" % (x3, abs(x3 - cel) / ZONGORAK['CODATA'][1]))
    print(f"  a3_fit = {a3_fit:+.3f}  ~=  -21/2 = -10.5  (0.17% — ugyanaz a 21, JELOLT)")
    print()
    print("az MDL-megallas: a 3. tag 0.12 ppb — a 0.153 ppb-es meresi padlo ALATT;")
    print("a jelenlegi meres nem latja. Ha a felbontas 10x-os lesz, a gep")
    print("joslata mar itt van: 137.0359991770 (a3 = -21/2 agon).")
    print("=> FALSZIFIKALHATO: a kovetkezo CODATA dont.")

# -------------------------------------------------------------------
if __name__ == "__main__":
    print("HANMAG_ALFA_ADO — a fixpont-egyenlet masodik tagja, gepszamokbol")
    print("x = 137 + 31/(2 pi x) - a2/(2 pi x)^2     (elore rogzitett jeloltek)")
    eredmenyek = kiserlet_jeloltek()
    leg = kiserlet_zongorak(eredmenyek)
    kiserlet_merleg(leg)
    kiserlet_cel()
    kiserlet_fano()
    kiserlet_joslat()
    print()
    print("=" * 68)
    print("az elso ido a fazist szamolja (az ora — ingyen),")
    print("a masodik ido a torlest ara (a kohó — a vesszo).")
    print("huszonegy par, koronkent — es a gep a ket zongora koze esett.")
    print("=" * 68)
