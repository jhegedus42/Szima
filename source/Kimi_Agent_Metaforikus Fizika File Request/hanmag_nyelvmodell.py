#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HanMag nyelvmodell — PPM (predikció részleges egyezéssel) + aritmetikai
kódoló, a gép állapotával mint PRIOR.

Ez a Tomasello-motor korpusz-méretben: a modell kontextus-statisztikákat
tanul ("konstrukciók"), a következő bájtot a leghosszabb ismert kontextus
jósolja ("slot-kitöltés"), kizárással és escape-pel lejjebb lép, egészen
az egyenletes (-1)-edrendű modellig. A modell ADAPTÍV: nem kell tárolni —
a dekóder tükörként ugyanazt építi. Ha az ELMÉLET-szöveg primingja megvan,
mindkét oldal azzal inicializál: az elmélet így szó szerint a tömörítő
kiinduló modellje — "ha megvan a teljes elmélet, az tömöríti a szöveget".

Formátum: "HNML01" | u8 priming-jelölő | u64 eredeti hossz | aritmetikai folyam

Használat:
    python3 hanmag_nyelvmodell.py teszt <fájl>            # roundtrip + hash
    python3 hanmag_nyelvmodell.py meres                   # teljes korpusz-táblázat
"""

import sys
import os
import struct
import hashlib
import zlib
import lzma
from collections import Counter

MAGIA = b"HNML01"
HALF, Q1, Q3 = 1 << 31, 1 << 30, 3 << 30


# ---------------------------------------------------------------
# Aritmetikai kódoló (32 bites, bit-szintű normalizáció, carry-tüskével)
# ---------------------------------------------------------------

class AKEnc:
    def __init__(s):
        s.lo, s.hi, s.pending = 0, 0xFFFFFFFF, 0
        s.out, s.acc, s.nbits = bytearray(), 0, 0

    def _bit(s, b):
        s.acc = (s.acc << 1) | b
        s.nbits += 1
        if s.nbits == 8:
            s.out.append(s.acc)
            s.acc, s.nbits = 0, 0

    def _bit_pp(s, b):
        s._bit(b)
        for _ in range(s.pending):
            s._bit(1 - b)
        s.pending = 0

    def encode(s, cum, f, t):
        r = (s.hi - s.lo + 1) // t
        s.lo += r * cum
        s.hi = s.lo + r * f - 1
        while True:
            if s.hi < HALF:
                s._bit_pp(0)
            elif s.lo >= HALF:
                s._bit_pp(1)
                s.lo -= HALF; s.hi -= HALF
            elif s.lo >= Q1 and s.hi < Q3:
                s.pending += 1
                s.lo -= Q1; s.hi -= Q1
            else:
                break
            s.lo = (s.lo << 1) & 0xFFFFFFFF
            s.hi = ((s.hi << 1) & 0xFFFFFFFF) | 1

    def flush(s):
        # Lezárás: a carry-tüske feloldása után a VÉGSŐ lo 32 bitjét is
        # kiírjuk. A folyam által reprezentált szám így biztosan a végső
        # intervallumba esik (ami része az összes korábbinak) — a dekóder
        # mindenhol helyesen fejt, a 4 bájt extra elhanyagolható.
        s.pending += 1
        s._bit_pp(0 if s.lo < Q1 else 1)   # WNC-szabály: lo<Q1 -> 0, különben 1
        for bit in range(31, -1, -1):
            s._bit((s.lo >> bit) & 1)
        if s.nbits:
            s.out.append(s.acc << (8 - s.nbits))
        return bytes(s.out)


class AKDec:
    def __init__(s, data):
        s.d = data
        s.lo, s.hi = 0, 0xFFFFFFFF
        fej = data[:4] + b"\x00" * max(0, 4 - len(data))
        s.val = int.from_bytes(fej, "big")
        s.pos = 32                     # bitpozíció! az első 4 bájt már beolvasva

    def _bit(s):
        idx, off = divmod(s.pos, 8)
        b = (s.d[idx] >> (7 - off)) & 1 if idx < len(s.d) else 0
        s.pos += 1
        s.val = ((s.val << 1) & 0xFFFFFFFF) | b

    def freq(s, t):
        r = (s.hi - s.lo + 1) // t
        return min((s.val - s.lo) // r, t - 1), r

    def update(s, cum, f, t, r):
        s.lo += r * cum
        s.hi = s.lo + r * f - 1
        while True:
            if s.hi < HALF:
                pass
            elif s.lo >= HALF:
                s.lo -= HALF; s.hi -= HALF; s.val -= HALF
            elif s.lo >= Q1 and s.hi < Q3:
                s.lo -= Q1; s.hi -= Q1; s.val -= Q1
            else:
                break
            s.lo = (s.lo << 1) & 0xFFFFFFFF
            s.hi = ((s.hi << 1) & 0xFFFFFFFF) | 1
            s._bit()


# ---------------------------------------------------------------
# PPM-modell: kontextus-statisztikák, kizárás, escape = 1
# ---------------------------------------------------------------

class PPM:
    def __init__(s, rend=5, periodus=0):
        s.rend = rend
        s.periodus = periodus   # 0/1: időtlen; >1: fázis-feltételes (CPT-sértés)
        s.ctx = {}              # (fázis, utótag) -> Counter(köv bájt)
        s.hist = bytearray()

    def _kulcs(s, k):
        """Kontextuskulcs. A LEGHOSSZABB rendnél a fázis is belemegy:
        minden karakter hordozza a saját fázisát (pozíció mod periódus)."""
        c = bytes(s.hist[len(s.hist) - k:]) if k else b""
        if s.periodus > 1 and k == min(s.rend, len(s.hist)):
            return (len(s.hist) % s.periodus, c)
        return (-1, c)

    def priming(s, data):
        """Az elmélet betáplálása: csak modelltanulás, kódolás nélkül.
        A dekóder ugyanazt teszi — az elmélet "ingyen" van megosztva."""
        for b in data:
            s._tanul(b)

    def _tanul(s, b):
        h, n = s.hist, len(s.hist)
        for k in range(min(s.rend, n), -1, -1):
            c = s._kulcs(k)
            if c not in s.ctx:
                s.ctx[c] = Counter()
            s.ctx[c][b] += 1
        s.hist.append(b)

    def _szint(s, k, excl):
        """Eloszlás a k-adrendű kontextusban a kizárások után.
        Vissza: (rendezett [(szimbólum, db)], escape_db, összeg)."""
        counts = s.ctx.get(s._kulcs(k))
        if not counts:
            return None
        rendezett = sorted((sym, db) for sym, db in counts.items() if sym not in excl)
        tot = sum(db for _, db in rendezett) + 1     # +1 az escape
        return rendezett, tot

    def kodol_bajt(s, ac, b):
        excl = set()
        for k in range(min(s.rend, len(s.hist)), -1, -1):
            sz = s._szint(k, excl)
            if sz is None:
                continue
            rendezett, tot = sz
            cum = 0
            for sym, db in rendezett:
                if sym == b:
                    ac.encode(cum, db, tot)
                    s._tanul(b)
                    return
                cum += db
            ac.encode(tot - 1, 1, tot)               # escape utolsóként
            excl |= set(sym for sym, _ in rendezett)
        # (-1)-edrendű: egyenletes a nem kizárt bájtokon
        szabad = [x for x in range(256) if x not in excl]
        ac.encode(szabad.index(b), 1, len(szabad))
        s._tanul(b)

    def dekod_bajt(s, ad):
        excl = set()
        for k in range(min(s.rend, len(s.hist)), -1, -1):
            sz = s._szint(k, excl)
            if sz is None:
                continue
            rendezett, tot = sz
            idx, r = ad.freq(tot)
            if idx == tot - 1:                       # escape
                ad.update(tot - 1, 1, tot, r)
                excl |= set(sym for sym, _ in rendezett)
                continue
            cum = 0
            for sym, db in rendezett:
                if cum <= idx < cum + db:
                    ad.update(cum, db, tot, r)
                    s._tanul(sym)
                    return sym
                cum += db
        szabad = [x for x in range(256) if x not in excl]
        idx, r = ad.freq(len(szabad))
        b = szabad[idx]
        ad.update(idx, 1, len(szabad), r)
        s._tanul(b)
        return b


# ---------------------------------------------------------------
# Fájl-szintű kódolás / dekódolás
# ---------------------------------------------------------------

def kodol(adat, elmelet=None):
    mod = PPM()
    if elmelet is not None:
        mod.priming(elmelet)
    ac = AKEnc()
    for b in adat:
        mod.kodol_bajt(ac, b)
    torzs = ac.flush()
    jelolo = 1 if elmelet is not None else 0
    return MAGIA + bytes([jelolo]) + struct.pack(">Q", len(adat)) + torzs


def dekod(kontener, elmelet=None):
    if not kontener.startswith(MAGIA):
        raise ValueError("nem HNML01-folyam")
    jelolo = kontener[len(MAGIA)]
    if jelolo and elmelet is None:
        raise ValueError("a folyam elmélet-primingos — dekódoláshoz kell az elmélet")
    (n,) = struct.unpack(">Q", kontener[len(MAGIA) + 1:len(MAGIA) + 9])
    mod = PPM()
    if jelolo:
        mod.priming(elmelet)
    ad = AKDec(kontener[len(MAGIA) + 9:])
    return bytes(mod.dekod_bajt(ad) for _ in range(n))


# ---------------------------------------------------------------
# GEODETIKUS MODELL: a szöveg görbült téridőre fektetve (henger, C kerület)
# A karaktert a fénykúpja jósolja: (felette, felette-bal, felette-jobb, utótag)
# ---------------------------------------------------------------

class PPMGeo(PPM):
    def __init__(s, rend=5, kerulet=0):
        super().__init__(rend, periodus=0)
        s.kerulet = kerulet     # a henger kerülete = a tér görbülete

    def _kulcs(s, k):
        c = bytes(s.hist[len(s.hist) - k:]) if k else b""
        n = len(s.hist)
        if s.kerulet > 1 and k == min(s.rend, n) and n >= s.kerulet:
            felette = s.hist[n - s.kerulet]
            fb = s.hist[n - s.kerulet - 1] if n > s.kerulet else 256
            fj = s.hist[n - s.kerulet + 1] if n - s.kerulet + 1 < n else 256
            return (felette, fb, fj, c)
        return (-1, 0, 0, c)


GEO_MAGIA = b"HNMG01"


def kodol_geo(adat, kerulet, elmelet=None):
    mod = PPMGeo(rend=5, kerulet=kerulet)
    if elmelet is not None:
        mod.priming(elmelet)
    ac = AKEnc()
    for b in adat:
        mod.kodol_bajt(ac, b)
    torzs = ac.flush()
    jelolo = 1 if elmelet is not None else 0
    return GEO_MAGIA + struct.pack(">H", kerulet) + bytes([jelolo]) + struct.pack(">Q", len(adat)) + torzs


def dekod_geo(kontener, elmelet=None):
    if not kontener.startswith(GEO_MAGIA):
        raise ValueError("nem HNMG01-folyam")
    (kerulet,) = struct.unpack(">H", kontener[len(GEO_MAGIA):len(GEO_MAGIA) + 2])
    jelolo = kontener[len(GEO_MAGIA) + 2]
    if jelolo and elmelet is None:
        raise ValueError("a folyam elmélet-primingos — dekódoláshoz kell az elmélet")
    (n,) = struct.unpack(">Q", kontener[len(GEO_MAGIA) + 3:len(GEO_MAGIA) + 11])
    mod = PPMGeo(rend=5, kerulet=kerulet)
    if jelolo:
        mod.priming(elmelet)
    ad = AKDec(kontener[len(GEO_MAGIA) + 11:])
    return bytes(mod.dekod_bajt(ad) for _ in range(n))


def gorbit_fut(adat, minta_hossz=65536, jeloltek=None):
    """A tér meghajlítása: a C kerületet az MDL választja — addig hajlik
    a tér, amíg a leírás minimális nem lesz. Determinisztikus: (méret, C)
    szerint rendezve az első. A görbületet a korpusz mintadarabján méri,
    aztán a teljes szöveget arra a téridőre fekteti."""
    if jeloltek is None:
        jeloltek = list(range(16, 257, 8))
    minta = adat[:minta_hossz]
    meresek = sorted((len(kodol_geo(minta, C)), C) for C in jeloltek)
    return meresek[0][1], meresek[:5]


# ---------------------------------------------------------------
# MDL-választó: fájlonként a legjobb kodek
# ---------------------------------------------------------------

BEST_MAGIA = b"HNMB01"
MOD_LZMA, MOD_PPM, MOD_PPME, MOD_GEO, MOD_GEOE = 0, 1, 2, 3, 4


def kodol_legjobb(adat, elmelet=None, geo=True):
    """A jelöltek versenye fájlonként — a legkisebb nyer (MDL).
    A törzs a teljes belső konténer (saját fejléccel jár)."""
    jeloltek = [(MOD_LZMA, lzma.compress(adat, preset=9))]
    jeloltek.append((MOD_PPM, kodol(adat)))
    if elmelet is not None:
        jeloltek.append((MOD_PPME, kodol(adat, elmelet)))
    kerulet = 0
    if geo and len(adat) >= 4096:
        kerulet, _ = gorbit_fut(adat)
        jeloltek.append((MOD_GEO, kodol_geo(adat, kerulet)))
        if elmelet is not None:
            jeloltek.append((MOD_GEOE, kodol_geo(adat, kerulet, elmelet)))
    mod, torzs = min(jeloltek, key=lambda mj: len(mj[1]))
    return BEST_MAGIA + bytes([mod]) + torzs, mod, kerulet


def dekod_legjobb(kontener, elmelet=None):
    if not kontener.startswith(BEST_MAGIA):
        raise ValueError("nem HNMB01-konténer")
    mod = kontener[len(BEST_MAGIA)]
    torzs = kontener[len(BEST_MAGIA) + 1:]
    if mod == MOD_LZMA:
        return lzma.decompress(torzs)
    if mod == MOD_PPM:
        return dekod(torzs)
    if mod == MOD_PPME:
        return dekod(torzs, elmelet)
    if mod == MOD_GEO:
        return dekod_geo(torzs)
    if mod == MOD_GEOE:
        return dekod_geo(torzs, elmelet)
    raise ValueError(f"ismeretlen mód: {mod}")


# ---------------------------------------------------------------
# Teszt és korpusz-mérés
# ---------------------------------------------------------------

def _sha(b):
    return hashlib.sha256(b).hexdigest()


def elmelet_be(output="/mnt/agents/output"):
    e = open(os.path.join(output, "hanmag_gep_szoveg.txt"), encoding="utf-8").read()
    for plusz in ("hanmag_uzemanyagrud.txt", "hanmag_szotar_prompt.md"):
        p = os.path.join(output, plusz)
        if os.path.exists(p):
            e += "\n" + open(p, encoding="utf-8").read()
    return e.encode("utf-8")


def teszt(utvonal):
    adat = open(utvonal, "rb").read()
    elm = elmelet_be()
    k1 = kodol(adat)
    k2 = kodol(adat, elm)
    v1 = dekod(k1)
    v2 = dekod(k2, elm)
    assert v1 == adat and v2 == adat, "VESZTESÉG!"
    z = len(zlib.compress(adat, 9))
    x = len(lzma.compress(adat, preset=9))
    print(f"nyers:      {len(adat):>9} B")
    print(f"zlib:       {z:>9} B")
    print(f"lzma:       {x:>9} B")
    print(f"PPM:        {len(k1):>9} B")
    print(f"PPM+elmélet:{len(k2):>9} B")
    print(f"SHA-256 mindenhol: {_sha(adat)[:16]}… == {_sha(v1)[:16]}… == {_sha(v2)[:16]}…")
    print("ODA-VISSZA: RENDBEN (PPM és PPM+elmélet is bitre visszaadja)")


def meres():
    import glob, subprocess, zipfile, re
    texts = {}
    for f in sorted(glob.glob("/mnt/agents/upload/*")):
        nev = os.path.basename(f)
        try:
            if nev.endswith((".txt", ".md")):
                texts[nev] = open(f, "rb").read()
            elif nev.endswith(".docx"):
                with zipfile.ZipFile(f) as z:
                    xml = z.read("word/document.xml").decode("utf-8", errors="replace")
                texts[nev] = re.sub(r"<[^>]+>", " ", xml).encode("utf-8")
            elif nev.endswith(".pdf"):
                out = subprocess.run(["pdftotext", f, "-"], capture_output=True, timeout=180)
                texts[nev] = out.stdout
        except Exception:
            pass
    elm = elmelet_be()
    print(f"{'fájl':<48}{'nyers':>9}{'zlib':>8}{'lzma':>8}{'PPM':>8}{'PPM+elm':>9}")
    print("-" * 92)
    S = [0, 0, 0, 0, 0]
    for nev, adat in sorted(texts.items(), key=lambda kv: -len(kv[1])):
        if len(adat) < 2000:
            continue
        z = len(zlib.compress(adat, 9))
        x = len(lzma.compress(adat, preset=6))
        p = len(kodol(adat))
        pe = len(kodol(adat, elm))
        for i, v in enumerate((len(adat), z, x, p, pe)):
            S[i] += v
        print(f"{nev[:46]:<48}{len(adat):>9}{z:>8}{x:>8}{p:>8}{pe:>9}")
    print("-" * 92)
    print(f"{'ÖSSZES':<48}{S[0]:>9}{S[1]:>8}{S[2]:>8}{S[3]:>8}{S[4]:>9}")
    print(f"\nbájt/karakter: nyers 1.00 | zlib {S[1]/S[0]:.3f} | lzma {S[2]/S[0]:.3f} "
          f"| PPM {S[3]/S[0]:.3f} | PPM+elmélet {S[4]/S[0]:.3f}")
    print(f"az elmélet hozadéka a PPM-en: {100*(S[3]-S[4])/S[3]:.1f}% "
          f"(a PPM {100*(S[2]-S[3])/S[2]:+.1f}% az lzma-hoz)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
    elif sys.argv[1] == "teszt":
        teszt(sys.argv[2])
    elif sys.argv[1] == "meres":
        meres()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
