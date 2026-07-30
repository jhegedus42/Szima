module KategoriaElmelet

import MagyarNyelv
import Steane713
import E8E8Algebra
import FogalomFa
import HaromKubit
import FazisAlgebra

||| Kategoria: objektumok + morfizmusok + osszetetel + azonos.
public export
record Kategoria (objektum : Type) (hom : objektum -> objektum -> Type) where
  constructor KategoriaKonstruktor
  azonos : (a : objektum) -> hom a a
  osszetetel : {a, b, c : objektum} -> hom a b -> hom b c -> hom a c

||| Monoidalis kategoria: tenzor szorzat + egysegelem.
public export
record MonoidalisKategoria (objektum : Type) (hom : objektum -> objektum -> Type) where
  constructor MonoidalisKategoriaKonstruktor
  kategoria : Kategoria objektum hom
  tenzor : objektum -> objektum -> objektum
  egyseg : objektum

||| DualisKategoria: minden objektumnak van dualisa.
public export
record DualisKategoria (objektum : Type) (hom : objektum -> objektum -> Type) where
  constructor DualisKategoriaKonstruktor
  monoidalis : MonoidalisKategoria objektum hom
  dualis : objektum -> objektum

||| Funktor: kategoria szerkezet megorzese.
public export
record Funktor (o1 : Type) (m1 : o1 -> o1 -> Type) (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor FunktorKonstruktor
  objektumKep : o1 -> o2
  morfizmusKep : {a, b : o1} -> m1 a b -> m2 (objektumKep a) (objektumKep b)

||| Termeszetes transzformacio: ket funktor kozotti lekepezes.
public export
record TermeszetesTranszformacio
       (o1 : Type) (m1 : o1 -> o1 -> Type) (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor TermeszetesKonstruktor
  felso : Funktor o1 m1 o2 m2
  also : Funktor o1 m1 o2 m2
  komponens : (a : o1) -> m2 (felso.objektumKep a) (also.objektumKep a)

||| Bifunktor: ket kategoria szorzatabol.
public export
record Bifunktor (bk : Kategoria o1 m1) (jk : Kategoria o2 m2) (kk : Kategoria o3 m3) where
  constructor BifunktorKonstruktor
  objektumKep : o1 -> o2 -> o3
  morfizmusKep : {a, b : o1} -> {c, d : o2}
              -> m1 a b -> m2 c d
              -> m3 (objektumKep a c) (objektumKep b d)

||| Span: ket morfizmus kozos forrassal.
public export
record Span (kategoria : Kategoria obj hom) (celpont : obj) where
  constructor SpanKonstruktor
  balForras : obj
  jobbForras : obj

||| Cospan: ket morfizmus kozos cellal.
public export
record Cospan (kategoria : Kategoria obj hom) (forras : obj) where
  constructor CospanKonstruktor
  balCel : obj
  jobbCel : obj

||| Szimmetrikus monoidalis kategoria: tenzor + braiding.
public export
record SzimmetrikusMonoidalisKategoria
       (objektum : Type) (hom : objektum -> objektum -> Type) where
  constructor SzimmetrikusKonstruktor
  monoidalis : MonoidalisKategoria objektum hom
  braiding : {a, b : objektum} -> hom (monoidalis.tenzor a b) (monoidalis.tenzor b a)

||| Szorzat kategoria: ha C es D kategoriak, akkor C × D is az.
public export
record SzorzatKategoria (o1 : Type) (m1 : o1 -> o1 -> Type)
                        (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor SzorzatKonstruktor
  balKategoria : Kategoria o1 m1
  jobbKategoria : Kategoria o2 m2

||| EllenKategoria (C^op): megforditott morfizmusok.
public export
data EllenMorf : {obj : Type} -> (hom : obj -> obj -> Type) -> obj -> obj -> Type where
  EllenNyil : {a, b : obj} -> hom a b -> EllenMorf hom b a

||| Adjunkcio: F -| G, ahol F : C → D, G : D → C.
||| A termeszetes bijekcio: Hom_D(F a, b) ≅ Hom_C(a, G b).
public export
record Adjunkcio (o1 : Type) (m1 : o1 -> o1 -> Type)
                 (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor AdjunkcioKonstruktor
  balFunktor : Funktor o1 m1 o2 m2
  jobbFunktor : Funktor o2 m2 o1 m1
  balEgyseg : (a : o1) -> m1 a (jobbFunktor.objektumKep (balFunktor.objektumKep a))
  jobbEgyseg : (b : o2) -> m2 (balFunktor.objektumKep (jobbFunktor.objektumKep b)) b

||| KettoKategoria: 2-sejtek a morfizmusok kozott.
||| Objektumok (0-sejtek), morfizmusok (1-sejtek), 2-morfizmusok (2-sejtek).
public export
record KettoKategoria (obj : Type) (hom : obj -> obj -> Type)
                      (ketHom : (a, b : obj) -> hom a b -> hom a b -> Type) where
  constructor KettoKategoriaKonstruktor
  alapKategoria : Kategoria obj hom
  fuggolegesOsszetetel : {a, b : obj} -> {f, g, h : hom a b}
                      -> ketHom a b f g -> ketHom a b g h -> ketHom a b f h
  vizszintesOsszetetel : {a, b, c : obj} -> {f1, f2 : hom a b} -> {g1, g2 : hom b c}
                      -> ketHom a b f1 f2 -> ketHom b c g1 g2
                      -> ketHom a c (alapKategoria.osszetetel f1 g1)
                                    (alapKategoria.osszetetel f2 g2)

||| Yoneda beagyazas: C → [C^op, Set].
||| Minden a objektumhoz a Hom(-, a) prefasítás.
public export
record YonedaBeagyazas (o : Type) (m : o -> o -> Type) where
  constructor YonedaKonstruktor
  kategoria : Kategoria o m
  objektumKep : (a : o) -> (x : o) -> m x a
  morfizmusKep : {a, b : o} -> m a b
              -> (x : o) -> m x a -> m x b
  -- Yoneda lemma: Nat(Hom(-, a), F) ≅ F a
  -- Itt a termeszetes transzformacio komponenseibol allitjuk elo az F a erteket.
  yonedaLemma : {a : o} -> {f : o -> Type}
             -> ((x : o) -> m x a -> f x) -> f a

-- ═══════════════════════════════════════════════════════════════
-- MORFIZMUS TIPUSOK (WRAPPER-EK A KATEGORIAKHOZ)
-- ═══════════════════════════════════════════════════════════════

||| Fogalom morfizmus: a FogalomLogika lezart kategoriakent.
||| Az Azonos es Ire mellett a Sorozat epit kompoziciot.
public export
data FogalomMorf : FogalomTipus -> FogalomTipus -> Type where
  FogalomAzonos : FogalomMorf a a
  FogalomIre : FogalomLogika a b -> FogalomMorf a b
  FogalomSorozat : (koztes : FogalomTipus) -> FogalomMorf a koztes -> FogalomMorf koztes c -> FogalomMorf a c

||| Fogalom 2-morfizmus: 2-sejtek ket parhuzamos FogalomMorf kozott.
||| A 2-sejt a fazis/amplitudo a ket ut kozott a 2-kategoriaban.
public export
data FogalomKetMorf : (a, b : FogalomTipus) -> FogalomMorf a b -> FogalomMorf a b -> Type where
  KetAzonos : FogalomKetMorf a b f f
  KetIre : FogalomKetMorf a b f g

||| Eset morfizmus: EsetLogika wrapper — csak azonos morfizmusok.
public export
data EsetMorf : Eset -> Eset -> Type where
  EsetMorfKonstruktor : EsetLogika a -> EsetMorf a a

||| E8 morfizmus: CliﬀordElem wrapper.
public export
data E8Morf : E8Pont -> E8Pont -> Type where
  E8MorfKonstruktor : CliﬀordElem -> E8Morf a b

||| HaromKubit morfizmus: fazis kapcsolat.
public export
data KubitMorf : HaromKubit -> HaromKubit -> Type where
  KubitMorfKonstruktor : HaromKubitMorfizmus a b -> KubitMorf a b

||| Ido morfizmus: ido irany.
public export
data IdoMorf : IgeIdo -> IgeIdo -> Type where
  IdoMorfKonstruktor : IdoMorfizmus a b -> IdoMorf a b

-- ═══════════════════════════════════════════════════════════════
-- AZONOSSAGOK ES OSSZETETELEK (minden kategoriahoz)
-- ═══════════════════════════════════════════════════════════════

||| Eset azonos: minden esethez a sajat logikaja.
esetAzonos : (a : Eset) -> EsetLogika a
esetAzonos Nominativusz = AlanyLogika
esetAzonos Accusativusz = TargyLogika
esetAzonos Datívusz = CimzettLogika
esetAzonos Instrumentalis = EszkozLogika
esetAzonos Komitativusz = TarsLogika
esetAzonos Kauzalis = OkLogika
esetAzonos Transzativusz = EredmenyLogika
esetAzonos Terminativusz = HatárLogika
esetAzonos Illativusz = IranyLogika
esetAzonos Inesszivusz = HelyLogika
esetAzonos Elativusz = HonnanLogika
esetAzonos Allativusz = CelLogika
esetAzonos Adesszivusz = KivelLogika
esetAzonos Ablativusz = HonnanLogika2
esetAzonos Szuperesszivusz = FelszinLogika
esetAzonos Delativusz = RolLogika
esetAzonos Szublativusz = CelLogika2
esetAzonos Temporalis = MikorLogika
esetAzonos Szociativusz = KentiLogika
esetAzonos Distributivus = ElosztLogika
esetAzonos Esszivusz = MinosegLogika
esetAzonos Modalis = ModLogika
esetAzonos Causalis = CausalLogika
esetAzonos Formaliss = AlakLogika

-- ═══════════════════════════════════════════════════════════════
-- HAROMKUBIT ES IDO SEGEDFUGGVENYEK
-- ═══════════════════════════════════════════════════════════════
public export
haromKubitAzonos : HaromKubitMorfizmus a a
haromKubitAzonos = HaromKubitMorfizmusKonstruktor

||| HaromKubit osszetetel.
public export
haromKubitOsszetetel : HaromKubitMorfizmus a b -> HaromKubitMorfizmus b c
                    -> HaromKubitMorfizmus a c
haromKubitOsszetetel HaromKubitMorfizmusKonstruktor HaromKubitMorfizmusKonstruktor =
  HaromKubitMorfizmusKonstruktor

||| Ido azonos.
public export
idoAzonos : IdoMorfizmus a a
idoAzonos = IdoMorfizmusKonstruktor

||| Ido osszetetel.
public export
idoOsszetetel : IdoMorfizmus a b -> IdoMorfizmus b c -> IdoMorfizmus a c
idoOsszetetel IdoMorfizmusKonstruktor IdoMorfizmusKonstruktor = IdoMorfizmusKonstruktor

-- ═══════════════════════════════════════════════════════════════
-- KATEGORIA OSSZETETEL SEGEDFUGGVENYEK
-- ═══════════════════════════════════════════════════════════════

fogalomOsszetetelMorf : {a : FogalomTipus} -> {b : FogalomTipus} -> {c : FogalomTipus}
                     -> FogalomMorf a b -> FogalomMorf b c -> FogalomMorf a c
fogalomOsszetetelMorf {a} {b} {c} f g = FogalomSorozat {a = a} {c = c} b f g

esetOsszetetelMorf : EsetMorf a b -> EsetMorf b c -> EsetMorf a c
esetOsszetetelMorf (EsetMorfKonstruktor f) (EsetMorfKonstruktor g) =
  EsetMorfKonstruktor f

e8OsszetetelMorf : E8Morf a b -> E8Morf b c -> E8Morf a c
e8OsszetetelMorf (E8MorfKonstruktor f) (E8MorfKonstruktor g) =
  E8MorfKonstruktor (cliﬀordSzorzat f g)

kubitOsszetetelMorf : KubitMorf a b -> KubitMorf b c -> KubitMorf a c
kubitOsszetetelMorf (KubitMorfKonstruktor f) (KubitMorfKonstruktor g) =
  KubitMorfKonstruktor (haromKubitOsszetetel f g)

idoOsszetetelMorf : IdoMorf a b -> IdoMorf b c -> IdoMorf a c
idoOsszetetelMorf (IdoMorfKonstruktor f) (IdoMorfKonstruktor g) =
  IdoMorfKonstruktor (idoOsszetetel f g)

-- ═══════════════════════════════════════════════════════════════
-- KATEGORIA PELDAK
-- ═══════════════════════════════════════════════════════════════

||| FogalomFa mint kategoria.
public export
fogalomKategoria : Kategoria FogalomTipus FogalomMorf
fogalomKategoria = KategoriaKonstruktor
  (\a => FogalomAzonos)
  fogalomOsszetetelMorf

||| Eset mint kategoria (diszkret).
public export
esetKategoria : Kategoria Eset EsetMorf
esetKategoria = KategoriaKonstruktor
  (\a => EsetMorfKonstruktor (esetAzonos a))
  esetOsszetetelMorf

||| E8 × E8 mint kategoria.
public export
e8Kategoria : Kategoria E8Pont E8Morf
e8Kategoria = KategoriaKonstruktor
  (\a => E8MorfKonstruktor (CliﬀordKonstruktor 1 0 0))
  e8OsszetetelMorf

||| HaromKubit mint kategoria.
public export
haromKubitKategoria : Kategoria HaromKubit KubitMorf
haromKubitKategoria = KategoriaKonstruktor
  (\a => KubitMorfKonstruktor haromKubitAzonos)
  kubitOsszetetelMorf

||| Ido mint kategoria.
public export
idoKategoria : Kategoria IgeIdo IdoMorf
idoKategoria = KategoriaKonstruktor
  (\a => IdoMorfKonstruktor idoAzonos)
  idoOsszetetelMorf

||| FogalomFa monoidalisan.
public export
fogalomMonoidalisKategoria : MonoidalisKategoria FogalomTipus FogalomMorf
fogalomMonoidalisKategoria = MonoidalisKategoriaKonstruktor
  fogalomKategoria
  (\a, b => Gyoker)
  Gyoker

fogalomDualis : FogalomTipus -> FogalomTipus
fogalomDualis Cel = Ok
fogalomDualis Ok = Kavzatum
fogalomDualis Kavzatum = Cel
fogalomDualis a = a

||| Dualis: Cel ↔ Ok, Ok ↔ Kavzatum, Kavzatum ↔ Cel.
public export
fogalomDualisKategoria : DualisKategoria FogalomTipus FogalomMorf
fogalomDualisKategoria = DualisKategoriaKonstruktor
  fogalomMonoidalisKategoria
  fogalomDualis

-- ═══════════════════════════════════════════════════════════════
-- 4 DIMENZIO KATEGORIA: TER, IDO, TOMEG, INFORMACIO
-- ═══════════════════════════════════════════════════════════════

||| A 4 alap dimenzio.
public export
data NegyDimenzio = Ter | Ido | Tomeg | Informacio

||| Morfizmusok a 4 dimenzio kozott.
||| A legegyszerubb nem trivialis kategoria: mindegyik
||| atalakithato a masikba.
public export
data DimenzioMorf : NegyDimenzio -> NegyDimenzio -> Type where
  DimAzonos  : DimenzioMorf a a
  DimTukor   : DimenzioMorf Ter Ter
  DimIdoFord : DimenzioMorf Ido Ido
  DimTerIdo  : DimenzioMorf Ter Ido
  DimIdoTer  : DimenzioMorf Ido Ter
  DimTerTomeg : DimenzioMorf Ter Tomeg
  DimTomegTer : DimenzioMorf Tomeg Ter
  DimTerInfo  : DimenzioMorf Ter Informacio
  DimInfoTer  : DimenzioMorf Informacio Ter
  DimIdoTomeg : DimenzioMorf Ido Tomeg
  DimTomegIdo : DimenzioMorf Tomeg Ido
  DimIdoInfo  : DimenzioMorf Ido Informacio
  DimInfoIdo  : DimenzioMorf Informacio Ido
  DimTomegInfo : DimenzioMorf Tomeg Informacio
  DimInfoTomeg : DimenzioMorf Informacio Tomeg

-- ═══════════════════════════════════════════════════════════════
-- FIZIKAI EGYENLETEK (a 4 dimenzio kozotti kapcsolatok)
-- ═══════════════════════════════════════════════════════════════

||| c = fenysebesseg (allando)
public export
data Fenysebesseg : Type where
  FenysebessegKonstruktor : Fenysebesseg

||| Lorentz transzformacio: Ter ↔ Ido
|||   t' = γ(t - v·x/c²)
|||   x' = γ(x - v·t)
|||   γ = 1/√(1 - v²/c²)
public export
data LorentzTranszformacio : Type where
  LorentzKonstruktor : LorentzTranszformacio

||| Ter → Tomeg: E = m·c² (Einstein)
|||   A tomeg es a ter kozotti ekvivalencia.
public export
data EinsteiniEgyenlet : Type where
  EinsteinKonstruktor : EinsteiniEgyenlet

||| Ter → Informacio: holografikus elv
|||   S = A / (4·ℓp²)
public export
data HolografikusElv : Type where
  HolografikusKonstruktor : HolografikusElv

||| Ido → Tomeg: tomeg okozta idodilatacio
|||   t' = t · √(1 - 2GM/(rc²))
public export
data IdoDilatacio : Type where
  IdoDilatacioKonstruktor : IdoDilatacio

||| Ido → Informacio: Shannon-Hartley tetel
|||   C = B · log₂(1 + S/N)
public export
data ShannonHartley : Type where
  ShannonKonstruktor : ShannonHartley

||| Tomeg → Informacio: Landauer elv
|||   E = k·T·ln(2) · I
public export
data LandauerElv : Type where
  LandauerKonstruktor : LandauerElv

||| Tukor (paritas forditas): (x, y, z) → (-x, -y, -z)
public export
data ParitasForditas : Type where
  TukorKonstruktor : ParitasForditas

||| Ido forditas: t → -t
|||   Amikor az ido megfordul, az osszes tobbi dimenzio is megfordul (CPT).
public export
data CptSzimmetria : Type where
  CptKonstruktor : CptSzimmetria

-- ═══════════════════════════════════════════════════════════════
-- CURRY-HOWARD-LAMBEK MEGFELELTETES
-- ═══════════════════════════════════════════════════════════════

||| Curry-Howard-Lambek megfeleltetes: Logika ↔ Tipuselmelet ↔ Kategoria.
||| Harom oszlop, minden szinten megfeleltetessel.
public export
data CurryHowardLambek : Type where
  ||| Propozicio ↔ Tipus ↔ Objektum
  PropozicioTipusObjektum : CurryHowardLambek
  ||| Bizonyitas ↔ Program/Term ↔ Morfizmus
  BizonyitasProgramMorfizmus : CurryHowardLambek
  ||| Implikacio ↔ Fuggvenytipus ↔ Exponencialis objektum
  ImplikacioFuggvenyExponencialis : CurryHowardLambek
  ||| Konjunkcio ↔ Szorzattipus ↔ Kategoriai szorzat
  KonjunkcioSzorzatKategoriai : CurryHowardLambek
  ||| Diszjunkcio ↔ Osszegtipus ↔ Kategoriai koproduktum
  DiszjunkcioOsszegKoproduktum : CurryHowardLambek
  ||| Egyetemes kvantor ↔ Pi-tipus ↔ Hatarertek
  EgyetemesKvantorPiHatar : CurryHowardLambek
  ||| Egzisztencialis kvantor ↔ Szigma-tipus ↔ Koequalizer
  EgzisztencialisKvantorSzigmaKo : CurryHowardLambek
  ||| Igaz ↔ Egysegtipus ↔ Vegso objektum
  IgazEgysegTerminalis : CurryHowardLambek
  ||| Hamis ↔ Ures tipus ↔ Inicialis objektum
  HamisUresInicialis : CurryHowardLambek
  ||| Tagadas ↔ Void tipus ↔ Dualis
  TagadasVoidDualis : CurryHowardLambek
  ||| Godel befejezetlenseg ↔ Tipuselmeleti befejezetlenseg ↔ Fixpont
  GodelTipusFixpont : CurryHowardLambek

||| E8 mint monoidalis kategoria: tenzor = pontonkenti osszeadas,
||| egyseg = nulla pont, braiding = azonos (kommutativitas miatt).
public export
e8Monoidalis : MonoidalisKategoria E8Pont E8Morf
e8Monoidalis = MonoidalisKategoriaKonstruktor
  e8Kategoria
  e8Osszead
  (E8PontKonstruktor 0 0 0 0 0 0 0 0)

||| E8 braiding: a⊕b → b⊕a. Mivel e8Osszead kommutativ,
||| a ket pont megegyezik, igy az azonos morfizmus jo.
public export
e8Braiding : {a, b : E8Pont}
          -> E8Morf (e8Osszead a b) (e8Osszead b a)
e8Braiding = E8MorfKonstruktor (CliﬀordKonstruktor 1 0 0)

||| E8 szimmetrikus monoidalis kategoria.
public export
e8Szimmetrikus : SzimmetrikusMonoidalisKategoria E8Pont E8Morf
e8Szimmetrikus = SzimmetrikusKonstruktor e8Monoidalis e8Braiding

||| E8 × E8 objektum: rendezett E8 pont par.
public export
E8xE8Obj : Type
E8xE8Obj = (E8Pont, E8Pont)

||| E8 × E8 morfizmus: parhuzamos E8 morfizmusok.
public export
data E8xE8Morf : E8xE8Obj -> E8xE8Obj -> Type where
  E8xE8Par : {a, c : E8Pont} -> {b, d : E8Pont}
          -> E8Morf a c -> E8Morf b d
          -> E8xE8Morf (a, b) (c, d)

||| E8 × E8 azonos morfizmus.
public export
e8xE8Azonos : (x : E8xE8Obj) -> E8xE8Morf x x
e8xE8Azonos (a, b) = E8xE8Par (e8Kategoria.azonos a) (e8Kategoria.azonos b)

||| E8 × E8 osszetetel.
public export
e8xE8Osszetetel : E8xE8Morf x y -> E8xE8Morf y z -> E8xE8Morf x z
e8xE8Osszetetel (E8xE8Par {a} {c = koztes} {b} {d = koztes2} f1 g1)
                (E8xE8Par {a = koztes} {c} {b = koztes2} {d} f2 g2) =
  E8xE8Par
    (e8Kategoria.osszetetel {a = a} {b = koztes} {c = c} f1 f2)
    (e8Kategoria.osszetetel {a = b} {b = koztes2} {c = d} g1 g2)

||| E8 × E8 szorzat kategoria.
public export
e8xE8Kategoria : Kategoria E8xE8Obj E8xE8Morf
e8xE8Kategoria = KategoriaKonstruktor e8xE8Azonos e8xE8Osszetetel

||| E8E8KodSzo → E8xE8Obj: a kod szo bal es jobb E8 pontja.
public export
e8e8KodSzoObj : E8E8KodSzo -> E8xE8Obj
e8e8KodSzoObj kod = (kod.balE8, kod.jobbE8)

||| E8xE8Obj → E8E8KodSzo: ures Steane koddal, azonos Cliﬀorddal.
public export
e8xE8ObjKodSzo : E8xE8Obj -> E8E8KodSzo
e8xE8ObjKodSzo (b, j) = KodKonstruktor "" b j
  (CliﬀordKonstruktor 1 0 0) (alapKod Nulla)

-- ═══════════════════════════════════════════════════════════════
-- 2-KATEGORIA + YONEDA + DUAL A FOGALMAKRA
-- ═══════════════════════════════════════════════════════════════

||| Fogalom 2-kategoria: FogalomTipus mint 0-sejt, FogalomMorf mint 1-sejt,
||| FogalomKetMorf mint 2-sejt.
public export
fogalomKettoKategoria : KettoKategoria FogalomTipus FogalomMorf FogalomKetMorf

||| Yoneda beagyazas a fogalom kategoriaban: C → [C^op, Set].
||| Minden fogalomtípushoz a Hom(-, a) prefasítás.
public export
fogalomYoneda : YonedaBeagyazas FogalomTipus FogalomMorf

||| Dual adjunkcio: C -| C^op.
||| A bal es jobb funktor az azonos es az ellentett kategoria kozott.
public export
fogalomDualisAdjunkcio : Adjunkcio FogalomTipus FogalomMorf FogalomTipus (EllenMorf FogalomMorf)

-- ═══════════════════════════════════════════════════════════════
-- KATEGORIAELMELETI LETRA: objektumtol a Yonedaig
-- ═══════════════════════════════════════════════════════════════

||| 0. szint: tipusok (objektumok).
||| A legalso fok — puszta tipusok, meg morfizmus nelkul.
public export
record NulladikLetra (obj : Type) where
  constructor NulladikLetraKonstruktor
  objektumok : Type

||| 1. szint: kategoria (objektumok + morfizmusok + azonos + osszetetel).
||| A kategoriaba szervezett tipusok.
public export
record ElsoLetra (obj : Type) (hom : obj -> obj -> Type) where
  constructor ElsoLetraKonstruktor
  nulladik : NulladikLetra obj
  kategoria : Kategoria obj hom

||| 2. szint: funktor (kategoriak kozotti lekepezes).
||| A kategoriak kozotti kapcsolat.
public export
record MasodikLetra (o1 : Type) (m1 : o1 -> o1 -> Type)
                    (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor MasodikLetraKonstruktor
  elso : ElsoLetra o1 m1
  funktor : Funktor o1 m1 o2 m2

||| 3. szint: termeszetes transzformacio (funktorok kozotti lekepezes).
||| A funktorok kozotti kapcsolat.
public export
record HarmadikLetra (o1 : Type) (m1 : o1 -> o1 -> Type)
                     (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor HarmadikLetraKonstruktor
  masodik : MasodikLetra o1 m1 o2 m2
  termeszetes : TermeszetesTranszformacio o1 m1 o2 m2

||| 4. szint: 2-kategoria (2-sejtek a morfizmusok kozott).
||| A kategoriak kategoriája.
public export
record NegyedikLetra (obj : Type) (hom : obj -> obj -> Type)
                     (ketHom : (a, b : obj) -> hom a b -> hom a b -> Type) where
  constructor NegyedikLetraKonstruktor
  elso : ElsoLetra obj hom
  kettoKategoria : KettoKategoria obj hom ketHom

||| 5. szint: Yoneda beagyazas (C → [C^op, Set]).
||| Minden objektum a Hom(-, a) presheafba van agyazva.
public export
record OtodikLetra (obj : Type) (hom : obj -> obj -> Type) where
  constructor OtodikLetraKonstruktor
  elso : ElsoLetra obj hom
  yoneda : YonedaBeagyazas obj hom

||| 6. szint: adjunkcio (C -| D).
||| A duális kategoriaval alkotott adjunkcio.
public export
record HatodikLetra (o1 : Type) (m1 : o1 -> o1 -> Type)
                    (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor HatodikLetraKonstruktor
  elso : ElsoLetra o1 m1
  adjunkcio : Adjunkcio o1 m1 o2 m2

||| Teljes letra: nulladik szinttol a Yoneda beagyazasig es adjunkciog.
||| Minden fok epit az elozo szintre.
public export
record TeljesLetra (obj : Type) (hom : obj -> obj -> Type)
                   (ketHom : (a, b : obj) -> hom a b -> hom a b -> Type)
                   (o2 : Type) (m2 : o2 -> o2 -> Type) where
  constructor TeljesLetraKonstruktor
  nulladik : NulladikLetra obj
  elso : ElsoLetra obj hom
  masodik : MasodikLetra obj hom obj hom
  harmadik : HarmadikLetra obj hom obj hom
  negyedik : NegyedikLetra obj hom ketHom
  otodik : OtodikLetra obj hom
  hatodik : HatodikLetra obj hom o2 m2

-- ═══════════════════════════════════════════════════════════════
-- FUNKTOR SEGEDFUGGVENYEK (objektum lekepezesek)
-- ═══════════════════════════════════════════════════════════════

||| FogalomTipus → E8Pont.
public export
fogalomTipusKod : FogalomTipus -> E8Pont
fogalomTipusKod Gyoker = E8PontKonstruktor 0 0 0 0 0 0 0 1
fogalomTipusKod Cel = E8PontKonstruktor 0 0 0 0 0 0 1 0
fogalomTipusKod ReszCel = E8PontKonstruktor 0 0 0 0 0 1 0 0
fogalomTipusKod Feladat = E8PontKonstruktor 0 0 0 0 1 0 0 0
fogalomTipusKod ReszFeladat = E8PontKonstruktor 0 0 0 1 0 0 0 0
fogalomTipusKod Cselekves = E8PontKonstruktor 0 0 1 0 0 0 0 0
fogalomTipusKod Dontes = E8PontKonstruktor 0 1 0 0 0 0 0 0
fogalomTipusKod Valasztas = E8PontKonstruktor 1 0 0 0 0 0 0 0
fogalomTipusKod Elutasitas = E8PontKonstruktor 1 1 0 0 0 0 0 0
fogalomTipusKod Ok = E8PontKonstruktor 1 0 1 0 0 0 0 0
fogalomTipusKod Kavzatum = E8PontKonstruktor 0 1 1 0 0 0 0 0
fogalomTipusKod Korlatozas = E8PontKonstruktor 1 1 1 0 0 0 0 0
fogalomTipusKod Megfigyeles = E8PontKonstruktor 0 0 0 0 0 0 1 1
fogalomTipusKod Hiba = E8PontKonstruktor 0 0 0 0 0 1 1 1
fogalomTipusKod Eredmeny = E8PontKonstruktor 0 0 0 0 1 1 1 1
fogalomTipusKod Minta = E8PontKonstruktor 0 0 0 1 1 1 1 1
fogalomTipusKod Javitas = E8PontKonstruktor 0 0 1 1 1 1 1 1
fogalomTipusKod Foltozas = E8PontKonstruktor 0 1 1 1 1 1 1 1
fogalomTipusKod InfraJavitas = E8PontKonstruktor 1 1 1 1 1 1 1 1
fogalomTipusKod Szabaly = E8PontKonstruktor 1 0 0 0 0 0 0 1
fogalomTipusKod KemenySzabaly = E8PontKonstruktor 1 0 0 0 0 0 1 1
fogalomTipusKod Egyezmeny = E8PontKonstruktor 1 0 0 0 0 1 0 1
fogalomTipusKod Eszkoz = E8PontKonstruktor 1 0 0 0 1 0 0 1
fogalomTipusKod Kesztseg = E8PontKonstruktor 1 0 0 1 0 0 0 1
fogalomTipusKod ModellKornyezetProtokoll = E8PontKonstruktor 1 0 1 0 0 0 0 1
fogalomTipusKod Kerdes = E8PontKonstruktor 0 1 0 0 0 0 0 1
fogalomTipusKod Magyarazat = E8PontKonstruktor 0 0 1 0 0 0 0 1
fogalomTipusKod E8xE8 = E8PontKonstruktor 1 1 0 0 0 0 1 1
fogalomTipusKod Dualitas = E8PontKonstruktor 0 1 1 0 0 0 1 1
fogalomTipusKod Kategoria = E8PontKonstruktor 0 0 1 1 0 0 1 1
fogalomTipusKod Szimmetria = E8PontKonstruktor 0 0 0 1 1 0 1 1
fogalomTipusKod Tenzor = E8PontKonstruktor 0 0 0 0 1 1 1 1
fogalomTipusKod Funktor = E8PontKonstruktor 1 0 0 0 0 1 1 1
fogalomTipusKod _ = E8PontKonstruktor 0 0 0 0 0 0 0 0

||| Kubit → Int.
public export
kubitErtek : Kubit -> Int
kubitErtek Nulla = 0
kubitErtek Egy = 1

||| HaromKubit → E8Pont: harom kubit 3 koordinata.
public export
haromKubitE8Kod : HaromKubit -> E8Pont
haromKubitE8Kod v =
  let sajatErtek = kubitErtek v.sajat
      masikErtek = kubitErtek v.masik
      fazisErtek = kubitErtek v.fazis
  in E8PontKonstruktor sajatErtek masikErtek fazisErtek 0 0 0 0 0

||| IgeIdo → E8Pont (6. pozicio).
public export
idoE8Kod : IgeIdo -> E8Pont
idoE8Kod Mult = E8PontKonstruktor 0 0 0 0 0 1 0 0
idoE8Kod Jelen = E8PontKonstruktor 0 0 0 0 0 0 1 0
idoE8Kod Jovo = E8PontKonstruktor 0 0 0 0 0 0 0 1

||| E8Pont osszeadas.
public export
e8PontOsszead : E8Pont -> E8Pont -> E8Pont
e8PontOsszead a b = E8PontKonstruktor
  (a.x1 + b.x1) (a.x2 + b.x2) (a.x3 + b.x3) (a.x4 + b.x4)
  (a.x5 + b.x5) (a.x6 + b.x6) (a.x7 + b.x7) (a.x8 + b.x8)

||| FogalomTipus → String.
public export
fogalomNev : FogalomTipus -> String
fogalomNev Gyoker = "gyoker"
fogalomNev Cel = "cel"
fogalomNev ReszCel = "reszcel"
fogalomNev Feladat = "feladat"
fogalomNev ReszFeladat = "reszfeladat"
fogalomNev Cselekves = "cselekves"
fogalomNev Dontes = "dontes"
fogalomNev Valasztas = "valasztas"
fogalomNev Elutasitas = "elutasitas"
fogalomNev Ok = "ok"
fogalomNev Kavzatum = "kavzatum"
fogalomNev Korlatozas = "korlatozas"
fogalomNev Megfigyeles = "megfigyeles"
fogalomNev Hiba = "hiba"
fogalomNev Eredmeny = "eredmeny"
fogalomNev Minta = "minta"
fogalomNev Javitas = "javitas"
fogalomNev Foltozas = "foltozas"
fogalomNev InfraJavitas = "infrajavitas"
fogalomNev Szabaly = "szabaly"
fogalomNev KemenySzabaly = "kemenyszabaly"
fogalomNev Egyezmeny = "egyezmeny"
fogalomNev Eszkoz = "eszkoz"
fogalomNev Kesztseg = "kesztseg"
fogalomNev ModellKornyezetProtokoll = "modellkornyezetprotokoll"
fogalomNev Kerdes = "kerdes"
fogalomNev Magyarazat = "magyarazat"
fogalomNev E8xE8 = "e8xe8"
fogalomNev Dualitas = "dualitas"
fogalomNev Kategoria = "kategoria"
fogalomNev Szimmetria = "szimmetria"
fogalomNev Tenzor = "tenzor"
fogalomNev Funktor = "funktor"
fogalomNev _ = "ismeretlen"

||| FogalomFa → HaromKubit.
public export
fogalomFaKubit : FogalomFa t -> HaromKubit
fogalomFaKubit fa =
  let m = meret fa
      g = gyerekekSzama fa
  in VilagKonstruktor
       (if m > 5 then Egy else Nulla)
       (if g > 3 then Egy else Nulla)
       (if m + g > 8 then Egy else Nulla)

-- ═══════════════════════════════════════════════════════════════
-- FUNKTOR MORFIZMUSKEP SEGEDFUGGVENYEK
-- ═══════════════════════════════════════════════════════════════

esetE8MorfizmusKep : {a, b : Eset} -> EsetMorf a b -> E8Morf (esetKod a) (esetKod b)
esetE8MorfizmusKep (EsetMorfKonstruktor _) = E8MorfKonstruktor (CliﬀordKonstruktor 1 0 0)

fogalomE8MorfizmusKep : {a : FogalomTipus} -> {b : FogalomTipus}
                     -> FogalomMorf a b -> E8Morf (fogalomTipusKod a) (fogalomTipusKod b)
fogalomE8MorfizmusKep {a} FogalomAzonos = E8MorfKonstruktor (CliﬀordKonstruktor 1 0 0)
fogalomE8MorfizmusKep {a} {b} (FogalomIre _) =
  let aa = fogalomTipusKod a
      bb = fogalomTipusKod b
      -- Az E8 × E8 geometriai szorzat: aa * bb = a·b + a∧b
      -- A skalaris resz (a·b) az atfedes merteke
      -- Hasznaljuk a CliﬀordKonstruktor-t a ket pont kulonbsegekent
      xx = aa.x1 - bb.x1
      yy = aa.x2 - bb.x2
      zz = aa.x3 - bb.x3
  in E8MorfKonstruktor (CliﬀordKonstruktor
    (if xx == 0 then 1 else 0)
    (if yy == 0 then 1 else 0)
    (if zz == 0 then 1 else 0))
fogalomE8MorfizmusKep {a} {b} (FogalomSorozat koztes f g) =
  let f1 : E8Morf (fogalomTipusKod a) (fogalomTipusKod koztes) = fogalomE8MorfizmusKep f
      g1 : E8Morf (fogalomTipusKod koztes) (fogalomTipusKod b) = fogalomE8MorfizmusKep g
  in e8OsszetetelMorf f1 g1

kubitE8MorfizmusKep : {a, b : HaromKubit} -> KubitMorf a b -> E8Morf (haromKubitE8Kod a) (haromKubitE8Kod b)
kubitE8MorfizmusKep (KubitMorfKonstruktor _) = E8MorfKonstruktor (CliﬀordKonstruktor 1 0 0)

idoE8MorfizmusKep : {a, b : IgeIdo} -> IdoMorf a b -> E8Morf (idoE8Kod a) (idoE8Kod b)
idoE8MorfizmusKep (IdoMorfKonstruktor _) = E8MorfKonstruktor (CliﬀordKonstruktor 1 0 0)

-- ═══════════════════════════════════════════════════════════════
-- FUNKTOROK (KATEGORIAK KAPCSOLASAI)
-- ═══════════════════════════════════════════════════════════════

||| Eset → E8: minden eset egy E8 pont.
public export
esetE8Funktor : Funktor Eset EsetMorf E8Pont E8Morf
esetE8Funktor = FunktorKonstruktor esetKod esetE8MorfizmusKep

||| Fogalom → E8: minden fogalom egy E8 pont.
public export
fogalomE8Funktor : Funktor FogalomTipus FogalomMorf E8Pont E8Morf
fogalomE8Funktor = FunktorKonstruktor fogalomTipusKod fogalomE8MorfizmusKep

||| HaromKubit → E8: harom kubit 3 koordinata.
public export
kubitE8Funktor : Funktor HaromKubit KubitMorf E8Pont E8Morf
kubitE8Funktor = FunktorKonstruktor haromKubitE8Kod kubitE8MorfizmusKep

||| Ido → E8: ido a 6. pozicioban.
public export
idoE8Funktor : Funktor IgeIdo IdoMorf E8Pont E8Morf
idoE8Funktor = FunktorKonstruktor idoE8Kod idoE8MorfizmusKep

-- ═══════════════════════════════════════════════════════════════
-- KAPCSOLATOK A MEGLEVO TIPUSOKHOZ
-- ═══════════════════════════════════════════════════════════════

||| RagozottSzo → E8Pont.
||| A szo.idobol az IgeIdot emeljuk ki az IdoBeljegyzesbol.
public export
ragozottSzoE8Pont : RagozottSzo -> E8Pont
ragozottSzoE8Pont szo =
  let (IdoBeljegyzesKonstruktor igeIdo _ _) = szo.ido
      fogKod = fogalomTipusKod szo.fogalom
      eKod = esetKod szo.eset
      iKod = idoE8Kod igeIdo
      fKod = haromKubitE8Kod szo.fazisKubit
  in e8PontOsszead (e8PontOsszead (e8PontOsszead fogKod eKod) iKod) fKod

||| NyelvtaniKapcsolat → E8E8KodSzo.
public export
nyelvtaniKapcsolatKod : NyelvtaniKapcsolat -> E8E8KodSzo
nyelvtaniKapcsolatKod kapcs =
  KodKonstruktor
    (fogalomNev kapcs.ige.fogalom)
    (ragozottSzoE8Pont kapcs.alany)
    (ragozottSzoE8Pont kapcs.targy)
    (CliﬀordKonstruktor 1 0 1)
    (alapKod Nulla)

||| VilagFa → ToltesParitasIdo.
||| A fazis (FogalomAdat) helyett a fazisKubit-ot szamoljuk
||| a FogalomAdat bizalmabol: magas bizalom → Egy fazis.
public export
vilagFaToltesParitasIdo : VilagFa -> ToltesParitasIdo
vilagFaToltesParitasIdo vf = ToltesParitasIdoKonstruktor
  (fogalomFaKubit vf.sajat)
  (fogalomFaKubit vf.masik)
  (VilagKonstruktor
    (if vf.fazis.bizalom > 0.5 then Egy else Nulla)
    (if vf.fazis.bizalom > 0.8 then Egy else Nulla)
    (if length vf.fazis.hivatkozasok > 2 then Egy else Nulla))
