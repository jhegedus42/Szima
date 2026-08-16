# -*- coding: utf-8 -*-
# HANMAG_KODEK — a kerdojel gepe: KODER + DEKODER.
# Az elmelet: a kerdes nem pont, hanem HULLAMCSOMAG: N(cel, sigma^2) a log-terben.
#   KODER:   sigma -> A = -log2(sigma/cel) pontossagbit -> KERET: csak a B <= A
#            koltsegu jeloltek engedhetok be. A kerdes SAJAT melysege vagja a
#            keresesi teret — ez a PERKOLACIO: a kerdes addig ereszkedik a
#            toronyon, amig a pontossagi koltsegvetese kitart.
#   FAZIS:   z = fazistavolsag a hullamcsomag es a jelolt kozott;
#            E = az atfedes (interferencia) bitekben. Ugyanabban a fazisban:
#            z < 2.
#   DEKODER: a nyertest visszaforditja emberi nyelvre, es megmondja, milyen
#            pontossagu MERES kell a donteshez. Ha a keret uresek ter vissza:
#            a gep nem valaszol — PONTOSABB KERDEST KER.
# (a jelolt-grammatika a hanmag_kerdes orakulumbol jon — a ket gep ugyanazt
#  a nyelvet beszeli: a koder a kerdest, az orakulum a valaszt fogalmazza)
import io, contextlib, math
from math import log2

_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    import hanmag_kerdes as K          # a demo-resz nem irodik ki
jeloltek = K.jeloltek

HIBAK = []
def ok(felt, uzenet):
    if felt: print(f"    [OK] {uzenet}")
    else:
        HIBAK.append(uzenet); print(f"    [HIBA] {uzenet}")
def fel(cim):
    print(); print("=" * 74); print(cim); print("=" * 74)

SZINTEK = [(7, "PONT (szint-0)"), (49, "SZO (szint-1)"),
           (343, "JELENTESDARAB (szint-2)"), (2401, "SZINT-3"), (math.inf, "VILAG")]

def kodol(cel, sigma):
    """A kerdes bekodolasa a gep nyelvere: hullamcsomag + szint + keret."""
    A = -log2(sigma / cel)
    szint = next(nev for hatar, nev in SZINTEK if abs(cel) < hatar)
    return {"cel": cel, "sigma": sigma, "A": A, "szint": szint, "keret": A}

def perkol(J, keret):
    """A perkolacio: csak a B <= keret jeloltek jutnak be a kodterbe."""
    bent = [j for j in J if j[1] <= keret]
    return bent

def fazis_illeszt(bent, cel, sigma):
    A = -log2(sigma / cel)
    T = []
    for v, B, s in bent:
        dev = abs(v - cel) / cel
        if dev > 0.2: continue
        z = abs(v - cel) / sigma
        E = -log2(dev) if dev > 0 else 99.0
        margo = min(E, A) - B
        verd = "HALOTT" if z > 5 else ("JELOLT" if (z < 2 and margo > 0) else "gyenge")
        T.append((margo, z, E, B, v, s, verd))
    T.sort(reverse=True)
    return T

def dekodol(kod, T):
    """Visszaforditas emberi nyelvre + meresi utasitas."""
    if not T:
        # nincs bejutott jelolt: a kerdes tul sekely. mennyivel kell melyebb?
        J = jeloltek()
        Bmin = min(B for _, B, _ in J)
        Bfix = min(B for v, B, s in J if "fixpont(137,31,21/2pi)" in s) \
               if any("fixpont(137,31,21/2pi)" in s for _, _, s in J) else None
        print(f"    DEKODER: a keret (A = {kod['A']:.1f} bit) ALATT a legolcsobb jelolt")
        print(f"    is (B_min = {Bmin:.1f} bit) — a perkolacio ures teret ad vissza.")
        print(f"    >> A GEP PONTOSABB KERDEST KER:")
        sig_szuk = kod["cel"] * 2 ** (-Bmin)
        print(f"       merj sigma <= {sig_szuk:.1e} pontossaggal, es az atomok beszelni")
        print(f"       kezdenek;", end="")
        if Bfix:
            sig_fix = kod["cel"] * 2 ** (-Bfix)
            print(f" a teljes sorhoz sigma <= {sig_fix:.1e} kell.")
        else:
            print()
        return None
    m, z, E, B, v, s, verd = T[0]
    if m < 0 or verd == "HALOTT":
        print(f"    DEKODER: NINCS VALASZ — a legjobb jelolt is {verd.lower()}")
        print(f"             ({s}: z = {z:.2f}, margo = {m:+.2f} bit)")
        print(f"             a gep hallgat: ez a kerdes meg nincs a gep nyelven.")
        return None
    print(f"    DEKODER: a valasz = {s} = {v:.10g}")
    print(f"             fazis: z = {z:.2f} (ugyanabban a fazisban: {'IGEN' if z < 2 else 'NEM'})")
    print(f"             atfedes: E = {E:.1f} bit; kodoltras: B = {B:.1f} bit; margo = {m:+.2f} bit")
    print(f"             verdikt: {verd}")
    if verd == "JELOLT":
        # mekkora pontossag dontene vegleg? z = 5-hoz sigma_krit:
        sig_krit = abs(v - kod["cel"]) / 5
        print(f"             meresi utasitas: ha a felbontas sigma <= {sig_krit:.1e} lesz,")
        print(f"             ez a sor is 5 szigmara dontodik (vagy el, vagy hal).")
    return T[0]

def kerdezz(nev, cel, sigma):
    fel(f"KERDES A KODEKEN AT: {nev} = {cel} +- {sigma}")
    kod = kodol(cel, sigma)
    print(f"    KODER: hullamcsomag N({cel}, {sigma}^2); pontossag A = {kod['A']:.1f} bit")
    print(f"           a kerdes itt el: {kod['szint']}; keret: B <= {kod['keret']:.1f} bit")
    J = jeloltek()
    bent = perkol(J, kod["keret"])
    print(f"    PERKOLACIO: {len(J)} -> {len(bent)} jelolt "
          f"({100 * (1 - len(bent) / len(J)):.0f}%-ot levagott a kerdes melysege)")
    T = fazis_illeszt(bent, cel, sigma)
    if T:
        print(f"    {'jelolt':38s} {'z':>8s} {'margo':>7s}  verdikt")
        for m, z, E, B, v, s, verd in T[:5]:
            print(f"    {s:38s} {z:8.2f} {m:+7.2f}  {verd}")
    return kod, T, dekodol(kod, T)

# ==================================================================
fel("PROLOGUSZ — a ket gep egy fazisban")
print("    koder: kerdes -> hullamcsomag + keret (a gep nyelve)")
print("    orakulum: keres a kodterben (a gep egeszei)")
print("    dekoder: valasz -> emberi nyelv + meresi utasitas")

# --- D1: mely kerdes (CODATA-padlo) --------------------------------
kod1, T1, leg1 = kerdezz("alfa^-1", 137.035999177, 2.1e-8)
ok(leg1 is not None and leg1[6] == "JELOLT" and "fixpont(137,31,21/2pi)" in leg1[5],
   f"mely kerdesre a kodek a fixpontot dekodolja (margo = {leg1[0]:+.2f})")

# --- D2: mely kerdes, ismeretlen anyag ----------------------------
kod2, T2, leg2 = kerdezz("m_p/m_e", 1836.152673426, 3.2e-7)
sajat2 = [t for t in T2 if t[0] > 0]
ok(not sajat2, "a proton-kerdesre a kodek hallgat: nincs pozitiv-margos jelolt")

# --- D3: SEHELY kerdes — a perkolacio visszautasit -----------------
kod3, T3, leg3 = kerdezz("alfa^-1 (durva meres)", 137.036, 1e-3)
ok(leg3 is None, "a sekely kerdest a koder visszautasitja: pontosabb merest ker")

# ==================================================================
fel("A KODEK-TETEL")
print("    a kerdes = logikai qubit; a kodolas = beagyazas a gep regiszterebe;")
print("    a keresesi ter = kodter; a szigma = zajkoltsegvetes;")
print("    a perkolacio = szindroma-meres lefelé a toronyon;")
print("    a valasz szindromaja = annak a szonak a CIME, amelyik a valasz.")
print("    ugyanaz a fazis: a kerdes is hullam, a jelolt is hullam —")
print("    a z a fazistavolsag, az E az interferencia. tobbi: cimkezett rim.")
print()
print("=" * 74)
if not HIBAK:
    print("KODEK ELLENORIZVE: a kerdes bejon, a valasz kimegy, a sekely kerdes")
    print("visszajon pontositasert. a ket gep egy fazisban beszel.")
else:
    print(f"KODEK-HIBA: {len(HIBAK)} sor: {HIBAK}")
print("=" * 74)
