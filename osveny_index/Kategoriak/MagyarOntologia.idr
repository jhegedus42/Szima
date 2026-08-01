module Kategoriak.MagyarOntologia

import Alap.KategoriaT

-- ═══════════════════════════════════════════════════════════════
-- MAGYAR ONTOLÓGIA — SZAVAK ÖNÁLLÓ TÍPUSOKKÉNT, NINCS STRING
-- ═══════════════════════════════════════════════════════════════
-- Minden szó = önálló típus. Nincs String, nincs Double, nincs Bool.
-- A képzők = typeclass instance-ok.
-- A kategóriák = typeclass-ok.
-- A tő = típus-szintű kapcsolat.
-- A rokon szavak = típus-szintű lista.

-- ═══════════════════════════════════════════════════════════════
-- 1. JELLENTÉSKATEGÓRIÁK
-- ═══════════════════════════════════════════════════════════════

public export
data JK = IndividuumJK | UniverzaleJK | GyujtemenyJK
        | CselekvesJK | AllapotJK | HelyJK | IdoJK
        | OkJK | ModJK | MennyisegJK | KapcsolatJK

-- ═══════════════════════════════════════════════════════════════
-- 2. SZÓTÖVEK — TÍPUSOK
-- ═══════════════════════════════════════════════════════════════

-- A tő is típus. Nincs String.
public export
data SzamToTipus = SzamToKonstruktor
public export
data TerToTipus = TerToKonstruktor
public export
data JoToTipus = JoToKonstruktor

-- ═══════════════════════════════════════════════════════════════
-- 3. KÉPZŐK — TÍPUSOK
-- ═══════════════════════════════════════════════════════════════

public export
data OlKepzoTipus = OlKepzoKonstruktor
public export
data ItKepzoTipus = ItKepzoKonstruktor
public export
data AsKepzoTipus = AsKepzoKonstruktor
public export
data ElKepzoTipus = ElKepzoKonstruktor
public export
data SagKepzoTipus = SagKepzoKonstruktor
public export
data LKepzoTipus = LKepzoKonstruktor
public export
data TalanKepzoTipus = TalanKepzoKonstruktor
public export
data OKepzoTipus = OKepzoKonstruktor

-- ═══════════════════════════════════════════════════════════════
-- 4. SZAVAK — MINDEN SZÓ ÖNÁLLÓ TÍPUS
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
-- 5. KATEGÓRIA TYPECLASS — MILYEN KATEGÓRIÁBA TARTOZIK?
-- ═══════════════════════════════════════════════════════════════

public export
interface JelentesT (0 szo : Type) (k : JK) | szo where

public export
JelentesT SzamTipus MennyisegJK
public export
JelentesT SzamolTipus CselekvesJK
public export
JelentesT SzamitTipus CselekvesJK
public export
JelentesT SzamitasTipus UniverzaleJK
public export
JelentesT SzamlaloTipus IndividuumJK
public export
JelentesT SzamitogepTipus IndividuumJK
public export
JelentesT SzamtalanTipus AllapotJK
public export
JelentesT TerTipus HelyJK
public export
JelentesT TerelTipus CselekvesJK
public export
JelentesT TeritTipus CselekvesJK
public export
JelentesT TerjedTipus CselekvesJK
public export
JelentesT TerfogatTipus MennyisegJK
public export
JelentesT JoTipus AllapotJK
public export
JelentesT JosagTipus UniverzaleJK
public export
JelentesT JolTipus ModJK

-- ═══════════════════════════════════════════════════════════════
-- 6. TŐ TYPECLASS — MILYEN TŐBŐL KELT?
-- ═══════════════════════════════════════════════════════════════

public export
interface SzotoT (0 szo : Type) (0 to : Type) | szo where

public export
SzotoT SzamTipus SzamToTipus
public export
SzotoT SzamolTipus SzamToTipus
public export
SzotoT SzamitTipus SzamToTipus
public export
SzotoT SzamitasTipus SzamToTipus
public export
SzotoT SzamlaloTipus SzamToTipus
public export
SzotoT SzamitogepTipus SzamToTipus
public export
SzotoT SzamtalanTipus SzamToTipus
public export
SzotoT TerTipus TerToTipus
public export
SzotoT TerelTipus TerToTipus
public export
SzotoT TeritTipus TerToTipus
public export
SzotoT TerjedTipus TerToTipus
public export
SzotoT TerfogatTipus TerToTipus
public export
SzotoT JoTipus JoToTipus
public export
SzotoT JosagTipus JoToTipus
public export
SzotoT JolTipus JoToTipus

-- ═══════════════════════════════════════════════════════════════
-- 7. KÉPZŐ TYPECLASS — MILYEN KÉPZŐVEL KELT?
-- ═══════════════════════════════════════════════════════════════

public export
interface KepzoT (0 forras : Type) (0 cel : Type) (0 kepzo : Type) | forras where

public export
KepzoT SzamTipus SzamolTipus OlKepzoTipus
public export
KepzoT SzamTipus SzamitTipus ItKepzoTipus
public export
KepzoT SzamitTipus SzamitasTipus AsKepzoTipus
public export
KepzoT SzamTipus SzamlaloTipus OKepzoTipus
public export
KepzoT SzamTipus SzamtalanTipus TalanKepzoTipus
public export
KepzoT TerTipus TerelTipus ElKepzoTipus
public export
KepzoT TerTipus TeritTipus ItKepzoTipus
public export
KepzoT JoTipus JosagTipus SagKepzoTipus
public export
KepzoT JoTipus JolTipus LKepzoTipus

-- ═══════════════════════════════════════════════════════════════
-- 8. ROKON SZÓ TYPECLASS — MIK A ROKON SZAVAK?
-- ═══════════════════════════════════════════════════════════════

-- A rokon szavak = típus-szintű kapcsolatok. Nincs List String.
public export
interface RokonSzoT (0 szo : Type) (0 rokon : Type) | szo where

public export
RokonSzoT SzamolTipus SzamitTipus
public export
RokonSzoT SzamitTipus SzamolTipus
public export
RokonSzoT SzamlaloTipus SzamitogepTipus
public export
RokonSzoT SzamitogepTipus SzamlaloTipus
public export
RokonSzoT TerelTipus TeritTipus
public export
RokonSzoT TeritTipus TerelTipus
public export
RokonSzoT JoTipus JosagTipus
public export
RokonSzoT JosagTipus JoTipus

-- ═══════════════════════════════════════════════════════════════
-- 9. KÍNAI MEGFELELŐ TYPECLASS
-- ═══════════════════════════════════════════════════════════════

-- A kínai megfelelő is típus. Nincs String.
public export
data SzamKinaiTipus = SzamKinaiKonstruktor
public export
data SzamitKinaiTipus = SzamitKinaiKonstruktor
public export
data SzamitogepKinaiTipus = SzamitogepKinaiKonstruktor
public export
data TerKinaiTipus = TerKinaiKonstruktor
public export
data JoKinaiTipus = JoKinaiKonstruktor

public export
interface KinaiMegfeleloT (0 magyar : Type) (0 kinai : Type) | magyar where

public export
KinaiMegfeleloT SzamTipus SzamKinaiTipus
public export
KinaiMegfeleloT SzamitTipus SzamitKinaiTipus
public export
KinaiMegfeleloT SzamitogepTipus SzamitogepKinaiTipus
public export
KinaiMegfeleloT TerTipus TerKinaiTipus
public export
KinaiMegfeleloT JoTipus JoKinaiTipus

-- ═══════════════════════════════════════════════════════════════
-- 10. MONDAT — TÍPUSOK KOMPOZÍCIÓJA
-- ═══════════════════════════════════════════════════════════════

-- Egy mondat = a szavak kompozíciója.
-- A mondat típusa = a szavak típusainak kompozíciója.
-- Nincs String — a mondat maga a típus.

-- "szám számol" = SzamTipus -> SzamolTipus (a számolás aktusa)
public export
record SzamSzamolMondat where
  constructor SzamSzamolMondatKonstruktor
  alany   : SzamTipus
  ige     : SzamolTipus

-- "számítógép számít" = SzamitogepTipus -> SzamitTipus
public export
record SzamitogepSzamitMondat where
  constructor SzamitogepSzamitMondatKonstruktor
  alany   : SzamitogepTipus
  ige     : SzamitTipus

-- "jó számítás" = JoTipus -> SzamitasTipus (minősités)
public export
record JoSzamitasMondat where
  constructor JoSzamitasMondatKonstruktor
  minoseg : JoTipus
  targy   : SzamitasTipus

-- ═══════════════════════════════════════════════════════════════
-- 11. ONTOLÓGIAI SZINTEK — MEO
-- ═══════════════════════════════════════════════════════════════

public export
data OntologiaiSzint = MetaMetaSzint | MetaSzint | TargySzint | InstanciaSzint

public export
data KeresztRelacio : OntologiaiSzint -> OntologiaiSzint -> Type where
  Instancialas  : KeresztRelacio InstanciaSzint TargySzint
  Tipizalas     : KeresztRelacio TargySzint MetaSzint
  Formalizalas  : KeresztRelacio MetaSzint MetaMetaSzint

-- ═══════════════════════════════════════════════════════════════
-- 12. ABSZTRAKT JELENTÉS — A STRUKTÚRÁBÓL
-- ═══════════════════════════════════════════════════════════════

-- Az absztrakt jelentés = a típusok kapcsolata.
-- "szám számol" = egy mennyiség cselekvést végez (MennyisegJK -> CselekvesJK)
-- "jó számítás" = egy állapot minősít egy fogalmat (AllapotJK -> UniverzaleJK)
-- A jelentés = a kompozíció eredménye. Nincs String.

-- A "számól" = emberi (ol képző), "számít" = gépi (it képző)
-- A különbség = a képző típusa (OlKepzoTipus vs ItKepzoTipus)
-- Ezt a típus mondja meg, nem egy String mező.

-- ═══════════════════════════════════════════════════════════════
-- 13. FŐPROGRAM
-- ═══════════════════════════════════════════════════════════════

public export
magyarOntologiaFom : IO ()
magyarOntologiaFom = do
  putStrLn "=== MAGYAR ONTOLÓGIA — NINCS STRING ==="
  putStrLn ""
  putStrLn "A szam- szocsalad (minden szo onallo tipus):"
  putStrLn "  SzamTipus (szam)       -> MennyisegJK"
  putStrLn "  SzamolTipus (szamol)   -> CselekvesJK  (kepzo: OlKepzoTipus)"
  putStrLn "  SzamitTipus (szamit)   -> CselekvesJK  (kepzo: ItKepzoTipus)"
  putStrLn "  SzamitasTipus (szamitas) -> UniverzaleJK"
  putStrLn "  SzamlaloTipus (szamlalo) -> IndividuumJK"
  putStrLn "  SzamitogepTipus (szamitogep) -> IndividuumJK"
  putStrLn "  SzamtalanTipus (szamtalan) -> AllapotJK"
  putStrLn ""
  putStrLn "A ter- szocsalad:"
  putStrLn "  TerTipus (ter)       -> HelyJK"
  putStrLn "  TerelTipus (terel)   -> CselekvesJK  (kepzo: ElKepzoTipus)"
  putStrLn "  TeritTipus (terit)   -> CselekvesJK  (kepzo: ItKepzoTipus)"
  putStrLn ""
  putStrLn "A jo- szocsalad:"
  putStrLn "  JoTipus (jo)       -> AllapotJK"
  putStrLn "  JosagTipus (josag)  -> UniverzaleJK  (kepzo: SagKepzoTipus)"
  putStrLn "  JolTipus (jol)      -> ModJK         (kepzo: LKepzoTipus)"
  putStrLn ""
  putStrLn "Kepzok (morfizmusok tipusok kozott):"
  putStrLn "  SzamTipus --(OlKepzoTipus)--> SzamolTipus"
  putStrLn "  SzamTipus --(ItKepzoTipus)--> SzamitTipus"
  putStrLn "  TerTipus  --(ElKepzoTipus)--> TerelTipus"
  putStrLn "  JoTipus   --(SagKepzoTipus)--> JosagTipus"
  putStrLn "  JoTipus   --(LKepzoTipus)--> JolTipus"
  putStrLn ""
  putStrLn "Mondatok (tipusok kompozicioja):"
  putStrLn "  SzamSzamolMondat = SzamTipus + SzamolTipus (szam szamol)"
  putStrLn "  SzamitogepSzamitMondat = SzamitogepTipus + SzamitTipus (szamitogep szamit)"
  putStrLn "  JoSzamitasMondat = JoTipus + SzamitasTipus (jo szamitas)"
  putStrLn ""
  putStrLn "Kinai megfelelok (人才的irotol too tipusok):"
  putStrLn "  SzamTipus -> SzamKinaiTipus"
  putStrLn "  SzamitTipus -> SzamitKinaiTipus"
  putStrLn "  TerTipus -> TerKinaiTipus"
  putStrLn "  JoTipus -> JoKinaiTipus"
  putStrLn ""
  putStrLn "MEO ontologiai szintek:"
  putStrLn "  meta-metaszint: relacioelmelet (kategoriaelmelet)"
  putStrLn "  metaszint: metafogalmak (funktorok)"
  putStrLn "  targyszint: fogalmak (szavak = tipusok)"
  putStrLn "  instanciaszint: peldanyok"
  putStrLn ""
  putStrLn "NINCS String. NINCS Double. NINCS Bool."
  putStrLn "Minden szo = onallo tipus."
  putStrLn "Minden kepzo = onallo tipus (a kepzo neve is tipus)."
  putStrLn "Minden rokon szo = tipus-szintu kapcsolat."
  putStrLn "Minden kinai megfelelo = onallo tipus."
  putStrLn "Minden mondat = rekord tipusokbol."
  putStrLn ""
  putStrLn "Kesz."