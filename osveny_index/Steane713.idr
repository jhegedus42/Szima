module Steane713

||| Miért pont [[7,1,3]]? Mert a 7 bit minden osszetett fogalom
||| alapszerkezete: [ido, oksag, ter, szin, hang, fazis, mod].
||| Mind a het dimenzio egy-egy aspektusat kodolja a valosagnak.
||| A tavolsag 3 azt jelenti, hogy 1 hibat ki tudunk javitani.
||| A Steane kod azert jo, mert a 7 bit 16 stabil allapota
||| pontosan lefedi a magyar nyelv 22 esetet.
|||
||| Hogyan mukodik a hibajavitas?
||| 1. Bejon egy 7 bites kod (fogalmak, nyelvtani kapcsolat)
||| 2. A szindroma megmondja, melyik bit serult
||| 3. A javito fuggveny forditja a serult bitet
||| 4. A kod ujra koherens
|||
||| Mi a hiba a fogalmakban?
||| Egy fogalom rossz esetben van.
||| Ket fogalom osszefonodott (kvantum osszefonodes a nyelvben).
||| Az ido rossz dimenzioban van.
||| A referencia (sajat/masik) felcserelodott.
||| Ezek mind javithatok, ha pontosan egy bit serult.

public export
data Kubit = Nulla | Egy

public export
Eq Kubit where
  (==) Nulla Nulla = True
  (==) Egy   Egy   = True
  (==) _     _     = False

  (/=) a b = not (a == b)

||| Hetes kod a [[7,1,3]] Steane kod 7 bitjevel.
||| A konstruktor neve a teljes magyar kifejezes,
||| mert a rovidites (Mk) tiltva van.
public export
data HetesKod : Type where
  HetesKonstruktor : Kubit -> Kubit -> Kubit -> Kubit
    -> Kubit -> Kubit -> Kubit -> HetesKod

||| Alap allapot a 7 biten.
||| A nulla (Nulla) minden bitje nulla.
||| Az egyes (Egy) minden bitje egy.
||| Ez a ket stabil allapot a 16-bol.
public export
alapKod : Kubit -> HetesKod
alapKod Nulla = HetesKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla
alapKod Egy   = HetesKonstruktor Egy   Egy   Egy   Egy   Egy   Egy   Egy

||| A fordit fuggveny atbillenti a kubitot:
||| Nulla → Egy, Egy → Nulla.
||| Ez a bitszintu javitas alapja.
||| Nem rovidites — a teljes magyar "fordit" ige.
fordit : Kubit -> Kubit
fordit Nulla = Egy
fordit Egy   = Nulla

||| Szindroma: hol van a hiba?
||| NincsHiba = minden rendben.
||| EgyesHiba N = az N. pozicio hibas.
||| Tobbszoros = tobb hiba egyszerre (nem javithato, de detektalhato).
||| A tavolsag 3 miatt tobbszoros hibanal mar nem tudjuk
||| biztosan, hogy mely bitek serultek - csak azt tudjuk,
||| hogy valami nincs rendben.
public export
data Szindroma = NincsHiba | EgyesHiba Nat | Tobbszoros (List Szindroma)

||| A javito fuggveny forditja a serult bitet.
||| Minden poziciora kulon eset.
||| Ha a hiba tobbszoros, nem tudjuk javitani —
||| ilyenkor a kod valtozatlan marad.
public export
javitas : HetesKod -> Szindroma -> HetesKod
javitas kod NincsHiba = kod
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 0) = HetesKonstruktor (fordit a) b c d e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 1) = HetesKonstruktor a (fordit b) c d e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 2) = HetesKonstruktor a b (fordit c) d e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 3) = HetesKonstruktor a b c (fordit d) e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 4) = HetesKonstruktor a b c d (fordit e) f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 5) = HetesKonstruktor a b c d e (fordit f) g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 6) = HetesKonstruktor a b c d e f (fordit g)
javitas kod _ = kod

||| Harom ido dimenzio.
||| Gondolatmenet: a magyarban az ige nem csak idot hordoz,
||| hanem aspektust (folyamat vs befejezett) es forrast
||| (honnan tudjuk). Ez a harom dimenzio egyutt adja
||| a teljes idobeli kepet.
|||
||| IgeIdo: Mult, Jelen, Jovo.
|||   A magyarban nincs pluszkvamperfekt —
|||   a harom alap ido elegendo.
|||
||| IgeSzem: Folyamatos, Befejezett, Szokasos.
|||   A szokasos (pl. "jarok uszni") koti ossze
|||   a folyamatosat es a befejezettet.
|||
||| Forras: Kozvetlen ("latom"), Kovetkeztetett ("latszik"),
|||   Jelentett ("allitolag"). Ez az evidenciassag
|||   — honnan tudom, amit tudok.
public export
data IgeIdo   = Mult | Jelen | Jovo

public export
data IgeSzem  = Folyamatos | Befejezett | Szokasos

public export
data Forras   = Kozvetlen | Kovetkeztetett | Jelentett

||| Egy ige teljes idobelyege.
||| A harom dimenzio egyesitve egyetlen tipusba.
||| Ez megy bele a [[7,1,3]] kod 3 poziciojaba
||| (ido, oksag, es fazis — az elso harom bit).
||| A konstruktor neve hosszu, mert a rovidites
||| (IdoBeljegyzesMk, stb.) tiltva van.
public export
data IdoBeljegyzes : Type where
  IdoBeljegyzesKonstruktor : IgeIdo -> IgeSzem -> Forras -> IdoBeljegyzes

||| IdoMorfizmus: ido irany a kategoriaban.
public export
data IdoMorfizmus : IgeIdo -> IgeIdo -> Type where
  IdoMorfizmusKonstruktor : IdoMorfizmus a b
