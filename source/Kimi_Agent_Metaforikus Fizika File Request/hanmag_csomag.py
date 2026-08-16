#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HanMag csomag — többfájlos veszteségmentes archívum (HNMP01 formátum).

A gép (hanmag_gep_szoveg.txt) a KIVONAT — ez a csomag a NYERS ANYAG:
minden feltöltött fájl bitje benne, fájlonkénti SHA-256-os nyilvántartással.
Kicsomagolás után minden fájl hash-e azonos kell legyen az eredetivel,
különben a program hibát dob.

Formátum:
    "HNMP01" | u32 fájlszám | ismétlődő bejegyzések:
    u16 névhossz | név (utf-8) | 32B sha256 | u64 eredeti méret |
    u64 tömörített méret | tömörített bájtok (zlib)

Használat:
    python3 hanmag_csomag.py csomag <kimenet.hnmp> <fájl1> [fájl2 ...]
    python3 hanmag_csomag.py kicsomag <bemenet.hnmp> <célkönyvtár>
    python3 hanmag_csomag.py teszt  <kimenet.hnmp> <fájl1> [fájl2 ...]
"""

import sys
import os
import zlib
import struct
import hashlib

MAGIA = b"HNMP01"


def _sha_b(bajtok):
    return hashlib.sha256(bajtok).hexdigest()


def csomagol(utvonalak):
    """Fájlok -> (konténer, jegyzék). A jegyzék: [(név, sha, méret), ...]."""
    jegyzek = []
    torzs = bytearray()
    for utvonal in utvonalak:
        with open(utvonal, "rb") as f:
            bajtok = f.read()
        nev = os.path.basename(utvonal)
        tomor = zlib.compress(bajtok, 9)
        # MDL-őszinteség: ha a zlib rontana, nyersen tárolunk (jelölt bájt)
        if len(tomor) < len(bajtok):
            tarolt, tomoritve = tomor, 1
        else:
            tarolt, tomoritve = bajtok, 0
        jegyzek.append((nev, _sha_b(bajtok), len(bajtok)))
        nb = nev.encode("utf-8")
        torzs.extend(struct.pack(">H", len(nb)))
        torzs.extend(nb)
        torzs.extend(hashlib.sha256(bajtok).digest())
        torzs.extend(struct.pack(">Q", len(bajtok)))
        torzs.extend(struct.pack(">B", tomoritve))
        torzs.extend(struct.pack(">Q", len(tarolt)))
        torzs.extend(tarolt)
    return MAGIA + struct.pack(">I", len(jegyzek)) + bytes(torzs), jegyzek


def kicsomagol(kontener, celkonyvtar=None):
    """Konténer -> jegyzék + (opcionálisan fájlok kiírva). Hash-ellenőrzés."""
    if not kontener.startswith(MAGIA):
        raise ValueError("nem HNMP01-konténer")
    pos = len(MAGIA)
    (nf,) = struct.unpack(">I", kontener[pos:pos + 4]); pos += 4
    jegyzek = []
    for _ in range(nf):
        (nl,) = struct.unpack(">H", kontener[pos:pos + 2]); pos += 2
        nev = kontener[pos:pos + nl].decode("utf-8"); pos += nl
        sha = kontener[pos:pos + 32]; pos += 32
        (eredeti_m,) = struct.unpack(">Q", kontener[pos:pos + 8]); pos += 8
        (tomoritve,) = struct.unpack(">B", kontener[pos:pos + 1]); pos += 1
        (tarolt_m,) = struct.unpack(">Q", kontener[pos:pos + 8]); pos += 8
        tarolt = kontener[pos:pos + tarolt_m]; pos += tarolt_m
        bajtok = zlib.decompress(tarolt) if tomoritve else tarolt
        if len(bajtok) != eredeti_m:
            raise ValueError(f"méret-eltérés: {nev}")
        if hashlib.sha256(bajtok).digest() != sha:
            raise ValueError(f"HASH-ELTÉRÉS: {nev} — a fájl sérült!")
        jegyzek.append((nev, hashlib.sha256(bajtok).hexdigest(), len(bajtok)))
        if celkonyvtar:
            os.makedirs(celkonyvtar, exist_ok=True)
            with open(os.path.join(celkonyvtar, nev), "wb") as f:
                f.write(bajtok)
    if pos != len(kontener):
        raise ValueError("fájlvég-eltérés: szemét a konténer végén")
    return jegyzek


def teszt(kimenet, utvonalak):
    kontener, jegyzek = csomagol(utvonalak)
    with open(kimenet, "wb") as f:
        f.write(kontener)
    # független visszaolvasás: a konténerből visszaállított jegyzék
    vissza = kicsomagol(kontener)
    assert vissza == jegyzek, "a jegyzék nem kerek"

    nyers = sum(m for _, _, m in jegyzek)
    print("=" * 64)
    print("HanMag csomag — teljes nyers anyag, veszteségmentesen (HNMP01)")
    print("=" * 64)
    for nev, sha, meret in jegyzek:
        print(f"  {meret:>10} B  {sha[:12]}…  {nev}")
    print("-" * 64)
    print(f"nyers összesen:   {nyers:>12} B  =  {nyers * 8 / 1e6:8.2f} megabit")
    print(f"HNMP01 csomag:    {len(kontener):>12} B  =  {len(kontener) * 8 / 1e6:8.2f} megabit"
          f"   ({100.0 * len(kontener) / nyers:.1f}%)")
    print(f"fájlok: {len(jegyzek)} db — MINDEGYIK hash-ellenőrzött, veszteség: 0 bit")
    print("-" * 64)
    print("főkönyv: a gép (kivonat) 2596 bit — a nyers anyag "
          f"{nyers * 8 / 2596:.0f}×-osa; a csomag a test, a gép a lélek.")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    mod = sys.argv[1]
    if mod == "teszt":
        teszt(sys.argv[2], sys.argv[3:])
    elif mod == "csomag":
        kontener, jegyzek = csomagol(sys.argv[3:])
        with open(sys.argv[2], "wb") as f:
            f.write(kontener)
        print(f"csomagolva: {sys.argv[2]} ({len(kontener)} bájt, {len(jegyzek)} fájl)")
    elif mod == "kicsomag":
        with open(sys.argv[2], "rb") as f:
            kontener = f.read()
        jegyzek = kicsomagol(kontener, sys.argv[3] if len(sys.argv) > 3 else None)
        print(f"kicsomagolva: {len(jegyzek)} fájl, mind hash-rendben")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
