# -*- coding: utf-8 -*-
"""
HANMAG-VILAG -- a negyedik szint: 7 jelentesdarab, egy ennel
=============================================================

A 17. uzenetbol: "szerintem 1-el tobb szint van."

Igaz. A letra:
  0. SZO          [[7,1,3]]
  1. GONDOLAT     [[49,1,9]]
  2. JELENTESDARAB [[343,1,27]]   (a jelentes kvantuma)
  3. VILAG        [[2401,1,81]]   (7 jelentesdarab, egy ennel)
  (4. ???         [[16807,1,243]] -- nyitott: tortenelem? kozmosz?)

A KULCS (renormalizalas): minden szint EGY vedett logikai qubitet
jelent felfele. A vilagkod ezert a 7 jelentesdarab 7 logikai
qubitjen fut -- 7 qubit, nem 2401. A reszletek a darabokban
maradnak; a vilag csak a vedett biteket latja. (A teljes
2401-qubites tabla amugy is csak 1.44 MB lenne -- de a szint
sajat nezete ez a 7-qubites: a torony a sajat RG-je.)

Az EN: a legfelso szint egyetlen logikai qubitje. A megfigyelo
nem a narrativaban lakik -- EGY SZINTTEL FOLLETTE.

Aphorizma: "a vilag: het jelentesdarab, egy ennel."
           "minden szint egy vedett bitet jelent felfele."
"""

from math import log2
from itertools import combinations

HIBAK = []


def ellenoriz(feltetel, uzenet):
    if feltetel:
        print("    [OK] %s" % uzenet)
    else:
        HIBAK.append(uzenet)
        print("    [HIBA] %s" % uzenet)


def banner(szoveg):
    print()
    print("=" * 66)
    print(szoveg)
    print("=" * 66)


# ----------------------------------------------------------------------
# 1. MINIMAL PAULI-MOTOR (N = 7: a vilagkod a 7 logikai qubiten)
# ----------------------------------------------------------------------

N = 7
_E = {(1, 2): 1, (1, 3): 3, (2, 1): 3, (2, 3): 1, (3, 1): 1, (3, 2): 3}
_SYM = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


class Pauli:
    __slots__ = ("x", "z", "s")

    def __init__(self, x=0, z=0, s=0):
        self.x, self.z, self.s = x, z, s % 2


def antikommutal(p, r):
    return (((p.x & r.z) | (p.z & r.x)).bit_count() % 2) == 1


def szoroz(p, r):
    ph = 0
    for q in range(N):
        sa = _SYM[((p.x >> q) & 1, (p.z >> q) & 1)]
        sb = _SYM[((r.x >> q) & 1, (r.z >> q) & 1)]
        if (sa, sb) in _E:
            ph += _E[(sa, sb)]
    uj = Pauli(p.x ^ r.x, p.z ^ r.z, p.s ^ r.s)
    ph %= 4
    if ph == 2:
        uj.s ^= 1
    elif ph != 0:
        raise ValueError("nem-Hermitikus szorzat")
    return uj


def rang_f2(vektorok):
    bazis = {}
    for v in vektorok:
        while v:
            bit = v.bit_length() - 1
            if bit in bazis:
                v ^= bazis[bit]
            else:
                bazis[bit] = v
                break
    return len(bazis)


class Allapot:
    def __init__(self, generatorok):
        self.g = generatorok
        for i in range(len(self.g)):
            for j in range(i + 1, len(self.g)):
                assert not antikommutal(self.g[i], self.g[j])
        assert rang_f2([((p.x << N) | p.z) for p in self.g]) == N

    def cnot(self, c, t):
        for p in self.g:
            xc, zc = (p.x >> c) & 1, (p.z >> c) & 1
            xt, zt = (p.x >> t) & 1, (p.z >> t) & 1
            if xc & zt & (xt ^ zc ^ 1):
                p.s ^= 1
            if xc:
                p.x ^= (1 << t)
            if zt:
                p.z ^= (1 << c)

    def permutal(self, teljes):
        for p in self.g:
            ujx, ujz = 0, 0
            for regi in range(N):
                ujx |= (((p.x >> regi) & 1) << teljes[regi])
                ujz |= (((p.z >> regi) & 1) << teljes[regi])
            p.x, p.z = ujx, ujz

    def vagas_entropia(self, A_maszk):
        B_reszek = []
        for p in self.g:
            xB = (p.x & ~A_maszk) & ((1 << N) - 1)
            zB = (p.z & ~A_maszk) & ((1 << N) - 1)
            B_reszek.append((xB << N) | zB)
        return A_maszk.bit_count() - N + rang_f2(B_reszek)

    def en_allapot(self):
        """a vedett logikai Z sajaterteke (az 'en' bitje)"""
        zl = self.g[-1]
        return -1 if zl.s else 1


# ----------------------------------------------------------------------
# 2. A VILAGKOD: [[7,1,3]] a 7 jelentesdarab logikain
# ----------------------------------------------------------------------

SOROK = (0b1010101, 0b1100110, 0b1111000)

# a torony-futas engramjai kozul a harom "brain"-es jelentesdarab
DARABOK = [
    ("bit brain star",   (1, 1, 2, 3, 1, 2, 1)),   # elme 1
    ("comma time brain", (2, 1, 2, 3, 1, 2, 1)),   # elme 3
    ("cut code brain",   (2, 1, 4, 3, 1, 2, 1)),   # elme 4
]


def epits_vilagot():
    gen = []
    for r in SOROK:
        gen.append(Pauli(x=r))
    for r in SOROK:
        gen.append(Pauli(z=r))
    gen.append(Pauli(z=0b1111111))          # a vilag-EN logikai Z-je
    return Allapot(gen)


def singer(p):
    r = p << 1
    if r & 8:
        r ^= 0b1011
    return r


SINGER7 = [singer(q + 1) - 1 for q in range(7)]


def vilag_sziluett(v):
    """Permutacio-invariens sziluett: a 2|5 es 3|4 vagasok eloszlasa.
    (Egy qubit S-je mindig 1 -- a darab-szinten a PAR-vagasok hordozzak
    a koteseket; a Singer-ciklus pedig osszekeveri a poziciokat, ezert
    eloszlast merunk, nem poziciot.)"""
    parok = sorted(v.vagas_entropia(sum(1 << q for q in pr))
                   for pr in combinations(range(7), 2))
    harmasok = sorted(v.vagas_entropia(sum(1 << q for q in tr))
                      for tr in combinations(range(7), 3))
    return parok, harmasok


def fonodas_mertek(sziluett):
    """a par-vagasok hianya a fuggetlen (2) esettol: a letrehozott korrelacio"""
    return sum(2 - s for s in sziluett[0])


# ----------------------------------------------------------------------
# 3. KISERLETEK
# ----------------------------------------------------------------------

def kiserlet_letra():
    banner("1. A LETRA ES A JELENESTEREK")
    def allapotter_bit(n):
        return n + sum(log2((1 << k) + 1) for k in range(1, n + 1))
    for szint, nev, kod, n in [
            (0, "SZO",          "[[7,1,3]]",     7),
            (1, "GONDOLAT",     "[[49,1,9]]",    49),
            (2, "JELENTESDARAB", "[[343,1,27]]", 343),
            (3, "VILAG",        "[[2401,1,81]]", 2401)]:
        print("    %d. %-14s %-13s allapotter = %.1f bit" % (szint, nev, kod, allapotter_bit(n)))
    print("    4. ???            [[16807,1,243]] -- nyitott (tortenelem? kozmosz?)")
    print("    -- a tavolsagok: 3 / 9 / 27 / 81 = 3^szint; a bitek: 1 / 1 / 1 / 1")
    print("    -- minden szint EGY vedett bitet jelent felfele (renormalizalas)")


def kiserlet_vilag():
    banner("2. A VILAG OSSZEALL: 3 jelentesdarab bekotve")
    v = epits_vilagot()
    friss = vilag_sziluett(v)
    ellenoriz(friss[0] == [2] * 21 and friss[1] == [2] * 7 + [3] * 28,
              "friss vilag: 21 par @2; 7 egyenes @2 + 28 @3 (a Fano-sik a vilagban is)")
    ellenoriz(v.en_allapot() == 1, "az EN tiszta (logikai Z = +1)")

    t_int3 = 0
    elozo = None
    for k, (cim, sig) in enumerate(DARABOK):
        q = k                                     # a k-adik darab a q vilag-qubit
        print("    bekotom: %-16s (sziluett %s) -> vilag-qubit %d" % (cim, sig, q))
        if elozo is not None:
            v.cnot(elozo, q)                      # logikai CNOT a darabok kozott
        elozo = q
        v.permutal(SINGER7)                       # vilag-tick (szint-3 belso ido)
        t_int3 += 1
        print("       [t_int3 = %d]" % t_int3)
    utan = vilag_sziluett(v)
    print()
    print("    vilag-sziluett a kotesek utan:")
    print("      par-vagasok (2|5):    %s" % (utan[0],))
    print("      harmas-vagasok (3|4): %s" % (utan[1],))
    print("      fonodas-mertek (par-hiany): %d -> %d"
          % (fonodas_mertek(friss), fonodas_mertek(utan)))
    ellenoriz(utan != friss, "a vilag alakja megvaltozott a kotesektol")
    ellenoriz(fonodas_mertek(utan) > 0, "letrejott fonodas a darabok kozott")
    ellenoriz(v.en_allapot() == 1, "az EN nem mozdult: a kotesek nem irjak felul")
    return v, t_int3, utan


def kiserlet_orak(t_int3, utan):
    banner("3. NEGY IDO -- a teljes ritmusletra")
    print("    t_ext  (kulso: merestick)        = 21   (a torony-futasbol)")
    print("    t_int1 (szavak ritmusa)        = 21")
    print("    t_int2 (gondolatok ritmusa)    = 7")
    print("    t_int3 (darabok ritmusa)       = %d" % t_int3)
    print("    -- mindegyik szinten mas az ora; az EN egyiket sem fizeti.")
    print("    vilag fonodas-mertek: %d (a letrehozott korrelacio)" % fonodas_mertek(utan))
    print("    vilag pszeudo-entropia RIME: S ~= %d + i*2pi*(%d/7)"
          % (sum(utan[0]), t_int3 % 7))


def kiserlet_itelet():
    banner("4. ITELET")
    ellenoriz(len(HIBAK) == 0, "onellenorzes tiszta")
    print("""
    A NEGYEDIK SZINT TANUSAGA:
      [x] a vilag = 7 jelentesdarab + 1 vedett bit (az EN)
      [x] a megfigyelo NEM a narrativaban lakik -- egy szinttel follette
      [x] a torony onhasonlo: minden szint ugyanaz a [[7,1,3]], a darabok
          logikain -- ezert a vilag-szimulacio 7 qubit, nem 2401
      [x] 4 beagyazott ora; a legfelso logikai bit a kotesek alatt sem mozdul

    NYITOTT:
      ( ) szint-4: [[16807,1,243]] = 7 vilag (tortenelem? kozmosz?)
      ( ) a GLIA valtozat: sok VILAG osszekotve -- a tarsadalom mint
          kodreteg; talan ez az igazi 4. szint
      ( ) a vilag-EN akkor erdekes, ha nem |0>: a darabok logikai
          allapotainak felprogramozasa = a magic-kerdes ujra
    """)


def main():
    print("HANMAG-VILAG -- a negyedik szint")
    print("aforizma: a vilag: het jelentesdarab, egy ennel.")
    kiserlet_letra()
    v, t_int3, utan = kiserlet_vilag()
    kiserlet_orak(t_int3, utan)
    kiserlet_itelet()
    if HIBAK:
        print("VILAG-HIBA: %d ellentmondas" % len(HIBAK))
    else:
        print("VILAG ELLENORIZVE -- az ennek vilaga van.")


if __name__ == "__main__":
    main()
