#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HanMag elmélet-tömörítés — a "teljes elmélet tömöríti a szöveget" tétele,
MÉRVE.

MDL-főkönyv:  L(elmélet) + L(szöveg | elmélet)  versus  L(szöveg).
Az "elmélet" a gép állapota (hanmag_gep_szoveg.txt + üzemanyag-rúd +
szótár-prompt), a feltételes kódhosszat zlib zdict-priming méri:
a tömörítő a gép szövegét előre betölti, így ami az elméletben benne
van, az a korpuszból "ingyen" hivatkozható.

Mért eredmény (2026-07-28, 19 feltöltött fájl szövegrétege):
  - a gép önmagában:        +0.3%  (alig magyaráz)
  - gép + nyelvi szótár:    per fájl 0.3–11.6%, de a szótár ára
                            miatt összesítve −2.0% — az MDL ELUTASÍTJA
  - a minta: a SAJÁT szövegeinket tömöríti (HOLO 11.6%, audit 8.8%),
    a könyveket nem (Bühler 0.3%, Tomasello 0.4%)
  - következtetés: az elmélet csak annak a szövegnek a tömörítője,
    amire elmélete van. A teljes szövegtömörítő = nyelvi modell
    (ez a Tomasello-program skálázva).

Futtatás:  python3 hanmag_elmelet_tomorites.py
"""

import zlib, os, glob, subprocess, zipfile, re
from collections import Counter

UPLOAD = "/mnt/agents/upload"
OUTPUT = "/mnt/agents/output"


def korpusz():
    texts = {}
    for f in sorted(glob.glob(os.path.join(UPLOAD, "*"))):
        nev = os.path.basename(f)
        try:
            if nev.endswith((".txt", ".md")):
                texts[nev] = open(f, encoding="utf-8", errors="replace").read()
            elif nev.endswith(".docx"):
                with zipfile.ZipFile(f) as z:
                    xml = z.read("word/document.xml").decode("utf-8", errors="replace")
                texts[nev] = re.sub(r"<[^>]+>", " ", xml)
            elif nev.endswith(".pdf"):
                out = subprocess.run(["pdftotext", f, "-"],
                                     capture_output=True, timeout=180)
                texts[nev] = out.stdout.decode("utf-8", errors="replace")
        except Exception:
            texts[nev] = ""
    return texts


def elmelet_be():
    e = open(os.path.join(OUTPUT, "hanmag_gep_szoveg.txt"), encoding="utf-8").read()
    for plusz in ("hanmag_uzemanyagrud.txt", "hanmag_szotar_prompt.md"):
        p = os.path.join(OUTPUT, plusz)
        if os.path.exists(p):
            e += "\n" + open(p, encoding="utf-8").read()
    return e


def L(txt, zdict=None):
    b = txt.encode("utf-8")
    if zdict is None:
        return len(zlib.compress(b, 9))
    c = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS, 9,
                         zlib.Z_DEFAULT_STRATEGY, zdict.encode("utf-8"))
    return len(c.compress(b) + c.flush())


def main():
    texts = korpusz()
    elmelet = elmelet_be()

    # megosztott nyelvi szótár a korpuszból (egyszeri költség)
    szavak = Counter()
    for txt in texts.values():
        for s in txt.split():
            if len(s) >= 3:
                szavak[s] += 1
    rendezett = sorted(szavak.items(), key=lambda kv: (-(kv[1] * len(kv[0])), kv[0]))
    szotar, meret = [], 0
    for szo, _ in rendezett:
        if meret + len(szo) + 1 > 24000:
            break
        szotar.append(szo); meret += len(szo) + 1
    teljes = elmelet + "\n" + " ".join(szotar)

    print(f"{'fájl':<52}{'zlib':>8}{'gép':>8}{'gép+nyelv':>10}")
    print("-" * 80)
    oz = og = ot = 0
    for nev, txt in sorted(texts.items(), key=lambda kv: -len(kv[1])):
        if len(txt.encode("utf-8")) < 2000:
            continue
        z, g, t = L(txt), L(txt, elmelet), L(txt, teljes)
        oz += z; og += g; ot += t
        print(f"{nev[:50]:<52}{z:>8}{g:>8}{t:>10}")
    print("-" * 80)
    L_e, L_t = len(elmelet.encode()), len(teljes.encode())
    print(f"MDL-főkönyv (szöveges fájlok, {oz} B zlib-alaphoz):")
    print(f"  gép:            elmélet {L_e:>6} + maradék {og} = {L_e+og} ({100*(L_e+og)/oz:.1f}%)")
    print(f"  gép+nyelv:      elmélet {L_t:>6} + maradék {ot} = {L_t+ot} ({100*(L_t+ot)/oz:.1f}%)")
    print("  ítélet: a gép a saját szövegeit tömöríti, a könyveket (még) nem —")
    print("  a teljes szövegtömörítő = nyelvi modell (Tomasello-program, skálázva)")


if __name__ == "__main__":
    main()
