module FogalomFa

import MagyarNyelv
import HaromKubit
import E8E8Algebra

||| Fogalom hierarchia: mely tipusok lehetnek egy masik gyerekei.
||| Egesziti ki a FogalomTipus-t a logikai kapcsolatokkal.
|||
||| Gondolat: nem minden fogalom lehet barmelyik masik gyereke.
||| Peldaul egy Kerdes soha nem lehet gyereke egy Cselekves-nek.
||| A 35 ervenyes kapcsolat a teljes hierarchiat irja le.
|||
||| A konstruktorok neve a ket fogalom osszefuzese:
|||   GyokerCel = "a Gyoker gyereke lehet Cel"
||| Ez a kategoriaelmeletben morfizmusnak felel meg.
public export
data FogalomLogika : FogalomTipus -> FogalomTipus -> Type where
  Azonos          : FogalomLogika a a
  GyokerCel       : FogalomLogika Gyoker Cel
  GyokerDontes    : FogalomLogika Gyoker Dontes
  GyokerSzabaly   : FogalomLogika Gyoker Szabaly
  GyokerMegfigyeles : FogalomLogika Gyoker Megfigyeles
  GyokerKerdes    : FogalomLogika Gyoker Kerdes
  CelReszCel      : FogalomLogika Cel ReszCel
  CelFeladat      : FogalomLogika Cel Feladat
  ReszCelFeladat  : FogalomLogika ReszCel Feladat
  FeladatReszFeladat : FogalomLogika Feladat ReszFeladat
  FeladatCselekves   : FogalomLogika Feladat Cselekves
  FeladatEredmeny    : FogalomLogika Feladat Eredmeny
  ReszFeladatCselekves : FogalomLogika ReszFeladat Cselekves
  CselekvesEredmeny    : FogalomLogika Cselekves Eredmeny
  CselekvesMegfigyeles  : FogalomLogika Cselekves Megfigyeles
  DontesOk             : FogalomLogika Dontes Ok
  DontesValasztas      : FogalomLogika Dontes Valasztas
  DontesElutasitas     : FogalomLogika Dontes Elutasitas
  ValasztasOk          : FogalomLogika Valasztas Ok
  ElutasitasOk         : FogalomLogika Elutasitas Ok
  OkKavzatum           : FogalomLogika Ok Kavzatum
  OkKorlatozas         : FogalomLogika Ok Korlatozas
  MegfigyelesHiba      : FogalomLogika Megfigyeles Hiba
  MegfigyelesEredmeny  : FogalomLogika Megfigyeles Eredmeny
  MegfigyelesMinta     : FogalomLogika Megfigyeles Minta
  MegfigyelesJavitas   : FogalomLogika Megfigyeles Javitas
  MegfigyelesDontes    : FogalomLogika Megfigyeles Dontes
  HibaOk              : FogalomLogika Hiba Ok
  HibaJavitas         : FogalomLogika Hiba Javitas
  JavitasFoltozas     : FogalomLogika Javitas Foltozas
  JavitasInfra        : FogalomLogika Javitas InfraJavitas
  SzabalyKemeny       : FogalomLogika Szabaly KemenySzabaly
  SzabalyEgyezmeny    : FogalomLogika Szabaly Egyezmeny
  EszkozKeszseg      : FogalomLogika Eszkoz Kesztseg
  EszkozModellKornyezetProtokoll : FogalomLogika Eszkoz ModellKornyezetProtokoll
  KerdesMagyarazat    : FogalomLogika Kerdes Magyarazat
  GyokerReszCel       : FogalomLogika Gyoker ReszCel
  GyokerFeladat       : FogalomLogika Gyoker Feladat
  CelReszFeladat      : FogalomLogika Cel ReszFeladat
  CelCselekves        : FogalomLogika Cel Cselekves
  GyokerOk            : FogalomLogika Gyoker Ok
  GyokerValasztas     : FogalomLogika Gyoker Valasztas
  GyokerElutasitas    : FogalomLogika Gyoker Elutasitas
  GyokerHiba          : FogalomLogika Gyoker Hiba
  GyokerEredmeny      : FogalomLogika Gyoker Eredmeny
  GyokerMagyarazat    : FogalomLogika Gyoker Magyarazat
  GyokerKemenySzabaly : FogalomLogika Gyoker KemenySzabaly
  GyokerEgyezmeny     : FogalomLogika Gyoker Egyezmeny
  GyokerJavitas       : FogalomLogika Gyoker Javitas
  MegfigyelesOk       : FogalomLogika Megfigyeles Ok
  HibaKavzatum        : FogalomLogika Hiba Kavzatum
  HibaKorlatozas      : FogalomLogika Hiba Korlatozas
  HibaFoltozas        : FogalomLogika Hiba Foltozas
  HibaInfra           : FogalomLogika Hiba InfraJavitas
  ReszFeladatEredmeny : FogalomLogika ReszFeladat Eredmeny
  -- E8xE8, dualitas, kategoria
  E8xE8Dualitas      : FogalomLogika E8xE8 Dualitas
  E8xE8Kategoria     : FogalomLogika E8xE8 Kategoria
  DualitasCel        : FogalomLogika Dualitas Cel
  DualitasOk         : FogalomLogika Dualitas Ok
  DualitasKavzatum   : FogalomLogika Dualitas Kavzatum
  KategoriaSzimmetria : FogalomLogika Kategoria Szimmetria
  KategoriaTenzor     : FogalomLogika Kategoria Tenzor
  SzimmetriaFunktor   : FogalomLogika Szimmetria Funktor
  TenzorFunktor       : FogalomLogika Tenzor Funktor
  -- Kozvetlen kompoziciok a gyokerbol az uj fogalmakhoz
  GyokerE8xE8        : FogalomLogika Gyoker E8xE8
  GyokerDualitas     : FogalomLogika Gyoker Dualitas
  GyokerKategoria    : FogalomLogika Gyoker Kategoria
  -- Szamok
  GyokerTermeszetesSzam  : FogalomLogika Gyoker TermeszetesSzam
  GyokerEgeszSzam        : FogalomLogika Gyoker EgeszSzam
  GyokerValosSzam        : FogalomLogika Gyoker ValosSzam
  GyokerKomplexSzam      : FogalomLogika Gyoker KomplexSzam
  TermeszetesSzamEgesz   : FogalomLogika TermeszetesSzam EgeszSzam
  EgeszSzamRacionalis    : FogalomLogika EgeszSzam RacionalisSzam
  -- Matematika logika
  GyokerAllitas          : FogalomLogika Gyoker Allitas
  AllitasBizonyitas      : FogalomLogika Allitas Bizonyitas
  BizonyitasGodel        : FogalomLogika Bizonyitas GodelSzam
  AllitasKonzisztencia   : FogalomLogika Allitas Konzisztencia
  AllitasOnhivatkozas    : FogalomLogika Allitas Onhivatkozas
  OnhivatkozasDiagonale  : FogalomLogika Onhivatkozas DiagonaleLemma
  DiagonaleGodelElso     : FogalomLogika DiagonaleLemma GodelElsoTetel
  KonzisztenciaGodelMasodik : FogalomLogika Konzisztencia GodelMasodikTetel
  AllitasBizonyithatosag : FogalomLogika Allitas Bizonyithatosag
  GyokerKonzisztencia    : FogalomLogika Gyoker Konzisztencia
  GyokerOnhivatkozas     : FogalomLogika Gyoker Onhivatkozas
  -- 4 dimenzio
  GyokerTer              : FogalomLogika Gyoker Ter
  GyokerIdo              : FogalomLogika Gyoker Ido
  GyokerEnergia          : FogalomLogika Gyoker Energia
  GyokerInformacio       : FogalomLogika Gyoker InformacioMennyiseg
  TerGeometria           : FogalomLogika Ter Geometria
  IdoFazisAtalakulas     : FogalomLogika Ido FazisAtalakulas
  EnergiaHomerseklet     : FogalomLogika Energia Homerseklet
  InformacioEntropia     : FogalomLogika InformacioMennyiseg Entropia
  -- Fizikai allapot, mechanika
  GyokerFizikaiAllapot   : FogalomLogika Gyoker FizikaiAllapot
  FizikaiAllapotMezo     : FogalomLogika FizikaiAllapot Mezo
  FizikaiAllapotKlasszikus : FogalomLogika FizikaiAllapot KlasszikusMechanika
  KlasszikusLagrange     : FogalomLogika KlasszikusMechanika LagrangeFuggveny
  LagrangeHamilton       : FogalomLogika LagrangeFuggveny HamiltonFuggveny
  LagrangeTranszform     : FogalomLogika LagrangeFuggveny LagrangeTranszformacio
  -- Szimmetriak
  GyokerSzimmetriaCsoport : FogalomLogika Gyoker SzimmetriaCsoport
  GyokerGeometria        : FogalomLogika Gyoker Geometria
  SzimmetriaE8           : FogalomLogika SzimmetriaCsoport E8Szimmetria
  SzimmetriaMertek       : FogalomLogika SzimmetriaCsoport MertekCsoport
  MertekElektromagneses  : FogalomLogika MertekCsoport Elektromagneses
  MertekGyenge           : FogalomLogika MertekCsoport Gyenge
  MertekEros             : FogalomLogika MertekCsoport Eros
  ErosGluon              : FogalomLogika Eros Gluon
  E8Gravitacio           : FogalomLogika E8Szimmetria Gravitacio
  GravitacioKvantum      : FogalomLogika Gravitacio KvantumGravitacio
  KvantumEgyesitett      : FogalomLogika KvantumGravitacio EgyesitettMezo
  EgyesitettStandard     : FogalomLogika EgyesitettMezo StandardModell
  -- Anyag
  GyokerAnyag            : FogalomLogika Gyoker Anyag
  AnyagAntianyag         : FogalomLogika Anyag Antianyag
  AnyagKvark             : FogalomLogika Anyag KvarkSzin
  KvarkSzinSzin          : FogalomLogika KvarkSzin Szin
  SzinToltesAntiszin     : FogalomLogika SzinToltes AntiszinToltes
  -- Kvantum
  GyokerKvantumMechanika : FogalomLogika Gyoker KvantumMechanika
  KvantumMechanikaAllapot : FogalomLogika KvantumMechanika KvantumAllapot
  KvantumAllapotHullam   : FogalomLogika KvantumAllapot HullamFuggveny
  KvantumAllapotOperator  : FogalomLogika KvantumAllapot Operator
  OperatorMegfigyelt     : FogalomLogika Operator Megfigyelt
  KvantumAllapotUgres    : FogalomLogika KvantumAllapot KvantumUgres
  HullamFolytonos        : FogalomLogika HullamFuggveny Folytonos
  UgresNemFolytonos      : FogalomLogika KvantumUgres NemFolytonos
  -- Hullamok
  GyokerHullam           : FogalomLogika Gyoker Hullam
  HullamHang             : FogalomLogika Hullam Hang
  HullamFeny             : FogalomLogika Hullam Feny
  HullamGravitacios      : FogalomLogika Hullam GravitaciosHullam
  HullamRadio            : FogalomLogika Hullam RadioHullam
  FenyElektromagneses    : FogalomLogika Feny Elektromagneses
  GravitaciosGravitacio  : FogalomLogika GravitaciosHullam Gravitacio
  RadioInformacio        : FogalomLogika RadioHullam Informacio
  -- Termodinamika
  GyokerTermodinamika    : FogalomLogika Gyoker Termodinamika
  TermodinamikaCarnot    : FogalomLogika Termodinamika CarnotCiklus
  FluktuacioDisszipacioTetel : FogalomLogika FluktuacioDisszipacioTetele Termodinamika
  FluktuacioDisszip       : FogalomLogika Fluktuacio Disszipacio
  HőEnergia              : FogalomLogika Hő Energia
  MunkaEnergia           : FogalomLogika Munka Energia
  BelsőHő                : FogalomLogika BelsőEnergia Hő
  -- Fazis
  FazisAtalakulasAtmenet  : FogalomLogika FazisAtalakulas FazisAtmenet
  FazisAtmenetFluktuacio  : FogalomLogika FazisAtmenet Fluktuacio
  FazisElolasDisszipacio  : FogalomLogika FazisElolas Disszipacio
  -- Kommunikacio
  GyokerKommunikacio     : FogalomLogika Gyoker Kommunikacio
  InformacioKommunikacio  : FogalomLogika Informacio Kommunikacio
  KommunikacioCsatorna   : FogalomLogika Kommunikacio Csatorna
  KommunikacioKod        : FogalomLogika Kommunikacio Kod
  KommunikacioJel        : FogalomLogika Kommunikacio Jel
  CsatornaZaj            : FogalomLogika Csatorna Zaj
  -- Folytonossag
  GyokerFolytonos        : FogalomLogika Gyoker Folytonos
  FolytonosCodata        : FogalomLogika Folytonos Codata
  NemFolytonosSorozat    : FogalomLogika NemFolytonos Sorozat
  SorozatHatar           : FogalomLogika Sorozat Hatar
  HatarVegtelen          : FogalomLogika Hatar Vegtelen
  -- Standard Modell
  StandardElektromagneses : FogalomLogika StandardModell Elektromagneses
  StandardGyenge          : FogalomLogika StandardModell Gyenge
  StandardEros            : FogalomLogika StandardModell Eros
  StandardAnyag           : FogalomLogika StandardModell Anyag
  StandardKvantum         : FogalomLogika StandardModell KvantumMechanika

||| Fa csomopont adatai.
||| Minden csomopontnak van:
|||   cimke = a csomopont neve (String, mert ez megjeleniteshez kell)
|||   leiras = reszletes leiras (String, mert ez emberi olvasasra)
|||   hivatkozasok = kapcsolodo referencia lista
|||   bizalom = a csomopont megbizhatosaga 0 es 1 kozott
|||
||| A String itt kivétel — a megjeleniteshez es emberi olvasashoz
||| van, nem a logikai mag resze. A mag tipusok (FogalomTipus, eset)
||| nem hasznalnak String-et.
public export
record FogalomAdat where
  constructor AdatKonstruktor
  cimke : String
  leiras : String
  hivatkozasok : List String
  bizalom : Double

||| Fogalom fa: egy csomopont, amely a FogalomTipus alapjan
||| tartalmazza a hierarchiaban elfoglalt helyet.
|||
||| A fa ketfele lehet:
|||   Level = levél (nincs gyereke)
|||   Ag = ag (van gyereke, es megadja a kapcsolat tipusat is)
|||
||| Az Ag a dependens tipussal biztosítja, hogy minden gyerek
||| kapcsolata ervenyes FogalomLogika legyen.
public export
data FogalomFa : FogalomTipus -> Type where
  Level  : FogalomAdat -> FogalomFa t
  Ag     : FogalomAdat
         -> List (s : FogalomTipus ** (FogalomFa s, FogalomLogika t s))
         -> FogalomFa t

||| A harom kubit kapcsolata a fa szerkezeteben.
||| A VilagFa egyesiti a harom nezoPontot:
|||   sajat = a rendszer sajat fogalomfaja (C = toltes)
|||   masik = a masik fel fogalomfaja  (P = paritas)
|||   fazis = a kapcsolat fazisa (T = ido)
|||
||| Ez a harom egyutt adja a teljes CPT szimmetriat.
public export
record VilagFa where
  constructor VilagFaKonstruktor
  sajat : FogalomFa Gyoker     -- a rendszer sajat nezoPontja (C)
  masik : FogalomFa Gyoker     -- a masik fel nezoPontja (P)
  fazis : FogalomAdat          -- a kapcsolat fazisa (T)

||| Fa merete: a csomopontok szama a faban.
||| Ez egy rekurziv szamlalas: minden level 1, minden ag
||| 1 plusz a gyerekek meretenek osszege.
|||
||| Kategoriaelmeleti ertelemben ez egy funktor a
||| FogalomFa kategoriaabol a Nat monoidba.
public export
meret : FogalomFa t -> Nat
meret (Level _) = 1
meret (Ag _ gyerekek) = 1 + sum (map (\(s ** (fa, _)) => meret fa) gyerekek)

||| Bizalom atlag: a fa osszes csomopontjanak bizalom atlaga.
||| Ez a koherencia egy merteke — ha alacsony, a fa reszben
||| megbizhatatlan (tobbszoros hiba).
public export
bizalomAtlag : FogalomFa t -> Double
bizalomAtlag (Level adat) = adat.bizalom
bizalomAtlag (Ag adat gyerekek) =
  let sajat = adat.bizalom
      gyerekBizalom = map (\(s ** (fa, _)) => bizalomAtlag fa) gyerekek
  in (sajat + sum gyerekBizalom) / cast (1 + length gyerekek)

||| Gyerekek szama egy csomopontban.
public export
gyerekekSzama : FogalomFa t -> Nat
gyerekekSzama (Level _) = 0
gyerekekSzama (Ag _ gyerekek) = length gyerekek
