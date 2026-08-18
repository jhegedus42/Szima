module Attekintes

-- ═══════════════════════════════════════════════════════════════
-- HTML-ÁTTEKINTÉST GENERÁLÓ MODUL — az Idris a forrása a webnek
-- ═══════════════════════════════════════════════════════════════
-- Szabály: minden generálás Idrisből jön — a HTML is.
-- A SABLON (CSS-struktúra) itt van; az ADATOK (modullista,
-- tesztszámok) a Teszt.idr-ből importálva.
-- Kimenet:
--   idris2 --exec htmlKiiras Attekintes.idr > docs/attekintes.html
-- ═══════════════════════════════════════════════════════════════

import Teszt

%default total

-- ─── 1. A MODULOK LISTÁJA (adattípus, nem String) ───────

public export
record ModulAdat where
  constructor ModulAdatKonstruktor
  modulNev       : String
  mitBizonyit    : String
  miertKell      : String
  allapotJel     : String

public export
modulok : List ModulAdat
modulok =
  [ ModulAdatKonstruktor "Fonetika.idr"
      "40 hang, IPA, szótagolás (AkH.226.f), ng→[ŋ]"
      "a szókincs TÍPUS — a szavak nem String, hanem Hang-konstruktorok"
      "65 teszt"
  , ModulAdatKonstruktor "FanoParitás.idr"
      "hangrend = paritásbit; Fanó-sík 7 egyenes XOR=0 [Refl]; Pauli [Refl]"
      "a nyelv önellenőrző — a rossz toldalékot a típus elutasítja"
      "12 teszt + 9 Refl"
  , ModulAdatKonstruktor "Kerdoszo.idr"
      "kérdőszó→esetrag típusos; „mikor?\"-ra nincs rag [Refl] (T≠C,P)"
      "a kíváncsiság TÍPUS: kérdés = morfizmus üres célal; Yoneda"
      "13 teszt + 7 Refl"
  , ModulAdatKonstruktor "HanMagKodolas.idr"
      "5 bit kínai + 3 bit magyar = 8 bit = E8Pont; 137=11²+4² [Refl]"
      "egy gondolat = egy bájt a Steane-rácsban, paritás-önellenőrző"
      "7 teszt + 5 Refl"
  , ModulAdatKonstruktor "E8Gyokrendszer.idr"
      "2→4→8→24→240 torony; 112+128=240 (két út) [Refl]; 128=2⁷"
      "a szó mérete = oktonion egységek = E8 gyökök"
      "12 teszt + 16 Refl"
  , ModulAdatKonstruktor "DiracGammaMatricak.idr"
      "Weyl γ⁰ keveri ψ_L↔ψ_R; szerveri sosem; γ⁵=diag [Refl]"
      "a kétnyelvű gondolkodás mechanizmusa: γ⁰ (idő/magyar) forgat"
      "6 teszt + 11 Refl"
  , ModulAdatKonstruktor "OktonionAlgebra.idr"
      "49 pár × 3 törvény EGY Refl-lel; Fano-sík [Refl]; nem-asszoc. [Refl]"
      "a mondat = nem assz. szorzat (a csoportosítás változtatja a jelentést)"
      "8 teszt + 3 Refl"
  , ModulAdatKonstruktor "SteaneHamiltonian.idr"
      "H=−6 alapállapot [Refl]; szindróma=hibapozíció binárisan [Refl]"
      "a hibajavítás = Carnot-ciklus (mérés→javítás→törlés→újrakészítés)"
      "9 teszt + 9 Refl"
  , ModulAdatKonstruktor "LejeuneTranszformacio.idr"
      "ℒ-család (Landauer ℒ_I); 2. főtétel: csak a törlési ütem fizet [Refl]"
      "Legendre általánosítása; a Carnot = kör a ℒ-gráfban"
      "5 teszt + 4 Refl"
  , ModulAdatKonstruktor "DiracIdoFejlodes.idr"
      "P(magyar)=sin²(t) két úton ≤10⁻¹²; szerveri γ⁰-val P=0 pontosan"
      "a jelentés oszcillál (Zitterbewegung); Idris számol, böngésző rajzol"
      "5 teszt"
  , ModulAdatKonstruktor "ErtelmezoSzotar.idr"
      "8 ÉKSZ-szócikk; GAUGE: kézzel írt == független parser [teszt]"
      "a szócikkek genus-differentia szerkezete = a fogalom-gráf"
      "14 teszt"
  , ModulAdatKonstruktor "LawvereGodel.idr"
      "Lawvere fixpont [Refl]; hazug p=1/2 [Refl]; Kleene 3-értékű"
      "az öntudat csírája: a rendszer kérdezhet önmagáról"
      "Refl"
  , ModulAdatKonstruktor "Komplex.idr"
      "φ-kontrakció 10⁻¹⁰; ϱ fixpont; oda-vissza (Loschmidt)"
      "a Y-kombinátor numerikus magja: a kontrakció = kérdés→információ"
      "Show"
  , ModulAdatKonstruktor "KorOsztas.idr"
      "Gauss-Wantzel; komma=23,46 cent; bájt=8 (256)"
      "a konszonancia-prímek = Fermat-prímek"
      "Refl"
  ]

-- ─── 2. HTML-SABLON ──────────────────────────────────────

public export
cssSablon : String
cssSablon = """
:root { --festek:#1a1a2e; --papir:#fafaf7; --kiemel:#2563eb; --siker:#059669; --arany:#b45309; --keret:#d8d4cc; --hatter:#f0eee9; }
* { box-sizing:border-box; }
body { font-family:Georgia,serif; background:var(--hatter); color:var(--festek); max-width:1000px; margin:0 auto; padding:2rem 1rem 4rem; line-height:1.65; }
header { border-bottom:3px double var(--festek); padding-bottom:1.2rem; margin-bottom:2rem; }
h1 { font-size:1.8rem; margin:0 0 .3rem; }
h2 { font-size:1.3rem; border-bottom:1px solid var(--keret); padding-bottom:.3rem; margin-top:2.4rem; }
table { border-collapse:collapse; width:100%; margin:1rem 0; font-size:.9rem; }
th,td { border:1px solid var(--keret); padding:.45rem .6rem; text-align:left; vertical-align:top; }
th { background:var(--papir); font-family:Menlo,monospace; font-size:.82rem; }
.pipa { color:var(--siker); font-weight:bold; }
.doboz { background:var(--papir); border:1px solid var(--keret); border-radius:6px; padding:1rem 1.2rem; margin:1rem 0; }
pre { background:var(--festek); color:#e5e7eb; padding:1rem 1.2rem; border-radius:6px; overflow-x:auto; font-size:.84rem; }
a { color:var(--kiemel); text-decoration:none; }
a:hover { text-decoration:underline; }
.kicsi { font-size:.85rem; color:#6b7280; }
.mod { font-family:Menlo,monospace; font-size:.85rem; color:var(--kiemel); }
footer { margin-top:3rem; border-top:3px double var(--festek); padding-top:1rem; font-size:.88rem; color:#555; }
nav { background:var(--papir); border:1px solid var(--keret); border-radius:6px; padding:1rem 1.4rem; margin-bottom:2rem; }
nav a { margin-right:1.2rem; }
"""

public export
modulSor : ModulAdat -> String
modulSor m =
  "<tr><td class=\"mod\">" ++ modulNev m ++ "</td>"
  ++ "<td>" ++ mitBizonyit m ++ "</td>"
  ++ "<td>" ++ miertKell m ++ "</td>"
  ++ "<td class=\"pipa\">" ++ allapotJel m ++ "</td></tr>"

public export
modulTablazat : String
modulTablazat =
  "<table>\n<tr><th>Modul</th><th>Mit bizonyít</th><th>Miért kell az AI-hez</th><th>Állapot</th></tr>\n"
  ++ concatMap (\m => modulSor m ++ "\n") modulok
  ++ "</table>"

-- ─── 3. A TESZTSZÁMOK A Teszt.idr-BŐL ────────────────────

public export
tesztSzamok : String
tesztSzamok =
  show (sikeresDb tesztJelentes) ++ "/" ++ show (tesztekDb tesztJelentes)
  ++ " teszt + " ++ show (bizonyitasokDb tesztJelentes) ++ " Refl"

-- ─── 4. A TELJES HTML ───────────────────────────────────

public export
htmlKimenet : String
htmlKimenet =
  "<!DOCTYPE html>\n<html lang=\"hu\">\n<head>\n<meta charset=\"UTF-8\">"
  ++ "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
  ++ "<title>Szima — Projekt-áttekintés (Idris-generált)</title>\n"
  ++ "<style>\n" ++ cssSablon ++ "\n</style>\n</head>\n<body>\n\n"
  ++ "<header>\n  <h1>Szima — Projekt-áttekintés</h1>\n"
  ++ "  <p class=\"kicsi\">A kód maga a kutatás. Ez az oldalt az <b>Idris generálta</b>"
  ++ " (<code>idris2 --exec htmlKiiras Attekintes.idr</code>).</p>\n"
  ++ "  <p class=\"kicsi\">Frissítve: 2026-08-18 · <b>" ++ tesztSzamok ++ " ✓</b> ·"
  ++ " <a href=\"https://github.com/jhegedus42/Szima\">github.com/jhegedus42/Szima</a></p>\n"
  ++ "</header>\n\n"
  ++ "<nav>\n  <b>Oldalak:</b>\n"
  ++ "  <a href=\"dashboard.html\">📊 Dashboard</a>\n"
  ++ "  <a href=\"carnot_entropia.html\">📖 Carnot</a>\n"
  ++ "  <a href=\"zitterbewegung.html\">📈 Zitterbewegung</a>\n"
  ++ "  <a href=\"index.html\">🏠 Régi főoldal</a>\n"
  ++ "</nav>\n\n"
  ++ "<h2>1. A megépült elemek (mind Idrisben, gép-ellenőrzött)</h2>\n\n"
  ++ modulTablazat ++ "\n\n"
  ++ "<h2>2. Ami NEM megvan (őszintén)</h2>\n"
  ++ "<div class=\"doboz\">\n"
  ++ "<ul>\n"
  ++ "  <li><b>Nincs egy <code>main</code>, ami gondolkodik.</b>"
  ++ " A LEGO-elemek külön-külön bizonyítottak, de nincsenek összekötve.</li>\n"
  ++ "  <li><b>A hiányzó lépés:</b> egy <code>main</code>, ami kap egy kérdést"
  ++ " (<code>Kerdoszo</code>), kódolja (<code>HanMag→E8Pont</code>),"
  ++ " lefuttatja a Carnot-ciklust, és ad egy választ — Idrisben.</li>\n"
  ++ "  <li><b>α⁻¹ = 137 + 9/250</b>: 6,5σ nyitott ⚡</li>\n"
  ++ "  <li><b>A szerveri Dirac-nyelv</b>: a gammák hibásak (javítva Idrisben, szerveren nem).</li>\n"
  ++ "</ul>\n</div>\n\n"
  ++ "<h2>3. Hogyan futtasd</h2>\n"
  ++ "<pre>git clone https://github.com/jhegedus42/Szima && cd Szima/osveny_index\n"
  ++ "idris2 -c Teszt.idr && idris2 --exec main Teszt.idr"
  ++ "  → " ++ tesztSzamok ++ " ✓\n\n"
  ++ "idris2 --exec htmlKiiras Attekintes.idr > ../docs/attekintes.html"
  ++ "  → ez az oldal\n"
  ++ "idris2 --exec jsonKiiras DiracIdoFejlodes.idr > ../docs/adatok/zitterbewegung.json"
  ++ "  → a grafikon adata\n"
  ++ "./ellenorzes.sh  → a harness ellenőrzi a szabályokat</pre>\n\n"
  ++ "<footer>\nSzima · a kód maga a kutatás ·"
  ++ " <a href=\"https://github.com/jhegedus42/Szima\">github.com/jhegedus42/Szima</a><br>\n"
  ++ "Dedikálva Szimának, a szeretett cicának 🐱\n</footer>\n\n"
  ++ "</body>\n</html>\n"

public export
htmlKiiras : IO ()
htmlKiiras = putStr htmlKimenet

main : IO ()
main = htmlKiiras