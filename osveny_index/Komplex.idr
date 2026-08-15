module Komplex

-- ═══════════════════════════════════════════════════════════════
-- KOMPLEX SZÁMOK — a fázis számolásához
-- ═══════════════════════════════════════════════════════════════
-- A kvantum Y-kombinátor fázisát komplex számokkal kell számolni:
--   e^{iφ} = cos(φ) + i·sin(φ)
--   Y_φ(f) = e^{iφ} · f(Y_φ(f))
-- 
-- A komplex fixpont: z* = a + bi
--   a = Re(z*) = a valós rész (a CODATA méri)
--   b = Im(z*) = a fázis rész (a Bach-korrekcio kalkulálja)
-- ═══════════════════════════════════════════════════════════════

-- ─── 1. KOMPLEX SZÁM ───────────────────────────────────────

public export
record Komplex where
  constructor K
  re : Double  -- valós rész
  im : Double  -- imaginárius rész

-- ─── 2. ALAP MŰVELETEK ──────────────────────────────────────

public export
kZero : Komplex
kZero = K 0.0 0.0

public export
kEgy : Komplex
kEgy = K 1.0 0.0

public export
kI : Komplex
kI = K 0.0 1.0

public export
kOsszead : Komplex -> Komplex -> Komplex
kOsszead (K a b) (K c d) = K (a + c) (b + d)

public export
kKivon : Komplex -> Komplex -> Komplex
kKivon (K a b) (K c d) = K (a - c) (b - d)

public export
kSzoroz : Komplex -> Komplex -> Komplex
kSzoroz (K a b) (K c d) = K (a*c - b*d) (a*d + b*c)

public export
kAbs : Komplex -> Double
kAbs (K a b) = sqrt (a*a + b*b)

public export
kArg : Komplex -> Double
kArg (K a b) =
  if a > 0.0 then atan (b / a)
  else if a < 0.0 && b >= 0.0 then atan (b / a) + 3.141592653589793
  else if a < 0.0 && b < 0.0 then atan (b / a) - 3.141592653589793
  else if a == 0.0 && b > 0.0 then 3.141592653589793 / 2.0
  else if a == 0.0 && b < 0.0 then -3.141592653589793 / 2.0
  else 0.0

-- ─── 3. EULER-FORMULA: e^{iφ} ──────────────────────────────

public export
euler : Double -> Komplex
euler szog = K (cos szog) (sin szog)

-- ─── 4. KOMPLEX Y-KOMBINÁTOR ───────────────────────────────

||| A kvantum Y-kombinátor komplex számokkal:
|||   Y_φ(f) = e^{iφ} · f(Y_φ(f))
||| 
||| Iterálva: a valós rész konvergál a fixponthoz (a spirál belseje),
||| az imaginárius rész a fázis (a spirál forgása).
|||
||| A fixpont: z* = a + bi ahol
|||   a = a valós fixpont (pl. α⁻¹ = 137.036)
|||   b = a fázis fixpont (a CPT-rest δ)
public export
kvantumYKomplex : (Komplex -> Komplex) -> Double -> Nat -> Komplex
kvantumYKomplex f fazisSzog 0 = kZero
kvantumYKomplex f fazisSzog (S k) =
  let elozo = kvantumYKomplex f fazisSzog k
      fazisSzorzo = euler (fromInteger (natToInteger k) * fazisSzog)
  in kSzoroz fazisSzorzo (f elozo)

-- ─── 5. BACH-KORREKCIO KOMPLEX ─────────────────────────────

||| A Bach-korrekcio komplex formában:
|||   Re(α⁻¹) = 137 + 9/250 - A4*(3/4)²/c  (valós, CODATA méri)
|||   Im(α⁻¹) = δ (fázis, a Bach-korrekcio kalkulálja)
|||   δ = aranymetszés szög - α⁻¹ = 137.5° - 137.036 = 0.5°
public export
bachAlfaInverz : Double -> Double -> Komplex
bachAlfaInverz aranyMetszesSzoog alfaRe =
  let alfaFok = aranyMetszesSzoog * 180.0 / 3.141592653589793
      delta = alfaFok - alfaRe  -- a CPT-rest fokban
      deltaRad = delta * 3.141592653589793 / 180.0
  in K alfaRe (sin deltaRad)  -- a fázis komplex számként

||| A Bach-korrekcio hiba (komplex abszolút érték)
public export
bachHibaKomplex : Komplex -> Komplex -> Double
bachHibaKomplex (K ar air) (K br bir) = sqrt ((ar-br)*(ar-br) + (air-bir)*(air-bir))

-- ─── 6. SPIRÁL KOMPLEX ─────────────────────────────────────

||| A spirál: minden lépésben a sugár csökken és a fázis nő.
||| z_{n+1} = z_n / φ * e^{i·goldenAngle}
public export
spiralKomplex : Double -> Double -> Nat -> Komplex
spiralKomplex sugar fazisSzog 0 = K sugar 0.0
spiralKomplex sugar fazisSzog (S k) =
  let elozo = spiralKomplex sugar fazisSzog k
      sugarUj = kAbs elozo / 1.618033988749895  -- aranymetszés
      fazisUj = kArg elozo + fazisSzog
  in K (sugarUj * cos fazisUj) (sugarUj * sin fazisUj)

||| A spirál konvergenciája: |z_n| → 0?
public export
spiralKonvergencia : Double -> Double -> Nat -> Double
spiralKonvergencia sugar fazisSzog n = kAbs (spiralKomplex sugar fazisSzog n)

-- ─── 7. SHOW ────────────────────────────────────────────────

public export
showKomplex : Komplex -> String
showKomplex (K a b) =
  show a ++ (if b >= 0.0 then " + " else " - ") ++ show (abs b) ++ "i"

-- ─── 8. ARANYMETSES FIXPONT — √(1+z) KONTRAKCIO ────────────

||| Az aranymetszés fixpontja: f(z) = √(1+z)
||| φ = √(1+φ) → φ² = 1+φ → φ²-φ-1 = 0 → φ = (1+√5)/2
||| |f'(z)| = |1/(2√(1+z))| < 1 ha |1+z| > 1/4 — kontrakcio!
||| Komplex síkon is konvergál: a spirál φ-hez tart.
|||
||| Forrás: John D. Cook, "Complex golden convergence" (2025)
|||   https://www.johndcook.com/blog/2025/02/23/complex-golden-convergence/
public export
komplexGyok : Komplex -> Komplex
komplexGyok (K a b) =
  let -- √(a+bi) = √((r+a)/2) + i·sgn(b)·√((r-a)/2), r = |a+bi|
      r = sqrt (a*a + b*b)
      reGyok = sqrt ((r + a) / 2.0)
      imGyok = if b >= 0.0 then sqrt ((r - a) / 2.0) else -sqrt ((r - a) / 2.0)
  in K reGyok imGyok

||| Az aranymetszés kontrakciós iterációja: z_{n+1} = √(1+z_n)
||| Konvergál φ = (1+√5)/2 ≈ 1.618 felé.
||| Komplex síkon: a spirál φ-hez tart.
public export
aranyMetszesIteracio : Komplex -> Nat -> Komplex
aranyMetszesIteracio z 0 = z
aranyMetszesIteracio z (S k) =
  aranyMetszesIteracio (komplexGyok (kOsszead kEgy z)) k

||| A konvergencia: |z_n - φ| → 0?
public export
aranyMetszesKonvergencia : Komplex -> Nat -> Double
aranyMetszesKonvergencia z n =
  let zn = aranyMetszesIteracio z n
      fiKomplex = K 1.618033988749895 0.0
  in kAbs (kKivon zn fiKomplex)

-- ─── 9. KVANTUM Y = ARANYMETSES KONTRAKCIO + FAZIS ──────────

||| A kvantum Y-kombinátor = aranymetszés kontrakció + fázis:
|||   Y_φ(f) = e^{iθ} · √(1 + Y_φ(f))
||| ahol θ = aranymetszés szög (137.5°)
||| 
||| A kontrakció (√(1+z)) garantálja a konvergenciát,
||| a fázis (e^{iθ}) a spirált biztosítja.
||| A fixpont = φ · e^{i·φ_spirál} = komplex aranymetszés.
public export
kvantumYAranyMetszes : Double -> Nat -> Komplex
kvantumYAranyMetszes fazisSzog 0 = K 0.0 0.0
kvantumYAranyMetszes fazisSzog (S k) =
  let elozo = kvantumYAranyMetszes fazisSzog k
      kontrakcio = komplexGyok (kOsszead kEgy elozo)
      fazisSzorzo = euler (fromInteger (natToInteger k) * fazisSzog * 0.01)  -- gyengitett fázis
  in kSzoroz fazisSzorzo kontrakcio

||| A kvantum Y konvergenciája a fixponthoz.
public export
kvantumYAMKonvergencia : Double -> Nat -> Double
kvantumYAMKonvergencia fazisSzog n =
  let zn = kvantumYAranyMetszes fazisSzog n
      fiKomplex = K 1.618033988749895 0.0
  in kAbs (kKivon zn fiKomplex)

public export
komplexFom : IO ()
komplexFom = do
  putStrLn "=== KOMPLEX SZAMOK — fazis szamolas ==="
  putStrLn ""
  putStrLn "1. EULER-FORMULA: e^{iφ} = cos(φ) + i·sin(φ)"
  putStrLn ("  e^{iπ/2} = " ++ showKomplex (euler (3.141592653589793 / 2.0)))
  putStrLn ("  e^{iπ}   = " ++ showKomplex (euler 3.141592653589793))
  putStrLn ("  e^{i0}   = " ++ showKomplex (euler 0.0))
  putStrLn ""
  putStrLn "2. BACH-KORREKCIO KOMPLEX:"
  let aranyMetszesSzoog = 2.0 * 3.141592653589793 / (1.618033988749895 * 1.618033988749895)
  let alfaRe = 137.035999177
  let alfaKomplex = bachAlfaInverz aranyMetszesSzoog alfaRe
  putStrLn ("  Re(α⁻¹) = " ++ show alfaRe ++ " (CODATA)")
  putStrLn ("  Im(α⁻¹) = " ++ show alfaKomplex.im ++ " (fazis = CPT-rest)")
  putStrLn ("  |α⁻¹|   = " ++ show (kAbs alfaKomplex) ++ " (komplex abszolut ertek)")
  putStrLn ("  arg(α⁻¹) = " ++ show (kArg alfaKomplex) ++ " rad")
  putStrLn ""
  putStrLn "3. SPIRAL KOMPLEX (konkret szamitas):"
  putStrLn ("  0 lepes: |z| = " ++ show (spiralKonvergencia 1.0 aranyMetszesSzoog 0))
  putStrLn ("  1 lepes: |z| = " ++ show (spiralKonvergencia 1.0 aranyMetszesSzoog 1))
  putStrLn ("  2 lepes: |z| = " ++ show (spiralKonvergencia 1.0 aranyMetszesSzoog 2))
  putStrLn ("  3 lepes: |z| = " ++ show (spiralKonvergencia 1.0 aranyMetszesSzoog 3))
  putStrLn ("  5 lepes: |z| = " ++ show (spiralKonvergencia 1.0 aranyMetszesSzoog 5))
  putStrLn ("  10 lepes: |z| = " ++ show (spiralKonvergencia 1.0 aranyMetszesSzoog 10))
  putStrLn ""
  putStrLn "4. ARANYMETSES KONTRAKCIO (f(z) = √(1+z) → φ):"
  putStrLn "  Kezdoertek: z0 = 0.0 + 0.0i"
  let z0 = K 0.0 0.0
  putStrLn ("  0 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 0) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 0))
  putStrLn ("  1 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 1) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 1))
  putStrLn ("  2 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 2) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 2))
  putStrLn ("  3 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 3) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 3))
  putStrLn ("  5 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 5) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 5))
  putStrLn ("  10 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 10) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 10))
  putStrLn ("  20 lepes: z = " ++ showKomplex (aranyMetszesIteracio z0 20) ++ "  |z-φ| = " ++ show (aranyMetszesKonvergencia z0 20))
  putStrLn ""
  putStrLn "5. KVANTUM Y = ARANYMETSES KONTRAKCIO + FAZIS:"
  let amsz = 2.399963229728653  -- aranyMetszesSzoog radban
  putStrLn ("  fazisSzog = " ++ show amsz ++ " rad (137.5°)")
  putStrLn ("  0 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 0))
  putStrLn ("  1 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 1))
  putStrLn ("  2 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 2))
  putStrLn ("  3 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 3))
  putStrLn ("  5 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 5))
  putStrLn ("  10 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 10))
  putStrLn ("  20 lepes: |Y-φ| = " ++ show (kvantumYAMKonvergencia amsz 20))
  putStrLn ""
  putStrLn "Kesz."