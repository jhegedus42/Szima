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
-- 5. Teljes hibajavítás: 2→3→4 kategória.
-- =====================================================================

public export
teljesHibajavitas : Allapot -> Allapot -> Allapot
teljesHibajavitas jelenlegi cel =
  let
    szint4 = termodinamikaiJavitas jelenlegi cel 100.0 1.0
    szint3 = geometriaiJavitas szint4 cel
  in szint3

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
