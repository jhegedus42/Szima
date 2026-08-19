# SZIMA-TER — TERV (2026-08-19)

> A felhasználó: „a mondat szintű fordítás több, mint 1 byte — komplex byte
> kell, ami E8-ba kódol el egy gondolatot. Mindent nulláról a source-ban
> újra kell értelmezni, kódolni. Az eddigi dolgokat nem felülírni, teljesen
> új könyvtárstruktúra kell."

---

## 1. Mi készült el eddig (2026-08-19)

| Fájl | Tartalom | Státusz |
|------|----------|---------|
| `modul/KomplexByte.idr` | A komplex bájt típusa: 8 komplex komponens (E8 ℂ⁸) + CPT + Steane + címke. Kubit, HetesKod, Komplex, CptFazis nulláról. Refl-bizonyítások (üres életjel, szorzás-egység, kubit-forgatás). | ✅ `idris2 --check` zöld |
| `modul/Paragrafus.idr` | Paragrafus → mondatok → komplex bájtok. Szótár, szó-vektor keresés (kisbetűsítéssel), mondat-jelentés összegzés. Refl (kisbetűsítés, mondat-szám). | ✅ `idris2 --check` zöld |
| `modul/Main.idr` | Futtatható teszt: paragrafus-kódolás kimenete. | ✅ fut, kimenet fent |
| `OLVASD.md` | A struktúra és a koncepció dokumentációja. | ✅ |

**Tesztkimenet** (a kódolás működik):
- `"Piroska."` → `[1,0,0,1,0,0,0]` = idő + szín (a kezdet, az ártatlan, piros)
- `"Mit mondott a farkas?"` → `[0,1,0,0,1,0,0,1]` = okság + hang + chiralitás
- `"Piroska. A farkas hazugsagot mondott."` → 2 komplex bájt (2 mondat)

---

## 2. A komplex bájt — mit jelent pontosan

```
KomplexBajt = (ℂ⁸) × CptFazis × HetesKod × String
  8 komplex komponens:  ido, oksag, ter, szin, hang, fazis, mod, chiralitas
  CptFazis:             3×3×3 = 27 (igeidő / szemlélet / forrás)
  HetesKod:             Steane [[7,1,3]] = 7 bit (hibajavítás)
  String:               a gondolat szövege (címke, veszteségmentes)
```

A `re` rész = mérés (CODATA), az `im` rész = fázis (kapcsolat-dinamika).
Ez illeszkedik a Komplex.idr-hagyományhoz és az E8-hez (ℂ⁸ = E8 komplexifikáció).

**Miért ez a választás?**
- A mondat ≠ 1 byte (42 bit volt), a gondolat ≠ 1 mondat.
- A paragrafus = List KomplexBajt (tetszőleges hosszú gondolat).
- A komplex érték a fázist tartja (a fázis szabja meg az információ-átvitel
  irányát és redundanciáját — AGENTS.md 5. szabály).
- A Steane a paritást és a hibajavítást őrzi a komplex komponensekből.

---

## 3. A soron következő lépések

### 3.1 A gondolat-kódolás finomítása (baby AI kiterjesztése)
- **Tő- és toldalék szétválasztás**: a magyar ragozás kezelése. A
  `"hazugsagot"` (ragozott) most nem találja a `"hazugsag"`-ot. A megoldás:
  a mondat-jelentés a SZAVAK HANGJÁBÓL is számolódjon (parciális tő-megfelelés),
  vagy a szótár tárolja a töveket is.
- **A CPT fázis a szavakból**: az igeidő/szemlélet/forrás a mondat
  ragozásából, nem mindig „jelen/folyamatos/közvetlen".
- **Steane javítás**: a komplex bájt `HetesKod`-jából a szindróma-javítás
  bekötése (a `Steane713.javitas` mintájára).

### 3.2 A források újraértelmezése (source/ → forras/)
- Minden PDF/EPUB → paragrafusok → JSON a `forras/`-ban.
- A JSON egy Idris-modulból generálódik (nincs Python — AGENTS.md 3.).
- A DJVU kimarad (nincs konverziós eszköz), amíg nincs `djvutxt`.

### 3.3 A tudás-index (forras/ → kod/)
- Minden paragrafus → List KomplexBajt a `Peldaszotar` kibővített változatával.
- A `kod/` JSON-tároló: paragrafus címke + komplex bájtok + forrás-hivatkozás.

### 3.4 A baby AI (KisAI) bekötése
- A `Dirac3D/KisAI.idr` mintájára: a szótár + a komplex bájtok + egy
  `keres` függvény, ami a legközelebbi gondolatot adja vissza
  (komplex távolság, nem Hamming — az E8 belső szorzat).
- A Paragrafus modul jelenlegi kódolása ehhez az alap.

---

## 4. A struktúra szabályai

- **Csak hozzáadás.** Semmi felülírás, semmi törlés. Az új Idris modulok
  az `osveny_index/`-et NEM importálják — függetlenek.
- **Minden magyar.** Azonosítók, kommentek, üzenetek magyar, rövidítés nélkül
  (kivéve az E8 és a Kubit standard terminusokat).
- **Minden Idris.** Nincs Python a feldolgozásban. A JSON-t Idris generálja.
- **Fordítás-ellenőrzés**: minden modul `idris2 --check`-kel zöld.
- **Refl, ahol a típus redukálódik; Show-teszt, ahol nem** (pl. a szótári
  keresés `==`-e nem redukálódik Refl-lel — futásidejű ellenőrzés).
- **Könyveket csak alügynökök olvasnak** (AGENTS.md 11.).

---

## 5. Megnyitott kérdések (a felhasználónak)

1. A komplex bájt 8 komponense: jó-e a jelenlegi 7+chiralitás felosztás,
   vagy a 8 komponens más legyen?
2. A paragrafus → List KomplexBajt: a sorrend számít-e (a listában) a
   jelentéshez? (Jelenleg a sorrend = a mondatok sorrendje.)
3. A szótár forrása: a `forras/` feldolgozásból épüljön-e fel automatikusan,
   vagy kézzel (a Peldaszotar mintájára)?
4. A JSON-generátor: egy külön Idris-modul legyen-e (`modul/JsonKodolo.idr`),
   ami a `kod/`-t generálja?