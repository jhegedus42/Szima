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

public export
Show Kubit where
  show Nulla = "0"
  show Egy   = "1"

||| Hetes kod a [[7,1,3]] Steane kod 7 bitjevel.
||| A konstruktor neve a teljes magyar kifejezes,
||| mert a rovidites (Mk) tiltva van.
public export
data HetesKod : Type where
  HetesKonstruktor : Kubit -> Kubit -> Kubit -> Kubit
    -> Kubit -> Kubit -> Kubit -> HetesKod

public export
Show HetesKod where
  show (HetesKonstruktor a b c d e f g) =
    show a ++ show b ++ show c ++ show d ++ show e ++ show f ++ show g

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
forditKubit : Kubit -> Kubit
forditKubit Nulla = Egy
forditKubit Egy   = Nulla

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
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 0) = HetesKonstruktor (forditKubit a) b c d e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 1) = HetesKonstruktor a (forditKubit b) c d e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 2) = HetesKonstruktor a b (forditKubit c) d e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 3) = HetesKonstruktor a b c (forditKubit d) e f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 4) = HetesKonstruktor a b c d (forditKubit e) f g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 5) = HetesKonstruktor a b c d e (forditKubit f) g
javitas (HetesKonstruktor a b c d e f g) (EgyesHiba 6) = HetesKonstruktor a b c d e f (forditKubit g)
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

-- ═══════════════════════════════════════════════════════════════
-- PAULI MATRIXOK, TENZOR SZORZATOK, [[15,1,3]] ES T-KAPU
-- ═══════════════════════════════════════════════════════════════

||| Pauli mátrixok: I, X, Y, Z.
|||   I = [[1,0],[0,1]]   Z = [[1,0],[0,-1]]
|||   X = [[0,1],[1,0]]   Y = [[0,-i],[i,0]] = i·X·Z
public export
data PauliMx : Type where
  PauliI : PauliMx
  PauliX : PauliMx
  PauliY : PauliMx
  PauliZ : PauliMx

||| Tenzor szorzat: n darab Pauli mátrix.
||| Pl. X⊗Z⊗I = PauliTenzor [PauliX, PauliZ, PauliI]
public export
record PauliTenzor where
  constructor TenzorKonstruktor
  tenzor : List PauliMx

||| [[15,1,3]] Reed-Muller kod.
||| 15 fizikai kubit, 1 logikai kubit, tavolsag 3.
||| A 7 X stabilizator es 7 Z stabilizator.
||| Specialis: transversal T-kapu = π/8 fazis = "az ido megall".
public export
data TizenotEgyHaromKod : Type where
  TizenotKodKonstruktor : PauliTenzor -> PauliTenzor -> TizenotEgyHaromKod

||| T-kapu = π/8 fazis: diag(1, e^(i·π/8)).
||| Azert all meg az ido, mert a T-kapu az
||| 1/16-ad teljes forgatas — a [[15,1,3]] kodban
||| transversalisan (bitenként) alkalmazhato
||| anelkul, hogy a kod megsertilne.
||| Ez a nem-Clifford kapu ami teljesse teszi
||| a kvantum szamitast.
public export
data TGate : Type where
  TGateKonstruktor : (fazis : Double) -> TGate

-- ═══════════════════════════════════════════════════════════════
-- TIPUSOSZTALYOK (INTERFESZEK) — komponalhato tipusosztalyok
-- ═══════════════════════════════════════════════════════════════

||| Inverz: egy muvelet sajat maga inverze (involucio).
|||   fordit : a -> a
|||   forditTorveny : fordit ∘ fordit = id
||| Komponalhato: Inverz a + Inverz b → Inverz (a, b)
public export
interface Inverz (a : Type) where
  fordit : a -> a
  forditTorveny : (x : a) -> fordit (fordit x) = x

||| Kodolo: informacio megtartasa kodolassal.
|||   kodol : a -> b
|||   dekodol : b -> a
|||   kodTorveny : dekodol ∘ kodol = id
||| Komponalhato: Kodolo a b + Kodolo b c → Kodolo a c
public export
interface Kodolo (a : Type) (b : Type) where
  kodol : a -> b
  dekodol : b -> a
  kodTorveny : (x : a) -> dekodol (kodol x) = x

||| Inverz par: Inverz a-bol es Inverz b-bol automatikusan Inverz (a, b).
|||   fordit (x, y) = (fordit x, fordit y)
public export
[ParInverz] {a : Type} -> {b : Type} -> Inverz a => Inverz b => Inverz (a, b) where
  fordit (x, y) = (fordit x, fordit y)
  forditTorveny (x, y) =
    let p1 = forditTorveny x
        p2 = forditTorveny y
        s1 = cong (\v => (v, fordit (fordit y))) p1
        s2 = cong (\w => (x, w)) p2
    in trans s1 s2

||| Kodolo kompozicio: Kodolo a b + Kodolo b c → Kodolo a c.
|||   kodol x = kodol_b (kodol_a x)  [a → b → c]
|||   dekodol x = dekodol_a (dekodol_b x)  [c → b → a]
public export
[KodoloOsszetetel] {a : Type} -> {b : Type} -> {c : Type}
  -> (elso : Kodolo a b) => (masodik : Kodolo b c) => Kodolo a c where
  kodol x = kodol @{masodik} (kodol @{elso} x)
  dekodol x = dekodol @{elso} (dekodol @{masodik} x)
  kodTorveny x =
    let p1 = kodTorveny @{masodik} (kodol @{elso} x)
        p2 = cong (dekodol @{elso}) p1
        p3 = kodTorveny @{elso} x
    in trans p2 p3

-- ═══════════════════════════════════════════════════════════════
-- PELDAK: INSTANCE-K
-- ═══════════════════════════════════════════════════════════════

||| Pauli X: Inverz Kubit (X^2 = I)
public export
Inverz Kubit where
  fordit Nulla = Egy
  fordit Egy   = Nulla
  forditTorveny Nulla = Refl
  forditTorveny Egy   = Refl

||| [[7,1,3]] Steane kod: Kodolo Kubit HetesKod
public export
Kodolo Kubit HetesKod where
  kodol Nulla = HetesKonstruktor Nulla Nulla Nulla Nulla Nulla Nulla Nulla
  kodol Egy   = HetesKonstruktor Egy   Egy   Egy   Egy   Egy   Egy   Egy
  dekodol (HetesKonstruktor a b c d e f g) =
    let nullak = length (filter (== Nulla) [a, b, c, d, e, f, g])
        egyek  = length (filter (== Egy)  [a, b, c, d, e, f, g])
    in if egyek > nullak then Egy else Nulla
  kodTorveny Nulla = Refl
  kodTorveny Egy   = Refl
