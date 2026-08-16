#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HanMag archívum — veszteségmentes szöveg-kodek (HNMA01 formátum).

A kódolás lényege: az eredeti szöveg BITRE visszajön. Két réteg:
  1. szótár-réteg: a szöveg leggyakoribb szavai rövid jelölést kapnak
     (a szótár a konténerben utazik, a dekóder önellátó);
  2. entrópia-réteg: zlib/DEFLATE a maradékon.

Mindkét réteg pontosan megfordítható — a visszakódolt szöveg
SHA-256 lenyomata azonos az eredetiével, különben a program hibát dob.

Használat:
    python3 hanmag_archivum.py kodol <bemenet.txt> <kimenet.hnma>
    python3 hanmag_archivum.py dekod <bemenet.hnma> <kimenet.txt>
    python3 hanmag_archivum.py teszt <bemenet.txt>     # teljes kör + hash
"""

import sys
import zlib
import hashlib

MAGIA = b"HNMA01"
JEL = "\x01"          # token-kezdő jel
MAX_SZOTAR = 255      # ennyi szótári bejegyzés fér 1 bájtos tokenbe


# ---------------------------------------------------------------
# SZÓTÁR-ÉPÍTÉS (determinisztikus: nyereség szerint, döntetlenre ábécé)
# ---------------------------------------------------------------

def szotar_epit(szoveg):
    """A leggyakoribb szavakból szótár, ha a csere TÉNYLEG spórol.
    Egy előfordulás nyeresége (hossz - 2) bájt (a token 2 bájt: JEL+kód),
    a szótári tárolás ára (hossz + 1) bájt. Csak a nettóan nyereséges
    bejegyzések maradnak — MDL-színvonal: a modell is fizet."""
    gyakorisag = {}
    for szo in szoveg.split():
        tiszta = szo.strip()
        if len(tiszta) >= 4:          # rövid szót nem éri meg cserélni
            gyakorisag[tiszta] = gyakorisag.get(tiszta, 0) + 1
    jeloltek = []
    for szo, db in gyakorisag.items():
        nyereseg = db * (len(szo) - 2) - (len(szo) + 1)
        if nyereseg > 0:
            jeloltek.append((-nyereseg, szo))   # mínusz: csökkenő sorrend
    jeloltek.sort()
    return [szo for _, szo in jeloltek[:MAX_SZOTAR]]


# ---------------------------------------------------------------
# KÓDOLÁS: szöveg -> jelölt átszöveg (balról jobbra, leghosszabb találat)
# ---------------------------------------------------------------

def jelol_kodol(szoveg, szotar):
    """Szöveg -> jelölt sorozat. JEL maga escape-elve: JEL+\\x00."""
    hossz_sorrend = sorted(szotar, key=lambda s: (-len(s), s))
    kimenet = []
    i, n = 0, len(szoveg)
    while i < n:
        if szoveg[i] == JEL:
            kimenet.append(JEL + "\x00")        # escape
            i += 1
            continue
        talalat = None
        for szo in hossz_sorrend:
            if szoveg.startswith(szo, i):
                talalat = szo
                break
        if talalat is not None:
            kimenet.append(JEL + chr(szotar.index(talalat) + 1))
            i += len(talalat)
        else:
            kimenet.append(szoveg[i])
            i += 1
    return "".join(kimenet)


def jelol_dekod(jelolt, szotar):
    """Jelölt sorozat -> eredeti szöveg (a kodol pontos inverze)."""
    kimenet = []
    i, n = 0, len(jelolt)
    while i < n:
        if jelolt[i] == JEL:
            kod = jelolt[i + 1]
            if kod == "\x00":
                kimenet.append(JEL)
            else:
                kimenet.append(szotar[ord(kod) - 1])
            i += 2
        else:
            kimenet.append(jelolt[i])
            i += 1
    return "".join(kimenet)


# ---------------------------------------------------------------
# KONTÉNER: MAGIA + szótár + zlib-tömörített jelölt szöveg
# ---------------------------------------------------------------

SIMA_MAGIA = b"HNMA00"    # szótár nélküli változat (MDL-fallback)


def kodol(szoveg):
    """Két jelölt versenyzik: szótáras és sima zlib — az olcsóbb nyer.
    Így a kodek SOHA nem rosszabb a sima DEFLATE-nél (MDL-fallback)."""
    # 1. jelölt: szótár + zlib
    szotar = szotar_epit(szoveg)
    jelolt = jelol_kodol(szoveg, szotar)
    tomor_szotar = zlib.compress(jelolt.encode("utf-8"), 9)
    fejlec = bytearray(MAGIA)
    fejlec.append(len(szotar))
    for szo in szotar:
        b = szo.encode("utf-8")
        fejlec.append(len(b))
        fejlec.extend(b)
    szotaras = bytes(fejlec) + tomor_szotar
    # 2. jelölt: sima zlib (üres szótár)
    sima = SIMA_MAGIA + zlib.compress(szoveg.encode("utf-8"), 9)
    if len(szotaras) <= len(sima):
        return szotaras, szotar
    return sima, []


def dekod(kontener):
    if kontener.startswith(SIMA_MAGIA):
        szoveg = zlib.decompress(kontener[len(SIMA_MAGIA):]).decode("utf-8")
        return szoveg, []
    if not kontener.startswith(MAGIA):
        raise ValueError("nem HNMA-konténer (hibás mágia)")
    pos = len(MAGIA)
    nszotar = kontener[pos]; pos += 1
    szotar = []
    for _ in range(nszotar):
        hossz = kontener[pos]; pos += 1
        szotar.append(kontener[pos:pos + hossz].decode("utf-8"))
        pos += hossz
    jelolt = zlib.decompress(kontener[pos:]).decode("utf-8")
    return jelol_dekod(jelolt, szotar), szotar


# ---------------------------------------------------------------
# HASH ÉS TESZT
# ---------------------------------------------------------------

def sha(szoveg):
    return hashlib.sha256(szoveg.encode("utf-8")).hexdigest()


def teszt(utvonal):
    with open(utvonal, encoding="utf-8") as f:
        eredeti = f.read()

    kontener, szotar = kodol(eredeti)
    vissza, _ = dekod(kontener)

    h_eredeti, h_vissza = sha(eredeti), sha(vissza)
    assert vissza == eredeti, "VESZTESÉG! a visszakódolt szöveg eltér"
    assert h_vissza == h_eredeti, "HASH-ELTÉRÉS!"

    nyers = len(eredeti.encode("utf-8"))
    sima_zlib = len(zlib.compress(eredeti.encode("utf-8"), 9))
    szotaras_e = kontener.startswith(MAGIA)
    szotar_bit = (7 + sum(1 + len(s.encode("utf-8")) for s in szotar)) if szotaras_e else 6
    valtozat = "HNMA01 (szótár+zlib)" if szotaras_e else "HNMA00 (sima zlib — a szótár nem fizetett)"

    print("=" * 56)
    print("HanMag archívum — veszteségmentes kódolás (HNMA01)")
    print("=" * 56)
    print(f"bemenet:            {utvonal}")
    print(f"nyers méret:        {nyers:>7} bájt")
    print(f"sima zlib (alap):   {sima_zlib:>7} bájt  ({100*sima_zlib/nyers:5.1f}%)")
    print(f"nyertes változat:   {valtozat}")
    print(f"HNMA konténer:      {len(kontener):>7} bájt  ({100*len(kontener)/nyers:5.1f}%)")
    print(f"  ebből fejléc+szótár: {szotar_bit:>4} bájt ({len(szotar)} bejegyzés)")
    print(f"  ebből tömör-törzs:   {len(kontener)-szotar_bit:>4} bájt")
    print("-" * 56)
    print(f"SHA-256(eredeti):   {h_eredeti}")
    print(f"SHA-256(vissza):    {h_vissza}")
    print("ODA-VISSZA: RENDBEN — a szöveg bitre, veszteség nélkül visszajött")
    print("-" * 56)
    print("szótár-minta (a gép által választott jelölések):")
    for i, szo in enumerate(szotar[:12]):
        print(f"  token {i+1:>3} -> {szo!r}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    mod = sys.argv[1]
    if mod == "teszt":
        teszt(sys.argv[2])
    elif mod == "kodol":
        with open(sys.argv[2], encoding="utf-8") as f:
            szoveg = f.read()
        kontener, _ = kodol(szoveg)
        with open(sys.argv[3], "wb") as f:
            f.write(kontener)
        print(f"kódolva: {sys.argv[3]} ({len(kontener)} bájt)")
    elif mod == "dekod":
        with open(sys.argv[2], "rb") as f:
            kontener = f.read()
        szoveg, _ = dekod(kontener)
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            f.write(szoveg)
        print(f"dekódolva: {sys.argv[3]} ({len(szoveg)} karakter)")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
