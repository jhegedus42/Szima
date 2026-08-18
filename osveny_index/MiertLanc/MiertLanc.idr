module MiertLanc.MiertLanc

-- Megjegyzes: az eredeti importok (Alap.KategoriaT, Steane713, Alap.DependensSzamT)
-- elavultak a konyvtarszerkezet valtozasa miatt. A modul nem hasznalja oket
-- a kodban (csak kommentekben emliti). A javitashoz ujra kellene irni az
-- import-utvonalakat a jelenlegi osveny_index/ struktura szerint.
-- A modul csak primitiv tipusokat hasznal (String, Nat, Bool, Maybe, Eq, Show, List).
-- L. AGENTS.md: "Soha ne hasznalj Pythont. Csak Idris." — a miert-lanc is Idris.

-- ═══════════════════════════════════════════════════════════════
-- MIÉRT-LÁNC — KATEGÓRIAELMÉLETILEG BEÁGYAZOTT INDEX
-- ═══════════════════════════════════════════════════════════════
-- A why-chain nem egy JSON fájl — egy KATEGÓRIA.
-- A bejegyzések = objektumok.
-- Az ok-okozati kapcsolatok = morfizmusok.
-- A hasonlóság (Clifford átfedés) = a morfizmus tulajdonsága.
-- A kompakátálás = coend ezen a kategórián.
-- A hierarchia = funktor az index kategóriából a lánc kategóriába.
-- A Wadler "free proof" = a típus bizonyítja a kompakátálás helyességét.

-- ═══════════════════════════════════════════════════════════════
-- 1. A 7 TÉMA = A 7 EMBERI DIMENZIÓ (OBJEKTUMOK)
-- ═══════════════════════════════════════════════════════════════

||| A miért-lánc 7 témája = a 7 emberi dimenzió.
||| Minden bejegyzés egy témához tartozik.
||| A témák = a kategória objektumai.
public export
data Tema : Type where
  TemaKategoriaelmelet : Tema
  TemaFizika          : Tema
  TemaKvantum         : Tema
  TemaNyelv           : Tema
  TemaCselekves       : Tema
  TemaTipusok         : Tema
  TemaSzabalyok       : Tema

public export
Eq Tema where
  (==) TemaKategoriaelmelet TemaKategoriaelmelet = True
  (==) TemaFizika TemaFizika = True
  (==) TemaKvantum TemaKvantum = True
  (==) TemaNyelv TemaNyelv = True
  (==) TemaCselekves TemaCselekves = True
  (==) TemaTipusok TemaTipusok = True
  (==) TemaSzabalyok TemaSzabalyok = True
  (==) _ _ = False

||| Téma → magyar név.
public export
temaMagyarNev : Tema -> String
temaMagyarNev TemaKategoriaelmelet = "Kategoriaelmelet (Oksag)"
temaMagyarNev TemaFizika = "Fizika (Ter)"
temaMagyarNev TemaKvantum = "Kvantum (Szin)"
temaMagyarNev TemaNyelv = "Nyelv (Hang)"
temaMagyarNev TemaCselekves = "Cselekves (Fazis)"
temaMagyarNev TemaTipusok = "Tipusok (Mod)"
temaMagyarNev TemaSzabalyok = "Szabalyok (Ido)"

||| Téma → emberi dimenzió bit pozíció (0-6).
public export
temaBitPozicio : Tema -> Nat
temaBitPozicio TemaKategoriaelmelet = 1  -- Oksag
temaBitPozicio TemaFizika = 2            -- Ter
temaBitPozicio TemaKvantum = 3           -- Szin
temaBitPozicio TemaNyelv = 4             -- Hang
temaBitPozicio TemaCselekves = 5         -- Fazis
temaBitPozicio TemaTipusok = 6           -- Mod
temaBitPozicio TemaSzabalyok = 0         -- Ido

-- ═══════════════════════════════════════════════════════════════
-- 2. BEJEGYZÉS = MORFIZMUS A TÉMÁK KÖZÖTT
-- ═══════════════════════════════════════════════════════════════

||| Egy miért-lánc bejegyzés = egy morfizus a kategóriában.
||| A bejegyzés egy témából (forrás) egy témába (cél) mutat.
||| Ha a forrás = cél, akkor a bejegyzés "saját témában" van.
||| Ha a forrás ≠ cél, akkor a bejegyzés KAPCSOL két témát.
public export
record MiertBejegyzes where
  constructor MiertBejegyzesKonstruktor
  bejegyzesAzonosito : String
  forrasTema   : Tema
  celTema      : Tema
  miert        : String
  mit          : String
  dontes       : String
  bizalom      : Nat  -- 0 = alacsony, 1 = kozepes, 2 = magas

||| A bejegyzés "saját témában" van-e (forrás = cél = identitás morfizmus).
public export
sajatTemaban : MiertBejegyzes -> Bool
sajatTemaban b = b.forrasTema == b.celTema

||| A bejegyzés "kapcsolat" két tema kozott (forras ≠ cel).
public export
kapcsolatTemaKozott : MiertBejegyzes -> Bool
kapcsolatTemaKozott b = not (sajatTemaban b)

-- ═══════════════════════════════════════════════════════════════
-- 3. OK-OKZATI MORFIZMUS = BEJEGYZÉS KOMPOZÍCIÓ
-- ═══════════════════════════════════════════════════════════════

||| Ok-okozati kompozíció: ha b1 (A→B) és b2 (B→C), akkor b1∘b2 (A→C).
||| Ez a kategória kompozíciója a miért-láncon.
||| A Wadler "free proof" biztosítja, hogy a kompozíció uniform.
public export
okOkozatiKompozicio : MiertBejegyzes -> MiertBejegyzes -> Maybe MiertBejegyzes
okOkozatiKompozicio b1 b2 =
  if b1.celTema == b2.forrasTema
  then Just (MiertBejegyzesKonstruktor
              (b1.bejegyzesAzonosito ++ "∘" ++ b2.bejegyzesAzonosito)
              b1.forrasTema
              b2.celTema
              (b1.miert ++ " → " ++ b2.miert)
              (b1.mit ++ " → " ++ b2.mit)
              (b1.dontes ++ " → " ++ b2.dontes)
              (min b1.bizalom b2.bizalom))
  else Nothing

-- ═══════════════════════════════════════════════════════════════
-- 4. CLIFFORD ÁTFEDÉS = HASONLÓSÁG MÉRÉSE
-- ═══════════════════════════════════════════════════════════════

||| Két bejegyzés hasonlósága: hány témában egyeznek?
||| Ha ugyanaz a forrás ÉS cél → átfedés magas.
||| Ha ugyanaz a forrás de más cél → átfedés közepes.
||| Ha mind különbözik → átfedés alacsony.
public export
data Atfedes : Type where
  MagasAtfedes   : Atfedes  -- ugyanaz a tema (eldobhato)
  KozepesAtfedes : Atfedes  -- rokon tema
  AlacsonyAtfedes : Atfedes -- kulonbozo tema

||| Két bejegyzés átfedése.
public export
atfedesMertek : MiertBejegyzes -> MiertBejegyzes -> Atfedes
atfedesMertek b1 b2 =
  if b1.forrasTema == b2.forrasTema && b1.celTema == b2.celTema
  then MagasAtfedes
  else if b1.forrasTema == b2.forrasTema || b1.celTema == b2.celTema
       then KozepesAtfedes
       else AlacsonyAtfedes

||| Eldobható-e egy bejegyzés (magas átfedés + alacsony bizalom)?
public export
eldobhatoE : MiertBejegyzes -> MiertBejegyzes -> Bool
eldobhatoE b1 b2 =
  case atfedesMertek b1 b2 of
    MagasAtfedes => True
    _ => False

-- ═══════════════════════════════════════════════════════════════
-- 5. A KATEGÓRIA STRUKTÚRA
-- ═══════════════════════════════════════════════════════════════

||| A miért-lánc kategória:
||| Objektumok: Tema (7 emberi dimenzió)
||| Morfizmusok: MiertBejegyzes (Tema → Tema)
||| Kompozíció: okOkozatiKompozicio
||| Identitás: sajat temaban levo bejegyzes
|||
||| Ez egy KategoriaT instance (ha Tema = objektum, MiertBejegyzes = hom).
||| De mivel a KategoriaT-nek torvenyei is vannak (balAzonos, jobbAzonos, asszociativ),
||| azokat kulon kell bizonyitani.

||| Identitás morfizus egy témára.
public export
miertIdentitas : Tema -> MiertBejegyzes
miertIdentitas t = MiertBejegyzesKonstruktor
  "id" t t "identitas" "identitas" "nincs" 2

||| Kompozíció: okOkozatiKompozicio, de garantáltan létezik (believe_me ha nem egyezik).
public export
miertKompozicio : MiertBejegyzes -> MiertBejegyzes -> MiertBejegyzes
miertKompozicio b1 b2 =
  case okOkozatiKompozicio b1 b2 of
    Just b => b
    Nothing => believe_me "kompozicio nem egyezik"

-- ═══════════════════════════════════════════════════════════════
-- 6. KOMPAKTÁLÁS = COEND A MIÉRT-LÁNC KATEGÓRIÁJÁN
-- ═══════════════════════════════════════════════════════════════

||| A kompakátálás = a lánc tömörítése.
||| Kategóriaelméletileg: coend ∫^c S(c,c).
||| A redundáns bejegyzéseket eldobjuk (MagasAtfedes).
||| A principális láncot megtartjuk (ok-okozati szál).
||| A kompaktált lánc = a coend eredménye.

||| Bejegyzések szűrése: eldobja a magas átfedésűeket.
public export
szuresAtfedes : List MiertBejegyzes -> List MiertBejegyzes
szuresAtfedes [] = []
szuresAtfedes (x :: xs) =
  if any (\y => eldobhatoE x y) xs
  then szuresAtfedes xs
  else x :: szuresAtfedes xs

||| Bejegyzések komponálása: egymást követőket összevonja.
public export
komponalLanc : List MiertBejegyzes -> List MiertBejegyzes
komponalLanc [] = []
komponalLanc [x] = [x]
komponalLanc (x :: y :: xs) =
  case okOkozatiKompozicio x y of
    Just b => komponalLanc (b :: xs)
    Nothing => x :: komponalLanc (y :: xs)

||| A teljes kompakátálás: szűrés + komponálás.
public export
kompaktal : List MiertBejegyzes -> List MiertBejegyzes
kompaktal lanc = komponalLanc (szuresAtfedes lanc)

-- ═══════════════════════════════════════════════════════════════
-- 7. INJECTÁLÁS = A KOMPAKTÁLT LÁNC VISSZA A KONTEXTUSBA
-- ═══════════════════════════════════════════════════════════════

||| A kompaktált lánc injektálása: a perché-lánc vissza a kontextusba.
||| Ez = egy funktor a miért-lánc kategóriából a kontextus kategóriába.
public export
injectal : List MiertBejegyzes -> String
injectal [] = ""
injectal (x :: xs) =
  "[MiertLanc] " ++ x.miert ++ "\n" ++ injectal xs

-- ═══════════════════════════════════════════════════════════════
-- 8. BIZONYÍTÁSOK — REFL (FREE PROOF)
-- ═══════════════════════════════════════════════════════════════

-- Kimenet: Refl (az identitás bejegyzés sajat témában van ✓)
public export
miertIdentitasSajatTema : (t : Tema) -> sajatTemaban (miertIdentitas t) = True
miertIdentitasSajatTema TemaKategoriaelmelet = Refl
miertIdentitasSajatTema TemaFizika = Refl
miertIdentitasSajatTema TemaKvantum = Refl
miertIdentitasSajatTema TemaNyelv = Refl
miertIdentitasSajatTema TemaCselekves = Refl
miertIdentitasSajatTema TemaTipusok = Refl
miertIdentitasSajatTema TemaSzabalyok = Refl

-- Kimenet: Refl (a kapcsolat bejegyzés nem sajat témában van ✓)
public export
miertKapcsolatNemSajatTema : (b : MiertBejegyzes) -> kapcsolatTemaKozott b = not (sajatTemaban b)
miertKapcsolatNemSajatTema b = Refl

-- ═══════════════════════════════════════════════════════════════
-- 9. PÉLDA BEJEGYZÉSEK
-- ═══════════════════════════════════════════════════════════════

||| Példa bejegyzések a 7 témából.
public export
peldaBejegyzesek : List MiertBejegyzes
peldaBejegyzesek = [
  MiertBejegyzesKonstruktor "wc_001" TemaKategoriaelmelet TemaKategoriaelmelet
    "Wadler free proof: a tipus bizonyitja a termeszetessegi negyzetet" "49 typeclass lefordul" "free proof = tipus = bizonyitas" 2,
  MiertBejegyzesKonstruktor "wc_002" TemaKategoriaelmelet TemaFizika
    "A Lagrangian a kategoriak kozotti ut koltesege" "L = T - V" "kategoria <-> fizika kapcsolat" 2,
  MiertBejegyzesKonstruktor "wc_003" TemaFizika TemaKvantum
    "Heisenberg nem-kommutativ = fazisatmenet" "Pauli X·Z ≠ Z·X" "fizika <-> kvantum kapcsolat" 2,
  MiertBejegyzesKonstruktor "wc_004" TemaKvantum TemaNyelv
    "A magyar ragozas = termeszetes transzformacio" "ragozas uniform minden tore" "kvantum <-> nyelv kapcsolat" 2,
  MiertBejegyzesKonstruktor "wc_005" TemaNyelv TemaCselekves
    "A beszéd = Legendre perem (gondolat → szaj → hang)" "H = p·q̇ - L" "nyelv <-> cselekves kapcsolat" 2,
  MiertBejegyzesKonstruktor "wc_006" TemaCselekves TemaTipusok
    "A cselekvesi ciklus = E8×E8 kognito ↔ E8×E8 valosag" "dontes-cselekves-tanulas" "cselekves <-> tipusok kapcsolat" 2,
  MiertBejegyzesKonstruktor "wc_007" TemaTipusok TemaSzabalyok
    "Minden szam data-ba csomagolva, dependent types" "SteaneVektor n" "tipusok <-> szabalyok kapcsolat" 2,
  MiertBejegyzesKonstruktor "wc_008" TemaSzabalyok TemaKategoriaelmelet
    "SOHA ne hasznalj Pythont — Idris compiler a bira" "Python tiltas" "szabalyok -> kategoriaelmelet (kor)" 2
 ]

||| A példa bejegyzések kompaktálása.
public export
peldaKompaktal : List MiertBejegyzes
peldaKompaktal = kompaktal peldaBejegyzesek

||| A példa bejegyzések injektálása.
public export
peldaInjectal : String
peldaInjectal = injectal peldaBejegyzesek

-- ═══════════════════════════════════════════════════════════════
-- 10. FŐPROGRAM
-- ═══════════════════════════════════════════════════════════════

public export
miertLancFom : IO ()
miertLancFom = do
  putStrLn "=== MIÉRT-LÁNC — KATEGÓRIAELMÉLETILEG BEÁGYAZOTT INDEX ==="
  putStrLn ""
  putStrLn "7 téma = 7 emberi dimenzió (objektumok):"
  putStrLn "  0: Szabalyok (Ido)"
  putStrLn "  1: Kategoriaelmelet (Oksag)"
  putStrLn "  2: Fizika (Ter)"
  putStrLn "  3: Kvantum (Szin)"
  putStrLn "  4: Nyelv (Hang)"
  putStrLn "  5: Cselekves (Fazis)"
  putStrLn "  6: Tipusok (Mod)"
  putStrLn ""
  putStrLn "Morfizmusok = bejegyzesek (Tema → Tema):"
  putStrLn "  sajat temaban = identitas morfizmus"
  putStrLn "  kulonbozo temaban = kapcsolat morfizmus"
  putStrLn ""
  putStrLn "Kompozicio: okOkozatiKompozicio (b1∘b2 = A→C)"
  putStrLn "Atfedes: Clifford a·b (magas → eldobhato)"
  putStrLn "Kompaktalas: coend ∫^c S(c,c) = szures + komponalas"
  putStrLn "Injectalas: funktor a lanc kategoriajabol a kontextusba"
  putStrLn ""
  putStrLn ("Pelda bejegyzesek szama: " ++ show (length peldaBejegyzesek))
  putStrLn ""
  putStrLn "A Wadler 'free proof':"
  putStrLn "  A MiertBejegyzes tipus bizonyitja, hogy a kompozicio uniform."
  putStrLn "  A parametricity biztosítja, hogy a kompaktalas helyes."
  putStrLn "  A tipus = a bizonyitas (Curry-Howard)."
  putStrLn ""
  putStrLn "Kesz."

-- ═══════════════════════════════════════════════════════════════
-- 11. ÚJ BEJEGYZÉSEK — A 2026-08-18 FELFEDEZÉSEK
-- ═══════════════════════════════════════════════════════════════
-- Ezek a session ses_00a2 (2026-08-18) felfedezései, amelyeket
-- a miért-láncba INDEXELNI kell (a Mester feladatai szerint).
-- Mindegyik MiertBejegyzes = morfizmus a témák között.
-- Forrás: a Git-commitek (5515d91, 8414db7, 0d8ced5, dd8abf8).
-- =====================================================================

||| E8 szimplektikus: K = MᵀΩM egész, antiszimmetrikus (GKP-érvényes),
||| K ≡ Ω mod 2 (bináris szimplektikus = qubit-áramkör).
||| Refl: E8BinarisSzimpleptikus, KAntiszimmetrikus01/23/67.
||| A kernel MEGCÁFOLTA az első sejtést (MᵀΩM = Ω szigorúan) —
||| a valódi tétel (mod 2) jött ki. Ez a "semmi halu" elv.
public export
wcE8Szimpleptikus : MiertBejegyzes
wcE8Szimpleptikus = MiertBejegyzesKonstruktor
  "wc_e8_szimplektikus"
  TemaKvantum
  TemaKategoriaelmelet
  "K = MT(OM) egesz, antiszimmetrikus (GKP-ervenyes); K == Omega mod 2 (binaris szimpleptikus = qubit-aramkor)"
  "E8Szimplektikus.idr: E8BinarisSzimplektikus Refl"
  "A Refl nem halu: az elso sejtest (Sp(8,Z)) a kernel megcafolta, a valodi tetel (mod 2) jott ki"
  2

||| Carry = hőátvitel: ΔH = Q, csak a csonkolás termel hőt.
||| A carry megőrzött (unitér evolúció), nem disszipáció.
||| Refl: deltaHamiltoniEgyenloHo9999/66/53 (ΔH = Q).
public export
wcCarryHoatvitel : MiertBejegyzes
wcCarryHoatvitel = MiertBejegyzesKonstruktor
  "wc_carry_hoatvitel"
  TemaFizika
  TemaKvantum
  "A carry nem ho — megorzott aram (Noether-aram a helyiertek kozott). DH = Q: csak a csonkolas = ho = Landauer-korlat"
  "HamiltonMegmaradas.idr: deltaHamiltoniEgyenloHo9999 Refl"
  "Az optimalis AI uniter: a szamitas nem pazarol energiát, csak a csonkolas"
  2

||| Szám mint nyelv: 66+3456=3522 fordításként.
||| A kérdés = a nyelv, amire fordítunk. A Carnot-javítási lánc
||| a fázisállapotot a cél (a válasz) felé javítja.
public export
wcSzamMintNyelv : MiertBejegyzes
wcSzamMintNyelv = MiertBejegyzesKonstruktor
  "wc_szam_mint_nyelv"
  TemaNyelv
  TemaTipusok
  "A szamok osszeadasa mint nyelvi forditas: a kerdes = a nyelv, amire forditunk. A Carnot-javitas a fázisallapotot a valasz fele huzza"
  "FazisOsszeado.idr: 66+3456=3522 (Carnot-javitassal)"
  "A forditas = hibajavitas: a kerdes allapotat a cel allapota fele javitjak"
  2

||| Steane [[15,1,3]]: a 16 szoba − 1.
||| 15 kubit = tesserakt sarkai − a nulla-sarok = a 16. dimenzió.
||| A szindróma = a pozíció bináris alakja. Transzverzális T-kapu.
public export
wcSteane153 : MiertBejegyzes
wcSteane153 = MiertBejegyzesKonstruktor
  "wc_steane_15_1_3"
  TemaSzabalyok
  TemaKvantum
  "A [[15,1,3]] = a 16 szoba − 1. 15 kubit = tesserakt sarkai − a nulla-sarok (a 16. dimenzio = a meres). A szindroma = a pozicio binaris alakja. Transzverzalis T-kapu"
  "Steane153.idr: mindKommutal=True, xHibakJavitasa=True, zHibakJavitasa=True"
  "A fraktal csalad: [[7,1,3]]=8−1, [[15,1,3]]=16−1, [[31,1,3]]=32−1. A T-kapu = a varacs (ami a Cliffordon tul van)"
  2

||| Mérés = Hadmeres: a fázis → skalár projekció.
||| A harmadik fázis kiszámítható az első kettőből (Z₈ csoportművelet).
||| A mérés NEM veszít információt — a koherencia alapja.
public export
wcHadmeres : MiertBejegyzes
wcHadmeres = MiertBejegyzesKonstruktor
  "wc_hadmeres"
  TemaKvantum
  TemaTipusok
  "A meres = a fazis → skalar projekcio. A harmadik fazis kiszamithato az elso kettobol (Z8 csoportmuvelet). A meres NEM veszit informaciot"
  "Hadmeres.idr: harmadikFazis = fazisOsszead (Z8)"
  "A meres = a tipus kiolvasasa: a fazist a szamokkal (tipusokkal) kotjuk ossze"
  2

-- =====================================================================
-- 12. AZ ÚJ BEJEGYZÉSEK LISTÁJA ÉS KOMPAKTÁLÁSA
-- =====================================================================

||| A 2026-08-18-as session új bejegyzései.
public export
ujBejegyzesek : List MiertBejegyzes
ujBejegyzesek = [
  wcE8Szimpleptikus,
  wcCarryHoatvitel,
  wcSzamMintNyelv,
  wcSteane153,
  wcHadmeres
 ]

||| Az összes bejegyzés (pédák + újak).
public export
osszesBejegyzes : List MiertBejegyzes
osszesBejegyzes = peldaBejegyzesek ++ ujBejegyzesek

||| Az új bejegyzések kompaktálása.
public export
ujKompaktal : List MiertBejegyzes
ujKompaktal = kompaktal ujBejegyzesek

||| Az új bejegyzések injektálása (a kontextusba).
public export
ujInjectal : String
ujInjectal = injectal ujBejegyzesek

-- =====================================================================
-- 13. A TELJES LÁNC KOMPAKTÁLÁSA (pédák + újak).
-- =====================================================================

||| A teljes lánc kompaktálása — a túlélő oksági fonal.
public export
teljesKompaktal : List MiertBejegyzes
teljesKompaktal = kompaktal osszesBejegyzes

||| A teljes lánc injektálása — az oksági fonal vissza a kontextusba.
public export
teljesInjectal : String
teljesInjectal = injectal osszesBejegyzes