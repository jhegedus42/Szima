module Rendszer

import Steane713
import HaromKubit
import E8E8Algebra
import MagyarNyelv
import FogalomFa
import FazisAlgebra
import KategoriaElmelet

||| A rendszer verifikacioja: egy teszt fuggveny,
||| ami ellenorzi, hogy a kategoriak osszekothetőek.
||| Ha fordul, akkor a tipusok konzisztensek.
|||
||| Ez a fuggveny nem csinal semmit runtime —
||| csak a forditas soran ellenőri a tipusokat.
public export
rendszerVerifikacio : ()
rendszerVerifikacio =
  let -- Kategoriak
      fk = fogalomKategoria
      ek = esetKategoria
      e8k = e8Kategoria
      hkk = haromKubitKategoria
      ik = idoKategoria

      -- Funktorok
      ef = esetE8Funktor
      ff = fogalomE8Funktor
      kef = kubitE8Funktor
      ief = idoE8Funktor

      -- A funktorok objektum kepei
      _ = ef.objektumKep Nominativusz
      _ = ff.objektumKep Gyoker
      _ = kef.objektumKep (VilagKonstruktor Nulla Nulla Nulla)

      -- Morfizmusok
      _ = fk.azonos Gyoker
      _ = ek.azonos Nominativusz
      _ = e8k.azonos (E8PontKonstruktor 0 0 0 0 0 0 0 0)

      -- Osszetetelek
      _ = fk.osszetetel (FogalomIre GyokerCel) (FogalomIre CelFeladat)
      _ = ek.osszetetel (EsetMorfKonstruktor AlanyLogika) (EsetMorfKonstruktor AlanyLogika)

      -- RagozottSzo pelda
      peldaSzo = SzoKonstruktor
        Cel
        Nulla
        Nulla
        Nominativusz
        (IdoBeljegyzesKonstruktor Jelen Folyamatos Kozvetlen)
        (VilagKonstruktor Nulla Nulla Nulla)

      _ = ragozottSzoE8Pont peldaSzo

      -- NyelvtaniKapcsolat pelda
      peldaIge = SzoKonstruktor
        Cselekves Nulla Nulla Nominativusz
        (IdoBeljegyzesKonstruktor Jelen Folyamatos Kozvetlen)
        (VilagKonstruktor Nulla Nulla Nulla)
      peldaKapcs = KapcsolatKonstruktor
        peldaSzo peldaIge peldaSzo
        []
        (KodKonstruktor "pelda"
          (E8PontKonstruktor 0 0 0 0 0 0 0 0)
          (E8PontKonstruktor 0 0 0 0 0 0 0 0)
          (CliﬀordKonstruktor 1 0 0)
          (alapKod Nulla))

      _ = nyelvtaniKapcsolatKod peldaKapcs

      -- Fazis
      _ = fazisOsszehasonlit
            (KodKonstruktor "a"
              (E8PontKonstruktor 1 0 0 0 0 0 0 0)
              (E8PontKonstruktor 0 1 0 0 0 0 0 0)
              (CliﬀordKonstruktor 1 0 0)
              (alapKod Nulla))
            (KodKonstruktor "b"
              (E8PontKonstruktor 0 0 0 0 0 0 0 0)
              (E8PontKonstruktor 1 0 0 0 0 0 0 0)
              (CliﬀordKonstruktor 0 1 0)
              (alapKod Egy))

      -- ToltesParitasIdo
      _ = fazisFaktorialis
            (ToltesParitasIdoKonstruktor
              (VilagKonstruktor Nulla Nulla Nulla)
              (VilagKonstruktor Nulla Nulla Nulla)
              (VilagKonstruktor Nulla Nulla Nulla))

  in ()

||| A [[7,1,3]] kod hasznalata: egy kod generalasa
||| a fogalom tipusbol.
||| A kod a Steane algoritmussal lesz generalva.
public export
fogalomKod : FogalomTipus -> E8E8KodSzo
fogalomKod f = KodKonstruktor
  (fogalomNev f)
  (fogalomTipusKod f)
  (fogalomTipusKod f)
  (CliﬀordKonstruktor 1 0 1)
  (alapKod Nulla)

||| A [[7,1,3]] hibajavitas hasznalata egy kodon.
public export
fogalomKodJavit : E8E8KodSzo -> Szindroma -> E8E8KodSzo
fogalomKodJavit (KodKonstruktor c b j cl s) szindroma =
  KodKonstruktor c b j cl (javitas s szindroma)

||| A fazis redundancia hasznalata: egy lista megszurése.
public export
redundanciaSzures : List E8E8KodSzo -> List E8E8KodSzo
redundanciaSzures = szurd
