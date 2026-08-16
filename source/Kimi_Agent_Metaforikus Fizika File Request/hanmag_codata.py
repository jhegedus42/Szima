#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HanMag CODATA-levezetés — a gép szám-készletéből, véletlen-kontrollal.

Módszer (a gép MDL-törvénye):
  1. Kifejezés-tér: a gép számaiból (7, 64, 21, 127, 343, 168, p_c, λ_R,
     ν, T*, T_qc, π, e, ln2, ...) zárt alakok, mindegyikhez bitköltség.
  2. Minden CODATA-célhoz a legjobb log-találat + ppm-hiba.
  3. Véletlen-kontroll: 2000 determinisztikus ál-cél ugyanabban a
     log-tartományban — p = P(ál-cél is kap ilyen jó találatot).
  4. Ítélet: ARANY p<0.01, EZÜST p<0.05, BRONZ p<0.15, különben ELUTASÍTVA.
     És a gép törvénye: a kifejezés bitköltsége < 50 (a nyers tény ára).

CODATA 2022 értékek. Futtatás:  python3 hanmag_codata.py
"""

import math
import numpy as np

PI, E, LN2 = math.pi, math.e, math.log(2)

# ---- a gép szám-készlete (érték, név, bitköltség) ----
BAZIS = [
    (7, "7", 6), (3, "3", 4), (6, "6", 5), (21, "21", 7), (64, "64", 8),
    (127, "127", 9), (343, "343=7^3", 9), (168, "168=|PSL(2,7)|", 10),
    (2, "2", 3), (PI, "pi", 6), (E, "e", 6), (LN2, "ln2", 6),
    (0.05785, "p_c=Y(P_L)", 12), (1.8035, "lambda_R=Y'(P_L)", 12), (3.30, "nu", 10),
    (0.83, "T*=Y(dC/dT)", 9), (0.717, "T_qc", 9),
    (1.29, "K_c(S1)", 10), (1.71, "K_c(S3)", 10), (0.361, "0.361bit/px", 12),
]

# ---- prímek + i, e, pi + Y (fixpont-kombinátor) ----
PRIMEK = [2, 3, 5, 7, 11, 13, 17, 19, 23, 31, 127]


def kifejezes_ter():
    """Zárt alakok generálása, deduplikálva (érték szerint), bitköltséggel."""
    talal = {}   # kerekített érték -> (érték, szöveg, költség)

    def add(v, sz, k):
        if not (math.isfinite(v) and 1e-30 < abs(v) < 1e45):
            return
        kulcs = round(math.log10(abs(v)), 9)
        if kulcs not in talal or talal[kulcs][2] > k:
            talal[kulcs] = (v, sz, k)

    for v, s, k in BAZIS:
        add(v, s, k)
    # szorzat/hányados párok
    for v1, s1, k1 in BAZIS:
        for v2, s2, k2 in BAZIS:
            add(v1 * v2, f"{s1}*{s2}", k1 + k2 + 2)
            add(v1 / v2, f"{s1}/{s2}", k1 + k2 + 2)
    # pi/e hatvány-szorzók és speciális formák
    for v1, s1, k1 in BAZIS:
        for n in range(-5, 6):
            if n:
                add(v1 * PI ** n, f"{s1}*pi^{n}", k1 + 4 + abs(n))
            if n in (-3, -2, -1, 1, 2, 3):
                add(v1 * E ** n, f"{s1}*e^{n}", k1 + 4 + abs(n))
    for a, sa, ka in ((2, "2", 3), (E, "e", 6), (PI, "pi", 6), (7, "7", 6)):
        for b, sb, kb in ((2, "2", 3), (3, "3", 4), (7, "7", 6), (127, "127", 9),
                          (343, "343", 9), (0.5, "1/2", 4), (1 / 3, "1/3", 5)):
            add(a ** b, f"{sa}^{sb}", ka + kb + 3)
    # hármas szorzatok (korlátozva)
    for v1, s1, k1 in BAZIS[:12]:
        for v2, s2, k2 in BAZIS[:12]:
            for v3, s3, k3 in ((PI, "pi", 6), (2, "2", 3), (LN2, "ln2", 6), (7, "7", 6)):
                add(v1 * v2 * v3, f"{s1}*{s2}*{s3}", k1 + k2 + k3 + 4)
    # (a*b)/c és (a/b)*c külön formák p_c-vel
    for v1, s1, k1 in BAZIS:
        add(v1 / 0.05785 ** 2, f"{s1}/p_c^2", k1 + 16)
        add(v1 * (1 - 0.05785), f"{s1}(1-p_c)", k1 + 10)
        add(v1 * (1 + 0.05785), f"{s1}(1+p_c)", k1 + 10)

    # ---- PRÍM-TÁR: +, *, ^ műveletek prímekkel és e, pi, ln2-vel ----
    alap = [(float(p), str(p), len(str(p)) + 2) for p in PRIMEK] + \
           [(PI, "pi", 6), (E, "e", 6), (LN2, "ln2", 6)]
    for a, sa, ka in alap:
        for b, sb, kb in alap:
            if abs(a) < 40 and abs(b) <= 127 and a > 0:
                v = a ** b
                if v < 1e45:
                    add(v, f"{sa}^{sb}", ka + kb + 3)
            add(a + b, f"{sa}+{sb}", ka + kb + 1)
            add(a * b, f"{sa}*{sb}", ka + kb + 1)
    # prím-négyzetösszegek (a^2+b^2 — a Gauss-féle 137-sztori)
    for a, sa, ka in alap:
        for b, sb, kb in alap:
            add(a * a + b * b, f"{sa}^2+{sb}^2", ka + kb + 4)
    # prímhatvány szorzatok p^q * r
    for p in PRIMEK[:8]:
        for q in PRIMEK[:8]:
            for r in PRIMEK[:8]:
                add(float(p) ** q * r, f"{p}^{q}*{r}", len(str(p)) + len(str(q)) + len(str(r)) + 5)
    # prímhatvány-összegek a^p + b^q  (2^7+3^2 = 137 — a prímek adják az alfa-t)
    for a, sa, ka in [(float(p), str(p), len(str(p)) + 2) for p in PRIMEK[:9]]:
        for p1 in PRIMEK[:6]:
            v1 = a ** p1
            if v1 > 1e42:
                continue
            for b, sb, kb in [(float(p), str(p), len(str(p)) + 2) for p in PRIMEK[:9]]:
                for q1 in PRIMEK[:6]:
                    v = v1 + b ** q1
                    if v < 1e42:
                        add(v, f"{sa}^{p1}+{sb}^{q1}", ka + kb + len(str(p1)) + len(str(q1)) + 4)
    # KVATERNIÓ-NORMA: négy négyzetösszeg (Hurwitz/Lagrange) — a kvaterniók a tárban
    negy = [(float(p), str(p), len(str(p)) + 2) for p in PRIMEK[:8]]
    for a, sa, ka in negy:
        for b, sb, kb in negy:
            ab2 = a * a + b * b
            for c, sc, kc in negy:
                abc2 = ab2 + c * c
                for d, sd, kd in negy:
                    add(abc2 + d * d, f"{sa}^2+{sb}^2+{sc}^2+{sd}^2", ka + kb + kc + kd + 6)
    return sorted(talal.values(), key=lambda t: t[2])


# ---- CODATA 2022 célok ----
CELOK = [
    ("alfa^-1", 137.035999084),
    ("mp/me", 1836.152673426),
    ("mmu/me", 206.7682830),
    ("mtau/me", 3477.23),
    ("mn/me", 1838.68366173),
    ("alfa_G^-1(mp)", 1.6930e38),
    ("sin^2(theta_W)", 0.23121),
    ("alfa_s(M_Z)", 0.1179),
    ("R_vegtelen [1/m]", 10973731.568160),
    ("Cabibbo lambda", 0.22500),
    ("mW/mZ", 0.88153),
    ("mH/mZ", 1.3732),
    ("VEV/mZ", 2.7002),
    ("mt/mZ", 1.8938),
]


def legjobb(T, ter, lv=None, rend=None):
    """Log-térben legközelebbi alak; lv/rend = előrendezett log-tömb (bisect, ha adott)."""
    if lv is None:
        d_best, leg = 1e9, None
        for v, sz, k in ter:
            d = abs(math.log(v / T))
            if d < d_best:
                d_best, leg = d, (v, sz, k)
        return leg, d_best
    c = math.log(T)
    i = int(np.searchsorted(lv, c))
    d_best, leg = 1e9, None
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(lv):
            d = abs(lv[j] - c)
            if d < d_best:
                d_best, leg = d, ter[rend[j]]
    return leg, d_best


def elorendez(ter):
    lv = np.array([math.log(v) for v, _, _ in ter])
    rend = np.argsort(lv)
    return lv[rend], rend


def main():
    ter = kifejezes_ter()
    lv, rend = elorendez(ter)
    print(f"kifejezés-tér: {len(ter)} zárt alak (a gép szám-készletéből)")
    print("=" * 88)
    print(f"{'cél':<16}{'CODATA':>15} {'kifejezés':<26}{'érték':>14}"
          f"{'ppm':>9}{'bit':>5}{'p':>7}  ítélet")
    print("-" * 88)
    for nev, T in CELOK:
        (v, sz, k), d = legjobb(T, ter, lv, rend)
        ppm = abs(v - T) / T * 1e6
        # véletlen-kontroll: ál-célak a log-tartományból (determinisztikus mag)
        rng = np.random.RandomState(hash(nev) % 2**31)
        al_T = T * np.exp(rng.uniform(-1.0, 1.0, 2000))
        talal = 0
        for Ta in al_T:
            _, da = legjobb(Ta, ter, lv, rend)
            if da <= d:
                talal += 1
        p = talal / 2000
        if p < 0.01:
            it = "ARANY"
        elif p < 0.05:
            it = "EZÜST"
        elif p < 0.15:
            it = "BRONZ"
        else:
            it = "elutasítva"
        if k >= 50:
            it += " (drága!)"
        print(f"{nev:<16}{T:>15.6g} {sz:<26}{v:>14.6g}{ppm:>9.1f}{k:>5}{p:>7.4f}  {it}")
    print("=" * 88)
    print("a gép törvénye: levezetés = p<0.05 ÉS költség < 50 bit;")
    print("ami felette van: numerológia — a gép őszintén elutasítja.")


if __name__ == "__main__":
    main()
