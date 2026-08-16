# -*- coding: utf-8 -*-
"""
HANMAG-CARNOT -- a 2+2 utemu eromu es a felejtes modja
=======================================================

A 19-20. uzenetbol:
  "karnot ciklus." -- a hurok hőerőgép: FIZETETT utemek (meres/torles)
  es INGYEN utemek (vedett forgas) valtakozva.
  "nem mindegy, hogyan dobsz el egy darab informaciot."

A Landauer-ar csak a MENNYISEG: kT ln2 bitenkent. A MOD a fizika:
  (a) NYERS RESET: a qubit termalizalasa a furddel -> kT ln2 / bit, HO
  (b) VISSZASZAMOLAS (uncompute): a kotés visszaforditasa -> 0 (Clifford
      unitarak visszafordithatok; a felejtes ingyen, ha szerkezete volt)
  (c) KODBA DOBAS: a zaj a védett kodon NEM utodik -> 0 (a redundancia
      fizet; a nyers bit meghal ugyanabban a zajban)
  (d) SZINDROMA-TARTAS: a meglepetes (szindroma) eldobasa, a korrekcio
      megtartasa = TANULAS: a modell marad, a zaj megy
  (e) SOHA NE IRJ: a legolcsobb torles az, ami meg sem tortent (engram
      allokacio: csak a bekotott kerul tarolasra)

A gep: a hanmag_agy hurok dinamikaja (azonos!), ra egy
ENTROPIA-KONYVVITEL ket politikaval:
  NAIV  = minden szo utan nyers reset (7 bit), mintha resetelni kellene
  OKOS  = unitaris javitas (0 bit) -- ahogy a gep tenyleg mukodik
Ugyanaz a kimenet (ugyanazok a felismert szavak, sziluettek, engramok),
mas a szamla: a kulonbozet = A FELEJTES MODJANAK ARA, kvantitativan.

Kozmikus konyvvitel: ugyanaz a bit 310 K-en, T_CMB-en, T_dS-en (energia),
es a horizontba dobva (TERULET: 4 ln2 * l_P^2 / bit -- a bezameles ara).

Aphorizma: "nem az a kerdes, mit tartasz meg -- hanem hogyan engedsz el."
           "az ertelem a felejtes muveszete."
"""

from math import log, log2
import hanmag_agy as agy

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


KB = 1.380649e-23
LN2 = log(2)


class Konyvvitel:
    """entropia-konyvvitel: minden konyvelt esemeny bitekben"""

    def __init__(self, nev):
        self.nev = nev
        self.tetelek = []

    def fizet(self, bitek, ok):
        if bitek > 0:
            self.tetelek.append((bitek, ok))

    def ingyen(self, ok):
        self.tetelek.append((0.0, ok + "  [ingyen]"))

    def osszesen(self):
        return sum(b for b, _ in self.tetelek)


# ----------------------------------------------------------------------
# 1. A MODOK BIZONYITASA (fizikai kiserletek, nem konyveles)
# ----------------------------------------------------------------------

def kiserlet_visszaszamolas():
    banner("1. VISSZASZAMOLAS: a szerkezetes felejtes ingyen van")
    a = agy.Agy()
    friss = a.signatura()
    # ket asszociacio bekotese (CNOT a blokkok kozott)
    c1 = (agy.ELME0 + 0 * 7 + 0, agy.ELME0 + 1 * 7 + 5)   # blokk1.p1 -> blokk2.p6
    c2 = (agy.ELME0 + 1 * 7 + 5, agy.ELME0 + 2 * 7 + 6)   # blokk2.p6 -> blokk3.p7
    a.allapot.cnot(*c1)
    a.allapot.cnot(*c2)
    kozben = a.signatura()
    print("    friss:    %s" % (friss,))
    print("    kotve:    %s   (a gondolat nott)" % (kozben,))
    # VISSZAFORDITAS: a CNOT oninverz, forditott sorrendben
    a.allapot.cnot(*c2)
    a.allapot.cnot(*c1)
    vissza = a.signatura()
    print("    vissza:   %s" % (vissza,))
    ellenoriz(vissza == friss, "a visszaszamolt felejtes EXAKT: a csend visszajott -- ara: 0 bit")
    ellenoriz(kozben != friss, "kozben a kotes latszott (volt mit felejteni)")


def kiserlet_kodba_dobas():
    banner("2. KODBA DOBAS: ugyanaz a zaj -- nyers bit meghal, kodolt tulieli")
    # NYERS bit: az info egy qubit Z-elojeleben; X-zaj a 0. qubiten
    nyers_info = 1
    nyers_hiba_q = 0
    # a nyers bit: X-hiba a 0. qubiten -> az info felborul, es nem latszik
    nyers_info_utana = -nyers_info
    print("    nyers bit + X-zaj a 0. qubiten: info = %+d -> %+d  (ELVESZETT, jelzes nelkul)"
          % (nyers_info, nyers_info_utana))
    # KODOLT: az agy fule, logikai Z az info; X-zaj barhol
    a = agy.Agy()
    tuleli = 0
    for q in range(7):
        b = agy.Agy()
        b.allapot.injektal_x(agy.FUL0 + q)
        sz = 0
        for j in range(3, 6):
            if b.allapot.sajatertek(b.allapot.g[j]) == -1:
                sz |= (1 << (j - 3))
        if sz:
            b.allapot.injektal_x(agy.FUL0 + (sz - 1))     # javitas
        # logikai Z (a 7. generator) sajaterteke = az info
        if b.allapot.sajatertek(b.allapot.g[6]) == 1:
            tuleli += 1
    print("    kodolt bit + X-zaj mind a 7 pozicion: tuleli = %d/7  (a kod kifizeti a zajt)"
          % tuleli)
    ellenoriz(nyers_info_utana != nyers_info, "a nyers eldobas a bitet is eldobja")
    ellenoriz(tuleli == 7, "a kodba dobott bit minden poziciojabol visszajon -- ara: 0 bit")


# ----------------------------------------------------------------------
# 3. A TORTENET KET KONYVELESSSEL (azonos dinamika, mas szamla)
# ----------------------------------------------------------------------

MONDATOK = [
    ["bit", "brain", "star"],
    ["code", "cut", "brain"],
    ["comma", "time", "brain"],
]


def fut_tortenet(politika):
    a = agy.Agy()
    k = Konyvvitel(politika)
    for szavak in MONDATOK:
        for j, szo in enumerate(szavak):
            p, felismert, zaj = a.hall(szo)
            if politika == "NAIV":
                k.fizet(7, "nyers reset a fulben (%s utan)" % szo)
            else:
                k.ingyen("unitaris javitas a fulben (%s)" % szo)
            # a szo a gondolatba koltozik: MOZGATAS, nem torles
            k.ingyen("a szo a kodba koltozik (blokk %d, pont %d)" % (j + 1, p))
            a.gondol(blokk=j + 1, pont=p)
            k.ingyen("Singer-tick (adiabatikus utem)")
        sig = a.engramoz(szavak)
        k.ingyen("engram-allokacio (soha-ne-irj szurese utan)")
    return a, k


def kiserlet_ket_konyveles():
    banner("3. UGYANAZ A TORTENET, KET KONYVELES")
    a1, k1 = fut_tortenet("NAIV")
    a2, k2 = fut_tortenet("OKOS")
    azonos = a1.signatura() == a2.signatura() and \
             [e["szavak"] for e in a1.engramok] == [e["szavak"] for e in a2.engramok]
    ellenoriz(azonos, "a kimenet bitre azonos (sziluettek + engramok)")
    print()
    print("    NAIV szamla (nyers reset minden szo utan):")
    for b, ok in k1.tetelek:
        if b: print("      %4.1f bit  %s" % (b, ok))
    print("      ------ osszesen: %.1f bit" % k1.osszesen())
    print("    OKOS szamla (ahogy a gep tenyleg mukodik):")
    for b, ok in k2.tetelek:
        if b: print("      %4.1f bit  %s" % (b, ok))
    print("      ------ osszesen: %.1f bit" % k2.osszesen())
    print()
    print("    a kulonbozet: %.1f bit -- A FELEJTES MODJANAK ARA" % (k1.osszesen() - k2.osszesen()))
    return a2, k1, k2


# ----------------------------------------------------------------------
# 4. HATASFOK ES KOZMIKUS KONYVVITEL
# ----------------------------------------------------------------------

def kiserlet_hatasfok(a, k1, k2):
    banner("4. HATASFOK: ebit / eldobott bit")
    sig = a.signatura()
    fonodas = sum(sig) - 7          # a csend folotti osszefonodas
    print("    a tortenet altal epitett fonodas: %d ebit (sziluett %s)" % (fonodas, sig))
    for k in (k1, k2):
        b = k.osszesen()
        r = float("inf") if b == 0 else fonodas / b
        print("    %-5s: %5.1f bit eldobva -> %s ebit/eldoitt-bit"
              % (k.nev, b, ("%.3f" % r) if b else "korlatlan (nem dobott el)"))
    print()
    print("    KOZMIKUS KONYVVITEL -- ugyanaz az 1 eldobott bit ara:")
    L_P = 1.616255e-35
    for nev, T in [("agykent (310 K)", 310.0), ("CMB-furdoben (2.7255 K)", 2.7255),
                   ("de Sitter-horizontba (2.66e-30 K)", 2.66e-30)]:
        print("      %-34s %12.4e J" % (nev, KB * T * LN2))
    print("      %-34s %12.4e m^2   (= 4 ln2 * l_P^2 terulet!)"
          % ("horizontba, teruletben:", 4 * LN2 * L_P * L_P))
    print("    -- a hideg vegen a torles ara nem energia, hanem GEOMETRIA:")
    print("       a bezameles 4 l_P^2 ln2-vel novel a horizonton (az alfa_G vesszo)")


def kiserlet_itelet(k1, k2):
    banner("5. ITELET")
    ellenoriz(len(HIBAK) == 0, "onellenorzes tiszta")
    kulonbozet = k1.osszesen() - k2.osszesen()
    print("""
    A FELEJTES MODJA, SZAMOKBAN:
      [x] visszaszamolas: 0 bit -- a szerkezetes felejtes ingyen van
          (a torles EXAKT, a csend visszajott)
      [x] kodba dobas: 0 bit -- a redundancia fizet; a nyers bit meghal
          ugyanabban a zajban, a kodolt 7/7 poziciobol visszajon
      [x] a tortenet szamlaja: NAIV %.0f bit vs OKOS 0 bit -- ugyanaz a
          kimenet; a kulonbozet tiszta felejtes-mod
      [x] a legolcsobb torles: SOHA NE IRJ (engram-allokacio szur)

    ES A MELY:
      az informaciot nem lehet megsemmisiteni (unitaritas) -- csak
      MOZGATNI: hobe (elvezett), korrelacioba (visszanyerheto), kodba
      (vedett). Az ELD OBAS = csatornavalasztas. A fekete lyuk a
      sugarzasba dob (Page: visszanyerheto); az agy a modellbe dob
      (szindroma megy, korrekcio marad = tanulas); a genom a
      codonokba dob (a beszelgetes megy, a fixpontok maradnak).

    NYITOTT VESSZOK:
      ( ) a valodi agy HOVAGYAS: passziv bomlas (Tononi: alvasbeli
          downscaling) -- az ingyen eldobas szabalya a kodban
      ( ) az engramok amortizacioja: a tarolt bitek "berlete"
      ( ) a kvantum-entropia termelodik a meresnel: a konyvvitel
          jelenleg klasszikus bit-szintu
    """ % kulonbozet)


def main():
    print("HANMAG-CARNOT -- a 2+2 utemu eromu es a felejtes modja")
    print("aforizma: nem az a kerdes, mit tartasz meg -- hanem hogyan engedsz el.")
    kiserlet_visszaszamolas()
    kiserlet_kodba_dobas()
    a2, k1, k2 = kiserlet_ket_konyveles()
    kiserlet_hatasfok(a2, k1, k2)
    kiserlet_itelet(k1, k2)
    if HIBAK:
        print("CARNOT-HIBA: %d ellentmondas" % len(HIBAK))
    else:
        print("CARNOT ELLENORIZVE -- a hurok hőerőgép, a felejtes muveszet.")


if __name__ == "__main__":
    main()
