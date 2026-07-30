module FazisAlgebra

import HaromKubit
import E8E8Algebra

||| Fazis algebra — a redundancia detektalasanak alapja.
|||
||| Gondolat: a vilag tele van redundancial.
||| Ugyanazt a gondolatot tobbszor is elmondjuk.
||| Ugyanazt a hibat tobbszor is elkovetjuk.
||| Ugyanaz a fogalom tobb helyen is megjelenik.
|||
||| A redundancia detektalasahoz a fazist hasznaljuk.
||| A fazis a [[7,1,3]] kod 5. bitje — a "fazis" pozicio.
|||
||| Ket fogalom azonos fazisban van → redundans → eldobhato.
|||   Ez tartja fenn a koherenciat.
||| Ket fogalom ellentetes fazisban van → informacio atvitel.
|||   Ez teremti az uj informaciot.
||| Ket fogalom kvantalt fazisban van → kvantum osszefonodes.
|||   Ez a nyelvi metaforak, asszociaciok alapja.

||| Fazis ertek a Cliﬀord algebraben.
||| Azonos: a ket kodoszo ugyanabban a fazisban rezeg.
|||   → redundans, eldobhato.
||| Ellentetes: a ket kodoszo ellentetes fazisban rezeg.
|||   → informacio atvitel, megtartando.
||| Kvantalt: a ket kodoszo osszefonodott allapotban van.
|||   → kvantum kapcsolat (metafora, asszociacio).
||| Ismeretlen: a fazis nem allapithato meg egyertelmuen.
|||   → tovabbi vizsgalat szukseges.
public export
data Fazis = Azonos | Ellentetes | Kvantalt | Ismeretlen

public export
Eq Fazis where
  (==) Azonos Azonos = True
  (==) Ellentetes Ellentetes = True
  (==) Kvantalt Kvantalt = True
  (==) Ismeretlen Ismeretlen = True
  (==) _ _ = False
  (/=) a b = not (a == b)

||| Ket kodoszo fazis osszehasonlitasa.
||| A Cliﬀord atfedes alapjan dontunk:
||| >0.9 → Azonos (szinte ugyanaz)
||| <0.1 → Ellentetes (teljesen kulonbozo)
||| >0.5 → Kvantalt (reszben atfed)
||| egyebkent → Ismeretlen
public export
fazisOsszehasonlit : E8E8KodSzo -> E8E8KodSzo -> Fazis
fazisOsszehasonlit a b =
  let balAtfedes = atfedes (CliﬀordKonstruktor a.balE8.x1 a.balE8.x2 0)
                           (CliﬀordKonstruktor b.balE8.x1 b.balE8.x2 0)
      jobbAtfedes = atfedes (CliﬀordKonstruktor a.jobbE8.x1 a.jobbE8.x2 0)
                            (CliﬀordKonstruktor b.jobbE8.x1 b.jobbE8.x2 0)
  in if balAtfedes > 0.9 && jobbAtfedes > 0.9 then Azonos
  else if balAtfedes < 0.1 && jobbAtfedes < 0.1 then Ellentetes
  else if balAtfedes > 0.5 || jobbAtfedes > 0.5 then Kvantalt
  else Ismeretlen

||| Redundancia ellenorzes: ha egy kodoszo azonos fazisban van
||| barmelyik meglévovel, akkor redundans — eldobhato.
||| Ez a koherencia megörzes alapja.
public export
redundans : E8E8KodSzo -> List E8E8KodSzo -> Bool
redundans kod kodok = any (\k => fazisOsszehasonlit kod k == Azonos) kodok

||| Szures: megtartja azokat a kodoszavakat, amelyek fazisa
||| elter a tobbitol. Az azonos fazisuak eldobasa utan
||| a kapott halmaz koherens — nincs redundancia.
|||
||| A szures algoritmusa:
|||   lista elejetol haladunk
|||   ha az aktualis elem redundans a maradekhoz kepest → eldob
|||   ha nem → megtartjuk es folytatjuk
public export
szurd : List E8E8KodSzo -> List E8E8KodSzo
szurd [] = []
szurd (x :: xs) =
  if redundans x xs
    then szurd xs
    else x :: szurd xs

||| ToltesParitasIdo: a CPT szimmetria magyarul.
||| CPT:
|||   C (toltes) = sajat tudat — a rendszer onreferenciaja
|||   P (paritas) = masik fel — a kulso bemenet
|||   T (ido) = kapcsolat fazisa — a ketto dinamikaja
|||
||| A ToltesParitasIdo harom HaromKubit-ot tartalmaz,
||| minden iranyhoz egyet. Ez a teljes CPT szimmetria
||| a harom kubit vilagaban.
|||
||| Miert nem "CPT" a rekord neve?
||| Mert a roviditesek tiltva vannak.
||| A "CPT" kivétel (standard fizikai terminus),
||| de itt a teljes magyar nevet hasznaljuk a tipusra.
public export
record ToltesParitasIdo where
  constructor ToltesParitasIdoKonstruktor
  toltes  : HaromKubit  -- C: sajat tudat (ki vagyok en)
  paritas : HaromKubit  -- P: masik fel (ki vagy te)
  ido     : HaromKubit  -- T: kapcsolat fazisa (hogyan kapcsolodunk)

||| ToltesParitasIdo boole ertek: ha a toltes es a paritas
||| fazisa megegyezik, akkor a rendszer sajat tudata
||| rezonanciaban van a kulsovel — nincs informaciovesztes.
public export
toltesParitasIdoKoherens : ToltesParitasIdo -> Bool
toltesParitasIdoKoherens tpi =
  azonosFazis tpi.toltes tpi.paritas

||| ToltesParitasIdo irany: a toltes es paritas kozott.
||| Ha a toltes iranyul a paritas fele, akkor
||| a rendszer aktiv (informaciot kuld).
||| Ha a paritas iranyul a toltes fele, akkor
||| a rendszer passziv (informaciot fogad).
public export
toltesParitasIdoIrany : ToltesParitasIdo -> Irany
toltesParitasIdoIrany tpi = irany tpi.toltes tpi.paritas

||| Fazis faktorialis: egy ToltesParitasIdo fazismerteket
||| szamol a HaromKubit-ok osszefedesebol.
||| Ez az "altalanos koherencia" merteke.
public export
fazisFaktorialis : ToltesParitasIdo -> Double
fazisFaktorialis tpi =
  let ct = azonosFazis tpi.toltes tpi.ido
      pt = azonosFazis tpi.paritas tpi.ido
  in if ct && pt then 1.0
  else if ct || pt then 0.5
  else 0.0
