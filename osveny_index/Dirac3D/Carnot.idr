module Carnot

import Data.Vect
import Fazis
import Lagrangian

-- =====================================================================
-- CARNOT modul: entropia kezelés = koherencia-őrzés.
--
-- Carnot-hűtőgép: T_meleg (zaj) ↔ T_hideg (koherencia).
-- η = 1 - T_hideg/T_meleg: maximális hatásfok.
-- Ez KORLÁTOZZA a hibajavítást.
--
-- QHMC = Carnot-ciklus alapú mintavételezés.
-- =====================================================================

%default total

-- =====================================================================
-- 1. Entropia.
-- =====================================================================

public export
entropia : Allapot -> Double
entropia allap =
  let egyedi = length (nub (toList (fazisok allap)))
  in log (cast egyedi + 1.0) / log 9.0
  where
    nub : Eq t => List t -> List t
    nub [] = []
    nub (x :: xs) = if x `elem` xs then nub xs else x :: nub xs

-- =====================================================================
-- 2. Carnot-hatásfok.
-- =====================================================================

public export
carnotHataskor : Double -> Double -> Double
carnotHataskor tMeleg tHideg = 1.0 - (tHideg / tMeleg)

-- =====================================================================
-- 3. Hőmérséklet és koherencia.
-- =====================================================================

public export
koherenciaHomerseklet : Allapot -> Double
koherenciaHomerseklet a = 1.0 + entropia a

-- =====================================================================
-- 4. Termodinamikai hibajavítás (4. kategória).
-- =====================================================================

public export
termodinamikaiJavitas : Allapot -> Allapot -> Double -> Double -> Allapot
termodinamikaiJavitas jelenlegi cel tMeleg tHideg =
  let
    hatasfok = carnotHataskor tMeleg tHideg
    jelenlegiEntropia = entropia jelenlegi
    celEntropia = entropia cel
    maxCsokkenes = hatasfok * (jelenlegiEntropia - celEntropia)
    ujEntropia = jelenlegiEntropia - maxCsokkenes
    ujFazisok = if ujEntropia < 0.1
                   then replicate 8 F0
                   else fazisok jelenlegi
  in MkAllapot ujFazisok (ido jelenlegi)

-- =====================================================================
-- 5. Algebrai hibajavítás (2. kategória: Steane).
--
-- A Steane [[7,1,3]] kód: 7 bites vektor, 3-as távolság.
-- Hibajavítás: ha egyetlen bit hibás → szindrómák alapján
--azonosítjuk, melyik, és javítjuk.
--
-- A 7 dimenzió: {idő, okság, tér, szín, hang, fázis, mód}
-- (l. Steane7Bit a MagasabbRendszer.modulban)
--
-- Szindróma számítás:
--   s1 = b1 ⊕ b2 ⊕ b4 ⊕ b6   (idő, tér, hang, fázis)
--   s2 = b1 ⊕ b3 ⊕ b5 ⊕ b6   (idő, okság, szín, fázis)
--   s3 = b2 ⊕ b3 ⊕ b5 ⊕ b6   (tér, okság, szín, fázis)
-- Ha s1=s2=s3=0 → nincs hiba.
-- Ha nem → a szindróma értéke = a hibás pozíció indexe (1-7).
--
-- A javítás: a hibás pozíciót a cél értékére állítjuk.
-- =====================================================================

||| Bit érték kinyerése: ha a fazis = F0, akkor 0, különben 1.
public export
fazisBit : Fazis -> Nat
fazisBit F0 = 0
fazisBit _ = 1

||| XOR két bit között (csak 0 és 1, minden más 0).
public export
xorBit : Nat -> Nat -> Nat
xorBit 0 0 = 0
xorBit 0 1 = 1
xorBit 1 0 = 1
xorBit 1 1 = 0
xorBit _ _ = 0

||| 8-elemű Vect cseréje: updateAt használatával.
public export
csereFazis : Fin 8 -> Fazis -> Vect 8 Fazis -> Vect 8 Fazis
csereFazis poz uj v = updateAt poz (const uj) v

||| Nat → Fin 8 konverzió (ha >=8, akkor FZ).
public export
natToFin8 : Nat -> Fin 8
natToFin8 0 = FZ
natToFin8 1 = FS FZ
natToFin8 2 = FS (FS FZ)
natToFin8 3 = FS (FS (FS FZ))
natToFin8 4 = FS (FS (FS (FS FZ)))
natToFin8 5 = FS (FS (FS (FS (FS FZ))))
natToFin8 6 = FS (FS (FS (FS (FS (FS FZ)))))
natToFin8 _ = FS (FS (FS (FS (FS (FS (FS FZ))))))

||| Szindróma számítás: 3 szindróma bit a 7 Steane-ből.
||| A szindróma a CEL-hez képesti eltérést méri:
|||   eltérés[i] = fazisBit(aktuális[i]) XOR fazisBit(cél[i])
|||   s1 = e[0] XOR e[2] XOR e[4] XOR e[6]   (idő, tér, hang, fázis)
|||   s2 = e[0] XOR e[1] XOR e[4] XOR e[5]   (idő, okság, szín, fázis)
|||   s3 = e[1] XOR e[2] XOR e[4] XOR e[5]   (tér, okság, szín, fázis)
||| Ha s1=s2=s3=0 → nincs hiba vagy páros hiba (javíthatatlan 1-bit korrekcióval).
public export
szindroma : Vect 8 Fazis -> Vect 8 Fazis -> (Nat, Nat, Nat)
szindroma akt c =
  let e = zipWith (\a, b => xorBit (fazisBit a) (fazisBit b)) akt c
      s1 = xorBit (index 0 e) (xorBit (index 2 e) (xorBit (index 4 e) (index 6 e)))
      s2 = xorBit (index 0 e) (xorBit (index 1 e) (xorBit (index 4 e) (index 5 e)))
      s3 = xorBit (index 1 e) (xorBit (index 2 e) (xorBit (index 4 e) (index 5 e)))
  in (s1, s2, s3)

||| Szindróma → hibás pozíció indexe (0-alapú, 7 = nincs hiba).
public export
szindromaPozicio : (Nat, Nat, Nat) -> Nat
szindromaPozicio (0, 0, 0) = 7   -- nincs hiba
szindromaPozicio (1, 0, 0) = 0   -- 1. bit: idő
szindromaPozicio (0, 1, 0) = 1   -- 2. bit: okság
szindromaPozicio (1, 1, 0) = 2   -- 3. bit: tér
szindromaPozicio (0, 0, 1) = 3   -- 4. bit: szín
szindromaPozicio (1, 0, 1) = 4   -- 5. bit: hang
szindromaPozicio (0, 1, 1) = 5   -- 6. bit: fázis
szindromaPozicio (1, 1, 1) = 6   -- 7. bit: mód
szindromaPozicio _         = 7   -- ismeretlen → nincs javítás

||| Algebrai hibajavítás: Steane szindróma alapú.
||| Ha egyetlen fazis hibás → kijavítjuk a cél értékére.
public export
algebraiJavitas : Allapot -> Allapot -> Allapot
algebraiJavitas jelenlegi cel =
  let (s1, s2, s3) = szindroma (fazisok jelenlegi) (fazisok cel)
      hibaPozicio = szindromaPozicio (s1, s2, s3)
      celFazisok = fazisok cel
      ujFazisok = if hibaPozicio == 7
                     then fazisok jelenlegi  -- nincs hiba
                     else csereFazis (natToFin8 hibaPozicio) (index (natToFin8 hibaPozicio) celFazisok) (fazisok jelenlegi)
  in MkAllapot ujFazisok (ido jelenlegi)

-- =====================================================================
-- 6. Teljes hibajavítás: 2→3→4 kategória.
--
-- Sorrend: algebrai (Steane) → geometriai (Lagrangian) → termodinamikai (Carnot)
--
-- 2. kategória: szindrómák → hibás fazis azonosítás → javítás.
-- 3. kategória: geometriai eltérés → visszaprojektálás a geodéziára.
-- 4. kategória: Carnot-hatásfok → maximális entropia-csökkentés.
-- =====================================================================

public export
teljesHibajavitas : Allapot -> Allapot -> Allapot
teljesHibajavitas jelenlegi cel =
  let
    szint2 = algebraiJavitas jelenlegi cel
    szint3 = geometriaiJavitas szint2 cel
    szint4 = termodinamikaiJavitas szint3 cel 100.0 1.0
  in szint4

-- =====================================================================
-- 6. QHMC: Quantum Hamiltonian Monte Carlo.
-- =====================================================================

public export
record QHMCAllapot where
  constructor MkQHMCAllapot
  pozicio  : Allapot
  momentum : Sebesseg

public export
qhmHamiltonian : QHMCAllapot -> Double -> Double
qhmHamiltonian q m =
  let t = 0.5 * tinetikusEnergia (momentum q) / m
      v = -entropia (pozicio q)
  in t + v

-- =====================================================================
-- 7. Lehetséges mód stabilitása.
-- =====================================================================

public export
lehetsegesModStabilitas : Allapot -> Double -> Double -> Double
lehetsegesModStabilitas a tMeleg tHideg =
  let eta = carnotHataskor tMeleg tHideg
      s = entropia a
  in eta * (1.0 - s)
