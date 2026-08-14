module Kereso

-- ═══════════════════════════════════════════════════════════════
-- KERESO — Magyar kerdes → valasz (bilingual szovegbol)
-- ═══════════════════════════════════════════════════════════════
-- A Carnot-ciklus harmadik lepese: kereses (munka) → valasz (energia).
-- A kerdest kodoljuk (Kodol.kodol), a szoveg minden mondatjat is,
-- es a legkisebb tavolsagu mondat a valasz.
-- Vesztesegmentes: a valasz = a megtalalt mondat szovege.
-- Determinisztikus: ugyanaz a kerdes → ugyanaz a valasz.
-- ═══════════════════════════════════════════════════════════════

import Steane713
import E8E8Algebra
import MagyarNyelvtan
import Kodol
import Tavolsag

-- ─── 1. BILINGUAL MONDAT ────────────────────────────────────

||| Egy bilingual mondat: magyar + angol + forras.
||| A magyar mondatbol kodoljuk az E8E8KodSzo-t.
||| A valasst a magyar + angol mondat egyutt adjak.
public export
record BilingualMondat where
  constructor BilingualKonstruktor
  magyar  : String
  angol   : String
  forras  : String
  kodSzo  : E8E8KodSzo

-- ─── 2. SZOVEG PARSZOLASA ───────────────────────────────────

||| HU:/EN:/SRC: formatum parszolasa List BilingualMondat-ta.
||| A bemenet a awodey_bilingual_ch1.txt fajl tartalma.
||| Minden harmas (HU/EN/SRC) egy BilingualMondat.
public export
data ParseAllapot = VarHU | VarEN | VarSRC | Keszen

||| Egy sorbol a cimke kinyerese: "HU: valami" → "valami"
public export
cimkeKinyer : String -> String
cimkeKinyer s =
  let cs = unpack s
  in  case cs of
        ('H' :: 'U' :: ':' :: ' ' :: marad) => pack marad
        ('E' :: 'N' :: ':' :: ' ' :: marad) => pack marad
        ('S' :: 'R' :: 'C' :: ':' :: ' ' :: marad) => pack marad
        _ => s

||| Sor tipusanak felismerese.
public export
sorTipus : String -> ParseAllapot
sorTipus s =
  let cs = unpack s
  in  case cs of
        ('H' :: 'U' :: ':' :: _) => VarHU
        ('E' :: 'N' :: ':' :: _) => VarEN
        ('S' :: 'R' :: 'C' :: ':' :: _) => VarSRC
        _ => Keszen

||| Sorok parszolasa BilingualMondat listava.
||| Egyszeru allapotgep: felismeri a HU/EN/SRC harmasokat.
public export
parszol : List String -> List BilingualMondat
parszol sorok = go sorok "" "" ""
  where
    go : List String -> String -> String -> String -> List BilingualMondat
    go [] hu en src =
      if hu /= "" && en /= ""
        then [BilingualKonstruktor hu en src (kodol hu)]
        else []
    go (s :: ss) hu en src =
      case sorTipus s of
        VarHU =>
          -- Ha mar van egy harmas, elmentjuk
          (if hu /= "" && en /= ""
             then [BilingualKonstruktor hu en src (kodol hu)]
             else []) ++
          go ss (cimkeKinyer s) "" ""
        VarEN => go ss hu (cimkeKinyer s) src
        VarSRC => go ss hu en (cimkeKinyer s)
        Keszen => go ss hu en src

-- ─── 3. KERESÉS ─────────────────────────────────────────────

||| Egy kerdes kodoszojanak tavolsaga minden bilingual mondathoz.
||| Visszaadja (tavolsag, BilingualMondat) parokat, rendezve.
public export
keresTavolsag : E8E8KodSzo -> List BilingualMondat -> List (Nat, BilingualMondat)
keresTavolsag kerdes mondatok =
  map (\m => (teljesTavolsag kerdes m.kodSzo, m)) mondatok

||| A legkisebb tavolsagu mondat = a valasz.
||| Ez a Carnot-ciklus kimenete: a megtalalt mondat = az energia.
public export
legkozelebbi : List (Nat, BilingualMondat) -> Maybe (Nat, BilingualMondat)
legkozelebbi [] = Nothing
legkozelebbi (x :: xs) = Just (legkisebb x xs)
  where
    legkisebb : (Nat, BilingualMondat) -> List (Nat, BilingualMondat) -> (Nat, BilingualMondat)
    legkisebb acc [] = acc
    legkisebb (d1, m1) ((d2, m2) :: rest) =
      if d2 < d1
        then legkisebb (d2, m2) rest
        else legkisebb (d1, m1) rest

||| A legkisebb N talalat (nem csak egy).
public export
legkozelebbiN : Nat -> List (Nat, BilingualMondat) -> List (Nat, BilingualMondat)
legkozelebbiN n xs = rendez xs
  where
    rendez : List (Nat, BilingualMondat) -> List (Nat, BilingualMondat)
    rendez [] = []
    rendez (y :: ys) =
      let kisebbek = filter (\z => fst z < fst y) ys
          nagyobbak = filter (\z => fst z >= fst y) ys
      in rendez kisebbek ++ [y] ++ rendez nagyobbak

-- ─── 4. VALASZ ──────────────────────────────────────────────

||| A valasz: a megtalalt mondat + a tavolsag + a hasonlosag.
public export
record Valasz where
  constructor ValaszKonstruktor
  magyarValasz  : String
  angolValasz   : String
  forrasHely    : String
  tavolsag      : Nat
  hasonlosagEr  : Hasonlosag

||| Egy kerdes → valasz a bilingual mondatok kozott.
||| Ez a teljes Carnot-ciklus:
|||   kerdes (entrópia) → kodol (információ) → keres (munka) → valasz (energia)
public export
keres : String -> List BilingualMondat -> Maybe Valasz
keres kerdesSzoveg mondatok =
  let kerdesKodSzo = kodol kerdesSzoveg
      tavolsagok = keresTavolsag kerdesKodSzo mondatok
  in  case legkozelebbi tavolsagok of
        Nothing => Nothing
        Just (d, m) => Just (ValaszKonstruktor m.magyar m.angol m.forras d (hasonlosag d))

-- ─── 5. FŐPROGRAM (teszt) ───────────────────────────────────

||| Teszt: par peldamondat kodolasa es kereses kozottuk.
||| A valodi fajl-beolvasas kulon kell (IO).
public export
keresoFom : IO ()
keresoFom = do
  putStrLn "=== KERESO — Magyar kerdes → valasz ==="
  putStrLn ""
  putStrLn "Teszt: 5 bilingual mondat + 3 kerdes"
  putStrLn ""
  -- Teszt mondatok (kezzel)
  let mondatok =
        [ BilingualKonstruktor
            "Egy kategória objektumokból és nyilakból áll."
            "A category consists of objects and arrows."
            "Awodey §1.3"
            (kodol "Egy kategória objektumokból és nyilakból áll.")
        , BilingualKonstruktor
            "A funktor két kategória közötti struktúramegőrző leképezés."
            "A functor is a structure-preserving map between two categories."
            "Awodey §7.1"
            (kodol "A funktor két kategória közötti struktúramegőrző leképezés.")
        , BilingualKonstruktor
            "Egy izomorfizmus egy invertálható morfizmus."
            "An isomorphism is an invertible morphism."
            "Awodey §1.5"
            (kodol "Egy izomorfizmus egy invertálható morfizmus.")
        , BilingualKonstruktor
            "Az objektum a kategória alapegysége."
            "An object is the basic unit of a category."
            "Awodey §1.3"
            (kodol "Az objektum a kategória alapegysége.")
        , BilingualKonstruktor
            "A kompozíció két morfizmus egymás utáni alkalmazása."
            "Composition is the application of two morphisms in sequence."
            "Awodey §1.3"
            (kodol "A kompozíció két morfizmus egymás utáni alkalmazása.")
        ]
  -- Kerdések
  putStrLn "Kérdés 1: 'Mi az a kategória?'"
  case keres "Mi az a kategória?" mondatok of
    Just v => do
      putStrLn ("  Válasz (HU): " ++ v.magyarValasz)
      putStrLn ("  Válasz (EN): " ++ v.angolValasz)
      putStrLn ("  Forrás: " ++ v.forrasHely)
      putStrLn ("  Távolság: " ++ show v.tavolsag ++ " (" ++ show v.hasonlosagEr ++ ")")
    Nothing => putStrLn "  Nincs találat."
  putStrLn ""
  putStrLn "Kérdés 2: 'Mi az a funktor?'"
  case keres "Mi az a funktor?" mondatok of
    Just v => do
      putStrLn ("  Válasz (HU): " ++ v.magyarValasz)
      putStrLn ("  Válasz (EN): " ++ v.angolValasz)
      putStrLn ("  Forrás: " ++ v.forrasHely)
      putStrLn ("  Távolság: " ++ show v.tavolsag ++ " (" ++ show v.hasonlosagEr ++ ")")
    Nothing => putStrLn "  Nincs találat."
  putStrLn ""
  putStrLn "Kérdés 3: 'Hol van az objektum?'"
  case keres "Hol van az objektum?" mondatok of
    Just v => do
      putStrLn ("  Válasz (HU): " ++ v.magyarValasz)
      putStrLn ("  Válasz (EN): " ++ v.angolValasz)
      putStrLn ("  Forrás: " ++ v.forrasHely)
      putStrLn ("  Távolság: " ++ show v.tavolsag ++ " (" ++ show v.hasonlosagEr ++ ")")
    Nothing => putStrLn "  Nincs találat."
  putStrLn ""
  putStrLn "Kész."