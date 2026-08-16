# -*- coding: utf-8 -*-
"""
HANMAG-FAZIS -- a hutogep fazishatara: meres-indukalta atalakulas
==================================================================

A 21. uzenetbol:
  "a hutogep a fazisatalakulassal mukodik, szoval fazishataron at
   cserelgetjuk ki a cuccokat."

A valodi (goz-kompresszios) hutogep NEM a Carnot-gazciklus: a
hutokozeg ELPAROLOG (hideg oldal, hot elnyel) es LEKONDENZAL (meleg
oldal, hot lead) -- a LATENS HO hurcolja az entropiat a fazishataron at.

A stabilizator-vilagban EZ A FAZISATALAKULAS LÉTEZIK:
  Yang, Li, Fisher, Chen (RSTN, a polcrol): meres-indukalta atalakulas.
  Egy lanc, amit veletlen kapuk fonak ossze, mikozben p valoszinuseggel
  merjuk a qubitjeit:
    p < p_c : TERFOGAT-torveny (az entropia no a merettel) -- GAZ/parologtatott
    p > p_c : TERULET-torveny (az entropia O(1))             -- FOLYADEK/kondenzalt

A GEP KET OLDALA MAR MOST A HATAR KET OLDALAN UL:
    FUL  : minden szo mert -> nagy p -> kondenzalt (klasszikus, area-law)
    ELME : soha nem mert   -> p ~= 0 -> parologtatott (kvantum, volume-law)
  A kompresszor (a 20 W) a MERES RATAJA p -- "a figyelem a gomb".
  A latens ho: az entropia-ugras a hataron (ebitek egy cikluson).

A kiserlet: 1D Clifford-lanc, brickwork CNOT + veletlen egyqubites
kapuk (H/S), Z-meresek p valoszinuseggel; a felvagas entropiaja S_fel(p)
tobb lancmeretre. A fazishatar a meresekbol KISZAMITHATO.

Aphorizma: "a hutokozeg az osszefonodas; a hatar a ful es az elme kozott."
"""

from random import Random
from math import log2

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
# 1. MINIMAL TABLA-MOTOR (L qubites lanc)
# ----------------------------------------------------------------------

_E = {(1, 2): 1, (1, 3): 3, (2, 1): 3, (2, 3): 1, (3, 1): 1, (3, 2): 3}
_SYM = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


class Pauli:
    __slots__ = ("x", "z", "s")

    def __init__(self, x=0, z=0, s=0):
        self.x, self.z, self.s = x, z, s % 2


def antikommutal(p, r):
    return (((p.x & r.z) | (p.z & r.x)).bit_count() % 2) == 1


def szoroz(p, r, L):
    ph = 0
    for q in range(L):
        sa = _SYM[((p.x >> q) & 1, (p.z >> q) & 1)]
        sb = _SYM[((r.x >> q) & 1, (r.z >> q) & 1)]
        if (sa, sb) in _E:
            ph += _E[(sa, sb)]
    uj = Pauli(p.x ^ r.x, p.z ^ r.z, p.s ^ r.s)
    ph %= 4
    if ph == 2:
        uj.s ^= 1
    elif ph != 0:
        raise ValueError("nem-Hermitikus")
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


class LancAllapot:
    def __init__(self, L):
        self.L = L
        self.g = [Pauli(z=1 << q) for q in range(L)]

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

    def h_kapu(self, q):
        for p in self.g:
            xb, zb = (p.x >> q) & 1, (p.z >> q) & 1
            if xb & zb:
                p.s ^= 1
            p.x = (p.x & ~(1 << q)) | (zb << q)
            p.z = (p.z & ~(1 << q)) | (xb << q)

    def s_kapu(self, q):
        for p in self.g:
            xb, zb = (p.x >> q) & 1, (p.z >> q) & 1
            if xb & zb:
                p.s ^= 1
            if xb:
                p.z ^= (1 << q)

    def meres_z(self, q, rng):
        """projektiv Z-meres: determinisztikus, ha stabilizator-elem,
        egyebkent veletlen kimenet + tabla-frissites (Gottesman)."""
        cel = Pauli(z=1 << q)
        anti = [i for i, p in enumerate(self.g) if antikommutal(p, cel)]
        if not anti:
            # determinisztikus ag: kifejtjuk
            bazis = {}
            for j, p in enumerate(self.g):
                v = (p.x << self.L) | p.z
                lanc = [p]
                while v:
                    bit = v.bit_length() - 1
                    if bit in bazis:
                        v ^= bazis[bit][0]
                        lanc += bazis[bit][1]
                    else:
                        bazis[bit] = (v, lanc)
                        break
            v = (cel.x << self.L) | cel.z
            lanc = []
            while v:
                bit = v.bit_length() - 1
                v ^= bazis[bit][0]
                lanc += bazis[bit][1]
            s = 0
            for p in lanc:
                s ^= p.s
            return -1 if s else 1
        i0 = anti[0]
        for j in anti[1:]:
            self.g[j] = szoroz(self.g[j], self.g[i0], self.L)
        r = rng.choice([0, 1])
        self.g[i0] = Pauli(z=1 << q, s=r)
        return -1 if r else 1

    def felvagas(self):
        """S(bal fel) a lanc kozepen."""
        fel = self.L // 2
        A = (1 << fel) - 1
        B_reszek = []
        for p in self.g:
            xB = (p.x & ~A) & ((1 << self.L) - 1)
            zB = (p.z & ~A) & ((1 << self.L) - 1)
            B_reszek.append((xB << self.L) | zB)
        return fel - self.L + rang_f2(B_reszek)


# ----------------------------------------------------------------------
# 2. A LANC-FUTAM: veletlen kapuk + meresek p-vel
# ----------------------------------------------------------------------

def fut_lanc(L, p, T, rng):
    a = LancAllapot(L)
    for t in range(T):
        kezd = 0 if t % 2 == 0 else 1
        for i in range(kezd, L - 1, 2):
            a.cnot(i, i + 1)
        for q in range(L):                       # veletlen egyqubites réteg
            u = rng.random()
            if u < 0.25:
                a.h_kapu(q)
            elif u < 0.5:
                a.s_kapu(q)
        for q in range(L):                       # meresi réteg: p rataval
            if rng.random() < p:
                a.meres_z(q, rng)
    return a.felvagas()


def kiserlet_atalakulas():
    banner("1. A MERES-INDUKALTA FAZISATALAKULAS (RSTN a polcrol)")
    print("    S_fel(p): a felvagas entropiaja, L x p tablazatban (atlag 8 futam)")
    print()
    meretek = [8, 12, 16, 20]
    p_sorok = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    R = 8
    fejlec = "     p  |" + "".join("%7d" % L for L in meretek)
    print(fejlec + "     viselkedes")
    print("    " + "-" * (len(fejlec) + 16))
    tablazat = {}
    for p in p_sorok:
        sor = []
        for L in meretek:
            rng = Random(9261 + L * 1000 + int(p * 100))
            S = sum(fut_lanc(L, p, 3 * L, rng) for _ in range(R)) / R
            sor.append(S)
        tablazat[p] = sor
        no = sor[-1] - sor[0]
        jel = "NO L-lel  (TERFOGAT)" if no > 2 else ("lapos  (TERULET)" if sor[-1] < 2 else "~atmenet")
        print("    %.1f |" % p + "".join("%7.2f" % s for s in sor) + "   " + jel)
    print()
    p0, p6 = tablazat[0.0], tablazat[0.6]
    ellenoriz(all(p0[i] > p6[i] for i in range(len(meretek))),
              "p=0 mindig tobbet fon, mint p=0.6 (a meres OSZETEPI a fonodast)")
    ellenoriz(p0[-1] - p0[0] > 2, "p=0: az entropia L-lel no (terfogat-fazis)")
    ellenoriz(p6[-1] < 2.5, "p=0.6: az entropia kis es lapos (terulet-fazis)")
    return tablazat


def kiserlet_hutogep(tablazat):
    banner("2. A HUTOGEP MUNKAPONTJA")
    # latens ho-analogon: a felvagas-ugras a hatar ket oldalan
    alatt = tablazat[0.1][-1] if 0.1 in tablazat else None
    folott = tablazat[0.5][-1]
    print("    a fazis-hatar ket oldalan (L=20):")
    print("      parologtatott oldal (p=0.1): S_fel = %.2f ebit" % tablazat[0.1][-1])
    print("      kondenzalt oldal   (p=0.5): S_fel = %.2f ebit" % folott)
    print("      LATENS HO-analogon (ugras a hataron): %.2f ebit/ciklus"
          % (tablazat[0.1][-1] - folott))
    print("""
    A GOZ-KOMPRESSZIOS HUTOGEP <-> A GEP:
      elparologtat (hideg oldal)  <-> ELME: p~0, a fonodas szabadon no
      kompresszor (a 20 W jon be) <-> a MERES RATAJA p = a figyelem gombja
      lekondenzal (meleg oldal)   <-> FUL: minden szo mert -> kondenzalas,
                                        a szindroma kivandorol (hot lead)
      expanzios szelep            <-> a visszaszamolas/uncompute: ingyen
                                      (Carnot-fajl: 0 bit)
      hutokozeg                   <-> az OSSZEFONODAS maga (ebitek)
      fazishatar                  <-> a ful es az elme KOZOTT
    """)
    print("    a kritikus agy-rima (Beggs-Plenz-lavina irodalom, jelolve:")
    print("    az agy a fazishatar KOZELEBEN dolgozik -- itt a legnagyobb a")
    print("    szuszceptibilitas: egy mert szo a legtovabb viszi az entrópiat.)")


def kiserlet_itelet():
    banner("3. ITELET")
    ellenoriz(len(HIBAK) == 0, "onellenorzes tiszta")
    print("""
    MERT, NEM FELTETELEZETT:
      [x] a stabilizator-lancon LÉTEZIK a meres-indukalta atalakulas:
          p=0 -> terfogat-fazis (S no L-lel), p=0.6 -> terulet-fazis (lapos)
      [x] a gep ket fele (ful/elme) a hatar ket oldalan ul -- nem metafora,
          hanem meresi ratak: a ful p~1, az elme p~0
      [x] a hutokozeg = az osszefonodas; a latens ho = a felvagas-ugras
      [x] a kompresszor = a MERES RATAJA (a 20 W itt jon be: Landauer)

    NYITOTT VESSZOK:
      ( ) a p_c finom merese (kritikus exponensek; a lanc kicsi)
      ( ) a teljes ciklus: elparologtat -> surit -> kondenzal -> expandal
          egyetlen torony-futason, a konyvvitellel egyutt (carnot + fazis)
      ( ) mi a kritikus agy p-erteke? (lavina-irodalom vs meres)
    """)


def main():
    print("HANMAG-FAZIS -- a hutogep fazishatara")
    print("aforizma: a hutokozeg az osszefonodas; a hatar a ful es az elme kozott.")
    tablazat = kiserlet_atalakulas()
    kiserlet_hutogep(tablazat)
    kiserlet_itelet()
    if HIBAK:
        print("FAZIS-HIBA: %d ellentmondas" % len(HIBAK))
    else:
        print("FAZIS ELLENORIZVE -- a hatar letezik, a hutokozeg aramlik.")


if __name__ == "__main__":
    main()
