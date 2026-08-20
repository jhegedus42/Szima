module AffinE8KarakterLevezetes

import Data.List
import Data.Vect
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

public export
binomialis : Nat -> Nat -> Nat
binomialis _ Z = 1
binomialis Z (S _) = 0
binomialis (S felso) (S also) =
  binomialis felso also + binomialis felso (S also)

-- =====================================================================
-- 2. CONSTRUCTION A THÉTA-SOR A KÓD SÚLYELOSZLÁSÁBÓL
--
-- A négy szükséges egész fokot a három kódszó-súlyosztály szerint
-- bontjuk fel. Ez ugyanaz a súlyfelsoroló-helyettesítés, de minden
-- együttható véges kombinatorikus receptként látható.
--
-- Nulla súlyú kódszó:
--   a nemnulla koordináták +-2 értékűek;
--   az n-edik fokhoz n koordinátát választunk és mindnek két előjele van.
--
-- Négy súlyú kódszó:
--   az alapállapot négy darab +-1 koordináta, ezért 2^4 lehetőség;
--   a következő fokokat a négy páros koordináta +-2 gerjesztése,
--   illetve egy páratlan koordináta +-1 helyett +-3 értéke adja.
--
-- Nyolc súlyú kódszó:
--   nyolc darab +-1 koordináta, ezért a második fokon 2^8 lehetőség.
-- =====================================================================

public export
NullaSulyuKodSzoThetaEgeszFokSor : List Nat
NullaSulyuKodSzoThetaEgeszFokSor =
  listaEgyutthatonkentSkalaz E8KodNullaSulyuSzavai
    [ 1
    , binomialis 8 1 * kettoHatvany 1
    , binomialis 8 2 * kettoHatvany 2
    , binomialis 8 3 * kettoHatvany 3
    ]

public export
NegySulyuKodSzoThetaEgeszFokSor : List Nat
NegySulyuKodSzoThetaEgeszFokSor =
  listaEgyutthatonkentSkalaz E8KodNegySulyuSzavai
    [ 0
    , kettoHatvany 4
    , (binomialis 4 1 * kettoHatvany 1) * kettoHatvany 4
    , (binomialis 4 2 * kettoHatvany 2) * kettoHatvany 4 +
      4 * kettoHatvany 4
    ]

public export
NyolcSulyuKodSzoThetaEgeszFokSor : List Nat
NyolcSulyuKodSzoThetaEgeszFokSor =
  listaEgyutthatonkentSkalaz E8KodNyolcSulyuSzavai
    [0, 0, kettoHatvany 8, 0]

public export
E8ThetaHaromFokig : List Nat
E8ThetaHaromFokig =
  listaEgyutthatonkentOsszead
    NullaSulyuKodSzoThetaEgeszFokSor
    (listaEgyutthatonkentOsszead
      NegySulyuKodSzoThetaEgeszFokSor
      NyolcSulyuKodSzoThetaEgeszFokSor)

BizonyitasE8ThetaHaromFokig :
  E8ThetaHaromFokig = [1, 240, 2160, 6720]
BizonyitasE8ThetaHaromFokig =
  rewrite BizonyitasE8KodNullaSulyuSzavai in
  rewrite BizonyitasE8KodNegySulyuSzavai in
  rewrite BizonyitasE8KodNyolcSulyuSzavai in
  Refl

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
BizonyitasAffinE8ElsoSzintuKarakterHaromFokig =
  rewrite BizonyitasE8ThetaHaromFokig in
  rewrite BizonyitasNyolcSzinuOszcillatorSorHaromFokig in
  Refl

public export
ElsoFokGyokEsCartanUton : Nat
ElsoFokGyokEsCartanUton = E8MinimalisVektorokSzama + E8Rang

public export
ElsoFokKarakterUton : Nat
ElsoFokKarakterUton =
  listaElemVagyNulla 1 AffinE8ElsoSzintuKarakterHaromFokig

BizonyitasElsoFokKetFuggetlenUton :
  ElsoFokGyokEsCartanUton = ElsoFokKarakterUton
BizonyitasElsoFokKetFuggetlenUton =
  rewrite BizonyitasE8MinimalisVektorokSzama in
  rewrite BizonyitasAffinE8ElsoSzintuKarakterHaromFokig in
  Refl

BizonyitasElsoFokKetszazNegyvennyolc :
  ElsoFokKarakterUton = 248
BizonyitasElsoFokKetszazNegyvennyolc =
  rewrite BizonyitasAffinE8ElsoSzintuKarakterHaromFokig in
  Refl

public export
MasodikFokFelbontasUton : Nat
MasodikFokFelbontasUton =
  listaElemVagyNulla 2 E8ThetaHaromFokig +
  listaElemVagyNulla 1 E8ThetaHaromFokig *
    listaElemVagyNulla 1 NyolcSzinuOszcillatorSorHaromFokig +
  listaElemVagyNulla 2 NyolcSzinuOszcillatorSorHaromFokig

BizonyitasMasodikFokNegyezerSzazHuszonnegy :
  MasodikFokFelbontasUton = 4124
BizonyitasMasodikFokNegyezerSzazHuszonnegy =
  rewrite BizonyitasE8ThetaHaromFokig in
  rewrite BizonyitasNyolcSzinuOszcillatorSorHaromFokig in
  Refl

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
BizonyitasHarmadikFokHarmincNegyezerHetszazOtvenketto =
  rewrite BizonyitasE8ThetaHaromFokig in
  rewrite BizonyitasNyolcSzinuOszcillatorSorHaromFokig in
  Refl

-- =====================================================================
-- 5. A MODULÁRIS j-INVARIÁNS KÖBGYÖKÉNEK VÉGES ELLENŐRZÉSE
--
-- A normalizált karakter q^(-1/3) szorzójának köbe q^(-1).
-- Ezért az alábbi lista rendre a q^(-1), q^0, q^1 és q^2
-- együtthatóját adja a karakter köbében.
--
-- A köb nagy együtthatóit Integer felett normalizáljuk. Idris 2 0.8.0
-- a típusszintű Nat-szorzást Peano-alakban végzi, ezért a 248^3
-- közvetlen Nat-Refl ellenőrzése indokolatlanul nagy fordítási fát ad.
-- =====================================================================

public export
termeszetesListaEgeszListava : List Nat -> List Integer
termeszetesListaEgeszListava = map cast

public export
egeszListaEgyutthatonkentOsszead :
  List Integer -> List Integer -> List Integer
egeszListaEgyutthatonkentOsszead [] jobb = jobb
egeszListaEgyutthatonkentOsszead bal [] = bal
egeszListaEgyutthatonkentOsszead
  (balElem :: tobbiBalElem)
  (jobbElem :: tobbiJobbElem) =
    (balElem + jobbElem) ::
    egeszListaEgyutthatonkentOsszead tobbiBalElem tobbiJobbElem

public export
egeszPolinomTeljesSzorzata :
  List Integer -> List Integer -> List Integer
egeszPolinomTeljesSzorzata [] _ = []
egeszPolinomTeljesSzorzata (balElem :: tobbiBalElem) jobb =
  egeszListaEgyutthatonkentOsszead
    (map (\jobbElem => balElem * jobbElem) jobb)
    (0 :: egeszPolinomTeljesSzorzata tobbiBalElem jobb)

public export
egeszPolinomCsonkoltSzorzata :
  (egyutthatokSzama : Nat) ->
  List Integer -> List Integer -> List Integer
egeszPolinomCsonkoltSzorzata egyutthatokSzama bal jobb =
  take egyutthatokSzama
    (egeszPolinomTeljesSzorzata bal jobb ++
     replicate egyutthatokSzama 0)

public export
egeszPolinomEgyseg : (egyutthatokSzama : Nat) -> List Integer
egeszPolinomEgyseg Z = []
egeszPolinomEgyseg (S tobbiEgyutthatoSzama) =
  1 :: replicate tobbiEgyutthatoSzama 0

public export
egeszPolinomCsonkoltHatvanya :
  (egyutthatokSzama : Nat) -> Nat -> List Integer -> List Integer
egeszPolinomCsonkoltHatvanya egyutthatokSzama Z _ =
  egeszPolinomEgyseg egyutthatokSzama
egeszPolinomCsonkoltHatvanya
  egyutthatokSzama (S kisebbHatvany) polinom =
    egeszPolinomCsonkoltSzorzata
      egyutthatokSzama
      polinom
      (egeszPolinomCsonkoltHatvanya
        egyutthatokSzama kisebbHatvany polinom)

public export
AffinE8ElsoSzintuKarakterHaromFokigEgesz : List Integer
AffinE8ElsoSzintuKarakterHaromFokigEgesz =
  termeszetesListaEgeszListava AffinE8ElsoSzintuKarakterHaromFokig

BizonyitasAffinE8ElsoSzintuKarakterHaromFokigEgesz :
  AffinE8ElsoSzintuKarakterHaromFokigEgesz =
    [1, 248, 4124, 34752]
BizonyitasAffinE8ElsoSzintuKarakterHaromFokigEgesz =
  cong
    termeszetesListaEgeszListava
    BizonyitasAffinE8ElsoSzintuKarakterHaromFokig

public export
KarakterBelsoKobeHaromFokig : List Integer
KarakterBelsoKobeHaromFokig =
  egeszPolinomCsonkoltHatvanya
    4 3 AffinE8ElsoSzintuKarakterHaromFokigEgesz

BizonyitasKarakterKobeModularisJInvariansKezdete :
  KarakterBelsoKobeHaromFokig =
    [1, 744, 196884, 21493760]
BizonyitasKarakterKobeModularisJInvariansKezdete =
  rewrite BizonyitasAffinE8ElsoSzintuKarakterHaromFokigEgesz in
  Refl

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
SugawaraKozpontiToltesSzamlalo : Nat
SugawaraKozpontiToltesSzamlalo =
  AffinSzint * E8LieAlgebraDimenzio

public export
SugawaraKozpontiToltesNevezo : Nat
SugawaraKozpontiToltesNevezo =
  AffinSzint + E8DualisCoxeterSzam

public export
RacsKozpontiToltesSzamlalo : Nat
RacsKozpontiToltesSzamlalo = E8Rang

public export
RacsKozpontiToltesNevezo : Nat
RacsKozpontiToltesNevezo = 1

BizonyitasKozpontiToltesKetUton :
  SugawaraKozpontiToltesSzamlalo * RacsKozpontiToltesNevezo =
  RacsKozpontiToltesSzamlalo * SugawaraKozpontiToltesNevezo
BizonyitasKozpontiToltesKetUton =
  rewrite BizonyitasE8MinimalisVektorokSzama in
  Refl

BizonyitasRacsKozpontiToltesNyolc :
  RacsKozpontiToltesSzamlalo = 8
BizonyitasRacsKozpontiToltesNyolc = Refl

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
            show SugawaraKozpontiToltesSzamlalo ++ "/" ++
            show SugawaraKozpontiToltesNevezo ++ " = " ++
            show RacsKozpontiToltesSzamlalo ++ "/" ++
            show RacsKozpontiToltesNevezo)
  putStrLn "Határ: ez affin reprezentációelmélet, nem kvantumhibajavító kód."
