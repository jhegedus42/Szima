module Kodol

-- ═══════════════════════════════════════════════════════════════
-- KODOL — Magyar mondat → E8E8KodSzo (Kubit alapon)
-- ═══════════════════════════════════════════════════════════════
-- A kódoló a Carnot-ciklus első lépése: entrópia (kérdés) → információ (kód).
-- Veszteségmentes: a cimke tartalmazza a mondatot, a kód csak index.
-- Nincs Double — minden Kubit (Nulla | Egy).
-- ═══════════════════════════════════════════════════════════════

import Steane713
import E8E8Algebra
import MagyarNyelvtan

-- ─── 1. SZÓTÁR — Fogalom → E8Pont (Kubit) ───────────────────

||| A fogalom szótár: magyar szó → E8Pont (8 Kubit).
||| Kezdetben a 1. fejezet fő fogalmai (Awodey).
public export
fogalomSzotar : List (String, E8Pont)
fogalomSzotar =
  [ ("kategória",    E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Nulla Nulla Nulla)
  , ("kategoria",    E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Nulla Nulla Nulla)
  , ("objektum",     E8PontKonstruktor Nulla Egy Nulla Nulla Nulla Nulla Nulla Nulla)
  , ("morfizmus",    E8PontKonstruktor Nulla Nulla Egy Nulla Nulla Nulla Nulla Nulla)
  , ("nyil",         E8PontKonstruktor Nulla Nulla Egy Nulla Nulla Nulla Nulla Nulla)
  , ("funktor",      E8PontKonstruktor Nulla Nulla Nulla Egy Nulla Nulla Nulla Nulla)
  , ("izomorfizmus", E8PontKonstruktor Nulla Nulla Nulla Nulla Egy Nulla Nulla Nulla)
  , ("izomorfizmust", E8PontKonstruktor Nulla Nulla Nulla Nulla Egy Nulla Nulla Nulla)
  , ("halmaz",       E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Egy Nulla Nulla)
  , ("fuggveny",     E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("függvény",     E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("identitas",    E8PontKonstruktor Egy Egy Nulla Nulla Nulla Nulla Nulla Nulla)
  , ("kompozicio",   E8PontKonstruktor Nulla Nulla Egy Egy Nulla Nulla Nulla Nulla)
  , ("szabad",       E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla Egy)
  , ("alap",         E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Nulla Nulla Egy)
  , ("szem",         E8PontKonstruktor Egy Nulla Nulla Nulla Egy Nulla Nulla Nulla)
  , ("lét",          E8PontKonstruktor Nulla Egy Nulla Nulla Egy Nulla Nulla Nulla)
  , ("let",          E8PontKonstruktor Nulla Egy Nulla Nulla Egy Nulla Nulla Nulla)
  , ("élet",         E8PontKonstruktor Nulla Egy Egy Nulla Egy Nulla Nulla Nulla)
  , ("élni",         E8PontKonstruktor Nulla Egy Egy Nulla Egy Nulla Nulla Nulla)
  , ("fog",          E8PontKonstruktor Nulla Nulla Nulla Egy Nulla Egy Nulla Nulla)
  , ("lé",            E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("víz",          E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("fény",         E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Nulla Nulla Nulla)
  , ("pillanat",     E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla Egy)
  -- József Attila: Tudod, hogy nincs bocsánat (1937)
  , ("bocsanat",     E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Egy Nulla Nulla)
  , ("bocsánat",     E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Egy Nulla Nulla)
  , ("bun",          E8PontKonstruktor Nulla Egy Nulla Nulla Nulla Egy Nulla Nulla)
  , ("bűn",          E8PontKonstruktor Nulla Egy Nulla Nulla Nulla Egy Nulla Nulla)
  , ("konny",        E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("könny",        E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("sziv",         E8PontKonstruktor Egy Nulla Nulla Egy Nulla Nulla Nulla Nulla)
  , ("szív",         E8PontKonstruktor Egy Nulla Nulla Egy Nulla Nulla Nulla Nulla)
  , ("fegyver",      E8PontKonstruktor Nulla Nulla Nulla Egy Nulla Egy Nulla Nulla)
  , ("pszichoanalizis", E8PontKonstruktor Nulla Nulla Egy Nulla Nulla Egy Egy Nulla)
  , ("carnot",       E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla Egy)
  , ("carnot-ciklus", E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla Egy)
  , ("dekoherencia", E8PontKonstruktor Nulla Nulla Egy Nulla Nulla Nulla Nulla Egy)
  , ("entropia",     E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla)
  , ("hibajavitas",  E8PontKonstruktor Egy Nulla Nulla Nulla Egy Nulla Nulla Egy)
  ]

public export
fogalomKeres : String -> Maybe E8Pont
fogalomKeres szo = keres szo fogalomSzotar
  where
    keres : String -> List (String, E8Pont) -> Maybe E8Pont
    keres _ [] = Nothing
    keres s ((nev, pont) :: xs) =
      if s == nev then Just pont else keres s xs

-- ─── 2. ESETRAG → E8Pont (Kubit) ────────────────────────────

||| Az esetrag E8 kódja (jobb E8 = szín = fázis).
||| 18 eset → 8 Kubit.
public export
esetKod : Esetrag -> E8Pont
esetKod NominativusE     = E8PontKonstruktor Egy Nulla Nulla Egy Nulla Nulla Nulla Nulla
esetKod AccusativusE     = E8PontKonstruktor Egy Nulla Nulla Nulla Egy Nulla Nulla Nulla
esetKod DativusE         = E8PontKonstruktor Egy Nulla Nulla Nulla Nulla Egy Nulla Nulla
esetKod InessivusE       = E8PontKonstruktor Nulla Egy Egy Nulla Nulla Nulla Nulla Nulla
esetKod ElativusE        = E8PontKonstruktor Nulla Egy Nulla Egy Nulla Nulla Nulla Nulla
esetKod IllativusE       = E8PontKonstruktor Nulla Egy Nulla Nulla Egy Nulla Nulla Nulla
esetKod SuperessivusE    = E8PontKonstruktor Nulla Egy Egy Nulla Nulla Nulla Nulla Nulla
esetKod AdessivusE       = E8PontKonstruktor Nulla Egy Nulla Nulla Nulla Egy Nulla Nulla
esetKod DelativusE       = E8PontKonstruktor Nulla Nulla Egy Egy Nulla Nulla Nulla Nulla
esetKod AblativusE       = E8PontKonstruktor Nulla Nulla Egy Nulla Egy Nulla Nulla Nulla
esetKod SublativusE      = E8PontKonstruktor Nulla Nulla Nulla Egy Egy Nulla Nulla Nulla
esetKod AllativusE       = E8PontKonstruktor Nulla Nulla Nulla Egy Nulla Egy Nulla Nulla
esetKod TerminativusE    = E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Egy Nulla
esetKod InstrumentalisE  = E8PontKonstruktor Nulla Nulla Nulla Nulla Egy Nulla Egy Nulla
esetKod CausalisFinalisE = E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Egy Egy Nulla
esetKod TranszlativusE   = E8PontKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla Egy
esetKod FormativusE      = E8PontKonstruktor Nulla Nulla Nulla Nulla Egy Egy Nulla Nulla
esetKod EssivusFormalisE = E8PontKonstruktor Nulla Nulla Nulla Nulla Egy Nulla Nulla Egy

-- ─── 3. CPT → CliffordElem (Kubit) ──────────────────────────

||| A CPT (igeidő/szemlélet/forrás) → CliffordElem (3 Kubit).
||| T (igeidő) → skalar: mult=Egy, jelen=Nulla, jovo=Nulla (nem morfologiai)
||| P (szemlelet) → vektor: befejezett=Egy, folyamatos=Nulla, szokasos=Egy
||| C (forras) → bivektor: kovetkeztetett=Egy, kozvetlen=Nulla, jelentett=Egy
public export
cptKod : CptIgeragozas -> CliffordElem
cptKod cpt =
  let t = case cpt.cptT of
            (JelenI) => Nulla
            (MultI)  => Egy
            (JovoI)  => Nulla  -- a fog = P, nem T
      p = case cpt.cptP of
            (FolyamatosSz)  => Nulla
            (BefejezettSz)  => Egy
            (SzokasosSz)    => Egy  -- szokasos = returning (ismetles) = Egy
      c = case cpt.cptC of
            (KozvetlenF)    => Nulla
            (KovetkeztetettF) => Egy
            (JelentettF)    => Egy
  in CliffordKonstruktor t p c

-- ─── 4. 7 BIT → HetesKod ────────────────────────────────────

||| A Steane [[7,1,3]] 7 bitje: [idő, okság, tér, szín, hang, fázis, mód]
public export
esetBit : Esetrag -> Nat -> Kubit
esetBit eset pos =
  let bitErtek : Nat =
        (if pos == 1 then (if eset == CausalisFinalisE then 1 else 0) else 0) +
        (if pos == 2 then (case esetragFunkcio eset of
                              HelyHely => 1
                              HelyIrany => 1
                              _ => 0) else 0) +
        (if pos == 3 then (case esetragFunkcio eset of
                              AllapotHatarozo => 1
                              _ => 0) else 0) +
        (if pos == 4 then (if eset == InstrumentalisE then 1 else 0) else 0) +
        (if pos == 5 then (case eset of
                              DativusE => 1
                              AllativusE => 1
                              _ => 0) else 0) +
        (if pos == 6 then (case eset of
                              FormativusE => 1
                              _ => 0) else 0)
  in if bitErtek > 0 then Egy else Nulla

public export
mondatSteane : Esetrag -> Igeido -> HetesKod
mondatSteane eset igeido =
  HetesKonstruktor
    (case igeido of (MultI) => Egy; _ => Nulla)
    (esetBit eset 1)
    (esetBit eset 2)
    (esetBit eset 3)
    (esetBit eset 4)
    (esetBit eset 5)
    (esetBit eset 6)

-- ─── 5. SEGÉDFÜGGVÉNYEK ─────────────────────────────────────

||| String felosztása egy karakter szerint.
public export
splitOnChar : Char -> String -> List String
splitOnChar c s = go (unpack s)
  where
    go : List Char -> List String
    go [] = [""]
    go (x :: xs) =
      if x == c
        then "" :: go xs
        else case go xs of
               (elso :: tobbi) => (strCons x elso) :: tobbi
               [] => [strCons x ""]

||| Irasjelek levagasa a szo vegerol + kisbetusites.
public export
kisbetusit : Char -> Char
kisbetusit 'A' = 'a'; kisbetusit 'B' = 'b'; kisbetusit 'C' = 'c'
kisbetusit 'D' = 'd'; kisbetusit 'E' = 'e'; kisbetusit 'F' = 'f'
kisbetusit 'G' = 'g'; kisbetusit 'H' = 'h'; kisbetusit 'I' = 'i'
kisbetusit 'J' = 'j'; kisbetusit 'K' = 'k'; kisbetusit 'L' = 'l'
kisbetusit 'M' = 'm'; kisbetusit 'N' = 'n'; kisbetusit 'O' = 'o'
kisbetusit 'P' = 'p'; kisbetusit 'Q' = 'q'; kisbetusit 'R' = 'r'
kisbetusit 'S' = 's'; kisbetusit 'T' = 't'; kisbetusit 'U' = 'u'
kisbetusit 'V' = 'v'; kisbetusit 'W' = 'w'; kisbetusit 'X' = 'x'
kisbetusit 'Y' = 'y'; kisbetusit 'Z' = 'z'
kisbetusit 'Á' = 'á'; kisbetusit 'É' = 'é'; kisbetusit 'Í' = 'í'
kisbetusit 'Ó' = 'ó'; kisbetusit 'Ö' = 'ö'; kisbetusit 'Ő' = 'ő'
kisbetusit 'Ú' = 'ú'; kisbetusit 'Ü' = 'ü'; kisbetusit 'Ű' = 'ű'
kisbetusit c = c

||| Irasjelek levagasa + kisbetusites.
public export
irasjelLevagas : String -> String
irasjelLevagas s = pack (go (map kisbetusit (unpack s)))
  where
    go : List Char -> List Char
    go [] = []
    go (x :: xs) =
      if x == '?' || x == '!' || x == '.' || x == ',' || x == ';' || x == ':'
        then go xs
        else x :: go xs

-- ─── 6. MONDAT → E8E8KodSzo ─────────────────────────────────

||| A teljes kódolás: magyar mondat → E8E8KodSzo.
||| Veszteségmentes: a cimke tartalmazza a mondatot.
public export
kodol : String -> E8E8KodSzo
kodol mondat =
  let szavak = map irasjelLevagas (splitOnChar ' ' mondat)
      esetKerdes = keresKerdoszo szavak
      esetRag = case esetKerdes of
                  Just e => e
                  Nothing => case szavak of
                              (elsoSzo :: _) => case ragFelismer elsoSzo of
                                                  Just (_, e) => e
                                                  Nothing => NominativusE
                              [] => NominativusE
      fogalomPont = keresFogalom szavak
      balE8Pont = case fogalomPont of
                    Just p => p
                    Nothing => e8Nulla
      jobbE8Pont = esetKod esetRag
      harmadikE8Pont = e8Nulla  -- hang: majd szóelemzésből
      negyedikE8Pont = e8Nulla  -- mod: majd Carnot-ciklusból
      cpt = CptIgeragozasKonstruktor JelenI FolyamatosSz KozvetlenF
      cliffordElem = cptKod cpt
      steaneKod = mondatSteane esetRag JelenI
  in KodKonstruktor mondat balE8Pont jobbE8Pont harmadikE8Pont negyedikE8Pont cliffordElem steaneKod
  where
    keresKerdoszo : List String -> Maybe Esetrag
    keresKerdoszo [] = Nothing
    keresKerdoszo (s :: ss) =
      case kerdoszoEset s of
        Just e => Just e
        Nothing => keresKerdoszo ss

    keresFogalom : List String -> Maybe E8Pont
    keresFogalom [] = Nothing
    keresFogalom (s :: ss) =
      case fogalomKeres s of
        Just p => Just p
        Nothing =>
          case ragFelismer s of
            Just (to, _) => case fogalomKeres to of
                              Just p => Just p
                              Nothing => keresFogalom ss
            Nothing => keresFogalom ss

-- ─── 7. FŐPROGRAM ───────────────────────────────────────────

public export
showE8 : E8Pont -> String
showE8 p =
  showKubit p.x1 ++ showKubit p.x2 ++ showKubit p.x3 ++ showKubit p.x4 ++
  showKubit p.x5 ++ showKubit p.x6 ++ showKubit p.x7 ++ showKubit p.x8
  where
    showKubit : Kubit -> String
    showKubit Nulla = "0"
    showKubit Egy = "1"

public export
kodolFom : IO ()
kodolFom = do
  putStrLn "=== KODOL — Magyar mondat → E8E8KodSzo (Kubit) ==="
  putStrLn ""
  putStrLn "Példa 1: 'Mi az a kategória?'"
  let ks1 = kodol "Mi az a kategória?"
  putStrLn ("  cimke: " ++ ks1.cimke)
  putStrLn ("  balE8 (ter/én):    " ++ showE8 ks1.balE8)
  putStrLn ("  jobbE8 (szín/te):  " ++ showE8 ks1.jobbE8)
  putStrLn ""
  putStrLn "Példa 2: 'Hogyan működik a funktor?'"
  let ks2 = kodol "Hogyan működik a funktor?"
  putStrLn ("  cimke: " ++ ks2.cimke)
  putStrLn ("  balE8 (ter/én):    " ++ showE8 ks2.balE8)
  putStrLn ("  jobbE8 (szín/te):  " ++ showE8 ks2.jobbE8)
  putStrLn ""
  putStrLn "Példa 3: 'Miért használunk izomorfizmust?'"
  let ks3 = kodol "Miért használunk izomorfizmust?"
  putStrLn ("  cimke: " ++ ks3.cimke)
  putStrLn ("  balE8 (ter/én):    " ++ showE8 ks3.balE8)
  putStrLn ("  jobbE8 (szín/te):  " ++ showE8 ks3.jobbE8)
  putStrLn ""
  putStrLn "Példa 4: 'Mivel kapcsolódik a funktor a kategóriához?'"
  let ks4 = kodol "Mivel kapcsolódik a funktor a kategóriához?"
  putStrLn ("  cimke: " ++ ks4.cimke)
  putStrLn ("  balE8 (ter/én):    " ++ showE8 ks4.balE8)
  putStrLn ("  jobbE8 (szín/te):  " ++ showE8 ks4.jobbE8)
  putStrLn ""
  putStrLn "Példa 5: 'Hol van az objektum?'"
  let ks5 = kodol "Hol van az objektum?"
  putStrLn ("  cimke: " ++ ks5.cimke)
  putStrLn ("  balE8 (ter/én):    " ++ showE8 ks5.balE8)
  putStrLn ("  jobbE8 (szín/te):  " ++ showE8 ks5.jobbE8)
  putStrLn ""
  putStrLn "Kész."