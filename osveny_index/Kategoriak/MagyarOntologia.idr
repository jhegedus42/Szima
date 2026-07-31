module Kategoriak.MagyarOntologia

import Alap.KategoriaT

-- ═══════════════════════════════════════════════════════════════
-- MAGYAR ONTOLÓGIA — SZAVAK ÖNÁLLÓ TÍPUSOKKÉNT
-- ═══════════════════════════════════════════════════════════════
-- Minden szó = önálló típus. Nincs String a mag típusokban.
-- A képzők = typeclass instance-ok (morfizmusok típusok között).
-- A kategóriák = typeclass-ok amikhez a szó instance-ot ad.

-- ═══════════════════════════════════════════════════════════════
-- 1. JELLENTÉSKATEGÓRIÁK
-- ═══════════════════════════════════════════════════════════════

public export
data JK = IndividuumJK | UniverzaleJK | GyujtemenyJK
        | CselekvesJK | AllapotJK | HelyJK | IdoJK
        | OkJK | ModJK | MennyisegJK | KapcsolatJK

public export
Show JK where
  show IndividuumJK = "individuum"
  show UniverzaleJK = "univerzale"
  show GyujtemenyJK = "gyujtemeny"
  show CselekvesJK = "cselekves"
  show AllapotJK = "allapot"
  show HelyJK = "hely"
  show IdoJK = "ido"
  show OkJK = "ok"
  show ModJK = "mod"
  show MennyisegJK = "mennyiseg"
  show KapcsolatJK = "kapcsolat"

-- ═══════════════════════════════════════════════════════════════
-- 2. SZAVAK — MINDEN SZÓ ÖNÁLLÓ TÍPUS (üres konstruktorral)
-- ═══════════════════════════════════════════════════════════════

-- A szám- szócsalád
public export
data SzamTipus = SzamKonstruktor
public export
data SzamolTipus = SzamolKonstruktor
public export
data SzamitTipus = SzamitKonstruktor
public export
data SzamitasTipus = SzamitasKonstruktor
public export
data SzamlaloTipus = SzamlaloKonstruktor
public export
data SzamitogepTipus = SzamitogepKonstruktor
public export
data SzamtalanTipus = SzamtalanKonstruktor

-- A tér- szócsalád
public export
data TerTipus = TerKonstruktor
public export
data TerelTipus = TerelKonstruktor
public export
data TeritTipus = TeritKonstruktor
public export
data TerjedTipus = TerjedKonstruktor
public export
data TerfogatTipus = TerfogatKonstruktor

-- A jó- szócsalád
public export
data JoTipus = JoKonstruktor
public export
data JosagTipus = JosagKonstruktor
public export
data JolTipus = JolKonstruktor

-- ═══════════════════════════════════════════════════════════════
-- 3. KATEGÓRIA TYPECLASS
-- ═══════════════════════════════════════════════════════════════

public export
interface JelentesT (0 szo : Type) (k : JK) | szo where
  jelentsKategoria : JK

public export
JelentesT SzamTipus MennyisegJK where
  jelentsKategoria = MennyisegJK

public export
JelentesT SzamolTipus CselekvesJK where
  jelentsKategoria = CselekvesJK

public export
JelentesT SzamitTipus CselekvesJK where
  jelentsKategoria = CselekvesJK

public export
JelentesT SzamitasTipus UniverzaleJK where
  jelentsKategoria = UniverzaleJK

public export
JelentesT SzamlaloTipus IndividuumJK where
  jelentsKategoria = IndividuumJK

public export
JelentesT SzamitogepTipus IndividuumJK where
  jelentsKategoria = IndividuumJK

public export
JelentesT SzamtalanTipus AllapotJK where
  jelentsKategoria = AllapotJK

public export
JelentesT TerTipus HelyJK where
  jelentsKategoria = HelyJK

public export
JelentesT TerelTipus CselekvesJK where
  jelentsKategoria = CselekvesJK

public export
JelentesT TeritTipus CselekvesJK where
  jelentsKategoria = CselekvesJK

public export
JelentesT TerjedTipus CselekvesJK where
  jelentsKategoria = CselekvesJK

public export
JelentesT TerfogatTipus MennyisegJK where
  jelentsKategoria = MennyisegJK

public export
JelentesT JoTipus AllapotJK where
  jelentsKategoria = AllapotJK

public export
JelentesT JosagTipus UniverzaleJK where
  jelentsKategoria = UniverzaleJK

public export
JelentesT JolTipus ModJK where
  jelentsKategoria = ModJK

-- ═══════════════════════════════════════════════════════════════
-- 4. TŐ TYPECLASS
-- ═══════════════════════════════════════════════════════════════

public export
interface SzotoT (0 szo : Type) where
  szotoNeve : String
  szoNeve   : String

public export
SzotoT SzamTipus where
  szotoNeve = "szam"
  szoNeve = "szam"

public export
SzotoT SzamolTipus where
  szotoNeve = "szam"
  szoNeve = "szamol"

public export
SzotoT SzamitTipus where
  szotoNeve = "szam"
  szoNeve = "szamit"

public export
SzotoT SzamitasTipus where
  szotoNeve = "szam"
  szoNeve = "szamitas"

public export
SzotoT SzamlaloTipus where
  szotoNeve = "szam"
  szoNeve = "szamlalo"

public export
SzotoT SzamitogepTipus where
  szotoNeve = "szam"
  szoNeve = "szamitogep"

public export
SzotoT SzamtalanTipus where
  szotoNeve = "szam"
  szoNeve = "szamtalan"

public export
SzotoT TerTipus where
  szotoNeve = "ter"
  szoNeve = "ter"

public export
SzotoT TerelTipus where
  szotoNeve = "ter"
  szoNeve = "terel"

public export
SzotoT TeritTipus where
  szotoNeve = "ter"
  szoNeve = "terit"

public export
SzotoT TerjedTipus where
  szotoNeve = "ter"
  szoNeve = "terjed"

public export
SzotoT TerfogatTipus where
  szotoNeve = "ter"
  szoNeve = "terfogat"

public export
SzotoT JoTipus where
  szotoNeve = "jo"
  szoNeve = "jo"

public export
SzotoT JosagTipus where
  szotoNeve = "jo"
  szoNeve = "josag"

public export
SzotoT JolTipus where
  szotoNeve = "jo"
  szoNeve = "jol"

-- ═══════════════════════════════════════════════════════════════
-- 5. KÉPZŐ TYPECLASS
-- ═══════════════════════════════════════════════════════════════

public export
interface KepzoT (0 forras : Type) (0 cel : Type) | forras where
  kepzoNeve : String

public export
KepzoT SzamTipus SzamolTipus where
  kepzoNeve = "-ol"

public export
KepzoT SzamTipus SzamitTipus where
  kepzoNeve = "-it"

public export
KepzoT SzamitTipus SzamitasTipus where
  kepzoNeve = "-it+-as"

public export
KepzoT SzamTipus SzamlaloTipus where
  kepzoNeve = "-ol+-o"

public export
KepzoT SzamTipus SzamtalanTipus where
  kepzoNeve = "-talan"

public export
KepzoT TerTipus TerelTipus where
  kepzoNeve = "-el"

public export
KepzoT TerTipus TeritTipus where
  kepzoNeve = "-it"

public export
KepzoT JoTipus JosagTipus where
  kepzoNeve = "-sag"

public export
KepzoT JoTipus JolTipus where
  kepzoNeve = "-l"

-- ═══════════════════════════════════════════════════════════════
-- 6. ONTOLÓGIAI SZINTEK — MEO
-- ═══════════════════════════════════════════════════════════════

public export
data OntologiaiSzint = MetaMetaSzint | MetaSzint | TargySzint | InstanciaSzint

public export
data KeresztRelacio : OntologiaiSzint -> OntologiaiSzint -> Type where
  Instancialas  : KeresztRelacio InstanciaSzint TargySzint
  Tipizalas     : KeresztRelacio TargySzint MetaSzint
  Formalizalas  : KeresztRelacio MetaSzint MetaMetaSzint

-- ═══════════════════════════════════════════════════════════════
-- 7. FŐPROGRAM
-- ═══════════════════════════════════════════════════════════════

public export
magyarOntologiaFom : IO ()
magyarOntologiaFom = do
  putStrLn "=== MAGYAR ONTOLÓGIA ==="
  putStrLn ""
  putStrLn "A szam- szocsalad (minden szo onall tipus):"
  putStrLn "  SzamTipus (szam)      = MennyisegJK"
  putStrLn "  SzamolTipus (szamol)  = CselekvesJK"
  putStrLn "  SzamitTipus (szamit)  = CselekvesJK"
  putStrLn "  SzamitasTipus (szamitas) = UniverzaleJK"
  putStrLn "  SzamlaloTipus (szamlalo) = IndividuumJK"
  putStrLn "  SzamitogepTipus (szamitogep) = IndividuumJK"
  putStrLn "  SzamtalanTipus (szamtalan) = AllapotJK"
  putStrLn ""
  putStrLn "A ter- szocsalad:"
  putStrLn "  TerTipus (ter)        = HelyJK"
  putStrLn "  TerelTipus (terel)    = CselekvesJK"
  putStrLn "  TeritTipus (terit)    = CselekvesJK"
  putStrLn "  TerjedTipus (terjed)  = CselekvesJK"
  putStrLn "  TerfogatTipus (terfogat) = MennyisegJK"
  putStrLn ""
  putStrLn "A jo- szocsalad:"
  putStrLn "  JoTipus (jo)          = AllapotJK"
  putStrLn "  JosagTipus (josag)    = UniverzaleJK"
  putStrLn "  JolTipus (jol)        = ModJK"
  putStrLn ""
  putStrLn "Kepzok (morfizmusok):"
  putStrLn "  SzamTipus --(-ol)--> SzamolTipus"
  putStrLn "  SzamTipus --(-it)--> SzamitTipus"
  putStrLn "  SzamitTipus --(-it+-as)--> SzamitasTipus"
  putStrLn "  TerTipus --(-el)--> TerelTipus"
  putStrLn "  TerTipus --(-it)--> TeritTipus"
  putStrLn "  JoTipus --(-sag)--> JosagTipus"
  putStrLn "  JoTipus --(-l)--> JolTipus"
  putStrLn ""
  putStrLn "MEO ontologiai szintek:"
  putStrLn "  meta-metaszint: relacioelmelet"
  putStrLn "  metaszint: metafogalmak"
  putStrLn "  targyszint: fogalmak (szavak)"
  putStrLn "  instanciaszint: peldanyok"
  putStrLn ""
  putStrLn "Kesz."