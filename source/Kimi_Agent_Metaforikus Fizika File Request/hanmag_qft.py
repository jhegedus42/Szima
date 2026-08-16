#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hanmag_qft.py — A GÉP QFT-SZINTJE: spinorok, Dirac, fermion-Fock, T-törés, mérés
================================================================================
Az építő korrigált fizikája:
  "ez QFT-gép, nem QM-gép — SPINOROK"
  "T = szimmetriatörés = FOLYAMATOS vs DISZKRÉT"
  "dephasing = NEM determinisztikus -> a gép nem dephasingol"
  "kör => vonal, kubit => bit"  (a T-nyíl és az infovesztés determinisztikus képe)

Rétegek (mind számszerű, 0 RNG, 0 dephasing-ensemble):
  1. SPINOROK: Pauli = kvaterniók; SU(2) forgatás: 2*pi -> -1, 4*pi -> +1 (spinor!)
     a téridő = 2x2 Hermit-mátrix X = x^mu sigma_mu, det X = minkowski norma;
     a Lorentz-csoport = SL(2,C)/{+-1}: X -> A X A^dagger. A spinor ALAPVETŐBB a vektornál.
  2. DIRAC: gamma-mátrixok (Weyl), Clifford-algebra, (p/ +- m) projektorok = spin-összegek,
     +-E energia-ágak = anyag/antianyag; C = i gamma^2 K töltéskonjugálás (ellenőrzött).
  3. FERMION-FOCK: a 7 kubit = 7 fermion-módus (Jordan-Wigner): {a_k, a_l^+} = delta_kl,
     tér-operátor a 7-gyűrűn: {psi(x), psi^+(y)} = delta_xy; Dirac-tenger = antianyag (lyuk).
  4. T-TÖRÉS = FOLYAMATOS vs DISZKRÉT (kör => vonal):
     (a) a folyamatos (unitér) fázis PONTOSAN visszafordítható (kör);
     (b) a diszkrét reset SOK-AZ-EGYHEZ leképezés: két különböző pre-állapot -> ugyanaz
         a post-állapot => nincs inverz => T DETERMINISZTIKUSAN törik (vonal);
     (c) 32 (= 2^5) ancilla-csatorna körfázisai -> 1 csatorna: ez a "kör => vonal" számszerűen.
         (A 32 a MÉRT csatornaszám; az alfa-korrekció jelöltje: 31 = 32-1, lásd hanmag_zaras.)
  5. KUBIT => BIT: a logikai Bloch-vektor |r| és a transzverzális (kör) vs z (bit) rész
     a ciklus minden lépésénél; a mérés/elvágás információvesztése = a kisugárzott normarész
     + a relatív entrópia — mindez DETERMINISZTIKUS függvénye a fonódásnak.
  6. HAWKING-PÁR: kétmódusú szorítás (Bogoliubov), tanh r = e^{-hom/2kT}: a belső módus
     TERMÁLIS — a T-törés itt is a KÜLÖNVÁLASZTÁS (elvágás), nem a dinamika.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hanmag_kvantumkarnot as hk

S1 = np.array([[0, 1], [1, 0]], dtype=complex)
S2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
S3 = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

# ---------------------------------------------------------------- 1. spinorok
def kiserlet_spinor():
    print("=" * 88)
    print("1. SPINOROK — SU(2) = egység-kvaterniók; a 2*pi-forgatás ELŐJELET vált")
    print("=" * 88)
    n = np.array([0.0, 1.0, 0.0])
    def U(fi): return np.cos(fi / 2) * I2 - 1j * np.sin(fi / 2) * (n[1] * S2)
    fel = np.array([1, 0], dtype=complex)
    print(f"  U(2pi)|fel> = -|fel>: {np.allclose(U(2 * np.pi) @ fel, -fel)}   "
          f"(a spinor NEM tér vissza!)")
    print(f"  U(4pi)|fel> = +|fel>: {np.allclose(U(4 * np.pi) @ fel, fel)}   "
          f"(csak 4pi után — ez a spin-1/2 lényege)")
    # téridő = 2x2 Hermit-mátrix; Lorentz = SL(2,C)
    t, x, y, z = 1.3, 0.4, -0.5, 0.9
    X = t * I2 + x * S1 + y * S2 + z * S3
    eta = 0.8
    A = np.cosh(eta / 2) * I2 + np.sinh(eta / 2) * S3   # boost a z-irányban, det A = 1
    X2 = A @ X @ A.conj().T
    print(f"  X = x^mu sigma_mu hermitikus: {np.allclose(X, X.conj().T)};  "
          f"det X = t^2-x^2-y^2-z^2: {np.isclose(np.real(np.linalg.det(X)), t*t-x*x-y*y-z*z)}")
    print(f"  Lorentz-boost: det(A X A^+) = det X: "
          f"{np.isclose(np.linalg.det(X2), np.linalg.det(X))}   -> SL(2,C) = Spin(1,3)")
    print(f"  => a téridő-vektor a spinorok KETTŐZÉSÉBŐL jön: a spinor az alap, a 3+1D a kép.")

# ---------------------------------------------------------------- 2. Dirac
def kiserlet_dirac():
    print()
    print("=" * 88)
    print("2. DIRAC-EGYENLET — gamma-algebra, +-E ágak = anyag/antianyag, C = i gamma^2 K")
    print("=" * 88)
    sm = [I2, S1, S2, S3]
    sb = [I2, -S1, -S2, -S3]
    O = np.zeros((2, 2), dtype=complex)
    gam = [np.block([[O, sm[m]], [sb[m], O]]) for m in range(4)]
    eta = np.diag([1, -1, -1, -1])
    cliff = all(np.allclose(gam[m] @ gam[n] + gam[n] @ gam[m], 2 * eta[m, n] * np.eye(4))
                for m in range(4) for n in range(4))
    print(f"  Clifford: {{gamma^mu, gamma^nu}} = 2 eta^munu:  {cliff}")
    m, pz = 1.0, 0.7
    E = np.sqrt(pz ** 2 + m ** 2)
    pslash = E * gam[0] - pz * gam[3]                 # p_μ = (E, -p⃗)
    Pp = (pslash + m * np.eye(4)) / (2 * m)
    Pm = (-pslash + m * np.eye(4)) / (2 * m)
    print(f"  projektorok: P+^2=P+ {np.allclose(Pp @ Pp, Pp)}, P-^2=P- {np.allclose(Pm @ Pm, Pm)},"
          f" P++P-=I {np.allclose(Pp + Pm, np.eye(4))}, P+P-=0 {np.allclose(Pp @ Pm, 0, atol=1e-12)}")
    print(f"  rang(P+) = {int(round(np.trace(Pp).real))}, rang(P-) = {int(round(np.trace(Pm).real))}"
          f"  -> spin-összegek: sum u ubar = p/+m, sum v vbar = p/-m")
    H = gam[0] @ (pz * gam[3] + m * np.eye(4))        # Dirac-Hamilton: gamma0(gamma.p + m)
    sajat = np.linalg.eigvalsh(H)
    print(f"  H_D sajátértékek: {np.round(sajat, 4)}  -> +E és -E ág, kétszeres degeneráció")
    u = Pp[:, 0]
    u = u / np.sqrt(u.conj() @ u)
    v = (1j * gam[2]) @ np.conj(u)                    # C = i gamma^2 K
    print(f"  C: u -> psi^c = i gamma^2 u*:  (p/+m) psi^c = 0: "
          f"{np.allclose((pslash + m * np.eye(4)) @ v, 0, atol=1e-10)}   (töltéskonjugálás OK)")
    print(f"  a -E ág = antianyag: a gép 15 szintje ennek diszkrét képe (7 fent / vákuum / 7 lent).")

# ---------------------------------------------------------------- 3. fermion-Fock
def kiserlet_fock():
    print()
    print("=" * 88)
    print("3. FERMION-FOCK — a 7 kubit = 7 fermion-módus (Jordan-Wigner), tér a 7-gyűrűn")
    print("=" * 88)
    Z = S3
    sz_minus = np.array([[0, 1], [0, 0]], dtype=complex)   # |1> -> |0>
    def a_op(k):
        M = np.eye(1, dtype=complex)
        for j in range(7):
            M = np.kron(M, Z if j < k else (sz_minus if j == k else I2))
        return M
    A = [a_op(k) for k in range(7)]
    car = all(np.allclose(A[k] @ A[l].conj().T + A[l].conj().T @ A[k],
                          (1.0 if k == l else 0.0) * np.eye(128))
              for k in range(7) for l in range(7))
    anti = all(np.allclose(A[k] @ A[l] + A[l] @ A[k], 0) for k in range(7) for l in range(7))
    print(f"  {{a_k, a_l^+}} = delta_kl: {car};   {{a_k, a_l}} = 0: {anti};   "
          f"(a_k^+)^2 = 0: {np.allclose(A[0].conj().T @ A[0].conj().T, 0)}")
    # tér-operátor a 7-gyűrűn, k_n = 2 pi n / 7
    kk = [2 * np.pi * n / 7 for n in range(7)]
    psi_x = [sum(A[n] * np.exp(1j * kk[n] * j) for n in range(7)) / np.sqrt(7) for j in range(7)]
    field_ok = all(np.allclose(psi_x[j] @ psi_x[l].conj().T + psi_x[l].conj().T @ psi_x[j],
                               (1.0 if j == l else 0.0) * np.eye(128))
                   for j in range(7) for l in range(7))
    print(f"  tér: psi(x_j) = (1/sqrt7) sum_n a_n e^(i k_n j);  "
          f"{{psi(x), psi^+(y)}} = delta_xy: {field_ok}")
    m0 = 0.5
    om = [np.sqrt(kk[n] ** 2 + m0 ** 2) for n in range(7)]
    H = sum(om[n] * (A[n].conj().T @ A[n]) for n in range(7))
    vac = np.zeros(128); vac[0] = 1.0
    E0 = np.real(vac @ H @ vac)
    E1 = min(np.real((A[n].conj().T @ vac) @ H @ (A[n].conj().T @ vac)) for n in range(7))
    print(f"  H = sum_n omega_n a_n^+ a_n,  omega = sqrt(k^2+m^2), m=0.5:")
    print(f"  VÁKUUM (középen!): E_0 = {E0:.1f};  első részecske: E_1 = {E1:.4f} hbar*om")
    tenger = np.zeros(128); tenger[127] = 1.0        # minden módus tele: Dirac-tenger
    lyuk = A[3] @ tenger
    print(f"  Dirac-tenger (n=1111111) és egy LYUK (a_3|tenger>): norma = {np.linalg.norm(lyuk):.1f}"
          f"  -> az antianyag = a tenger lyukai (C: részecske <-> lyuk)")

# ---------------------------------------------------------------- 4. T-törés: kör => vonal
def kiserlet_tores_kor_vonal():
    print()
    print("=" * 88)
    print("4. T-TÖRÉS = FOLYAMATOS vs DISZKRÉT — a KÖR VONAL LESZ (0 dephasing, 0 RNG)")
    print("=" * 88)
    th = 0.2
    psi0 = hk.kezdet()
    psi = hk.szivargas(psi0.copy(), th)
    psi = hk.ry_logikai(psi, np.pi / 5)
    psi = hk.korrekcio(hk.kivonat(psi))
    # (a) folyamatos kör: pontos inverz
    vissza = hk.kivonat_inv(hk.korrekcio(psi.copy(), inverz=True))
    vissza = hk.ry_logikai(vissza, -np.pi / 5)
    for q in range(6, -1, -1):
        vissza = hk.cnot(vissza, q, 13 + (q % 3))
        vissza = hk.kapu1(vissza, hk.rx(-2 * th), q)
    print(f"  (a) KÖR (folyamatos = ÉN): unitér + pontos inverz: "
          f"||vissza - eredeti|| = {np.linalg.norm(vissza - psi0):.2e}  -> T PONTOS")
    # (b) diszkrét vonal: a reset sok-az-egyhez
    a = psi.reshape(8, 64, 128).copy()
    post1 = a.copy(); post1[:, 1:, :] = 0.0
    post1 = (post1 / np.linalg.norm(post1.reshape(-1))).reshape(-1)
    pre2 = post1.copy()                                  # MÁS pre-állapot: már resetált
    a2 = pre2.reshape(8, 64, 128).copy(); a2[:, 1:, :] = 0.0
    post2 = (a2 / np.linalg.norm(a2.reshape(-1))).reshape(-1)
    print(f"  (b) VONAL (diszkrét = TE): két KÜLÖNBÖZÖ pre-állapot "
          f"(||különbség|| = {np.linalg.norm(psi - pre2):.4f}) ugyanabba a post-állapotba megy:")
    print(f"      ||post1 - post2|| = {np.linalg.norm(post1 - post2):.2e}  -> NINCS inverz: T TÖRIK")
    # (c) 32 körfázis -> 1 csatorna (a 32 = 2^5 MÉRT érték; a 64-es komment elavult volt)
    cs = int(np.sum(np.abs(a.reshape(-1).reshape(8, 64, 128)).sum(axis=(0, 2)) > 1e-12))
    fazisok = np.angle(a[:, 1:, :][np.abs(a[:, 1:, :]) > 1e-9])
    print(f"  (c) kör => vonal számszerűen: {cs} ancilla-csatorna körfázisa "
          f"(szórás: {np.std(fazisok):.3f} rad) -> reset után 1 csatorna (fázis nélkül)")

# ---------------------------------------------------------------- 5. kubit => bit
def bloch(rho_d):
    idx127 = np.arange(128) ^ 127
    x = np.real(np.sum(rho_d[np.arange(128), idx127]))
    y = np.real(1j * np.sum(hk.ZLD * rho_d[np.arange(128), idx127]))
    z = np.real(np.sum(hk.ZLD * np.diag(rho_d)))
    return np.array([x, y, z])

def kiserlet_kubit_bit():
    print()
    print("=" * 88)
    print("5. KUBIT => BIT — a Bloch-gömb (folyamatos) z-vetülete (diszkrét); a veszteség determinisztikus")
    print("=" * 88)
    th = 0.2
    psi = hk.kezdet()
    r0 = bloch(hk.rho_resz(psi, list(range(7))))
    psi = hk.szivargas(psi, th)                       # környezet: fonódás öli a kört
    r1 = bloch(hk.rho_resz(psi, list(range(7))))
    psi = hk.ry_logikai(psi, np.pi / 5)
    psi = hk.korrekcio(hk.kivonat(psi))               # korrektor: vissza bit -> kubit
    r2 = bloch(hk.rho_resz(psi, list(range(7))))
    a = psi.reshape(8, 64, 128)
    rad = float(np.sum(np.abs(a[:, 1:, :]) ** 2))
    a[:, 1:, :] = 0.0
    psi3 = (a / np.linalg.norm(a.reshape(-1))).reshape(-1)   # elvágás
    r3 = bloch(hk.rho_resz(psi3, list(range(7))))
    def sor(r, nev):
        rt = np.linalg.norm(r[:2])
        print(f"  {nev:<34} |r|={np.linalg.norm(r):.4f}  r_kör(x,y)={rt:.4f}  r_bit(z)={r[2]:+.4f}")
    sor(r0, "indulás (tiszta kubit)")
    sor(r1, "szivárgás után (fonódás: kör hal)")
    sor(r2, "korrekció után (bit -> kubit!)")
    sor(r3, "elvágás után (kivetítés)")
    S_elotte = hk.entropia(hk.rho_resz(psi, list(range(7))))
    S_utana = hk.entropia(hk.rho_resz(psi3, list(range(7))))
    print(f"  a mérés/elvágás DETERMINISZTIKUS mérlege: kisugárzott normarész = {rad:.4f}")
    print(f"  S(adat) elvágás előtt = {S_elotte:.4f} bit, utána = {S_utana:.4f} bit;")
    print(f"  a veszteség a SUGÁRZÁS-registerben maradt: ennyi a 'kubit => bit' ára.")

# ---------------------------------------------------------------- 6. Hawking-pár
def kiserlet_bogoliubov():
    print()
    print("=" * 88)
    print("6. HAWKING-PÁR — Bogoliubov-szorítás; a T-törés = a különválasztás")
    print("=" * 88)
    kT = 0.3133                                        # a motor forró-fürdő hőmérséklete
    t = np.exp(-1.0 / (2 * kT))                        # tanh r = e^{-hbar om / 2 kT}
    a0 = 1 / np.sqrt(1 + t ** 2); a1 = t / np.sqrt(1 + t ** 2)
    rho_A = np.diag([a0 ** 2, a1 ** 2])
    S = hk.entropia(rho_A)
    p1 = a1 ** 2
    S_term = -np.log2(1 - np.exp(-1.0 / kT) + 1e-30) * 0  # helyhiány: közvetlen h2
    print(f"  |psi> = {a0:.4f}|00> + {a1:.4f}|11>   (tanh r = e^(-1/2kT) = {t:.4f})")
    print(f"  belső módus: P(gerjesztett) = {p1:.4f} = termikus Boltzmann-arány e^(-1/kT)/(1+...)")
    print(f"  S(belső) = {S:.4f} bit = S(kinti)  (tiszta pár: a fonódás EGYENLŐ)")
    print(f"  a párkeltés UNITÉR (determinisztikus!); a hőmérsékleti alak csak az ELVÁGÁS után")
    print(f"  jelenik meg: a belső módus (bolygó) akkor 'hőmérsékletes', ha a kinti módust")
    print(f"  (sugárzás) leválasztjuk — kör => vonal, kubit => bit a horizonton is.")

def torvenytabla():
    print()
    print("=" * 88)
    print("7. QFT-TÖRVÉNYTÁBLA")
    print("=" * 88)
    print("  spinor      : SU(2)/kvaternió; 2*pi -> -1; a téridő a spinor kettőzése (SL(2,C))")
    print("  anyag/anti  : a Dirac +-E ágai; C = i gamma^2 K; JW-Fock: részecske <-> lyuk")
    print("  C, P, CPT   : a dinamikán pontosak (a szimmetria-fájlban ellenőrzött)")
    print("  T           : FOLYAMATOS szinten pontos (kör: pontos inverz, ||.|| ~ 1e-15)")
    print("                DISZKRÉT szinten TÖRIK (vonal: a reset sok-az-egyhez, nincs inverz)")
    print("  mérés       : NEM dephasing-ensemble: determinisztikus elvágás + kivetítés;")
    print("                az infovesztés = a kisugárzott normarész (kör => vonal, kubit => bit)")

if __name__ == "__main__":
    print("HANMAG QFT-RÉTEG — SPINOROK, DIRAC, FOCK, T-TÖRÉS, MÉRÉS (0 RNG, 0 dephasing)")
    print()
    kiserlet_spinor()
    kiserlet_dirac()
    kiserlet_fock()
    kiserlet_tores_kor_vonal()
    kiserlet_kubit_bit()
    kiserlet_bogoliubov()
    torvenytabla()
