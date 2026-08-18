module Main3D

import Kina2D
import Magyar
import Dirac3D
import Data.List

-- =====================================================================
-- Bemutató: a 3D nyelv működés közben.
--
-- A program futtatása megmutatja:
--   1. Példa 3D ketek (kínai × magyar)
--   2. Szótípusfüggő távolságok kiszámítása
--   3. CPT involúció teszt (CPT² = I ellenőrzés)
--   4. Strukturális bizonyítások (dimenzió, PSL rendje)
-- =====================================================================

-- =====================================================================
-- 1. Példa 3D ketek összeállítása.
-- =====================================================================

||| Kínai karakterek (Kina2D példák) és magyar szavak párosítása 3D kettősségekbe.
||| Minden pár: (karakter, szó, szemantikai horgony)
harmadDimPeldak : List Ket3D
harmadDimPeldak =
  [ -- 明 (bright) ⊗ ház(in houses)
    MkKet3D
      (head peldaKarakterek)
      (elemzesToKet (elemzes "házakban"))
      "ház"
  , -- 明 (bright) ⊗ ház(house) — nominatívusz
    MkKet3D
      (head peldaKarakterek)
      (elemzesToKet (elemzes "ház"))
      "ház"
  , -- 休 (rest) ⊗ futott(ran)
    MkKet3D
      (head (drop 1 peldaKarakterek))
      (elemzesToKet (elemzes "futott"))
      "futás"
  , -- 森 (forest) ⊗ futás(in running)
    MkKet3D
      (head (drop 7 peldaKarakterek))
      (elemzesToKet (elemzes "futás"))
      "sűrű"
  , -- 仙 (immortal) ⊗ ég(skies)
    MkKet3D
      (head (drop 5 peldaKarakterek))
      (elemzesToKet (elemzes "égbolt"))
      "ég"
  ]

-- =====================================================================
-- 2. Páros távolságok kiszámítása.
-- =====================================================================

||| Szótípus meghatározása: ha a kínai kompozíció Egyeduli, akkor főnév/állapot.
||| Ha nem Egyeduli, és a magyar feature != 0, akkor morfizmus/művelet.
szotipusKerdes : Karakter2D -> Ket1D -> Szotipus
szotipusKerdes ch w =
  if fanoPont (kompo ch) == 6
     then FonevAllapot
     else if ketFeat w == 0
            then FonevAllapot
            else MorfMuvelet

||| Egy pár távolságainak kiírása.
parTavolsag : Ket3D -> Ket3D -> String
parTavolsag k1 k2 =
  let tipus = szotipusKerdes (char2D k1) (word1D k1)
      d3 = tavolsag3D tipus k1 k2
      d2 = tavolsag2D (char2D k1) (char2D k2)
      d1 = tavolsag1D (word1D k1) (word1D k2)
      (alpha, beta) = tavolsagSulyok tipus
  in "  tipus=" ++ show tipus ++
     "  d3D=" ++ show d3 ++ " (a=" ++ show alpha ++ ",b=" ++ show beta ++ ")" ++
     "  d2D=" ++ show d2 ++ "  d1D=" ++ show d1

||| Összes páros távolság.
osszesPar : List Ket3D -> List String
osszesPar [] = []
osszesPar (x :: xs) = map (parTavolsag x) xs ++ osszesPar xs

-- =====================================================================
-- 3. Main: futtatás.
-- =====================================================================

main : IO ()
main = do
  putStrLn "═══════════════════════════════════════════════════"
  putStrLn "  3D NYELV: Kínai(2D) × Magyar(1D)"
  putStrLn "  Direkt szorzat írásrendszer Dirac jelölésben"
  putStrLn "═══════════════════════════════════════════════════"
  putStrLn ""

  putStrLn "─── Példa 3D nyelvi elemek ───"
  traverse_ (\k => do putStrLn ""; putStrLn (showKet3D k)) harmadDimPeldak

  putStrLn ""
  putStrLn "─── CPT involúció teszt ───"
  let k0 = head harmadDimPeldak
  putStrLn ("Eredeti: " ++ show (ketFeat (word1D k0)))
  let cptK = cpt3D k0
  putStrLn ("CPT után: " ++ show (ketFeat (word1D cptK)))
  let cpt2K = cpt3D cptK
  putStrLn ("CPT² után: " ++ show (ketFeat (word1D cpt2K)))
  putStrLn ("CPT² = I? " ++ show (ketFeat (word1D cpt2K) == ketFeat (word1D k0)))

  putStrLn ""
  putStrLn "─── Szótípusfüggő távolságok ───"
  traverse_ (\s => do putStrLn "") (osszesPar harmadDimPeldak)

  putStrLn ""
  putStrLn "─── Strukturális bizonyítások ───"
  putStrLn ("allapotTerDim = " ++ show allapotTerDim ++ " (bizonyítás: 16×27=432)")
  putStrLn ("pslRend = " ++ show pslRend ++ " (bizonyítás: 8×3×7=168)")
  putStrLn ("teljesDim3D = " ++ show teljesDim3D ++ " = 432×7")
  putStrLn ("cptMaszk = " ++ show cptMaszk)
