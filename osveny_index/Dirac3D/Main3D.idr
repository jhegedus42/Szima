module Main3D

import Kina2D
import Magyar
import Dirac3D
import Fazis
import Lagrangian
import Carnot
import MagasabbRendszer
import Data.Vect
import Data.List

-- =====================================================================
-- Bemutató: a 3D nyelv működés közben.
-- =====================================================================

-- =====================================================================
-- Példa: fázisvektorok E8-hoz (Fazis.modul E8FazisPont).
-- =====================================================================

nullaFazisPont : E8FazisPont
nullaFazisPont = MkE8FazisPont (replicate 8 F0)

egyFazisPont : E8FazisPont
egyFazisPont = MkE8FazisPont [F0,F1,F2,F3,F4,F5,F6,F7]

mindenFazisPont : E8FazisPont
mindenFazisPont = MkE8FazisPont [F1,F1,F1,F1,F1,F1,F1,F1]

-- =================================================================----
-- Példa: Magyar szavak elemzése (Dirac ket).
-- =====================================================================

peldaSzavak : List (String, Ket1D)
peldaSzavak =
  [ ("ház", elemzesToKet (elemzes "ház"))
  , ("házakban", elemzesToKet (elemzes "házakban"))
  , ("futott", elemzesToKet (elemzes "futott"))
  , ("futás", elemzesToKet (elemzes "futás"))
  , ("égbolt", elemzesToKet (elemzes "égbolt"))
  ]

-- =====================================================================
-- Példa: állapotok a Carnot-hoz.
-- =====================================================================

koherensAllapot : Allapot
koherensAllapot = MkAllapot (replicate 8 F0) 0.0

zajosAllapot : Allapot
zajosAllapot = MkAllapot [F1,F2,F3,F4,F5,F6,F7,F0] 1.0

celAllapot : Allapot
celAllapot = MkAllapot [F0,F1,F2,F0,F0,F1,F2,F0] 2.0

-- =====================================================================
-- Példa: E8×E8, E16, E15 (MagasabbRendszer.modul).
-- =====================================================================

e8BalPelda : E8Egyseg
e8BalPelda = MkE8Egyseg [F0,F1,F2,F3,F4,F5,F6,F7]

e8JobbPelda : E8Egyseg
e8JobbPelda = MkE8Egyseg [F0,F0,F1,F1,F2,F2,F3,F3]

e8xE8Pelda : E8szorzes
e8xE8Pelda = MkE8szorzes e8BalPelda e8JobbPelda

e16Pelda : E16
e16Pelda = MkE16
  (MkE8Egyseg [F0,F1,F2,F3,F4,F5,F6,F7])
  (MkE8Egyseg [F7,F6,F5,F4,F3,F2,F1,F0])

e15Pelda : E15
e15Pelda = MkE15
  (MkE8Egyseg [F0,F1,F2,F3,F4,F5,F6,F7])
  [F0,F1,F2,F3,F4,F5,F6]

-- =====================================================================
-- Main: futtatás.
-- =====================================================================

main : IO ()
main = do
  putStrLn "═══════════════════════════════════════════════════"
  putStrLn "  DIRAC 3D: Fázis × Lagrangian × Carnot"
  putStrLn "  Hibajavítás 3 szinten + QHMC"
  putStrLn "═══════════════════════════════════════════════════"
  putStrLn ""

  -- 1. Fázis csoport
  putStrLn "─── 1. Z₈ fázis csoport ───"
  putStrLn ("fazisOsszead F2 F3 = " ++ show (fazisOsszead F2 F3))
  putStrLn ("fazisInverz F3 = " ++ show (fazisInverz F3))
  putStrLn ("F3 + F5 = F0? " ++ show (fazisOsszead F3 (fazisInverz F3) == F0))
  putStrLn ""

  -- 2. Magyar szavak Dirac-ban
  putStrLn "─── 2. Magyar szavak Dirac jelölésben ───"
  traverse_ (\(s, k) => do putStrLn ("  |" ++ s ++ "⟩ = " ++ showKet1D k)) peldaSzavak
  putStrLn ""

  -- 3. Entropia és Carnot
  putStrLn "─── 3. Entropia és Carnot-hatásfok ───"
  putStrLn ("Koherens entropia: " ++ show (entropia koherensAllapot))
  putStrLn ("Zajos entropia:   " ++ show (entropia zajosAllapot))
  putStrLn ("Carnot hatásfok (T=300K, T0=300K): " ++ show (carnotHataskor 300.0 300.0))
  putStrLn ("Carnot hatásfok (T=300K, T0=100K): " ++ show (carnotHataskor 300.0 100.0))
  putStrLn ""

  -- 4. Lehetséges mód stabilitás
  putStrLn "─── 4. Lehetséges mód stabilitás ───"
  let stab1 = lehetsegesModStabilitas koherensAllapot 300.0 100.0
  let stab2 = lehetsegesModStabilitas zajosAllapot 300.0 100.0
  putStrLn ("Koherens stabilitás: " ++ show stab1)
  putStrLn ("Zajos stabilitás:   " ++ show stab2)
  putStrLn ("Koherens > Zajos? " ++ show (stab1 > stab2))
  putStrLn ""

  -- 5. Hibajavítás 3 szinten — külön-külön és együtt
  putStrLn "─── 5. Hibajavítás 3 szinten ───"
  putStrLn "  [1] Algebrai (Steane szindróma → 1 hibás fazis javítása)"
  let sz2 = algebraiJavitas zajosAllapot celAllapot
  putStrLn ("  Eredeti entropia:  " ++ show (entropia zajosAllapot))
  putStrLn ("  Algebrai után:    " ++ show (entropia sz2))

  putStrLn "  [2] Geometriai (Lagrangian geodézia → visszaprojektálás)"
  let sz3 = geometriaiJavitas sz2 celAllapot
  putStrLn ("  Geometriai után:  " ++ show (entropia sz3))

  putStrLn "  [3] Termodinamikai (Carnot → entropia csökkentés)"
  let sz4 = termodinamikaiJavitas sz3 celAllapot 100.0 1.0
  putStrLn ("  Termodinamikai után: " ++ show (entropia sz4))

  putStrLn ("  Cél entropia:        " ++ show (entropia celAllapot))
  putStrLn ""

  putStrLn "  Teljes lánc (2→3→4):"
  let javitott = teljesHibajavitas zajosAllapot celAllapot
  putStrLn ("  Eredeti → Javított: " ++ show (entropia zajosAllapot) ++ " → " ++ show (entropia javitott))
  putStrLn ""

  -- 6. E8×E8, E16, E15
  putStrLn "─── 6. Magasabb rendszerek ───"
  putStrLn ("E8×E8 dimenzió: " ++ show e8szorzesDimenzio)
  putStrLn ("E8×E8 gyökök:   " ++ show e8szorzesGyokok)
  putStrLn ("E16 dimenzió:    " ++ show e16Dimenzio)
  putStrLn ("E16 gyökök:      " ++ show e16Gyokok)
  putStrLn ("E15 dimenzió:    " ++ show e15Dimenzio)
  putStrLn ""

  -- 7. Steane 7 bit
  putStrLn "─── 7. Steane 7 bit: {idő, okság, tér, szín, hang, fázis, mód} ───"
  putStrLn ("steaneIndex Ido = " ++ show (steaneIndex Ido))
  putStrLn ("steaneIndex Mod = " ++ show (steaneIndex Mod))
  putStrLn ""

  -- 8. Strukturális bizonyítások
  putStrLn "─── 8. Strukturális bizonyítások ───"
  putStrLn ("allapotTerDim = " ++ show allapotTerDim ++ " (bizonyítás: 16×27=432)")
  putStrLn ("pslRend = " ++ show pslRend ++ " (bizonyítás: 8×3×7=168)")
  putStrLn ("teljesDim3D = " ++ show teljesDim3D ++ " = 432×7")
  putStrLn ("cptMaszk = " ++ show cptMaszk)
  putStrLn ""

  -- 9. QHMC: Quantum Hamiltonian Monte Carlo
  putStrLn "─── 9. QHMC mintavétel (leapfrog + Metropolis) ───"
  let kezdoMom = MkSebesseg [F1,F2,F3,F4,F5,F6,F7,F0] 0.0  -- nem nulla momentum
  let qhmcKezdo = MkQHMCAllapot zajosAllapot kezdoMom
  putStrLn ("Kezdeti H = " ++ show (qhmHamiltonian qhmcKezdo 1.0))
  let qhmc1 = qhmLepes qhmcKezdo 1.0 0.5 100.0
  putStrLn ("1 lépés után H = " ++ show (qhmHamiltonian qhmc1 1.0))
  putStrLn ("  Pozíció entropia: " ++ show (entropia (pozicio qhmc1)))
  let qhmc2 = qhmLepes qhmc1 1.0 0.5 100.0
  putStrLn ("2 lépés után H = " ++ show (qhmHamiltonian qhmc2 1.0))
  putStrLn ("  Pozíció entropia: " ++ show (entropia (pozicio qhmc2)))
  let qhmc3 = qhmLepes qhmc2 1.0 0.5 100.0
  putStrLn ("3 lépés után H = " ++ show (qhmHamiltonian qhmc3 1.0))
  putStrLn ("  Pozíció entropia: " ++ show (entropia (pozicio qhmc3)))
  let qhmc5 = qhmLepes (qhmLepes (qhmLepes qhmc3 1.0 0.5 100.0) 1.0 0.5 100.0) 1.0 0.5 100.0
  putStrLn ("5 lépés után H = " ++ show (qhmHamiltonian qhmc5 1.0))
  putStrLn ("  Pozíció entropia: " ++ show (entropia (pozicio qhmc5)))
  putStrLn ("Entropia változás: " ++ show (entropia (pozicio qhmcKezdo)) ++ " → " ++ show (entropia (pozicio qhmc5)))
