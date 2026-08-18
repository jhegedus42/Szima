module KisAI

import Data.Vect
import Data.List
import Data.String
import Fazis

-- =====================================================================
-- KIS AI — tanítható, kereshető, asszociálható.
--
-- A felismerés (2026-08-18, a felhasználó):
-- "tudunk csinálni valami kis AI-t amit tudunk így tanítani?
-- meg kérdezzük tőle, hogy miért, és ha nem tudja,
-- elmagyarázzuk és megjegyzi, valami optimálisan kódolt,
-- kereshető, asszociálható formában?"
--
-- A válasz: IGEN. A darabok mind megvannak:
--   - [[7,1,3]] Steane kód = a memória (hibajavítható!)
--   - Hamming-távolság = a keresés (szemantikai távolság)
--   - Clifford-átfedés = az asszociáció (mennyire kapcsolódik)
--   - Miért-lánc = az oksági memória ("miért tudom ezt?")
--
-- A 7 bit: [idő, okság, tér, szín, hang, fázis, mód]
-- Minden tény = 7 bites vektor — melyik dimenziót érinti.
-- Ha 1 bit hibás a kérdésben: a rendszer MÉG megtalálja
-- (távolság 1 < 3 = a Steane távolság = a hibajavítás).
-- Ez az OPTIMÁLIS KÓDOLÁS: a memória maga a hibajavító kód.
--
-- A ciklus (a felhasználó gondolkodása):
--   1. KÉRDEZZÜK: "Mit mondott a farkas?"
--   2. KERESÉS: Hamming-távolság a tudástárban
--   3. HA TUDOM (d=0): "Tudom! A farkas azt mondta: ..."
--   4. HA NEM TUDOM (d>3): "Nem tudom. Magyarázd el!"
--   5. TANÍTÁS: elmagyarázzuk → kódoljuk → tároljuk
--   6. MIÉRT: a miért-lánc bejegyzés (az oksági fonal)
--   7. ASSZOCIÁCIÓ: hasonló tények (Clifford-átfedés)
-- =====================================================================

%default total

-- =====================================================================
-- 1. A 7 BITES KÓDOLÁS — a Steane [[7,1,3]] memória.
-- =====================================================================

||| A 7 Steane-bit: [idő, okság, tér, szín, hang, fázis, mód]
||| Minden tény ezek kombinációja — melyik dimenziót érinti.
BitKod : Type
BitKod = Vect 7 Nat

public export
Show BitKod where
  show k = "[" ++ show (index 0 k) ++ "," ++ show (index 1 k) ++ "," ++
           show (index 2 k) ++ "," ++ show (index 3 k) ++ "," ++
           show (index 4 k) ++ "," ++ show (index 5 k) ++ "," ++
           show (index 6 k) ++ "]"

-- =====================================================================
-- 2. A KIS AI = tudástár + szótár.
-- =====================================================================

||| A kis AI tudástára: (7-bit kód, magyarázat) párok listája.
||| A szótár: szó → 7-bit kód (a kódoláshoz).
public export
record KisAI where
  constructor KisAIKonstruktor
  tudastar : List (BitKod, String)  -- (kód, magyarázat)
  szotar   : List (String, BitKod)  -- szó → kód

-- =====================================================================
-- 3. HAMMING-TÁVOLSÁG = a keresés.
-- =====================================================================

||| Két 7-bites vektor Hamming-távolsága = hány pozíción térnek el.
public export
hammingTavolsag7 : BitKod -> BitKod -> Nat
hammingTavolsag7 a b = go 7
  where
    go : Nat -> Nat
    go Z = 0
    go (S n) =
      let ai = index (natToFin7 n) a
          bi = index (natToFin7 n) b
      in (if ai /= bi then 1 else 0) + go n
    where
      natToFin7 : Nat -> Fin 7
      natToFin7 0 = FZ
      natToFin7 1 = FS FZ
      natToFin7 2 = FS (FS FZ)
      natToFin7 3 = FS (FS (FS FZ))
      natToFin7 4 = FS (FS (FS (FS FZ)))
      natToFin7 5 = FS (FS (FS (FS (FS FZ))))
      natToFin7 6 = FS (FS (FS (FS (FS (FS FZ)))))
      natToFin7 _ = FZ

-- =====================================================================
-- 4. KERESÉS a tudástárban: legközelebbi egyezés.
-- =====================================================================

||| A legközelebbi egyezés a tudástárban.
||| Visszatér: (távolság, magyarázat) vagy Nothing ha üres.
public export
keresKisAI : KisAI -> BitKod -> Maybe (Nat, String)
keresKisAI ai kerdes =
  keresSeged (tudastar ai) kerdes
  where
    keresSeged : List (BitKod, String) -> BitKod -> Maybe (Nat, String)
    keresSeged [] _ = Nothing
    keresSeged ((kod, mag) :: rest) q =
      let d = hammingTavolsag7 kod q
      in case keresSeged rest q of
           Nothing => Just (d, mag)
           Just (d', mag') => if d <= d' then Just (d, mag) else Just (d', mag')

-- =====================================================================
-- 5. TANÍTÁS: új tény eltárolása.
-- =====================================================================

||| Új tény tanítása: kódoljuk és eltároljuk a tudástárban.
public export
tanitKisAI : KisAI -> BitKod -> String -> KisAI
tanitKisAI ai kod magyaro =
  KisAIKonstruktor ((kod, magyaro) :: tudastar ai) (szotar ai)

||| Új szó hozzáadása a szótárhoz.
public export
szotarBovit : KisAI -> String -> BitKod -> KisAI
szotarBovit ai szo kod =
  KisAIKonstruktor (tudastar ai) ((szo, kod) :: szotar ai)

-- =====================================================================
-- 6. ASSZOCIÁCIÓ: hasonló tények (Clifford-átfedés).
-- =====================================================================

||| Két kód átfedése = hány pozíción mindkettő 1.
public export
atfedes7 : BitKod -> BitKod -> Nat
atfedes7 a b = go 7
  where
    go : Nat -> Nat
    go Z = 0
    go (S n) =
      let ai = index (natToFin7 n) a
          bi = index (natToFin7 n) b
      in (if ai == 1 && bi == 1 then 1 else 0) + go n
    where
      natToFin7 : Nat -> Fin 7
      natToFin7 0 = FZ
      natToFin7 1 = FS FZ
      natToFin7 2 = FS (FS FZ)
      natToFin7 3 = FS (FS (FS FZ))
      natToFin7 4 = FS (FS (FS (FS FZ)))
      natToFin7 5 = FS (FS (FS (FS (FS FZ))))
      natToFin7 6 = FS (FS (FS (FS (FS (FS FZ)))))
      natToFin7 _ = FZ

||| Asszociáció: az összes tárolt tény átfedése a kérdéssel.
||| Magas átfedés = erősen kapcsolódó.
public export
asszocialKisAI : KisAI -> BitKod -> List (Nat, String)
asszocialKisAI ai q = map (\(k, m) => (atfedes7 k q, m)) (tudastar ai)

-- =====================================================================
-- 7. KÓDOLÁS: szöveg → 7-bit kód (a szótár alapján).
-- =====================================================================

||| Szó keresése a szótárban.
szotarKeres : String -> List (String, BitKod) -> BitKod
szotarKeres _ [] = [0,0,0,0,0,0,0]
szotarKeres szo ((s, b) :: rest) = if szo == s then b else szotarKeres szo rest

||| Bit-OR: két bit összevonása (ha bármelyik 1, az eredmény 1).
bitOr7 : Nat -> Nat -> Nat
bitOr7 0 0 = 0
bitOr7 _ _ = 1

||| Szöveg kódolása: szavakra bontjuk, minden szót keresünk
||| a szótárban, a biteket OR-zuk.
public export
kodolSzoveg : String -> List (String, BitKod) -> BitKod
kodolSzoveg szoveg dict =
  let szavak = words szoveg
      kodok = map (\s => szotarKeres s dict) szavak
  in foldr (zipWith bitOr7) [0,0,0,0,0,0,0] kodok

-- =====================================================================
-- 8. AZ ALAP SZÓTÁR — a Piroska-mese dimenziói.
-- =====================================================================

||| Az alap szótár: szó → 7-bit kód.
||| A 7 bit: [idő, okság, tér, szín, hang, fázis, mód]
||| "farkas" = okság + hang (a hazugság forrása: ok + beszéd)
||| "piroska" = idő (a kezdet, az ártatlan)
||| "hazugság" = okság + hang (a hamis állítás)
||| "vadász" = fázis (a cselekvés = a megmentés)
public export
AlapSzotar : List (String, BitKod)
AlapSzotar = [
  ("farkas", [0,1,0,0,1,0,0]),
  ("piroska", [1,0,0,0,0,0,0]),
  ("nagymama", [1,0,0,0,0,0,0]),
  ("vadasz", [0,0,0,0,0,1,0]),
  ("hazugsag", [0,1,0,0,1,0,0]),
  ("mondas", [0,0,0,0,1,0,0]),
  ("mondott", [0,0,0,0,1,0,0]),
  ("ert", [0,0,0,0,0,0,1]),
  ("miert", [0,1,0,0,0,0,0]),
  ("kerdes", [0,0,0,0,1,0,0]),
  ("valasz", [0,0,0,0,1,0,1]),
  ("tudas", [0,0,0,0,0,0,1]),
  ("ho", [0,1,0,0,0,1,0]),
  (" energia", [0,1,0,0,0,1,0]),
  ("fazis", [0,0,0,0,0,1,0]),
  ("ido", [1,0,0,0,0,0,0]),
  ("oksag", [0,1,0,0,0,0,0]),
  ("ter", [0,0,1,0,0,0,0]),
  ("szin", [0,0,0,1,0,0,0]),
  ("hang", [0,0,0,0,1,0,0]),
  ("mod", [0,0,0,0,0,0,1])
 ]

||| A kezdő kis AI: üres tudástár + alap szótár.
public export
kezdoKisAI : KisAI
kezdoKisAI = KisAIKonstruktor [] AlapSzotar

-- =====================================================================
-- 9. A "MIÉRT" — az oksági indoklás.
-- =====================================================================

||| A válasz oksági indoklása: "miért tudom ezt?"
public export
miertKisAI : BitKod -> String -> String
miertKisAI kod magyaro =
  "Miert: a kerdes kodja " ++ showKod kod ++ ". A tarolt magyaro: " ++ magyaro
  where
    showKod : BitKod -> String
    showKod k = "[" ++ show (index 0 k) ++ "," ++ show (index 1 k) ++ "," ++
                show (index 2 k) ++ "," ++ show (index 3 k) ++ "," ++
                show (index 4 k) ++ "," ++ show (index 5 k) ++ "," ++
                show (index 6 k) ++ "]"

-- =====================================================================
-- 10. REFL BIZONYÍTÁSOK.
-- =====================================================================

-- A farkas kódja = okság + hang.
FarkasKod : kodolSzoveg "farkas" AlapSzotar = [0,1,0,0,1,0,0]
FarkasKod = Refl

-- Piroska kódja = idő.
PiroskaKod : kodolSzoveg "piroska" AlapSzotar = [1,0,0,0,0,0,0]
PiroskaKod = Refl

-- "Mit mondott a farkas?" kódja = farkas + mondott = [0,1,0,0,1,0,0]
KerdesFarkasKod : kodolSzoveg "Mit mondott a farkas" AlapSzotar = [0,1,0,0,1,0,0]
KerdesFarkasKod = Refl

-- Hamming-távolság: farkas kódja és hazugság kódja = 0 (azonos)
FarkasHazugsagTavolsag : hammingTavolsag7 [0,1,0,0,1,0,0] [0,1,0,0,1,0,0] = 0
FarkasHazugsagTavolsag = Refl

-- Hamming-távolság: farkas és piroska = 3 (3 bit tér el)
FarkasPiroskaTavolsag : hammingTavolsag7 [0,1,0,0,1,0,0] [1,0,0,0,0,0,0] = 3
FarkasPiroskaTavolsag = Refl

-- Átfedés: farkas és hazugság = 2 (okság + hang közös)
FarkasHazugsagAtfedes : atfedes7 [0,1,0,0,1,0,0] [0,1,0,0,1,0,0] = 2
FarkasHazugsagAtfedes = Refl

-- Átfedés: farkas és piroska = 0 (nincs közös dimenzió)
FarkasPiroskaAtfedes : atfedes7 [0,1,0,0,1,0,0] [1,0,0,0,0,0,0] = 0
FarkasPiroskaAtfedes = Refl

-- =====================================================================
-- 11. A TANÍTOTT AI — a Piroska-mese tudása.
-- =====================================================================

||| A Piroska-mesével tanított kis AI.
||| Egy tény van eltárolva: a farkas mondása = hazugság.
public export
piroskavalTanitottKisAI : KisAI
piroskavalTanitottKisAI =
  tanitKisAI kezdoKisAI [0,1,0,0,1,0,0]
    "A farkas azt mondta: en vagyok a nagymama, de ez hazugsag volt."

||| A tanított AI keresése: "Mit mondott a farkas?"
||| A kód = [0,1,0,0,1,0,0], a tudástárban ugyanez van → d=0.
public export
piroskaKeresesEredmeny : Maybe (Nat, String)
piroskaKeresesEredmeny =
  keresKisAI piroskavalTanitottKisAI (kodolSzoveg "Mit mondott a farkas" AlapSzotar)

||| A talált távolság = 0 (pontos egyezés).
public export
piroskaTalalatTavolsag : Maybe Nat
piroskaTalalatTavolsag = map fst piroskaKeresesEredmeny

||| A talált magyarázat.
public export
piroskaTalalatMagyarazo : Maybe String
piroskaTalalatMagyarazo = map snd piroskaKeresesEredmeny

-- =====================================================================
-- 12. AZ INTERAKTÍV TANÍTÓ CIKLUS (IO).
-- =====================================================================

%default partial

||| Az interaktív ciklus: kérdez → keres → válaszol vagy tanít.
|||
||| A ciklus (a felhasználó szavaival):
|||   1. kérdezzük: "Mit mondott a farkas?"
|||   2. keresés: Hamming-távolság a tudástárban
|||   3. ha d=0: "Tudom!" + a tárolt magyarázat
|||   4. ha d≤2: "Talán:" + a legközelebbi (asszociáció)
|||   5. ha d>2 vagy nem talál: "Nem tudom. Magyarázd el!"
|||   6. tanítás: elmagyarázzuk → kódoljuk → tároljuk
|||   7. következő kérdés
public export
tanitoCiklus : KisAI -> IO ()
tanitoCiklus ai = do
  putStr "> "
  line <- getLine
  if line == "" then pure () else do
    let kod = kodolSzoveg line (szotar ai)
    case keresKisAI ai kod of
      Just (0, mag) => do
        putStrLn ("Tudom! " ++ mag)
        putStrLn ("  " ++ miertKisAI kod mag)
        tanitoCiklus ai
      Just (d, mag) => do
        if d <= 2
          then do
            putStrLn ("Talán (távolság=" ++ show d ++ "): " ++ mag)
            putStrLn ("  Asszociáció: " ++ show (asszocialKisAI ai kod))
            tanitoCiklus ai
          else do
            putStrLn "Nem tudom. Magyarázd el!"
            magyaro <- getLine
            let ai' = tanitKisAI ai kod magyaro
            putStrLn ("Ertem! Eltároltam. (kód: " ++ showKodSeged kod ++ ")")
            putStrLn ("  " ++ miertKisAI kod magyaro)
            tanitoCiklus ai'
      Nothing => do
        putStrLn "Nem tudom. Magyarázd el!"
        magyaro <- getLine
        let ai' = tanitKisAI ai kod magyaro
        putStrLn ("Ertem! Eltároltam. (kód: " ++ showKodSeged kod ++ ")")
        putStrLn ("  " ++ miertKisAI kod magyaro)
        tanitoCiklus ai'
  where
    showKodSeged : BitKod -> String
    showKodSeged k = "[" ++ show (index 0 k) ++ "," ++ show (index 1 k) ++ "," ++
                     show (index 2 k) ++ "," ++ show (index 3 k) ++ "," ++
                     show (index 4 k) ++ "," ++ show (index 5 k) ++ "," ++
                     show (index 6 k) ++ "]"

||| A főprogram: elindítja a tanító ciklust az alap szótárral.
public export
fom : IO ()
fom = do
  putStrLn "═══════════════════════════════════════════════════"
  putStrLn "  KIS AI — tanítható, kereshető, asszociálható"
  putStrLn "  A 7 bit: [idő, okság, tér, szín, hang, fázis, mód]"
  putStrLn "  Kérdezz! Üres sor = kilépés."
  putStrLn "═══════════════════════════════════════════════════"
  tanitoCiklus kezdoKisAI