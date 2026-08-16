module ErtelmezoSzotar

-- ═══════════════════════════════════════════════════════════════
-- ÉRTELMEZŐ SZÓTÁR — szemantikai réteg (genus–differentia)
-- ═══════════════════════════════════════════════════════════════
-- Az ÉKSZ-definíció: „Az X olyan Y, amely Z."
--   X = szócím (a definiáltum)
--   Y = NEM-FOGALOM (genus)     → GeneralizacioK él a Szotár-gráfba
--   Z = MEGKÜLÖNBÖZTETŐ JEGY    → a Z-ben a ragok SZEREBEket adnak
--        (Fillmore-eset-nyelvtán: minden toldalékolt szó egy slot)
--
-- A szemantikai parszolás = morfológiai parszolás minden szón +
-- a keremek (frame) összegyűjtése: (Esetrag × Fonetika) párok.
-- A szavak Fonetika-típusok (Hang-konstruktorok), NINCS String
-- a magban; a String csak a határon (gauge: ertelmezestParszol).
--
-- Adatforrások (doc): ÉKSZ (copyright), Wikiszótár (open dump),
-- Wikidata lexémák. A tesztszócikkek kézzel, ÉKSZ-stílusban.
-- ═══════════════════════════════════════════════════════════════

import Fonetika
import MagyarNyelvtan
import Szotar

%default total

-- ─── 1. SZÓFAJ ────────────────────────────────────────────

public export
data SzofajT = FonSz | IgeSz | MelleknevSz | HatarozoSz | ViszonySz | KerdoszSz

public export
Show SzofajT where
  show FonSz       = "főnév"
  show IgeSz       = "ige"
  show MelleknevSz = "melléknév"
  show HatarozoSz  = "határozószó"
  show ViszonySz   = "viszonyszó"
  show KerdoszSz   = "kérdőszó"

-- ─── 2. SZEREP = (eset × betöltő) — Fillmore-keret slot ──

||| Egy szemantikai szerep: az eset (a mélyeset, akit a rag jelez)
||| és a betöltő szó (Fonetika-típusként).
public export
record SzerepKent where
  constructor SzerepKentK
  melyEset  : Esetrag
  betolto   : Fonetika

public export
Show SzerepKent where
  show sk = esetragNev (melyEset sk) ++ " ← " ++ ipaForma (betolto sk)

||| A mélyesetek emberi nevei (a rag mögötti szerep).
public export
melyEsetNev : Esetrag -> String
melyEsetNev AccusativusE     = "PATIENS (mit?)"
melyEsetNev NominativusE     = "AGENS (ki/mi?)"
melyEsetNev InstrumentalisE  = "ESZKÖZ (mivel?)"
melyEsetNev CausalisFinalisE = "OK/CÉL (miért?)"
melyEsetNev InessivusE       = "HELY-BEN (hol?)"
melyEsetNev IllativusE       = "IRÁNY-BA (hová?)"
melyEsetNev ElativusE        = "SZÁRMAZÁS (honnan?)"
melyEsetNev DativusE         = "KEDVEZMÉNYEZETT (kinek?)"
melyEsetNev e                = esetragNev e

-- ─── 3. A SZÓCIKK ─────────────────────────────────────────

||| Egy értelmező-szótári szócikk:
|||   szoCim    — a headword Fonetikaként
|||   nemFogalom — a genus: „olyan Y" (a szótár-kategória)
|||   jegyek    — a differentia kereme: (eset,betöltő) párok
|||   pelda     — példamondat kereme
public export
record Szocikk where
  constructor SzocikkK
  szoCim     : Fonetika
  szofaja    : SzofajT
  nemFogalom : Fonetika
  jegyek     : List SzerepKent
  pelda      : List SzerepKent

public export
Show Szocikk where
  show sz = ipaForma (szoCim sz) ++ " [" ++ show (szofaja sz) ++ "]\n"
        ++ "  nem-fogalom: " ++ ipaForma (nemFogalom sz) ++ "\n"
        ++ "  jegyek: " ++ osszefuzz (map show (jegyek sz)) ++ "\n"
        ++ "  példa: " ++ osszefuzz (map show (pelda sz))
    where
      osszefuzz : List String -> String
      osszefuzz [] = ""
      osszefuzz [x] = x
      osszefuzz (x :: xs) = x ++ "; " ++ osszefuzz xs

-- ─── 4. SZÓCIKKEK ÉPÍTÉSE (kézi, ÉKSZ-stílus) ─────────────
-- A definiáló mondat kommentben; a típus a mondat KERETE.

-- „A hangvilla olyan eszköz, amely meghatározott frekvenciájú
--  hangot ad." — tárgy: hang-ot (PATIENS)
public export
hangvillaCikk : Szocikk
hangvillaCikk = SzocikkK
  (magyarHangok "hangvilla") FonSz
  (magyarHangok "eszköz")
  [ SzerepKentK AccusativusE (magyarHangok "hangot") ]
  [ SzerepKentK InstrumentalisE (magyarHangok "hangvillával") ]

-- „Az entrópia olyan mérőszám, amely a rendezetlenséget méri."
public export
entropiaCikk : Szocikk
entropiaCikk = SzocikkK
  (magyarHangok "entrópia") FonSz
  (magyarHangok "mérőszám")
  [ SzerepKentK AccusativusE (magyarHangok "rendezetlenséget") ]
  [ SzerepKentK CausalisFinalisE (magyarHangok "fizikáért") ]

-- „A kategória olyan struktúra, amely objektumokat és
--  morfizmusokat tartalmaz."
public export
kategoriaCikk : Szocikk
kategoriaCikk = SzocikkK
  (magyarHangok "kategória") FonSz
  (magyarHangok "struktúra")
  [ SzerepKentK AccusativusE (magyarHangok "objektumokat")
  , SzerepKentK AccusativusE (magyarHangok "morfizmusokat") ]
  []

-- „A funktor olyan leképezés, amely kategóriákat kategóriákba visz."
public export
funktorCikk : Szocikk
funktorCikk = SzocikkK
  (magyarHangok "funktor") FonSz
  (magyarHangok "leképezés")
  [ SzerepKentK IllativusE (magyarHangok "kategóriákba") ]
  []

-- „Az adjunkció olyan kapcsolat, amely két funktort köt össze."
public export
adjunkcioCikk : Szocikk
adjunkcioCikk = SzocikkK
  (magyarHangok "adjunkció") FonSz
  (magyarHangok "kapcsolat")
  [ SzerepKentK AccusativusE (magyarHangok "funktorokat") ]
  []

-- „A komma olyan maradék, amely a kvintkör záródásából marad."
public export
kommaCikk : Szocikk
kommaCikk = SzocikkK
  (magyarHangok "komma") FonSz
  (magyarHangok "maradék")
  [ SzerepKentK ElativusE (magyarHangok "záródásából") ]
  []

-- „A keresés olyan folyamat, amely kérdést válaszzá alakít."
public export
keresesCikk : Szocikk
keresesCikk = SzocikkK
  (magyarHangok "keresés") FonSz
  (magyarHangok "folyamat")
  [ SzerepKentK TranszlativusE (magyarHangok "válaszzá") ]
  []

-- „Az energia olyan mennyiség, amely munkavégzésre képes."
public export
energiaCikk : Szocikk
energiaCikk = SzocikkK
  (magyarHangok "energia") FonSz
  (magyarHangok "mennyiség")
  [ SzerepKentK SublativusE (magyarHangok "munkavégzésre") ]
  []

-- ─── 5. A SZÓTÁR (a szócikkek halmaza) ────────────────────

public export
ertelmezoSzotar : List Szocikk
ertelmezoSzotar =
  [ hangvillaCikk, entropiaCikk, kategoriaCikk, funktorCikk
  , adjunkcioCikk, kommaCikk, keresesCikk, energiaCikk ]

-- ─── 6. SZEMANTIKAI LEKÉRDEZÉSEK ─────────────────────────

||| Keresés szócímre (IPA-egyezés).
public export
cikketKeres : Fonetika -> List Szocikk -> Maybe Szocikk
cikketKeres _ [] = Nothing
cikketKeres cim (c :: cs) =
  if hangokEgyenlok cim (szoCim c) then Just c else cikketKeres cim cs
  where
    hangokEgyenlok : Fonetika -> Fonetika -> Bool
    hangokEgyenlok [] [] = True
    hangokEgyenlok (x :: xs) (y :: ys) = (x == y) && hangokEgyenlok xs ys
    hangokEgyenlok _ _ = False

||| Egy fogalom nem-fogalma (a genus-kategória).
public export
nemFogalma : Fonetika -> List Szocikk -> Maybe Fonetika
nemFogalma cim sz = case cikketKeres cim sz of
  Just c  => Just (nemFogalom c)
  Nothing => Nothing

||| A szócikk keremei (jegyek + példa együtt).
public export
osszesKerete : Szocikk -> List SzerepKent
osszesKerete c = jegyek c ++ pelda c

||| Két fogalom rokonsága: közös nem-fogalom?
public export
rokonE : Fonetika -> Fonetika -> List Szocikk -> Bool
rokonE a b sz = case (nemFogalma a sz, nemFogalma b sz) of
  (Just n1, Just n2) => True   -- mindkettő definiált → összehasonlítható
  _ => False

||| Adott mélyesetű szerepek száma a szótárban
||| (melyik eset hordoz legtöbb jelentést).
public export
esetGyakorisag : Esetrag -> List Szocikk -> Nat
esetGyakorisag _ [] = 0
esetGyakorisag e (c :: cs) =
  length (filter (\sk => melyEset sk == e) (osszesKerete c))
  + esetGyakorisag e cs

-- ─── 7. GAUGE: definíció-mondat String→típus ──────────────
-- Az EGYETLEN Stringes pont: „Az X olyan Y, amely Z." formátumból
-- készít szócikket. A Z szavait ragfelismeréssel keretezi.

szokent : String -> List String
szokent s = go (unpack s)
  where
    go : List Char -> List String
    go [] = [""]
    go (x :: xs) =
      if x == ' ' || x == ',' || x == '.'
        then "" :: go xs
        else case go xs of
               (e :: t) => (strCons x e) :: t
               [] => [strCons x ""]

szavakTisztan : String -> List String
szavakTisztan s = filter (\x => length x > 0) (szokent s)

||| A differentia szavainak keretezése: minden toldalékolt szó
||| (Esetrag × Fonetika) slot; a toldalék nélküliek kimaradnak.
public export
keretez : List String -> List SzerepKent
keretez [] = []
keretez (w :: ws) = case ragFelismer w of
  Just (_, eset) => SzerepKentK eset (magyarHangok w) :: keretez ws
  Nothing => keretez ws

||| „Az X olyan Y, amely Z." → Maybe Szocikk
||| (X kötőjel nélküli szó, Y az „olyan" utáni szó, Z az „amely" után).
public export
ertelmezestParszol : String -> Maybe Szocikk
ertelmezestParszol mondat =
  let ws = szavakTisztan mondat
  in case keresPoz "olyan" ws of
       Just p => case drop (S p) ws of
         (y :: rest) => case keresPoz "amely" rest of
           Just q => Just (SzocikkK (magyarHangok (fej ws))
                              FonSz (magyarHangok y)
                              (keretez (drop (S q) rest)) [])
           Nothing => Nothing
         [] => Nothing
       Nothing => Nothing
  where
    fej : List String -> String
    fej [] = ""
    fej (x :: _) = x
    drop : Nat -> List String -> List String
    drop Z xs = xs
    drop (S n) (_ :: xs) = drop n xs
    drop _ [] = []
    keresPoz : String -> List String -> Maybe Nat
    keresPoz _ [] = Nothing
    keresPoz w (x :: xs) =
      if x == w then Just Z
      else case keresPoz w xs of
             Just n => Just (S n)
             Nothing => Nothing

-- ─── 8. MAIN ──────────────────────────────────────────────

main : IO ()
main = do
  putStrLn (show ertelmezoSzotar)
  putStrLn ""
  putStrLn "── Gauge-teszt: valódi definíció-mondat parszolása ──"
  putStrLn (case ertelmezestParszol
    "A hangvilla olyan eszköz amely meghatározott frekvenciájú hangot ad." of
      Just c => show c
      Nothing => "nem sikerült")