# AGENTS.md — Ügynök Szabályok / Agent Rules

`/Users/joco/opencode` — Idris 2 kategorikus algebrai alapozás (kategóriaelmélet, E8×E8 Clifford algebra, Steane [[7,1,3]] kvantumhibajavítás). Git repository, GitHubon: https://github.com/jhegedus42/opencode. `gh` authentikálva (`jhegedus42`).

---

## 0. Kódolási Nyelv / Coding Language

**Minden azonosító, komment, és üzenet MAGYAR.**  
All identifiers, comments, and messages are in HUNGARIAN.

- Idris keywords maradnak angolul (`module`, `public export`, `data`, `Type`, `where`, stb.)
- Minden felhasználói név magyar: típusok, függvények, konstruktorok, változók
- A magyar nyelv esetrendszere a logikai algebra alapja (22 eset → 22 logikai kapcsolat)
- A magyar nyelv három idő dimenziója: igeidő (múlt/jelen/jövő), aspektus (folyamatos/befejezett/szokásos), evidenciálisság (közvetlen/ következtetett/jelentett)
- A magyar agglutináció (tő + szám + birtok + eset) a logikai kompozíció mintája

## 0. Rövidítések Tiltása / No Abbreviations

**Semmilyen rövidítés nem használható sehol.**  
No abbreviations anywhere. Ever.

- `Mk` → `Konstruktor` utótag (pl. `VilagKonstruktor`, `AdatKonstruktor`)
- `CPT` → `ToltesParitasIdo`
- `MCP` → `ModellKornyezetProtokoll`
- `E8` kivétel (standard matematikai jelölés)
- `Kubit` kivétel (standard fizikai terminus)

Ha egy név rövidítésnek tűnik, írd ki teljesen.

---

## 1. Kemény Szabályok / Hard Rules (soha nem sérthető)

1. **Nincs szerver írás engedély nélkül.** Ne hozz létre, szerkessz, vagy törölj fájlt a Hetzner szerveren (88.99.218.155) amíg a felhasználó kifejezetten nem kéri. Olvasás rendben. Kérdezz először.

2. **Három egyforma hiba → infrastruktúra javítás.** Ha ugyanazt a hibát 3-szor látod, ne próbálkozz tovább — javítsd meg a gyökérokot (add hozzá AGENTS.md-hez, frissítsd az eszközöket, változtass módszert).

3. **Minden logika szigorúan típusozott Idris-ben.** Python csak numerikus számításhoz, web integrációhoz, vagy API hívásokhoz használható. A maglogika (típusok, relációk, kapcsolatok, parsolás) Idris-ben van.

4. **Ne használj String-et a mag típusokban.** Használj algebrai adattípusokat. A megjelenítéshez használj `Render` vagy `Show` típusosztályt.

5. **Három kubit:** saját (önreferencia), másik (külső bemenet), fázis (kapcsolat). A fázis határozza meg az információátvitel irányát és a redundanciát.

6. **[[7,1,3]] Steane kód:** minden fogalom 7 bites vektor. Távolság 3 → 1 hibát javít. A 7 bit: [idő, okság, tér, szín, hang, fázis, mód].

7. **E8 × E8 algebra:** bal E8 = tér, jobb E8 = szín, Cliﬀord szorzat = hang. A geometriai szorzat belső része (a·b) az átfedés → ha magas, a fogalom redundáns és eldobható.

8. **Fázis alapú redundancia:** azonos fázisú fogalmak → redundáns → eldobható. Ez tartja fenn a koherenciát.

9. **CPT szimmetria — három réteg, egy struktúra.** A CPT diszkrét szimmetria három rétegen jelenik meg; a három réteg egymásra épül, de nem ekvivalens.

   **a) Fizikai réteg (Pauli 1955, Lüders 1954):**
   - C (Charge, töltés) = részecske ↔ antirészecske konjugáció
   - P (Parity, paritás) = tér tükrözése (bal ↔ jobb)
   - T (Time, idő) = idő visszafordítása

   **b) Nyelvtani réteg (MagyarOntologia.idr, magyar-lexikon skill):**
   - C = **Forrás** (közvetlen / következtetett / jelentett) — honnan tudom?
   - P = **Szemlélet** (folyamatos / befejezett / szokásos) — hogyan látom?
   - T = **Igeidő** (múlt / jelen / jövő) — mikor?
   - Ez a magyar ige ragozásának három dimenziója: 3×3×3 = 27 kombináció.

   **c) Pszichofizikai réteg (FazisAlgebra.idr, a projekt saját metaforája):**
   - C = **Saját tudat** — ki vagyok én? (önreferencia, Én)
   - P = **Másik fél** — ki vagy te? (külső bemenet, Te)
   - T = **Kapcsolat fázisa** — hogyan kapcsolódunk? (a kettő dinamikája)

   **A kapcsolat a rétegek között:**
   - A nyelvtani réteg **leírja** a világot (Forrás = honnan tudom → Szemlélet = hogyan → Igeidő = mikor).
   - A pszichofizikai réteg **él** a világban (Saját = ki vagyok → Másik = ki vagy te → Kapcsolat = hogyan vagyunk együtt).
   - A fizikai réteg **mérhető** (Charge, Parity, Time = mérhető mennyiségek).
   - **Fontos:** a három réteg NEM ekvivalens. A "Forrás" (C) ≠ "Saját tudat" (C). A rétegek közötti leképezés **homomorfizmus** (Conant-Ashby), nem izomorfizmus.
   - A `FazisAlgebra.idr`-ben a `ToltesParitasIdo` rekord tartalmazza a teljes három kubit struktúrát: `toltes` (C), `paritas` (P), `ido` (T). A `fazisFaktorialis` függvény számítja ki a három kubit koherenciáját.

10. **Git snapshot minden 3. promptnál.** Minden harmadik üzenetváltás után: `git add -A && git commit -m "snapshot N: ..."`.

11. **Könyveket csak alügynökök olvasnak.** A fő ügynök soha nem olvas könyveket közvetlenül. Alügynököket kell indítani a `task` eszközzel.

12. **Hierarchikus olvasó architektúra:** 3 szint — L1: párhuzamos előolvasók (ingyenes), L2: összegző és ellenőrző (GAN hármas), L3: indexelő és tömörítő.

---

## 2. Környezet / Environment

- macOS (arm64), shell `zsh`. `~/.zshenv` egy hiányzó `~/.cargo/env`-et hivatkozik — ártalmatlan, ne "javítsd" ki.
- Csomagkezelők: Homebrew (`brew`), npm (Node v25).
- opencode globális konfig: `~/.config/opencode/opencode.jsonc`. Perzisztens szabályok: `~/.config/opencode/AGENTS.md` (még nem létezik).
- opencode adat/auth: `~/.local/share/opencode/` (`mcp-auth.json`). Skill-ek: `~/.agents/skills/`.

## 3. Telepített Eszközök / Installed Tooling

- `gws` (Google Workspace CLI) v0.22.5 — `brew install googleworkspace-cli`.
- `gcloud` (Google Cloud SDK) — `brew install --cask google-cloud-sdk`. **Figyelem:** nincs PATH-on amíg a `path.zsh.inc` be nem töltődik; ha `gcloud` nem található, forrás: `/opt/homebrew/share/google-cloud-sdk/path.zsh.inc`.
- Telepített skill-ek: `bx`, `find-skills`, `firecrawl-research-index`, `research-agent`, `gws-gmail`, `szerver-ismeret`.
- MCP authentikálva: `exa-search`.
- Idris 2: `/opt/homebrew/bin/idris2` (0.8.0 verzió).

### Szerverek — Fontos Figyelmeztetés

**A `chickenloop` SSH alias NEM a Hetzner szerverre mutat.**
- `chickenloop` → SiteGround shared hosting (`gtxm1079.siteground.biz`)
- Hetzner IP (`88.99.218.155`) → Jelenleg nincs működő SSH hozzáférés
- **Minden szerver-elérés előtt:** használd a `szerver-ismeret` skill-et (`skill szerver-ismeret`) — a részletek ott vannak.
- **Soha ne tételezz fel** egy szerver identitását az IP alapján vagy az SSH alias alapján.

## 4. Gmail hozzáférés (gws-gmail skill)

- Szükséges: `gws` bináris (telepítve) + egyszeri Google OAuth bejelentkezés.
- `gws auth setup` interaktív (böngésző) és `gcloud` kell hozzá. `@gmail.com` fióknál az ellenőrizetlen alkalmazás 25-scope korlát vonatkozik, ezért egyedi scope-okkal jelentkezz be: `gws auth login --scopes gmail`.
- **Auth státusz: MÉG NEM KÉSZ.** Mielőtt feltételeznéd, hogy a Gmail működik, ellenőrizd: `gws gmail users getProfile`.
- Használat: `gws gmail +triage`, `gws gmail +read`, `gws gmail +reply --message-id <id> --body "..."`.

---

## 5. Bizalmas Fájlok — NE olvasd, ne írd ki, ne tedd elérhetővé

A ProtonDrive gyökérben (`~/Library/CloudStorage/ProtonDrive-chickenloop42@proton.me-folder/`):
- `1Password*.zip`, `1password-credentials*.json`, `1PasswordExport-*.1pux`
- `AccessKey.csv`, `RAM Access Key AliBaba.txt`, `R12.der`
- `proton-recovery-phrase.pdf`, `ai/dev/secret_1pw.env`
- Bármilyen `.env`, recovery kifejezés, vagy credentials fájl általában.

Ha egy feladat titkot igényel, kérdezd meg a felhasználót — ne kutakodj ezekben a fájlokban.

---

## 6. Felhasználó AI Kutatása (kontextus; ne szerkeszd)

- Aktív munka: `…/ai/dev/` (Obsidian vault, opencode forrás) és egy nagy kutatási dump `…/ai/` alatt: komplex értékű / temporális transzformerek (GPT-2 alapú), neurális hálózatok × QFT, és kapcsolódó arXiv preprint-ek.
- Több AI szolgáltatónál dolgozik (DeepSeek, Kimi, Gemini, Claude, Z.ai/GLM).

---

## 7. Git Használat / Git Usage

- `git init` megtörtént a `/Users/joco/opencode/` könyvtárban
- Snapshot minden 3. prompt után: `git add -A && git commit -m "snapshot N: rövid leírás"`
- `.gitignore`: `session-*.md`, `trail_index/build/`
