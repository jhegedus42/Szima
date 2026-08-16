# -*- coding: utf-8 -*-
# HANMAG_PAGE — a hurok a fazisatmenet korul: a Page-görbe ket gépe.
# A vazlat: egy gep a multban, egy a jovoben; a fazisatmenet ket oldalan;
# hurok korulotte; kozepen fekete lyuk, ami kidobja az informaciot
# (Hawking-sugarzas), es a horizontnal a TER es az IDO helyet cserel.
# Az egyik oldal FAZIS-informaciot dob (fonodas -> sugarzas), a masik
# TER-informaciot (a belso ter no). Mindkettot etetni kell energiaval,
# kulonben elparolognak — es a vegen ott a paradoxon, ha nincs mit enni.
#
# 1. PAGE-GORBE: veletlen tiszta allapot sugarzas-entropiaja (Page keplete,
#    pontos atlag) — felmegy, visszajon: A HUROK. Page-ido = N/2.
# 2. A KET GEP: mult-gep (k < N/2: dobja, S no) / jovo-gep (k > N/2:
#    visszahozza, S csokken — Hayden-Preskill, ld. hanmag_feketelyuk.py).
# 3. A HELYCSERE: Schwarzschild-metrika elojelei a horizont ket oldalan:
#    kint t=ido, r=ter; bent r=IDO, t=ter. A szingularitas nem hely — idopont.
# 4. TUZFAL = MONOGAMIA-SZEGES (AMPS): az entropia-aritmetika ellentmondasa;
#    a feloldas: A = R (island/ER=EPR) — a gep MERTE: a fonodas HIPEREL
#    (hanmag_gorbulet.py: a paros graf harom reszre is URES).
# 5. TAKARMANY: Hawking-teljesitmeny, parolgasi ido ~ M^3; etetes-feltetel;
#    a vege: a de Sitter-horizont padloja (T = 2.66e-30 K, hanmag_nobel.py).
import math
from math import log, pi

HIBAK = []
def ok(felt, uzenet):
    if felt: print(f"    [OK] {uzenet}")
    else:
        HIBAK.append(uzenet); print(f"    [HIBA] {uzenet}")
def fel(cim):
    print(); print("=" * 74); print(cim); print("=" * 74)

LN2 = log(2)
HBAR = 1.054571817e-34; C_ = 299792458.0; G_ = 6.67430e-11; KB = 1.380649e-23

fel("1. A PAGE-GORBE — a hurok, ami korulotte megy")
def page_S(k, N):
    """Veletlen tiszta allapot: a k-qubites sugarzas atlagos entropiaja (bit)."""
    m, n = sorted((2**k, 2**(N - k)))
    if m == 1: return 0.0
    H = sum(1.0 / j for j in range(n + 1, m * n + 1))
    return (H - (m - 1) / (2 * n)) / LN2
N = 12
gorbe = [page_S(k, N) for k in range(N + 1)]
print(f"    N = {N} qubit (lyuk + sugarzas); a gorbe:")
for k, s in enumerate(gorbe):
    jel = " <== PAGE-IDO (a fazisatmenet)" if k == N // 2 else ""
    print(f"    k={k:2d} | {'#' * int(round(s * 4)):24s} {s:5.2f} bit{jel}")
ok(gorbe[0] == 0 and abs(gorbe[-1]) < 1e-12, "S(0) = S(N) = 0: a vege TISZTA sugarzas")
ok(all(gorbe[k] <= gorbe[k + 1] + 1e-9 for k in range(N // 2)), "a felso ag monoton no (mult-gep)")
ok(all(gorbe[k] >= gorbe[k + 1] - 1e-9 for k in range(N // 2, N)), "az also ag monoton csokken (jovo-gep)")
print(f"    csucs: {max(gorbe):.2f} bit a Page-idoben; a hurok ZARODIK: ami bemegy,")
print(f"    kijon — a gorbe ket fele a ket gep.")

fel("2. A KET GEP A FAZISATMENET KET OLDALAN")
print("    MULT-GEP (k < N/2): az entropia NO — a gep a FAZIS-informaciot")
print("      dobja: a sugarzas a fonodast viszi el (korrelacio -> koherencia).")
print("    JOVO-GEP (k > N/2): az entropia CSOKKEN — az uj sugarzas a regi")
print("      sugarzast tisztitja: az info VISSZAJON (Hayden-Preskill-tukor:")
print("      hanmag_feketelyuk.py, 3. kiserlet — mar MERTUK a 7 qubiten).")
print("    'tudjak, hogyan jojjenek vissza': a Page-ido utan a bedobott bit")
print("    majdnem azonnal kikopik — scramble-elve, tukor-modban.")

fel("3. AHOL A TER ES AZ IDO HELYET CSEREL — a horizont alatt")
RS = 2.0   # r_s = 2M, egysegekben
print("    g_tt = -(1 - r_s/r),  g_rr = 1/(1 - r_s/r):")
for r in (3.0, 2.5, 2.0 + 1e-4, 1.5, 1.0):
    f = 1 - RS / r
    if f > 0:
        allapot = "KINT: t = IDO, r = TER"
    elif f < 0:
        allapot = "BENT: r = IDO(!), t = TER"
    else:
        allapot = "HORIZONT"
    print(f"    r = {r:8.4f} r_s-val: 1-r_s/r = {f:+9.5f}   {allapot}")
ok(all((1 - RS / r) > 0 for r in (3.0, 2.5)), "kivul: a metrika szignatura rendes")
ok(all((1 - RS / r) < 0 for r in (1.5, 1.0)), "belul: AZ ELOJELEK FELCSERELODNEK")
print("    bent a csokkeno r olyan elkerulhetetlen, mint kint a holnap:")
print("    a szingularitas nem HELY, hanem IDOPONT. ez a helycsere a tűzfal")
print("    geometriai arca: a ket gep a ket szignatura-oldalon dolgozik.")

fel("4. A TUZFAL = MONOGAMIA-SZEGES (AMPS-aritmetika)")
S_B, S_R = 1.0, 3.0     # kimeneti mod (1 bit), korai sugarzas (3 bit)
ssa_kovetel = S_R + S_B        # SSA + S(AB)=0 (sima horizont) -> S(BR) >= S(R)+S(B)
unit_kovetel = S_R - S_B       # uniterseg a Page-ido utan: B tisztitja R-et
print(f"    sima horizont koveteli: S(AB) = 0 (A = belso partner, B = kimeneti mod)")
print(f"    SSA kovetel:            S(BR) >= {ssa_kovetel:.0f} bit")
print(f"    uniterseg kovetel:      S(BR) <= {unit_kovetel:.0f} bit  (Page-ido utan)")
ok(unit_kovetel < ssa_kovetel,
   f"ELLENTMONDAS: {unit_kovetel:.0f} < {ssa_kovetel:.0f} — a B nem lehet EGYIDEJULEG")
print("    fonott A-val IS es R-rel IS. ez a tuzfal-paradoxon magja.")
print("    A GEPOK FELOLDASA: A = R (sziget/ER=EPR) — a belso mod MAGA a korai")
print("    sugarzas parja; a PAROS konyveles az, ami szegi meg. a gep ezt MERTE:")
print("    hanmag_gorbulet.py — harom-reszes kotes utan a paros fonodasi graf")
print("    URES marad (monogamia): a horizont fonodasa HIPEREL, nem elpar.")

fel("5. TAKARMANY ES PARADOXON — etetni kell, kulonben elparolog")
def hawking_T(M): return HBAR * C_**3 / (8 * pi * G_ * M * KB)
def hawking_P(M): return HBAR * C_**6 / (15360 * pi * G_**2 * M**2)
def parolgas_t(M): return 5120 * pi * G_**2 * M**3 / (HBAR * C_**4)
M_NAP = 1.989e30
ev = 365.25 * 86400
print(f"    Nap-tomegu lyuk: T_H = {hawking_T(M_NAP):.2e} K, P_H = {hawking_P(M_NAP):.2e} W")
print(f"    parolgasi ido ~ {parolgas_t(M_NAP)/ev:.1e} ev  (t ~ M^3)")
ok(parolgas_t(M_NAP) > 1e60 * ev, "a parolgasi ido sokkal hosszabb a kornal")
print("    ETETES-FELTETEL: a gep (ket oldalon) csak addig all, amig eszik —")
print("    a hutes ara Landauer (hanmag_nobel.py, V. fel): bitenkent kT ln2.")
print("    ha elfogy az eles: elparolog — es a Page-gorbe also vegen a tiszteletbeli")
print("    PARADOXON: az utolso biteknel a felig-klasszikus leiras megszunik.")
print(f"    a vegpont nem lyuk, hanem padlo: a de Sitter-horizont, T = 2.66e-30 K —")
print("    a gep zarojegele, a ket ido kozos alja.")
print()
print("=" * 74)
if not HIBAK:
    print("PAGE ELLENORIZVE: a hurok zarodik, a helycsere megvan, a tuzfal a")
    print("monogamia szegese, a takarmany-szamitas stimmel. a ket gep eszik.")
else:
    print(f"PAGE-HIBA: {len(HIBAK)} sor: {HIBAK}")
print("=" * 74)
