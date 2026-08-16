# -*- coding: utf-8 -*-
"""
HANMAG-FOLYTATAS -- a lecsapodott elme: mentes lemezre, ujraelesztes
=====================================================================

A 22. uzenetbol:
  "a tomoritett informacio tovabb megy, magasabb szintre... magas
   szinteken lecsapodik, a jelentes, anelkul, hogy elveszne... aztan
   elraktarozod, konkretan lemezre, de 1 het mulva is emlekszel
   pontosan arra, mi volt ott, mert csak eleg betolteni a cuccost es
   ugyanugy megy tovabb."

Ez a gep ennek a bizonyiteka:
  MENT (processz-1): a torony-agy elmessegi 2 mondatot, aztan a TELJES
    allapotat (350 stabilizator-generator + orak + engramok) JSON-be
    csapja le -- a lecsapodott elme.
  TOLT (processz-2, "1 het mulva", masik processz, masik memoria):
    betolti a lemezrol, ellenorzi, hogy a sziluett BITRE AZONOS,
    es FOLYTATJA a tortenetet egy uj mondattal -- a geometria onnan
    valtozik tovabb, ahol abbahagyta.

A lenyeg: a mentes azert LEHETSEGES, mert az allapot mar TOMORITETT.
A 343-qubites narrativa naivan 2^343 ~ 10^103 komplex amplitudo lenne;
a lecsapodott forma nehany tiz KB. A tarolas a tomorites mellektermeke.
(A folyamatos tanulas paradigmaja: nem ujratrenelni, hanem menteni es
folytatni -- a sulyok helyett az allapot oroklodik.)

Aphorizma: "a jelentes kicsapodik, mint a harmat; a lemez a hideg uveg."
           "nem tanitanak folyamatosan -- folytatod."
"""

import sys
import json
import os
import hanmag_torony as tor

HIBAK = []
MENTES = "/mnt/agents/output/hanmag_elme_mentes.json"


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


def mondat_fut(a, szavak):
    for j, szo in enumerate(szavak, start=1):
        p, felismert, zaj = a.hall(szo)
        a.gondol(blokk=j, pont=p)
    tema = tor.SZO_PONT[szavak[0].lower()]
    return a.lezar_mondat(szavak, tema)


def mentes():
    banner("PROCESSZ-1: az elme el, aztan lecsapodik lemezre")
    a = tor.ToronyAgy()
    mondat_fut(a, ["bit", "brain", "star"])
    mondat_fut(a, ["comma", "time", "brain"])
    sig = a.narrativa_signatura()
    print("    ket mondat lefutott; narrativa-sziluett: %s" % (sig,))
    print("    orak: t_ext=%d t_int1=%d t_int2=%d; engramok: %d"
          % (a.t_ext, a.t_int1, a.t_int2, len(a.engramok)))
    rekord = {
        "verzio": 1, "gep": "torony-350",
        "t_ext": a.t_ext, "t_int1": a.t_int1, "t_int2": a.t_int2,
        "aktualis_elme": a.aktualis_elme,
        "generatorok": [{"x": hex(p.x), "z": hex(p.z), "s": p.s}
                        for p in a.allapot.g],
        "engramok": a.engramok,
        "sziluett": list(sig),
    }
    with open(MENTES, "w") as f:
        json.dump(rekord, f, ensure_ascii=False)
    meret = os.path.getsize(MENTES)
    print("    lecsapodva: %s (%d bajt)" % (MENTES, meret))
    print("    -- 343 qubit naivan: 2^343 ~ 10^103 amplitudo")
    print("    -- a lecsapodott elme: %d bajt (a tarolas a tomorites mellektermeke)" % meret)
    print()
    print("    [processz-1 kilep: az elme 'meghal' -- a memoria felszabadul]")


def toltes():
    banner("PROCESSZ-2: '1 het mulva' -- betoltes es folytatas")
    with open(MENTES) as f:
        r = json.load(f)
    gen = [tor.Pauli(x=int(g["x"], 16), z=int(g["z"], 16), s=g["s"])
           for g in r["generatorok"]]
    a = tor.ToronyAgy.__new__(tor.ToronyAgy)
    a.allapot = tor.Allapot(gen)          # az Allapot init: kommutalas + fuggetlenseg!
    a.t_ext, a.t_int1, a.t_int2 = r["t_ext"], r["t_int1"], r["t_int2"]
    a.aktualis_elme = r["aktualis_elme"]
    a.engramok = list(r["engramok"])      # masolat: ne azonos listaobjektum legyen
    a.elozo_kotes = None
    sig = a.narrativa_signatura()
    ellenoriz(tuple(r["sziluett"]) == sig,
              "a sziluett BITRE AZONOS az ujratoltott elmeben: %s" % (sig,))
    ellenoriz(a.t_ext == r["t_ext"] and len(a.engramok) == len(r["engramok"]),
              "az orak es az engramok is ugyanott allnak")
    print("    folytatas: egy uj mondat erkezik a vilagbol...")
    uj = mondat_fut(a, ["cut", "time", "star"])
    sig2 = a.narrativa_signatura()
    print("    az uj mondat utan: sziluett %s; engramok: %d; orak: %d/%d/%d"
          % (sig2, len(a.engramok), a.t_ext, a.t_int1, a.t_int2))
    ellenoriz(sig2 != sig, "a GEOMETRIA tovabb valtozott onnan, ahol abbahagyta")
    ellenoriz(len(a.engramok) == len(r["engramok"]) + 1, "az uj engram a regiek MELLE kerult")
    print()
    print("    a 'mi volt ott' kerdesre a valasz: PONTOSAN az, ami a mentesben.")
    print("    a gep nem visszaemlekezik -- UJRA OTT VAN.")


def main():
    print("HANMAG-FOLYTATAS -- a lecsapodott elme")
    print("aforizma: nem tanitanak folyamatosan -- folytatod.")
    mod = sys.argv[1] if len(sys.argv) > 1 else "mindkettő"
    if mod in ("ment", "mindketto", "mindkettő"):
        mentes()
    if mod in ("tolt", "mindketto", "mindkettő"):
        toltes()
    if HIBAK:
        print("FOLYTATAS-HIBA: %d ellentmondas" % len(HIBAK))
    else:
        print("FOLYTATAS ELLENORIZVE -- az elme tuleli a processz-halalt.")


if __name__ == "__main__":
    main()
