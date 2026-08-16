module Teszt

-- ═══════════════════════════════════════════════════════════════
-- TESZT — Két szint: fordítás (Refl) + tiszta Show-értékek
-- ═══════════════════════════════════════════════════════════════
-- 1. szint: FORDÍTÁSI BIZONYÍTÁS (Refl) — csak definicionálisan
--    redukálható egyenlőségekre (konstruktorok, literálok).
--    A típus-ellenőrző a bíró: ha fordul, bizonyítva.
--
-- 2. szint: TISZTA SHOW-ÉRTÉKEK — minden más eredménye
--    String (Show-ból). A logika tiszta, a main csak show-t hív.
--
-- Hiányzó Show/Eq instance-ok itt vannak definiálva (ADD,
-- nem módosítjuk a forrás modulokat).
-- ═══════════════════════════════════════════════════════════════

import Steane713
import E8E8Algebra
import MagyarNyelvtan
import LawvereGodel
import Szotar
import Fonetika

%default total

-- ═══════════════════════════════════════════════════════════════
-- 0. HIÁNYZÓ INSTANCE-OK (Show, Eq) — ADD a forráshoz
-- ═══════════════════════════════════════════════════════════════

-- Show E8Pont (a Kodol-ban van, de nem exportáltuk ide — itt definiáljuk)
showK : Kubit -> String
showK Nulla = "0"
showK Egy = "1"

public export
Show E8Pont where
  show p = showK p.x1 ++ showK p.x2 ++ showK p.x3 ++ showK p.x4
        ++ showK p.x5 ++ showK p.x6 ++ showK p.x7 ++ showK p.x8

public export
Show Esetrag where
  show NominativusE     = "nominativus"
  show AccusativusE     = "accusativus"
  show DativusE         = "dativus"
  show InessivusE       = "inessivus"
  show ElativusE        = "elativus"
  show IllativusE       = "illativus"
  show SuperessivusE    = "superessivus"
  show AdessivusE       = "adessivus"
  show DelativusE       = "delativus"
  show AblativusE       = "ablativus"
  show SublativusE      = "sublativus"
  show AllativusE       = "allativus"
  show TerminativusE    = "terminativus"
  show InstrumentalisE  = "instrumentalis"
  show CausalisFinalisE = "causalis-finalis"
  show TranszlativusE   = "transzlativus"
  show FormativusE      = "formativus"
  show EssivusFormalisE = "essivus-formalis"

public export
Show CliffordElem where
  show c = "Clifford(" ++ showK c.skalar ++ "," ++ showK c.vektor ++ "," ++ showK c.bivektor ++ ")"

public export
Eq HaromErtek where
  Igaz == Igaz = True
  Hamis == Hamis = True
  Ertektelen == Ertektelen = True
  _ == _ = False

public export
Show HetesKod where
  show (HetesKonstruktor a b c d e f g) =
    showK a ++ showK b ++ showK c ++ showK d ++ showK e ++ showK f ++ showK g

-- ═══════════════════════════════════════════════════════════════
-- 1. SZINT: FORDÍTÁSI BIZONYÍTÁSOK (Refl)
--    CSAK definicionálisan redukálhatóakra!
-- ═══════════════════════════════════════════════════════════════

-- Kimenet: Refl (Nulla ⊕ Nulla = Nulla — XOR alaptörvény)
public export
bizKubitXorNulla : kubitXor Nulla Nulla = Nulla
bizKubitXorNulla = Refl

-- Kimenet: Refl (Egy ⊕ Egy = Nulla — x ⊕ x = 0)
public export
bizKubitXorEgy : kubitXor Egy Egy = Nulla
bizKubitXorEgy = Refl

-- Kimenet: Refl (Nulla ⊕ Egy = Egy — a nulla egység)
public export
bizKubitXorEgyseg : kubitXor Nulla Egy = Egy
bizKubitXorEgyseg = Refl

-- Kimenet: Refl (Egy ⊕ Nulla = Egy)
public export
bizKubitXorKommutativ : kubitXor Egy Nulla = Egy
bizKubitXorKommutativ = Refl

-- Kimenet: Refl (kubitEgyezik Nulla Nulla = True)
public export
bizKubitEgyezikNulla : kubitEgyezik Nulla Nulla = True
bizKubitEgyezikNulla = Refl

-- Kimenet: Refl (kubitEgyezik Egy Nulla = False)
public export
bizKubitNemEgyezik : kubitEgyezik Egy Nulla = False
bizKubitNemEgyezik = Refl

-- Kimenet: Refl (kubitEs Egy Egy = Egy — AND)
public export
bizKubitEsEgy : kubitEs Egy Egy = Egy
bizKubitEsEgy = Refl

-- Kimenet: Refl (kubitEs Nulla Egy = Nulla)
public export
bizKubitEsNulla : kubitEs Nulla Egy = Nulla
bizKubitEsNulla = Refl

-- Kimenet: Refl (Clifford(0,0,0) ⊗ Clifford(0,0,0) = Clifford(0,0,0))
public export
bizCliffordNulla :
  cliffordSzorzat (CliffordKonstruktor Nulla Nulla Nulla)
                  (CliffordKonstruktor Nulla Nulla Nulla)
  = CliffordKonstruktor Nulla Nulla Nulla
bizCliffordNulla = Refl

-- Kimenet: Refl (Clifford(1,0,0) ⊗ Clifford(0,0,0) = Clifford(1,0,0))
public export
bizCliffordEgyseg :
  cliffordSzorzat (CliffordKonstruktor Egy Nulla Nulla)
                  (CliffordKonstruktor Nulla Nulla Nulla)
  = CliffordKonstruktor Egy Nulla Nulla
bizCliffordEgyseg = Refl

-- Kimenet: Refl (a hazug p = 1/2: (1·2+1·2)·1 = 1·(2·2), azaz 4 = 4)
public export
bizHazugFele : (1 * 2 + 1 * 2) * 1 = 1 * (2 * 2)
bizHazugFele = Refl

-- Kimenet: Refl (a Kleene-tagadás Ertektelen-t önmagára képezi)
public export
bizKleeneFixpont : kleeneTagadas Ertektelen = Ertektelen
bizKleeneFixpont = Refl

-- Kimenet: Refl (alapKod Nulla → steaneDekodol = Nulla — Noether)
public export
bizNoetherNulla : steaneDekodol (alapKod Nulla) = Nulla
bizNoetherNulla = Refl

-- Kimenet: Refl (alapKod Egy → steaneDekodol = Egy — Noether)
public export
bizNoetherEgy : steaneDekodol (alapKod Egy) = Egy
bizNoetherEgy = Refl

-- ─── A bizonyítások listája (dokumentáció) ─────────────────

public export
bizonyitasLista : List String
bizonyitasLista =
  [ "bizKubitXorNulla       : Nulla⊕Nulla=Nulla [Refl]"
  , "bizKubitXorEgy         : Egy⊕Egy=Nulla [Refl]"
  , "bizKubitXorEgyseg      : Nulla⊕Egy=Egy [Refl]"
  , "bizKubitXorKommutativ  : Egy⊕Nulla=Egy [Refl]"
  , "bizKubitEgyezikNulla   : Nulla≈Nulla=True [Refl]"
  , "bizKubitNemEgyezik     : Egy≈Nulla=False [Refl]"
  , "bizKubitEsEgy          : Egy∧Egy=Egy [Refl]"
  , "bizKubitEsNulla        : Nulla∧Egy=Nulla [Refl]"
  , "bizCliffordNulla       : 0⊗0=0 [Refl]"
  , "bizCliffordEgyseg      : 1⊗0=1 [Refl]"
  , "bizHazugFele           : p=1/2: 4·1=1·4 [Refl]"
  , "bizKleeneFixpont       : kleene(Ertektelen)=Ertektelen [Refl]"
  , "bizNoetherNulla        : dekodol(kodol(Nulla))=Nulla [Refl]"
  , "bizNoetherEgy          : dekodol(kodol(Egy))=Egy [Refl]"
  ]

public export
bizonyitasokSzama : Nat
bizonyitasokSzama = length bizonyitasLista

-- ═══════════════════════════════════════════════════════════════
-- 2. SZINT: TISZTA SHOW-ÉRTÉKEK (halu teszt)
-- ═══════════════════════════════════════════════════════════════

public export
record TesztEredmeny where
  constructor TesztEredmenyK
  tesztNev : String
  kapott   : String
  sikeres  : Bool

public export
Show TesztEredmeny where
  show t = (if sikeres t then "✓" else "✗")
        ++ " " ++ tesztNev t
        ++ " → " ++ kapott t

-- Segédfüggvény: Bool-teszt
public export
teszt : String -> Bool -> TesztEredmeny
teszt nev siker = TesztEredmenyK nev (if siker then "OK" else "HIBA") siker

-- ─── E8 algebra tesztek (Show-val) ─────────────────────────

public export
e8Tesztek : List TesztEredmeny
e8Tesztek =
  [ teszt "e8Nulla⊕e8Nulla=e8Nulla" (e8Osszead e8Nulla e8Nulla == e8Nulla)
  , teszt "e8Egy⊕e8Egy=e8Nulla (XOR)" (e8Osszead e8Egy e8Egy == e8Nulla)
  , teszt "e8Nulla⊕e8Egy=e8Egy" (e8Osszead e8Nulla e8Egy == e8Egy)
  , teszt "e8Egy⊕e8Nulla=e8Egy" (e8Osszead e8Egy e8Nulla == e8Egy)
  , teszt "e8Ketto⊕e8Ketto=e8Nulla" (e8Osszead e8Ketto e8Ketto == e8Nulla)
  ]

-- ─── Hamming távolság tesztek ──────────────────────────────

public export
hammingTesztek : List TesztEredmeny
hammingTesztek =
  [ teszt "hamming(e8Nulla,e8Nulla)=0" (hammingTavolsag e8Nulla e8Nulla == 0)
  , teszt "hamming(e8Nulla,e8Egy)=1" (hammingTavolsag e8Nulla e8Egy == 1)
  , teszt "hamming(e8Egy,e8Ketto)=2" (hammingTavolsag e8Egy e8Ketto == 2)
  , teszt "hamming(e8Nulla,e8Nyolc)=1" (hammingTavolsag e8Nulla e8Nyolc == 1)
  ]

-- ─── Esetrag-felismerő tesztek ─────────────────────────────

public export
ragTesztek : List TesztEredmeny
ragTesztek =
  [ teszt "házban→inessivus"
      (ragFelismer "házban" == Just ("ház", InessivusE))
  , teszt "kézzel→instrumentalist"
      (ragFelismer "kézzel" == Just ("kéz", InstrumentalisE))
  , teszt "kérésért→causalis"
      (ragFelismer "kérésért" == Just ("kérés", CausalisFinalisE))
  , teszt "kategória→nominativus"
      (ragFelismer "kategória" == Just ("kategória", NominativusE))
  , teszt "funktorral→instrumentalist"
      (ragFelismer "funktorral" == Just ("funktor", InstrumentalisE))
  , teszt "objektum→nominativus"
      (ragFelismer "objektum" == Just ("objektum", NominativusE))
  ]

-- ─── Kérdőszó tesztek ──────────────────────────────────────

public export
kerdoszoTesztek : List TesztEredmeny
kerdoszoTesztek =
  [ teszt "miért→causalis" (kerdoszoEset "miért" == Just CausalisFinalisE)
  , teszt "hol→inessivus" (kerdoszoEset "hol" == Just InessivusE)
  , teszt "mivel→instrumentalist" (kerdoszoEset "mivel" == Just InstrumentalisE)
  , teszt "hogyan→formativus" (kerdoszoEset "hogyan" == Just FormativusE)
  , teszt "hová→illativus" (kerdoszoEset "hová" == Just IllativusE)
  , teszt "honnan→elativus" (kerdoszoEset "honnan" == Just ElativusE)
  ]

-- ─── Szótár-gráf tesztek ───────────────────────────────────

public export
grafTesztek : List TesztEredmeny
grafTesztek =
  [ teszt "fogalmak>50" (length (fogalmak projektGraf) > 50)
  , teszt "élek>60" (length (elek projektGraf) > 60)
  , teszt "\"kategória\"∈gráf"
      (case fogalomKeres "kategória" projektGraf of
         Just _ => True
         Nothing => False)
  , teszt "\"entrópia\"∈gráf"
      (case fogalomKeres "entrópia" projektGraf of
         Just _ => True
         Nothing => False)
  , teszt "\"Carnot-ciklus\"∈gráf"
      (case fogalomKeres "Carnot-ciklus" projektGraf of
         Just _ => True
         Nothing => False)
  , teszt "\"Idris\"∈gráf"
      (case fogalomKeres "Idris" projektGraf of
         Just _ => True
         Nothing => False)
  , teszt "fok(kategória)>0" (fokSzam "kategória" projektGraf > 0)
  , teszt "fok(entrópia)>0" (fokSzam "entrópia" projektGraf > 0)
  ]

-- ─── MDL-távolság tesztek ──────────────────────────────────

public export
mdlTesztek : List TesztEredmeny
mdlTesztek =
  [ TesztEredmenyK "MDL(kategória,entrópia)"
      (case utHossz 6 "kategória" "entrópia" projektGraf of
         Just d => show d ++ " él"
         Nothing => "nincs út")
      (case utHossz 6 "kategória" "entrópia" projektGraf of
         Just _ => True
         Nothing => False)
  , TesztEredmenyK "MDL(entrópia,információ)"
      (case utHossz 6 "entrópia" "információ" projektGraf of
         Just d => show d ++ " él"
         Nothing => "nincs út")
      (case utHossz 6 "entrópia" "információ" projektGraf of
         Just _ => True
         Nothing => False)
  , TesztEredmenyK "MDL(kategória,E8)"
      (case utHossz 6 "kategória" "E8" projektGraf of
         Just d => show d ++ " él"
         Nothing => "nincs út")
      (case utHossz 6 "kategória" "E8" projektGraf of
         Just _ => True
         Nothing => False)
  , TesztEredmenyK "MDL(Idris,kategória)"
      (case utHossz 6 "Idris" "kategória" projektGraf of
         Just d => show d ++ " él"
         Nothing => "nincs út")
      (case utHossz 6 "Idris" "kategória" projektGraf of
         Just _ => True
         Nothing => False)
  ]

-- ─── Valószínűség tesztek ──────────────────────────────────

public export
valoszinusegTesztek : List TesztEredmeny
valoszinusegTesztek =
  [ teszt "P(causalis)>0" (tipusDarab CausalisK projektGraf > 0)
  , teszt "P(inessivus)>0" (tipusDarab InessivusK projektGraf > 0)
  , teszt "P(instrumentalis)>0" (tipusDarab InstrumentalisK projektGraf > 0)
  , teszt "összes él>70" (osszesEl projektGraf > 70)
  ]

-- ─── Lawvere tesztek ──────────────────────────────────────

public export
lawvereTesztek : List TesztEredmeny
lawvereTesztek =
  [ teszt "Kleene fixpont=Ertektelen" (kleeneTagadas Ertektelen == Ertektelen)
  , teszt "Kleene: Igaz→Hamis" (kleeneTagadas Igaz == Hamis)
  , teszt "Kleene: Hamis→Igaz" (kleeneTagadas Hamis == Igaz)
  ]

-- ─── Fonetika tesztek (magyarHangok: determinisztikus IPA-atiras) ──

public export
fonetikaTesztek : List TesztEredmeny
fonetikaTesztek =
  [ teszt "hangrendszer = 40 (14+17+9, E9 'Hungarian=O')" (hangrendszerSzama == 40)
  , teszt "magánhangzók = 14"  (maganhagzokSzama == 14)
  , teszt "mássalhangzók = 17" (massalhangzokSzama == 17)
  , teszt "digráfok = 9 (oktonion imagináriusok)" (digrafokSzama == 9)
  , teszt "IPA \"kategória\" = [kɒtɛɡoːriɒ] (Wikipedia IPA/HU)"
      (magyarIPA "kategória" == "[kɒtɛɡoːriɒ]")
  , teszt "IPA \"konszonáns\" = [konsonaːnʃ] (sz=EGY fonéma [s]!)"
      (magyarIPA "konszonáns" == "[konsonaːnʃ]")
  , teszt "IPA \"szótár\" = [soːtaːr] (sz=[s], ó=[oː], á=[aː])"
      (magyarIPA "szótár" == "[soːtaːr]")
  , teszt "IPA \"győr\" = [ɟøːr] (gy=[ɟ], ő=[øː])"
      (magyarIPA "győr" == "[ɟøːr]")
  , teszt "IPA \"hangvilla\" = [hɒŋvillɒ] (ng→[ŋ] asszimiláció)"
      (magyarIPA "hangvilla" == "[hɒŋvillɒ]")
  , teszt "IPA \"edzés\" = [ɛd͡zeːʃ] (dz=[d͡z], s=[ʃ])"
      (magyarIPA "edzés" == "[ɛd͡zeːʃ]")
  , teszt "IPA \"kutya\" = [kucɒ] (ty=[c])"
      (magyarIPA "kutya" == "[kucɒ]")
  , teszt "IPA \"lyuk\" = [juk] (ly=[j]!)"
      (magyarIPA "lyuk" == "[juk]")
  , teszt "IPA \"dzsessz\" = [d͡ʒɛss] (ssz = hosszú sz = [ss])"
      (magyarIPA "dzsessz" == "[d͡ʒɛss]")
  , teszt "táv(szó,zó)=1 (s≠z, ó egyezik)"
      (fonetikaiTavolsag (magyarHangok "szó") (magyarHangok "zó") == 1)
  , teszt "táv(x,x)=0"
      (fonetikaiTavolsag (magyarHangok "kategória") (magyarHangok "kategória") == 0)
  , teszt "ékezetfüggetlen: KATEGÓRIA ≡ kategória"
      (magyarIPA "KATEGÓRIA" == magyarIPA "kategória")
  -- ── szótagolás (determinisztikus; minden magánhangzó = egy szótag) ──
  , teszt "szótag: kategória = ka·te·gó·ri·a (5, hiátussal: ri·a)"
      (grafForma "kategória" == "ka·te·gó·ri·a" && szotagSzam "kategória" == 5)
  , teszt "szótag: kutya = ku·tya (2)"
      (grafForma "kutya" == "ku·tya" && szotagSzam "kutya" == 2)
  , teszt "szótag: anya = a·nya (1 mássalhangzó → támadás)"
      (grafForma "anya" == "a·nya")
  , teszt "szótag: asztal = asz·tal (2 mássalhangzó → kóda+támadás)"
      (grafForma "asztal" == "asz·tal")
  , teszt "szótag: bandita = ban·di·ta (3)"
      (grafForma "bandita" == "ban·di·ta")
  , teszt "szótag: papír = pa·pír + szóvégi kóda [r]"
      (grafForma "papír" == "pa·pír")
  , teszt "szótag: mennyezet = meny·nye·zet (AkH. 226.f: teljes rövid mindkét oldalon!)"
      (grafForma "mennyezet" == "meny·nye·zet" && szotagSzam "mennyezet" == 3)
  , teszt "szótag: egészség = e·gész·ség (é-sz-s-é: az sz EGÉSZ digráf!)"
      (grafForma "egészség" == "e·gész·ség" && szotagSzam "egészség" == 3)
  , teszt "hangsúly MINDIG az első szótagon (determinisztikus)"
      (hangsulyPozicio == 0)
  ]

-- ═══════════════════════════════════════════════════════════════
-- ÖSSZEFOGLALÓ
-- ═══════════════════════════════════════════════════════════════

public export
osszesTeszt : List TesztEredmeny
osszesTeszt =
  e8Tesztek ++ hammingTesztek ++ ragTesztek ++ kerdoszoTesztek
  ++ grafTesztek ++ mdlTesztek ++ valoszinusegTesztek ++ lawvereTesztek
  ++ fonetikaTesztek

public export
sikeres : List TesztEredmeny
sikeres = filter (\t => sikeres t) osszesTeszt

public export
sikertelen : List TesztEredmeny
sikertelen = filter (\t => not (sikeres t)) osszesTeszt

public export
record TesztOsszefoglalo where
  constructor TesztOsszefoglaloK
  bizonyitasokDb  : Nat    -- 1. szint: Refl
  tesztekDb       : Nat    -- 2. szint: Show
  sikeresDb       : Nat
  sikertelenList  : List TesztEredmeny

public export
Show TesztOsszefoglalo where
  show o =
    "═══ TESZT EREDMÉNY ═══\n"
    ++ "1. szint (Refl bizonyítások): " ++ show (bizonyitasokDb o) ++ " [FORDÍTVA = BIZONYÍTVA]\n"
    ++ "2. szint (Show tesztek): " ++ show (sikeresDb o) ++ "/" ++ show (tesztekDb o) ++ " sikeres"
    ++ (if length (sikertelenList o) == 0
          then " — MIND SIKERES ✓"
          else "\nSikertelenek:\n" ++ concatMap (\t => "  " ++ show t ++ "\n") (sikertelenList o))

public export
tesztJelentes : TesztOsszefoglalo
tesztJelentes =
  TesztOsszefoglaloK bizonyitasokSzama (length osszesTeszt)
                    (length sikeres) sikertelen

-- ─── main: vékony IO-burkoló ───────────────────────────────

main : IO ()
main = putStrLn (show tesztJelentes)