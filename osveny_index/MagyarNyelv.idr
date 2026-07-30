module MagyarNyelv

import Steane713
import E8E8Algebra
import HaromKubit

||| Magyar esetrendszer — 22 eset, mindegyik egy logikai kapcsolat.
|||
||| Gondolat: a magyar nyelv agglutinativ — a toldalekok
||| egymas utan fuzodnek a tohoz. Minden toldalek egy
||| logikai kapcsolatot kodol. A 22 eset a logikai
||| kapcsolatok teljes rendszeret alkotja.
|||
||| Az esetrendszer a [[7,1,3]] kod algebrababa van agyazva.
||| Minden eset egy E8 pontba van kodolva.
|||
||| Mi a kapcsolat az esetek es a logika kozott?
|||   Nominativusz = alany (ki/mi?)
|||   Accusativusz = targy (kit/mit?)
|||   Dativusz = cimzett (kinek/minek?)
|||   Instrumentalis = eszkoz (kivel/mivel?)
|||   ... a tobbi hasonloan.
|||
||| A logikai kapcsolat nem a hagyomanyos arisztoteleszi logika,
||| hanem a magyar nyelv esetrendszeren alapulo "eset logika".
||| Ez 24 kapcsolatbol all (22 eset + 2 atmenet).

public export
data Eset = Nominativusz | Accusativusz | Datívusz | Instrumentalis
          | Komitativusz | Kauzalis | Transzativusz | Terminativusz
          | Illativusz | Inesszivusz | Elativusz | Allativusz
          | Adesszivusz | Ablativusz | Szuperesszivusz | Delativusz
          | Szublativusz | Temporalis | Szociativusz | Distributivus
          | Esszivusz | Modalis | Causalis | Formaliss

||| Minden esethez tartozik egy logikai kapcsolat tipus.
||| A konstruktor neve a kapcsolat logikai nevet viseli,
||| nem az eset nevet — ez a kulonbseg a grammatika
||| es a logika kozott.
||| A nevek magyar teljes szavak, nem roviditesek.
public export
data EsetLogika : Eset -> Type where
  AlanyLogika    : EsetLogika Nominativusz
  TargyLogika    : EsetLogika Accusativusz
  CimzettLogika  : EsetLogika Datívusz
  EszkozLogika   : EsetLogika Instrumentalis
  TarsLogika     : EsetLogika Komitativusz
  OkLogika       : EsetLogika Kauzalis
  EredmenyLogika : EsetLogika Transzativusz
  HatárLogika    : EsetLogika Terminativusz
  IranyLogika    : EsetLogika Illativusz
  HelyLogika     : EsetLogika Inesszivusz
  HonnanLogika   : EsetLogika Elativusz
  CelLogika      : EsetLogika Allativusz
  KivelLogika    : EsetLogika Adesszivusz
  HonnanLogika2  : EsetLogika Ablativusz
  FelszinLogika  : EsetLogika Szuperesszivusz
  RolLogika      : EsetLogika Delativusz
  CelLogika2     : EsetLogika Szublativusz
  MikorLogika    : EsetLogika Temporalis
  KentiLogika    : EsetLogika Szociativusz
  ElosztLogika   : EsetLogika Distributivus
  MinosegLogika  : EsetLogika Esszivusz
  ModLogika      : EsetLogika Modalis
  CausalLogika   : EsetLogika Causalis
  AlakLogika     : EsetLogika Formaliss

||| Eset → E8 kodoszo (minden eset egy egyedi 8 bites vektor az E8 racsban).
||| A 24 eset kodolasa:
|||   elso 5 bit: a 24 eset egyedi azonositoja
|||   utolso 3 bit: a Steane kod 3 bitje (ido, oksag, fazis)
|||
||| A kodolas a Hamming tavolsagot maximalizalja —
||| a 24 eset kozott nincs ket egymashoz 3 bitnel
||| kozelebb. Ez azt jelenti, hogy 1 bit hiba javithato.
public export
esetKod : Eset -> E8Pont
esetKod Nominativusz   = E8PontKonstruktor 0 0 0 0 0 0 0 0
esetKod Accusativusz   = E8PontKonstruktor 1 0 0 0 0 0 0 0
esetKod Datívusz       = E8PontKonstruktor 0 1 0 0 0 0 0 0
esetKod Instrumentalis = E8PontKonstruktor 0 0 1 0 0 0 0 0
esetKod Komitativusz   = E8PontKonstruktor 0 0 0 1 0 0 0 0
esetKod Kauzalis       = E8PontKonstruktor 1 1 0 0 0 0 0 0
esetKod Transzativusz  = E8PontKonstruktor 1 0 1 0 0 0 0 0
esetKod Terminativusz  = E8PontKonstruktor 1 0 0 1 0 0 0 0
esetKod Illativusz     = E8PontKonstruktor 0 1 1 0 0 0 0 0
esetKod Inesszivusz    = E8PontKonstruktor 0 1 0 1 0 0 0 0
esetKod Elativusz      = E8PontKonstruktor 0 0 1 1 0 0 0 0
esetKod Allativusz     = E8PontKonstruktor 1 1 1 0 0 0 0 0
esetKod Adesszivusz    = E8PontKonstruktor 1 1 0 1 0 0 0 0
esetKod Ablativusz     = E8PontKonstruktor 1 0 1 1 0 0 0 0
esetKod Szuperesszivusz = E8PontKonstruktor 0 1 1 1 0 0 0 0
esetKod Delativusz     = E8PontKonstruktor 1 1 1 1 0 0 0 0
esetKod Szublativusz   = E8PontKonstruktor 0 0 0 0 1 0 0 0
esetKod Temporalis     = E8PontKonstruktor 0 0 0 0 0 1 0 0
esetKod Szociativusz   = E8PontKonstruktor 0 0 0 0 0 0 1 0
esetKod Distributivus  = E8PontKonstruktor 0 0 0 0 0 0 0 1
esetKod Esszivusz      = E8PontKonstruktor 1 0 0 0 1 0 0 0
esetKod Modalis        = E8PontKonstruktor 1 0 0 0 0 1 0 0
esetKod Causalis       = E8PontKonstruktor 1 0 0 0 0 0 1 0
esetKod Formaliss      = E8PontKonstruktor 1 0 0 0 0 0 0 1

||| FogalomTipus: a fogalmak tipusai a hierarchiaban.
||| Itt definialva, mert a RagozottSzo es a NyelvtaniKapcsolat
||| hasznalja. A FogalomFa modul ezt egesziti ki a logikai
||| kapcsolatokkal (FogalomLogika).
public export
data FogalomTipus = Gyoker | Cel | ReszCel | Feladat | ReszFeladat
                  | Cselekves | Dontes | Valasztas | Elutasitas
                  | Ok | Kavzatum | Korlatozas | Megfigyeles
                  | Hiba | Eredmeny | Minta | Javitas | Foltozas
                  | InfraJavitas | Szabaly | KemenySzabaly | Egyezmeny
                  | Eszkoz | Kesztseg | ModellKornyezetProtokoll | Kerdes | Magyarazat
                  | E8xE8 | Dualitas | Kategoria | Szimmetria | Tenzor | Funktor
                  -- Szamok
                  | TermeszetesSzam | EgeszSzam | RacionalisSzam | ValosSzam | KomplexSzam
                  -- Matematika logika
                  | Allitas | Bizonyitas | GodelSzam | Konzisztencia | Onhivatkozas
                  | GodelElsoTetel | GodelMasodikTetel | DiagonaleLemma | Bizonyithatosag
                  | InkonzisztenciaVonal | WickForgatas | KomplexFazis | KettoMatematika
                  -- Curry-Howard-Lambek
                  | Chl
                  -- Matematika alapaxiomak
                  | Halmazelmelet | PeanoAxiomak | ZfcAxiomak | KivalasztasiAxioma
                  | UresHalmaz | Szamossag | FolytonossagiHipotetikus
                  -- Fizika alapok — 4 dimenzio: ter, ido, energia, informaciomennyiseg
                  | FizikaiAllapot | Mezo | Ter | Ido | Tomeg | InformacioMennyiseg
                  -- Szimmetriak
                  | SzimmetriaCsoport | MertekCsoport | SzimmetriaTores | E8Szimmetria
                  -- Geometria, anyag
                  | Geometria | Anyag | Antianyag
                  -- Mechanika
                  | KlasszikusMechanika | LagrangeFuggveny | HamiltonFuggveny | LagrangeTranszformacio
                  -- Kvantum
                  | KvantumMechanika | KvantumAllapot | HullamFuggveny | Operator | Megfigyelt | KvantumUgres
                  -- Fazis
                  | FazisAtalakulas | FazisAtmenet | FazisElolas
                  -- Kolcsonhatasok
                  | Elektromagneses | Gyenge | Eros | Gravitacio | KvantumGravitacio
                  | EgyesitettMezo | StandardModell
                  -- Hullamok
                  | Hullam | Hang | Feny | GravitaciosHullam | RadioHullam
                  -- Fluktacio-disszipacio, homerseklet
                  | Fluktuacio | Disszipacio | FluktuacioDisszipacioTetele | Homerseklet
                  -- Termodinamika
                  | Termodinamika | CarnotCiklus | Entropia | Hő | Munka | BelsőEnergia | InformacioTorles
                  -- Szinek
                  | Szin | SzinToltes | AntiszinToltes | Gluon | KvarkSzin
                  -- Kommunikacio
                  | Informacio | Kommunikacio | Kod | Jel | Csatorna | Zaj | Bit
                  -- Folytonossag
                  | Folytonos | NemFolytonos | Codata | Sorozat | Hatar | Vegtelen

||| SzoTipus: minden szó egy konstruktor.
||| A szavak tipusként vannak reprezentálva — nincs String.
||| A szoFogalom, szoEset fuggvenyek adjak a nyelvtani tulajdonsagokat.
||| Eleinte a fogalomnevek (cel, ok, hiba...) maguk is magyar szavak.
public export
data SzoTipus : Type where
  -- Fogalomnevek mint magyar szavak (alanyeset)
  CelSzo           : SzoTipus  -- "cél" (Cel)
  OkSzo            : SzoTipus  -- "ok" (Ok)
  HibaSzo          : SzoTipus  -- "hiba" (Hiba)
  JavitasSzo       : SzoTipus  -- "javítás" (Javitas)
  SzabalySzo       : SzoTipus  -- "szabály" (Szabaly)
  EszkozSzo        : SzoTipus  -- "eszköz" (Eszkoz)
  KerdesSzo        : SzoTipus  -- "kérdés" (Kerdes)
  MagyarazatSzo     : SzoTipus  -- "magyarázat" (Magyarazat)
  CselekvesSzo     : SzoTipus  -- "cselekvés" (Cselekves)
  FeladatSzo       : SzoTipus  -- "feladat" (Feladat)
  DontesSzo        : SzoTipus  -- "döntés" (Dontes)
  EredmenySzo      : SzoTipus  -- "eredmény" (Eredmeny)
  -- Konkret mindennapi szavak
  HazSzo           : SzoTipus  -- "ház" (Eszkoz: lakhely)
  EmberSzo         : SzoTipus  -- "ember" (Gyoker: cselekvo)
  KutyaSzo         : SzoTipus  -- "kutya" (Eszkoz: tars)
  FaSzo            : SzoTipus  -- "fa" (Eszkoz: anyag)
  VizSzo           : SzoTipus  -- "víz" (Eszkoz: anyag)
  AsztalSzo        : SzoTipus  -- "asztal" (Eszkoz: hely)
  KonyvSzo         : SzoTipus  -- "könyv" (Eszkoz: tudas)
  EtelSzo          : SzoTipus  -- "étel" (Cel: táp)
  BaratSzo         : SzoTipus  -- "barát" (Gyoker: forras)
  TanuloSzo        : SzoTipus  -- "tanuló" (Gyoker: alany)
  HelySzo          : SzoTipus  -- "hely" (Eszkoz: ter)
  IdoSzo           : SzoTipus  -- "idő" (Minta: mertek)
  GondolatSzo      : SzoTipus  -- "gondolat" (Megfigyeles: elme)
  -- Ragozott alakok (pelda)
  CeltSzo          : SzoTipus  -- "célt" (Cel + Acc)
  CelnakSzo        : SzoTipus  -- "célnak" (Cel + Dat)
  OknakSzo         : SzoTipus  -- "oknak" (Ok + Dat)
  HibavalSzo       : SzoTipus  -- "hibával" (Hiba + Instr)
  EszkozzalSzo     : SzoTipus  -- "eszközzel" (Eszkoz + Instr)
  MagyarazatotSzo  : SzoTipus  -- "magyarázatot" (Magyarazat + Acc)
  HazatSzo         : SzoTipus  -- "házat" (Haz + Acc)
  HazbanSzo        : SzoTipus  -- "házban" (Haz + Inessivusz)
  HazbolSzo        : SzoTipus  -- "házból" (Haz + Elativusz)
  EmbertSzo        : SzoTipus  -- "embert" (Ember + Acc)
  EmbernekSzo      : SzoTipus  -- "embernek" (Ember + Dat)
  KonyvetSzo       : SzoTipus  -- "könyvet" (Konyv + Acc)
  KonyvvelSzo      : SzoTipus  -- "könyvvel" (Konyv + Instr)
  EteltSzo         : SzoTipus  -- "ételt" (Etel + Acc)
  VizetSzo         : SzoTipus  -- "vizet" (Viz + Acc)

||| Minden SzoTipushoz tartozik egy FogalomTipus.
public export
szoFogalom : SzoTipus -> FogalomTipus
szoFogalom CelSzo = Cel
szoFogalom OkSzo = Ok
szoFogalom HibaSzo = Hiba
szoFogalom JavitasSzo = Javitas
szoFogalom SzabalySzo = Szabaly
szoFogalom EszkozSzo = Eszkoz
szoFogalom KerdesSzo = Kerdes
szoFogalom MagyarazatSzo = Magyarazat
szoFogalom CselekvesSzo = Cselekves
szoFogalom FeladatSzo = Feladat
szoFogalom DontesSzo = Dontes
szoFogalom EredmenySzo = Eredmeny
szoFogalom HazSzo = Eszkoz
szoFogalom EmberSzo = Gyoker
szoFogalom KutyaSzo = Eszkoz
szoFogalom FaSzo = Eszkoz
szoFogalom VizSzo = Eszkoz
szoFogalom AsztalSzo = Eszkoz
szoFogalom KonyvSzo = Eszkoz
szoFogalom EtelSzo = Cel
szoFogalom BaratSzo = Gyoker
szoFogalom TanuloSzo = Gyoker
szoFogalom HelySzo = Eszkoz
szoFogalom IdoSzo = Minta
szoFogalom GondolatSzo = Megfigyeles
szoFogalom CeltSzo = Cel
szoFogalom CelnakSzo = Cel
szoFogalom OknakSzo = Ok
szoFogalom HibavalSzo = Hiba
szoFogalom EszkozzalSzo = Eszkoz
szoFogalom MagyarazatotSzo = Magyarazat
szoFogalom HazatSzo = Eszkoz
szoFogalom HazbanSzo = Eszkoz
szoFogalom HazbolSzo = Eszkoz
szoFogalom EmbertSzo = Gyoker
szoFogalom EmbernekSzo = Gyoker
szoFogalom KonyvetSzo = Eszkoz
szoFogalom KonyvvelSzo = Eszkoz
szoFogalom EteltSzo = Cel
szoFogalom VizetSzo = Eszkoz

||| Minden SzoTipushoz tartozik egy Eset.
public export
szoEset : SzoTipus -> Eset
szoEset CeltSzo = Accusativusz
szoEset CelnakSzo = Datívusz
szoEset OknakSzo = Datívusz
szoEset HibavalSzo = Instrumentalis
szoEset EszkozzalSzo = Instrumentalis
szoEset MagyarazatotSzo = Accusativusz
szoEset HazatSzo = Accusativusz
szoEset HazbanSzo = Inesszivusz
szoEset HazbolSzo = Elativusz
szoEset EmbertSzo = Accusativusz
szoEset EmbernekSzo = Datívusz
szoEset KonyvetSzo = Accusativusz
szoEset KonyvvelSzo = Instrumentalis
szoEset EteltSzo = Accusativusz
szoEset VizetSzo = Accusativusz
szoEset _ = Nominativusz

||| Minden SzoTipushoz tartozik egy IdoBeljegyzes.
public export
szoIdo : SzoTipus -> IdoBeljegyzes
szoIdo _ = IdoBeljegyzesKonstruktor Jelen Folyamatos Kozvetlen

||| Minden SzoTipushoz tartozik egy fazis (HaromKubit).
public export
szoFazis : SzoTipus -> HaromKubit
szoFazis _ = VilagKonstruktor Nulla Nulla Nulla

||| Magyar szo: to + szam + birtok + eset.
||| Az agglutinacio sorrendje rögzitett:
|||   to + szam + birtok + eset
||| Ez a morfologiai struktura a kategoriaelmeletben
||| egy bifunktornak felel meg: Fogalom × Eset × Ido → E8.
|||
||| A mezők:
|||   fogalom = a szo fogalmi tipusa
|||   szam = Kubit (Nulla=egyes, Egy=tobbes)
|||   birtok = Kubit (Nulla=nincs, Egy=van)
|||   eset = a 24 eset egyike
|||   ido = a harom ido dimenzio
|||   fazisKubit = a szo fazisa a harom kubitben
public export
record RagozottSzo where
  constructor SzoKonstruktor
  fogalom    : FogalomTipus  -- a szo fogalma
  szam       : Kubit         -- Nulla=egyes, Egy=tobbes
  birtok     : Kubit         -- Nulla=nincs, Egy=van
  eset       : Eset
  ido        : IdoBeljegyzes -- harom ido dimenzio
  fazisKubit : HaromKubit    -- a szo fazisa

||| Magyar nyelvtani kapcsolat: alany + ige + targy + egyeb esetek.
||| Minden kapcsolat a [[7,1,3]] koddal van kodolva.
|||
||| A kapcsolat egy cospan a kategoriaelmeletben:
|||   alany → ige ← targy
||| A kozos celpont az ige — ez kot ossze mindent.
|||
||| Az egyeb esetek (listaban) a kapcsolat tovabbi
||| resztvevoit tartalmazzak (pl. eszkoz, hely, ido).
public export
record NyelvtaniKapcsolat where
  constructor KapcsolatKonstruktor
  alany  : RagozottSzo
  ige    : RagozottSzo
  targy  : RagozottSzo
  egyeb  : List (Eset, RagozottSzo)
  kod    : E8E8KodSzo        -- E8 × E8 kodoszo
