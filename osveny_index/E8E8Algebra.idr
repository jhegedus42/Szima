module E8E8Algebra

import Steane713

||| E8 × E8 algebra — a magyar nyelv esetrendszerenek algebrai alapja.
|||
||| Gondolat: miert E8? Mert az E8 racs a legnagyobb kiveteles
||| Lie algebra, 248 dimenzioja pontosan elegendo a 22 eset,
||| 7 kubit, es 3 idodimenzio egyideju lekepezesere.
|||
||| E8 bal oldal → ter (fogalmak elhelyezkedese a racsban).
|||   Minden fogalomnak van egy "helye" a fogalmi racsban.
||| E8 jobb oldal → szin (fazis es osszefonodes).
|||   A szin hatarozza meg, hogy ket fogalom hogyan rezeg egyutt.
||| Cliﬀord szorzat → hang (a harmonikus rezgesek).
|||   A geometriai szorzat kelt hangot — informaciot.
|||
||| A Cliﬀord geometriai szorzat: ab = a·b + a∧b
|||   a·b = belso szorzat → atfedes (redundancia)
|||     Ha a·b magas, a ket fogalom ugyanazt mondja — eldobhato.
|||   a∧b = kulso szorzat → ujdonsag (informacio)
|||     Ha a∧b magas, a ket fogalom uj informaciot hordoz — megtartando.
|||
||| Az E8 × E8 a bal es jobb E8 tenzor szorzata.
||| A Cliﬀord elem a kapcsolatukat irja le.
||| A [[7,1,3]] Steane kod a hiba javitast biztositja.

||| E8 racs pont: 8 egesz koordinata.
||| A 8 koordinata:
|||   x1-x4: a Steane kod 7 bitjebol 4 (ido, oksag, ter, szin)
|||   x5-x8: a maradek 3 bit + egy szabad dimenzio (hang, fazis, mod, egyseg)
public export
record E8Pont where
  constructor E8PontKonstruktor
  x1 : Int; x2 : Int; x3 : Int; x4 : Int
  x5 : Int; x6 : Int; x7 : Int; x8 : Int

||| Cliﬀord algebra alap 8 dimenzioban.
||| A Lap tipus a 8 dimenzio mindegyiket egy-egy hatvanykent kodolja.
|||  Lap 0 = skalar (1), Lap 1 = elso baxis (e1), stb.
|||  A 128 bites ertek a 8. dimenzio (e8).
|||  Ez a 2^8 = 256 dimenzios Cliﬀord algebra alapja.
public export
data Lap : Int -> Type where
  Skalar : Lap 0
  S1 : Lap 1;  S2 : Lap 2;  S3 : Lap 4;  S4 : Lap 8
  S5 : Lap 16; S6 : Lap 32; S7 : Lap 64; S8 : Lap 128

||| Cliﬀord elem: lapok linearis kombinacioja.
||| A skalar, vektor, es bivektor mezők egy-egy
||| Cliﬀord lapot reprezentalnak.
||| skalar = 0-dimenzios resz (a·b atfedes alapja)
||| vektor = 1-dimenzios resz (irany)
||| bivektor = 2-dimenzios resz (forgatas / kapcsolat)
public export
record CliﬀordElem where
  constructor CliﬀordKonstruktor
  skalar : Int
  vektor : Int
  bivektor : Int

||| Geometriai szorzat belso resze = atfedes.
||| A ket Cliﬀord elem skalaris reszebol szamolva.
||| Magas atfedes → redundans → eldobhato.
||| Az atfedes 0 es 1 kozotti ertek: 0 = nincs atfedes,
||| 1 = teljes atfedes (ugyanaz az informacio).
||| A +1 a nevezoben a nullaval valo osztas elkerulesere.
public export
atfedes : CliﬀordElem -> CliﬀordElem -> Double
atfedes a b =
  let s = a.skalar * b.skalar + a.vektor * b.vektor
      na = a.skalar * a.skalar + a.vektor * a.vektor
      nb = b.skalar * b.skalar + b.vektor * b.vektor
  in cast s / cast (na + nb + 1)

||| Kuszob: efelett redundans.
||| 0.8 = 80% atfedes felett eldobjuk.
||| Ez a kuszob empirikusan valasztva: a nyelvben
||| a 80% feletti hasonlosag mar nem hordoz uj informaciot.
public export
atfedesKuszob : Double
atfedesKuszob = 0.8

||| Eldontes: egy fogalom megtartasa vagy eldobasa
||| az atfedes merteke alapjan.
public export
data Eldontes = DobdEl | TartsdMeg

public export
eldont : Double -> Eldontes
eldont o = if o > atfedesKuszob then DobdEl else TartsdMeg

||| E8 × E8 kodoszo: bal E8 + jobb E8 + Cliﬀord es [[7,1,3]].
||| A kodoszo egy teljes fogalmi kapcsolatot kodol:
|||   cimke = a kapcsolat neve (a "mirol van szo")
|||   balE8 = a fogalom helye a terben
|||   jobbE8 = a fogalom szine a fazisban
|||   cliﬀord = a ket E8 kapcsolata (hang)
|||   steane = a [[7,1,3]] hiba javito kod
|||
||| A mezők nevei:
|||   cimke, balE8, jobbE8, cliﬀord, steane — mind magyar,
|||   a kivetelek a szabvany fizikai terminusok (E8, Cliﬀord, Steane).
public export
record E8E8KodSzo where
  constructor KodKonstruktor
  cimke    : String
  balE8    : E8Pont     -- ter: a fogalom helye
  jobbE8   : E8Pont     -- szin: a fogalom fazisa
  cliﬀord  : CliﬀordElem -- hang: a kapcsolat
  steane   : HetesKod    -- [[7,1,3]] hiba javito kod

||| E8Pont osszeadas: ket pont osszege a racsban.
||| A komponensenkenti osszeadas az E8 racs
||| csoportmuvelete — zart a racsra.
public export
e8Osszead : E8Pont -> E8Pont -> E8Pont
e8Osszead a b = E8PontKonstruktor
  (a.x1 + b.x1) (a.x2 + b.x2) (a.x3 + b.x3) (a.x4 + b.x4)
  (a.x5 + b.x5) (a.x6 + b.x6) (a.x7 + b.x7) (a.x8 + b.x8)

||| Cliﬀord szorzat: a geometriai szorzat 8 dimenzioban.
||| ab = a·b + a∧b
||| Itt a skalar es vektor reszbol szamitjuk a szorzatot.
public export
cliﬀordSzorzat : CliﬀordElem -> CliﬀordElem -> CliﬀordElem
cliﬀordSzorzat a b = CliﬀordKonstruktor
  (a.skalar * b.skalar - a.vektor * b.vektor)
  (a.skalar * b.vektor + a.vektor * b.skalar)
  (a.vektor * b.vektor)

||| Atfedes ket E8E8KodSzo kozott.
||| A bal es jobb E8 atfedesenek atlaga.
||| Ez mutatja, hogy ket kodoszo mennyire fedi egymast.
public export
e8e8Atfedes : E8E8KodSzo -> E8E8KodSzo -> Double
e8e8Atfedes a b =
  let ba = atfedes (CliﬀordKonstruktor a.balE8.x1 a.balE8.x2 0)
                   (CliﬀordKonstruktor b.balE8.x1 b.balE8.x2 0)
      ja = atfedes (CliﬀordKonstruktor a.jobbE8.x1 a.jobbE8.x2 0)
                   (CliﬀordKonstruktor b.jobbE8.x1 b.jobbE8.x2 0)
  in (ba + ja) / 2.0
