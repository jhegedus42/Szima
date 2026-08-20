module AffinE8KarakterLevezetes

import Data.List
import E8SteaneLevezetes

%default total

-- =====================================================================
-- AZ AFFIN E8 ELSŐ SZINTŰ KARAKTERÉNEK VÉGES LEVEZETÉSE
--
-- Ez a modul nem kvantumhibajavító kódot készít.
--
-- A matematikai lánc:
--
--   [8,4,4] kiterjesztett Hamming-kód
--       -> Construction A
--   E8-rács
--       -> rács-vertexoperátor-algebra
--   az affin E8 első szintű alapreprezentációja.
--
-- Az általános izomorfia a Frenkel--Kac-tétel irodalmi eredménye.
-- Az Idris-kernel itt a lánc első véges együtthatóit számolja ki:
--
--   théta-sor:       1, 240, 2160, 6720
--   oszcillátorsor:  1,   8,   44,  192
--   karakter:        1, 248, 4124, 34752
--
-- A karakter köbének első együtthatói:
--
--   1, 744, 196884, 21493760,
--
-- amelyek a q^(-1) kezdőfok eltolása után a moduláris j-invariáns
-- első együtthatói. A teljes karakterazonosság irodalmi tétel;
-- a modul csak a feltüntetett véges kezdőszeletet bizonyítja.
-- =====================================================================

-- =====================================================================
-- 1. VÉGES POLINOMARITMETIKA
-- =====================================================================

public export
listaEgyutthatonkentOsszead : List Nat -> List Nat -> List Nat
listaEgyutthatonkentOsszead [] jobb = jobb
listaEgyutthatonkentOsszead bal [] = bal
listaEgyutthatonkentOsszead
  (balElem :: tobbiBalElem)
  (jobbElem :: tobbiJobbElem) =
    (balElem + jobbElem) ::
    listaEgyutthatonkentOsszead tobbiBalElem tobbiJobbElem

public export
listaEgyutthatonkentSkalaz : Nat -> List Nat -> List Nat
listaEgyutthatonkentSkalaz szorzo =
  map (\egyutthato => szorzo * egyutthato)

public export
polinomTeljesSzorzata : List Nat -> List Nat -> List Nat
polinomTeljesSzorzata [] _ = []
polinomTeljesSzorzata (balElem :: tobbiBalElem) jobb =
  listaEgyutthatonkentOsszead
    (map (\jobbElem => balElem * jobbElem) jobb)
    (0 :: polinomTeljesSzorzata tobbiBalElem jobb)

public export
polinomCsonkoltSzorzata :
  (egyutthatokSzama : Nat) -> List Nat -> List Nat -> List Nat
polinomCsonkoltSzorzata egyutthatokSzama bal jobb =
  take egyutthatokSzama
    (polinomTeljesSzorzata bal jobb ++
     replicate egyutthatokSzama 0)

public export
polinomEgyseg : (egyutthatokSzama : Nat) -> List Nat
polinomEgyseg Z = []
polinomEgyseg (S tobbiEgyutthatoSzama) =
  1 :: replicate tobbiEgyutthatoSzama 0

public export
polinomCsonkoltHatvanya :
  (egyutthatokSzama : Nat) -> Nat -> List Nat -> List Nat
polinomCsonkoltHatvanya egyutthatokSzama Z _ =
  polinomEgyseg egyutthatokSzama
polinomCsonkoltHatvanya egyutthatokSzama (S kisebbHatvany) polinom =
  polinomCsonkoltSzorzata
    egyutthatokSzama
    polinom
    (polinomCsonkoltHatvanya
      egyutthatokSzama kisebbHatvany polinom)

public export
listaElemVagyNulla : Nat -> List Nat -> Nat
listaElemVagyNulla _ [] = 0
listaElemVagyNulla Z (elem :: _) = elem
listaElemVagyNulla (S kisebbIndex) (_ :: tobbiElem) =
  listaElemVagyNulla kisebbIndex tobbiElem

-- =====================================================================
-- 2. CONSTRUCTION A THÉTA-SOR A KÓD SÚLYELOSZLÁSÁBÓL
--
-- Negyedfok-egységeket használunk, hogy a páratlan koordináták
-- negyedegész kitevői is természetes számú indexet kapjanak.
--
-- Páros koordináta:
--   x = 0       -> negyedfok 0, egy lehetőség
--   x = +-2     -> negyedfok 4, két lehetőség.
--
-- Páratlan koordináta:
--   x = +-1     -> negyedfok 1, két lehetőség
--   x = +-3     -> negyedfok 9, két lehetőség.
--
-- A tizenkettedik negyedfokig más koordináta nem járul hozzá.
-- =====================================================================

public export
NegyedfokEgyutthatokSzama : Nat
NegyedfokEgyutthatokSzama = 13

public export
ParosKoordinataNegyedfokSor : List Nat
ParosKoordinataNegyedfokSor =
  [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]

public export
ParatlanKoordinataNegyedfokSor : List Nat
ParatlanKoordinataNegyedfokSor =
  [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]

public export
NullaSulyuKodSzoThetaTag : List Nat
NullaSulyuKodSzoThetaTag =
  listaEgyutthatonkentSkalaz
    E8KodNullaSulyuSzavai
    (polinomCsonkoltHatvanya
      NegyedfokEgyutthatokSzama 8 ParosKoordinataNegyedfokSor)

public export
NegySulyuKodSzoThetaTag : List Nat
NegySulyuKodSzoThetaTag =
  listaEgyutthatonkentSkalaz
    E8KodNegySulyuSzavai
    (polinomCsonkoltSzorzata
      NegyedfokEgyutthatokSzama
      (polinomCsonkoltHatvanya
        NegyedfokEgyutthatokSzama 4 ParosKoordinataNegyedfokSor)
      (polinomCsonkoltHatvanya
        NegyedfokEgyutthatokSzama 4 ParatlanKoordinataNegyedfokSor))

public export
NyolcSulyuKodSzoThetaTag : List Nat
NyolcSulyuKodSzoThetaTag =
  listaEgyutthatonkentSkalaz
    E8KodNyolcSulyuSzavai
    (polinomCsonkoltHatvanya
      NegyedfokEgyutthatokSzama 8 ParatlanKoordinataNegyedfokSor)

public export
ConstructionAThetaNegyedfokSor : List Nat
ConstructionAThetaNegyedfokSor =
  listaEgyutthatonkentOsszead
    NullaSulyuKodSzoThetaTag
    (listaEgyutthatonkentOsszead
      NegySulyuKodSzoThetaTag
      NyolcSulyuKodSzoThetaTag)

BizonyitasConstructionAThetaNegyedfokSor :
  ConstructionAThetaNegyedfokSor =
    [1, 0, 0, 0, 240, 0, 0, 0, 2160, 0, 0, 0, 6720]
BizonyitasConstructionAThetaNegyedfokSor = Refl

public export
E8ThetaHaromFokig : List Nat
E8ThetaHaromFokig =
  [ listaElemVagyNulla 0 ConstructionAThetaNegyedfokSor
  , listaElemVagyNulla 4 ConstructionAThetaNegyedfokSor
  , listaElemVagyNulla 8 ConstructionAThetaNegyedfokSor
  , listaElemVagyNulla 12 ConstructionAThetaNegyedfokSor
  ]

BizonyitasE8ThetaHaromFokig :
  E8ThetaHaromFokig = [1, 240, 2160, 6720]
BizonyitasE8ThetaHaromFokig = Refl

-- =====================================================================
-- 3. NYOLCSZÍNŰ BOZONIKUS OSZCILLÁTORSOR
--
-- Nyolc megkülönböztethető oszcillátorszín között r gerjesztés
-- szétosztásainak száma:
--
--   binomiális(r + 7, 7).
--
-- A harmadik fokig csak az első három frekvenciamód kell.
-- =====================================================================

public export
binomialis : Nat -> Nat -> Nat
binomialis _ Z = 1
binomialis Z (S _) = 0
binomialis (S felso) (S also) =
  binomialis felso also + binomialis felso (S also)

public export
nyolcSzinuElosztasokSzama : Nat -> Nat
nyolcSzinuElosztasokSzama gerjesztesekSzama =
  binomialis (gerjesztesekSzama + 7) 7

public export
ElsoFrekvenciaModusSor : List Nat
ElsoFrekvenciaModusSor =
  [ nyolcSzinuElosztasokSzama 0
  , nyolcSzinuElosztasokSzama 1
  , nyolcSzinuElosztasokSzama 2
  , nyolcSzinuElosztasokSzama 3
  ]

public export
MasodikFrekvenciaModusSor : List Nat
MasodikFrekvenciaModusSor =
  [nyolcSzinuElosztasokSzama 0, 0,
   nyolcSzinuElosztasokSzama 1, 0]

public export
HarmadikFrekvenciaModusSor : List Nat
HarmadikFrekvenciaModusSor =
  [nyolcSzinuElosztasokSzama 0, 0, 0,
   nyolcSzinuElosztasokSzama 1]

BizonyitasElsoFrekvenciaModusSor :
  ElsoFrekvenciaModusSor = [1, 8, 36, 120]
BizonyitasElsoFrekvenciaModusSor = Refl

public export
NyolcSzinuOszcillatorSorHaromFokig : List Nat
NyolcSzinuOszcillatorSorHaromFokig =
  polinomCsonkoltSzorzata 4
    ElsoFrekvenciaModusSor
    (polinomCsonkoltSzorzata 4
      MasodikFrekvenciaModusSor
      HarmadikFrekvenciaModusSor)

BizonyitasNyolcSzinuOszcillatorSorHaromFokig :
  NyolcSzinuOszcillatorSorHaromFokig = [1, 8, 44, 192]
BizonyitasNyolcSzinuOszcillatorSorHaromFokig = Refl

-- =====================================================================
-- 4. AZ AFFIN E8 ELSŐ SZINTŰ KARAKTERE
--
-- A rács-vertexoperátor-algebra karakterének fokozott dimenziói a
-- théta-sor és a nyolcszínű oszcillátorsor konvolúciójából adódnak.
-- =====================================================================

public export
AffinE8ElsoSzintuKarakterHaromFokig : List Nat
AffinE8ElsoSzintuKarakterHaromFokig =
  polinomCsonkoltSzorzata
    4 E8ThetaHaromFokig NyolcSzinuOszcillatorSorHaromFokig

BizonyitasAffinE8ElsoSzintuKarakterHaromFokig :
  AffinE8ElsoSzintuKarakterHaromFokig =
    [1, 248, 4124, 34752]
BizonyitasAffinE8ElsoSzintuKarakterHaromFokig = Refl

public export
ElsoFokGyokEsCartanUton : Nat
ElsoFokGyokEsCartanUton = E8MinimalisVektorokSzama + E8Rang

public export
ElsoFokKarakterUton : Nat
ElsoFokKarakterUton =
  listaElemVagyNulla 1 AffinE8ElsoSzintuKarakterHaromFokig

BizonyitasElsoFokKetFuggetlenUton :
  ElsoFokGyokEsCartanUton = ElsoFokKarakterUton
BizonyitasElsoFokKetFuggetlenUton = Refl

BizonyitasElsoFokKetszazNegyvennyolc :
  ElsoFokKarakterUton = 248
BizonyitasElsoFokKetszazNegyvennyolc = Refl

public export
MasodikFokFelbontasUton : Nat
MasodikFokFelbontasUton =
  listaElemVagyNulla 2 E8ThetaHaromFokig +
  listaElemVagyNulla 1 E8ThetaHaromFokig *
    listaElemVagyNulla 1 NyolcSzinuOszcillatorSorHaromFokig +
  listaElemVagyNulla 2 NyolcSzinuOszcillatorSorHaromFokig

BizonyitasMasodikFokNegyezerSzazHuszonnegy :
  MasodikFokFelbontasUton = 4124
BizonyitasMasodikFokNegyezerSzazHuszonnegy = Refl

public export
HarmadikFokFelbontasUton : Nat
HarmadikFokFelbontasUton =
  listaElemVagyNulla 3 E8ThetaHaromFokig +
  listaElemVagyNulla 2 E8ThetaHaromFokig *
    listaElemVagyNulla 1 NyolcSzinuOszcillatorSorHaromFokig +
  listaElemVagyNulla 1 E8ThetaHaromFokig *
    listaElemVagyNulla 2 NyolcSzinuOszcillatorSorHaromFokig +
  listaElemVagyNulla 3 NyolcSzinuOszcillatorSorHaromFokig

BizonyitasHarmadikFokHarmincNegyezerHetszazOtvenketto :
  HarmadikFokFelbontasUton = 34752
BizonyitasHarmadikFokHarmincNegyezerHetszazOtvenketto = Refl

-- =====================================================================
-- 5. A MODULÁRIS j-INVARIÁNS KÖBGYÖKÉNEK VÉGES ELLENŐRZÉSE
--
-- A normalizált karakter q^(-1/3) szorzójának köbe q^(-1).
-- Ezért az alábbi lista rendre a q^(-1), q^0, q^1 és q^2
-- együtthatóját adja a karakter köbében.
-- =====================================================================

public export
KarakterBelsoKobeHaromFokig : List Nat
KarakterBelsoKobeHaromFokig =
  polinomCsonkoltHatvanya
    4 3 AffinE8ElsoSzintuKarakterHaromFokig

BizonyitasKarakterKobeModularisJInvariansKezdete :
  KarakterBelsoKobeHaromFokig =
    [1, 744, 196884, 21493760]
BizonyitasKarakterKobeModularisJInvariansKezdete = Refl

-- =====================================================================
-- 6. A NYOLCAS KÖZPONTI TÖLTÉS KÉT ÚTON
-- =====================================================================

public export
AffinSzint : Nat
AffinSzint = 1

public export
E8LieAlgebraDimenzio : Nat
E8LieAlgebraDimenzio = ElsoFokGyokEsCartanUton

public export
E8DualisCoxeterSzam : Nat
E8DualisCoxeterSzam = 30

public export
SugawaraKozpontiToltes : Nat
SugawaraKozpontiToltes =
  (AffinSzint * E8LieAlgebraDimenzio) `div`
  (AffinSzint + E8DualisCoxeterSzam)

public export
RacsKozpontiToltes : Nat
RacsKozpontiToltes = E8Rang

BizonyitasKozpontiToltesKetUton :
  SugawaraKozpontiToltes = RacsKozpontiToltes
BizonyitasKozpontiToltesKetUton = Refl

BizonyitasKozpontiToltesNyolc :
  SugawaraKozpontiToltes = 8
BizonyitasKozpontiToltesNyolc = Refl

-- =====================================================================
-- 7. FUTTATHATÓ JELENTÉS
-- =====================================================================

public export
affinE8KarakterJelentes : IO ()
affinE8KarakterJelentes = do
  putStrLn "Affin E8 első szintű karakter:"
  putStrLn ("  Construction A théta-sor: " ++
            show E8ThetaHaromFokig)
  putStrLn ("  nyolcszínű oszcillátorsor: " ++
            show NyolcSzinuOszcillatorSorHaromFokig)
  putStrLn ("  fokozott karakter: " ++
            show AffinE8ElsoSzintuKarakterHaromFokig)
  putStrLn ("  248 két független úton: " ++
            show ElsoFokGyokEsCartanUton ++ " = " ++
            show ElsoFokKarakterUton)
  putStrLn ("  karakterköb, a moduláris j-invariáns kezdete: " ++
            show KarakterBelsoKobeHaromFokig)
  putStrLn ("  központi töltés két úton: " ++
            show SugawaraKozpontiToltes ++ " = " ++
            show RacsKozpontiToltes)
  putStrLn "Határ: ez affin reprezentációelmélet, nem kvantumhibajavító kód."
