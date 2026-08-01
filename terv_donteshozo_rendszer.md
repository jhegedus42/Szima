# Tervezési Napló — Idris Döntéshozó Rendszer (Magyarul Beszélő, Információt Megőrző)

**Dátum:** 2026-08-01
**Fázis:** Tervezés (nincs kód, csak napló + terv)
**Kiindulás:** `MagyarOntologia.idr` cb3875b commit (22 eset = 22 morfizmus, RagT typeclass, CPT szimmetria)
**Tervező skill-ek:** `idris-stilus`, `legkisebb-muvelet`, `kompaktalas`, `magyar-lexikon`

---

## 0. A Feladat Értelmezése

A felhasználó kérése (2026-08-01): építsünk egy **Idris döntéshozó rendszert**, amely magyFrom:

- **Magyarul beszél** velem (a felhasználóval)
- **Kérdéseket tesz fel** — nemcsak válaszol
- **Eldönti mit érdemes csinálni és miért** — indokolja a miértet
- **Tervezési algoritmus**: optimalizáció + valószínűség-becslés
- **Kvantum Hamilton Monte Carlo vagy DFT elképzelés** — NEM sima Monte Carlo
- **Sima Monte Carlo tilalom oka**: információt veszít (sampling + reject) — ez "baromság, ha az ember információval dolgozik és a legtöbbet akarja belőle értelmes formába önteni"

A kritikus elv: **a struktúra tükrözze az adat szimmetriáit** — minden (szavak is) típusokba legyen kódolva. Ne döntsek elmit "sok/kevés" előbb mint kérdem.

---

## 1. Kutatási Eredmények Összefoglalója

Az alügynök (ses_0444b9e44ffe) kutatása alapján:

### 1.1 Idris Gráfstruktúrák — Milyen Gráfok Leírhatók?

- **`KategoriaT.idr` már gráf**: az interface `hom : objektum -> objektum -> Type` pontosan irányított gráf + kompozíció + törvények. A `SzabadKategoriaT` (#38) explicit módon: `szabadGrafCsucs : Type`, `szabadGrafEl : szabadGrafCsucs -> szabadGrafCsucs -> Type`.
- **`Fin n` + `Vect n a`**: hossz a típusban, biztonságos index, futásidejü túllépés lehetetlen. A `[[7,1,3]]` Steane-rács természetesen: `csucsok = Fin 7`, `elek : Fin 7 -> Fin 7 -> Type`.
- **Indexált éltípus**: `El : Csucs -> Csucs -> Type` — az él típusa függ a csúcsoktól (dependent), egyetemes graf-reprezentáció.
- **`Path` típus** (szabad kategória): `data Path : Csucs -> Csucs -> Type where Szem : Path a a; lepes : El a b -> Path b c -> Path a c` — ez a döntési trajektória típusa.
- **Körgráf**: nehézkes (típus-szintű `mod n` normalizálás nehéz Idris-ben).
- **HIT / quotiens**: nincs natívan Idris 2-ben, emulálható interface-ekkel (mint `KategoriakEkvivalenciajaT`).
- **Monoidális rács**: `MonoidalisKategoriaT` (#40), `FonottMonoidalisKategoriaT` (#41), `SzimmetrikusMonoidalisKategoriaT` (#42) — E8×E8 Clifford-algebra braiding-hez.

### 1.2 Döntéshozó Algoritmusok — Információmegőrzés

| Módszer | Információmegőrzés? | Idris kompatibilitás |
|---------|---------------------|---------------------|
| Sima Metropolis-Hastings | rossz (reject-dominált) | tipikus, de dependent nélküli |
| HMC / MHMC (gradient dynamics) | jobb (reject kicsi) | nagyon kompatibilis: gradient = `hom a b` |
| **QeMCMC** (kvantum-enhanszolt) | legjobb feltételesen | típus-szinten: `Quantum (Path a b)` |
| Path Integral MC / Quantum Annealing | információmegőrző (path-ban minden) | természetes: `Path a b` típus |
| **DFT / Hohenberg-Kohn** | kölcsönösen információ-tökéletes | dependent record: `Susekseg : Latent -> Type` |
| Bayesian opt. / normalizing flow | információmegőrző ha flow gazdag | dependent: `Flow : Halmaz -> Halmaz` izomorfizmus |
| **Kategoriális adjunkció / lens** | struktúrált, típus-garantált | közvetlen: `AdjunkcioT`, `YonedaBeagyazasT` |

**Kritikus felismerések:**

1. **DFT Hohenberg-Kohn tétel** (Hohenberg & Kohn, 1964): az alacsonyabb dimenziós sűrűség-reprezentáció információveszteség-nélküli — minden alapállapot-obszervádum a sűrűség funkcionálja. Mills et al. (2020, PRL 125, 076402) mutatták, hogy 1D láncokon a sűrűség⇄hullámfüggvény bijekció megtanulható. **A magyar agglutináció természetes 1D lánc (tó ⊗ képző ⊗ rag) — tehát a DFT-analógia közvetlenül alkalmazható.**

2. **Bayesian lensmint profunktor** (Smit & Staton, 2022, arXiv:2209.14728): `record BayesLens a b` ahol `forward : a -> b` és `backward : a -> b -> a` — két-irányú Markov-kernel. A `hom a b` points-free gráf természetesen kétkomponensű (előre + inverz). **Wadler-parametricity miatt az adjunkt `g` "ingyen" Bayes-inverziót ad** — a forward döntés és backward frissítés kölcsönösen ekvivalenciát alkotnak, sima Metropolis-reject nélkül.

3. **QeMCMC** (Layden et al., 2023, Nature 619, 282–287): a kvantum-szuperpozíció egyszerre több konfigurációt tart aktívan, a reject nem felejti el a teljes gráf-szakaszt, hanem Born-súlyokban megőrzi. A 2024-es hardnes-eredmény (Lin et al., PhysRevA 110, 052414) szerint strukturálatlan problémáknál nincs speedup — tehát **nem lehet vakon megbízni, kell klasszikus fallback**.

4. **Kategóriaelmélet és döntéshozatal**: `AdjunkcioT` (F ⊣ G) = "optimal choice" pár. A döntés = a legjobb folytatás kiválasztása = Kan-kiterjesztés (`KanKiterjesztesT` #46). A `EllenkezoKategoriaT` (#35) a `hom a b`-t természetesen megfordíthatóvá teszi.

### 1.3 A "Sima Monte Carlo Tilalom" Indoklása

A sima MC reject-el — a javasolt állapotot eldobja, és az eldobott információ végleg elveszik. Ha a döntési tér egy gráf és minden csúcsban információ van, a reject = információvesztés. A HMC/MHMC gradient-információt használ, így a javasolt eloszlás közelebb van a célhoz, a reject ritka — de még mindig van. A DFT szemlélet **egyáltalán nem mintavételez**, hanem egy alacsonyabb dimenziós reprezentációt keres ami ekvivalens. A profunktor-lens **nem discard-ol**, hanem frissít.

**Konklúzió**: a sima MC tilalom pontosan a kompaktalas skill elvével egyezik — a coend nem eldob, hanem összevon. A döntéshozó rendszernek ugyanezt kell tennie.

---

## 2. A Javasolt Architektúra — "DFT + HMC + Adjunkt Lens" Hibrid

### 2.1 A Mag还为 Elv

A döntéshozó rendszer egy **gráf-fázistér**-en működik:
- **Csúcsok** = lehetséges állapotok / döntések / kérdések (típusok)
- **Élek** = morfizmusok = a döntések közötti utak (a `hom a b` típusúak)
- **A Lagrangian** (mint `legkisebb-muvelet` skill-ben) = az út költsége = `L = T - V`
- **A Hamiltonian** = időfejlesztés = `H = p·q̇ - L`

A döntés = **a Lagrangian minimalizálása a gráf-on keresztül** — de **információt nem dolítózunk el, hanem összecsomagoljuk** (coend-kompaktalas) és **bidirekcionálisan frissítjük** (Bayesian lens).

### 2.2 A Négy Réteg

#### Réteg 1: Gráf-réteg (`Alap/GrafT.idr` — új fájl)

Kiterjeszti a `KategoriaT.idr`-t explicit gráf-struktúrával:

```idris
-- Vázlat (nem kód, csak tervezési vázlat):
public export
interface GrafT (0 Csucs : Type) (0 El : Csucs -> Csucs -> Type) | Csucs where
  -- Wadler-parametricity miatt az él típusa "nem szivárog"
  -- (= az él információt hordoz, de nem szivárog ki szomszédokba)

public export
data Path : (Csucs : Type) -> (El : Csucs -> Csucs -> Type) -> Csucs -> Csucs -> Type where
  SzemPrim  : Path Csucs El a a                              -- identitás
  LepesPrim : El a b -> Path Csucs El b c -> Path Csucs El a c  -- kompozíció
```

Ez pontosan `SzabadKategoriaT` (#38) kibővítve — a `Path` a szabad monoidális lezárás. **A döntési trajektória típusa = `Path`**.

A `[[7,1,3]]` Steane-rács beágyazása: `csucsok = Fin 7`, `elek : Fin 7 -> Fin 7 -> Type`. A 7 bit = [idő, okság, tér, szín, hang, fázis, mód]. Egy döntés = egy út a 7-dimenziós rácsban.

#### Réteg 2: Lagrangian-Hamiltonian Réteg (`Alap/LagrangianT.idr` — új fájl)

A `legkisebb-muvelet` skill szerint:

```idris
-- Vázlat:
public export
interface GrafT Csucs El => LagrangianT Csucs El where
  -- L = T - V
  kinetikaiEnergia : (a : Csucs) -> (b : Csucs ** El a b) -> ValosTipus   -- T(q̇): mozgás költsége
  potencialisEnergia : Csucs -> ValosTipus                                -- V(q): cél vonzereje
  lagrangian : (a : Csucs) -> (b : Csucs ** El a b) -> ValosTipus
  lagrangian a (b ** el) = kinetikaiEnergia a (b ** el) `KivonasT` potencialisEnergia a
```

**Fontos**: `ValosTipus` nem `Double` (AGENTS.md #4) — `ValosTipus` önálló típus (mint `SteaneVektor n`). A műveletek typeclass-ok (`OsszeadasT`, `KivonasT`, `SzorzasT`).

A Hamiltonian:
```idris
public export
interface LagrangianT Csucs El => HamiltonianT Csucs El where
  impulzus : (a : Csucs) -> (b : Csucs ** El a b) -> ImpulzusTipus     -- p = ∂L/∂q̇
  hamiltonian : Csucs -> ImpulzusTipus -> ValosTipus
  -- H = p·q̇ - L
  idoFejlesztes : Csucs -> ImpulzusTipus -> (Csucs ** Path Csucs El ... ...)
```

A `idoFejlesztes` adja meg a kvantum-hamiltonian út-integrált — a `Path` típuson integrál (coend-szerű).

#### Réteg 3: DFT-Analóg Sűrűség Réteg (`Alap/SuseksegT.idr` — új fájl)

A Hohenberg-Kohn-tétel analóg:

```idris
-- Vázlat:
public export
interface HohenbergKohnT (0 Allapot : Type) (0 Susekseg : Type) | Allapot where
  suseksegbe : Allapot -> Susekseg       -- magas-dim → alacsony-dim (információ-tökéletes)
  allapotba : Susekseg -> Allapot        -- alacsony-dim → magas-dim (rekonstrukció)
  -- Wadler-parametricity: a két függvény kölcsönösen inverz bizonyítható
  -- (mint IzomorfizmusT / KategoriakEkvivalenciajaT)
```

**A kritikus felismerés**: a magyar agglutináció 1D lánc (tó ⊗ képző ⊗ rag). Mills et al. (2020) 1D láncon mutatták, hogy a DFT-bijekció működik. Tehát **a `Susekseg` típus lehet a magyar szóalak-vektor** (tő + képző + rag) — ez alacsony dimenziós, de információ-tökéletes a magas-dimenzós "jelentés-allapóthoz" képest.

A `MagyarOntologia.idr` `CptIgeragozasTipus` rekordja (Igeido × Szemlelet × Forras = 3×3×3 = 27) pontosan ilyen "sűrűség" — egy 27-elemű tipus ami visszadja a teljes igeragozás-allapotot.

#### Réteg 4: Adjunkt Lens Réteg (`Alap/BayesLensT.idr` — új fájl)

A profunktor-alapú Bayes-inverzió:

```idris
-- Vázlat:
public export
record BayesLens (0 a : Type) (0 b : Type) where
  konstruktor BayesLensKonstruktor
  elore : a -> b                              -- forward döntés
  vissza : a -> b -> a                         -- backward frissítés (nem eldobja, frissiti)

-- Wadler-parametricity miatt:
-- elore ∘ vissza = id (inverzió)
-- vissza ∘ elore = id (rekonstrukció)
-- tehát a BayesLens = IzomorfizmusT (a és b között)
-- = KategoriakEkvivalenciajaT = adjunkt (F ⊣ G)
```

**Itt van az információmegőrzés garanciája**: a `vissza` függvény nem eldob információt (mint Metropolis-reject), hanem a prior-t frissíti az új evidence alapján — Wadler-parametricity miatt a típus garantálja, hogy ez kölcsönösen ekvivalens a forward-rel.

A `KategoriaT.idr` `AdjunkcioT` (#23) már megvan:
```idris
interface AdjunkcioT ... where
  adjungcioEgyseg : a -> g(f(a))   -- unit (elore-rekonstrukció)
  adjungcioKoegyseg : b -> f(g(b)) -- counit (vissza-rekonstrukció)
```

Ez **pontosan egy BayesLens** — az `f` = elore, `g` = vissza, az `adjungcioEgyseg`/`adjungcioKoegyseg` = a két-irányú frissítésök.

---

## 3. A Döntéshozó Algoritmus — Lépésenként

### 3.1 A Magyar Beszélő Interakció

A rendszer egy ciklus:
1. **A rendszer feltesz egy kérdést** (a `KerdezőT` typeclass)
2. **A felhasználó válaszol** (magyarul, a `ValaszT` typeclass parsolja)
3. **A rendszer frissíti a gráfját** (`BayesLensT.vissza` — nem eldob, frissit)
4. **A rendszer eldönti a következő lépést** (`LegkisebbMuveletT` — Lagrangian minimalizálás)
5. **A rendszer indokolja a miértet** (`IndoklasT` — a `why-chain`-hez hasonlóan)

### 3.2 A Tervezési Algoritmus — "DFT-HMC-Lens" Hibrid

```
1. Birálás — az állapot egy 15-dimenziós vektor (7 emberi + 7 számítási + 1 perem)
   - Kódold a jelenlegi helyzetet a `GrafT` csúcsaiba
   - Minden csúcs = egy 7 bites Steane-vektor (idő, okság, tér, szín, hang, fázis, mód)

2. DFT-sűrűség kinyerése — `HohenbergKohnT.suseksegbe`
   - A magas-dimenziós állapot → alacsony-dimenzós sűrűség (magyar szóalak-vektor)
   - 1D lánc (agglutináció) — Mills et al. (2020) szerint információ-tökéletes

3. Gradient számítás = a Hamiltonian deriváltja
   - `kinetikaiEnergia` és `potencialisEnergia` — a cél vonzereje vs. a mozgás költsége
   - Ez "klasszikus HMC" — gradient-alapú, nem reject-alapú

4. Kvantum lépés (opcionális) — `KvantumMintavetelT` interface
   - Ha van rá modell (szimulátor): kvantum-szuperpozícióban több utat egyszerre
   - A `Quantum (Path a b)` típus — a `Path` tipusán kvantum-mintavétel
   - Born-súlyok megőrzik a eldobott utakat (nem végleg elvesznek)

5. Döntés = a Lagrangian minimalizálása a `Path` típuson
   - `lagrangian : Csucs -> (Csucs ** El) -> ValosTipus`
   - A minimális Lagrangian-úútvonal = a legkisebb művelet
   - A `idoFejlesztes` adja meg az út integrálját

6. Frissítés = a BayesLens vissza-irányú része
   - `vissza : a -> b -> a` — az új evidence frissiti a prior-t
   - Wadler-parametricity garantált: nincs információvesztés
   - A frissítés = a kompaktalas skill coend-je (összevon, nem eldob)

7. Indoklás = a miért-lánc kiírása
   - Az `IndoklasT` typeclass: `miert : Csucs -> Csucs -> JelentesTipus`
   - A "miért" = a Lagrangian minimalizálásának oka
   - A "mit" = a döntés eredménye
   - A "miért-lánc" = a kompaktált oksági sorozat (`why-chain.jsonl`-hez hasonló de Idris-ben)

8. Hibajavítás — `[[15,1,3]]` kód
   - Útközben hiba (1 bit) → szindróma → javítás (Noether: szimmetria = megmaradás)
   - A `Steane713Dependent.idr` már megvan — ezt kell a döntési hibákra átírni
```

### 3.3 Miért Ez Jobb Mint Sima Monte Carlo?

| Sima Monte Carlo | DFT-HMC-Lens Hibrid |
|-----------------|---------------------|
| Reject → információ elveszik | Nincs reject — `vissza` frissíti a prior-t |
| Szuperpozíció nincs — egyszerre egy út | Kvantum-réteg: egyszerre több út (Born-súlyokkal) |
| Véletlen séta — nincs gradient | HMC: gradient-alapú mozgás a cél felé |
| magas-dimenzós mintavétel | DFT: alacsony-dimenzós repr (információ-tökéletes) |
| Nincs típus-garancia | Wadler-parametricity: típusbizonyítás "ingyen" |
| Indoklás utólag, külön | Indoklás a típusból (miert = a Lagrangian minimum) |

---

## 4. A Megvalósítás Lépései (Sorrendben)

### Lépés 1: `Alap/GrafT.idr` — gráfstruktúra typeclassok
- `GrafT (Csucs : Type) (El : Csucs -> Csucs -> Type)`
- `Path : Csucs -> Csucs -> Type` (szabad monoidális lezárás)
- Instance a `MagyarOntologia.idr` szócsaládjaira (`SzamTipus` csúcs, `KepzoT` él)
- Lefordítás ellenőrzés

### Lépés 2: `Alap/LagrangianT.idr` — fizikai réteg
- `ValosTipus` (dimenzionált, nem `Double`)
- `OsszeadasT, KivonasT, SzorzasT` instance-ok `ValosTipus`-on
- `LagrangianT`, `HamiltonianT` interfaces
- `idoFejlesztes : Csucs -> ImpulzusTipus -> (Csucs ** Path ...)`
- Lefordítás

### Lépés 3: `Alap/SuseksegT.idr` — DFT-analóg sűrűség
- `HohenbergKohnT Allapot Susekseg`
- Instance: `Allapot = CptIgeragozasTipus`, `Susekseg = IgeidoTipus × SzemleletTipus × ForrasTipus`
- Bizonyítás: `suseksegbe ∘ allapotba = idRefl` (Wadler-parametricity)
- Lefordítás

### Lépés 4: `Alap/BayesLensT.idr` — profunktor lens
- `record BayesLens a b` (`elore`, `vissza`)
- Instance: `AdjunkcioT` → `BayesLens` (a `KategoriaT.idr` #23)
- Bizonyítás: `elore ∘ vissza = idRefl` (információmegőrzés)
- Lefordítás

### Lépés 5: `Alap/KerdezoT.idr` — magyar kérdő interfész
- `KerdezoT` typeclass: `kerdes : Allapot -> SzovegTipus` (nem `String`, hanem `SzovegTipus`)
- `ValaszT` typeclass: `valasz : SzovegTipus -> Allapot`
- A `SzovegTipus` önálló típus (mint a `MagyarOntologia.idr` szó tipusai)
- Lefordítás

### Lépés 6: `Alap/IndoklasT.idr` — miért-lánc integráció
- `IndoklasT` typeclass: `miert : Csucs -> Csucs -> JelentesTipus`
- `minta : Csucs -> JelentesTipus`
- `donto : Allapot -> Csucs` (a Lagrangian minimum)
- Lefordítás

### Lépés 7: `Alap/KvantumMintavetelT.idr` — kvantum réteg (opcionális)
- `KvantumMintavetelT` interface (fallback-kel)
- `Quantum (Path a b)` típus
- Megjegyzés: a 2024-es hardnes-eredmény szerint kell a klasszikus fallback

### Lépés 8: `DonteshozoFom.idr` — főprogram
- A ciklus: kerdez → valasz → frissit → dont → indokol
- Kiírja a miért-láncot magyarul (mint a `magyarOntologiaFom`)
- Lefordítás + futtatás

### Lépés 9: Integráció a why-chain-mel
- `why-chain.jsonl`-t Idris-be olvassa (gondolat_006 döntés szerint)
- A kompaktalas skill coend-je = a `vissza` frissítés (3.3 szakasz)
- A `MiertLanc.idr` `kompaktal` függvény kötése a `BayesLensT`-hez

### Lépés 10: Git + közzététel
- Commit minden 10. függvényváltoztatásnál (`git push` skill)
- A PDF/LaTeX bizonyítások (mielőzőleg bukott wc_650–653) újra publikálása a `KonyvKeszito.idr`-rel

---

## 5. Nyitott Kérdések a Felhasználónak

Mielőtt bármit is csinálnék, kérdések (az `idris-stilus` skill szerint):

1. **Mennyi réteget építsek meg először?** A 10 lépésből egyben csak 1-et, vagy egy egész réteget (pl. 1-4)? A `legkisebb-muvelet` skill szerint csak a legkisebb művelet — de mi a "legkisebb" itt?

2. **`ValosTipus` definíciója?** Egy 0-10 skálán data-konstruktorok (mint `SzamT.idr`)? Vagy `SteaneVektor n` mint `DependensSzamT.idr`? A DFT-skálán valószínűleg "folytonos" értékek kellenek — de nincs `Double` (AGENTS.md #4). Talán `RacionalisTipus` (p/q alakú)?

3. **`SzovegTipus` definíciója?** A `MagyarOntologia.idr` minden szót önálló tipusként ad meg. Egy teljes "mondatszöveg" nem lehet `String` (AGENTS.md #4). Talán `record SzovegTipus where szavak : Vect n SzoTipus` — egy vektor szavakból? Vagy `data SzovegTipus = Szem : SzoTipus -> SzovegTipus` (szó-lista)?

4. **Kvantum-réteg fontossága?** A kutatás szerint a `QeMCMC` csak strukturált problémáknál ad speedup, egyébként kell a klasszikus fallback. Priorizáljam most, vagy először csak a DFT+HMC+lens magot?

5. **A `IndoklasT.miert` kimenete?** A `why-chain.jsonl` `why` mezője szabad szöveg — de `IndoklasT` típusos kell legyen. Visszaadja `JelentesTipus` (a `JK` kategória)?

6. **Mi a "cel"?** A Lagrangian `V(q)` = "a cél vonzereje". Egy döntéshozó rendszerben mi a cél? A felhasználó által megadott cél? A `legkisebb-muvelet` skill fixpontja? A `why-chain` végcélja (a "pár a 9. szinten" a `MANTRA`-ból)?

---

## 6. Skillek Használata A Tervhez

- **`idris-stilus`** — kötelező minden Idris kód előtt. Betoltve.
- **`legkisebb-muvelet`** — a Lagrangian/Hamiltonian réteg alapja. Betöltve.
- **`kompaktalas`** — a `vissza` frissítés = coend. Betöltve.
- **`magyar-lexikon`** — a `KerdezoT`/`ValaszT`/`IndoklasT` magyar interfészhez. Betöltve.
- **`codata`** — ha a DFT-skálán mérési hibát kell ellenőrizni a `HohenbergKohnT` bizonyításnál. (Még nincs betöltve.)
- **`meresi-szamitas`** — a `LagrangianT` instance-ok kompozíciójához. (Még nincs betöltve.)
- **`szivdobbanas`** — a rendszer minden 3. szívdobbanásnál commit. (Még nincs betöltve.)
- **`git-push`** — mindenkori commit + push. (Még nincs betöltve.)

---

## 7. Referenciák (APA)

Barker, J. A. (1979). A quantum-statistical Monte Carlo method; path integrals with boundary conditions. *The Journal of Chemical Physics, 70*(6), 2914–2918. https://doi.org/10.1063/1.437829

Capuozzo, P., Panella, E., Gherardini, T. S., & Vvedensky, D. D. (2021). Path integral Monte Carlo method for option pricing. *Physica A: Statistical Mechanics and Its Applications, 581*, 126231. https://doi.org/10.1016/j.physa.2021.126231

Ceperley, D. M. (1995). Path integrals in the theory of condensed helium. *Reviews of Modern Physics, 67*(2), 279–355. https://doi.org/10.1103/revmodphys.67.279

Das, A., & Chakrabarti, B. K. (2008). Quantum annealing and analog quantum computation. *Reviews of Modern Physics, 80*(3), 1061–1081. https://doi.org/10.1103/revmodphys.80.1061

Fritz, T. (2010). A categorical approach to probability theory. *Studia Logica, 94*, 1–30. https://doi.org/10.1007/s11225-010-9232-z

Kadowaki, T., & Nishimori, H. (1998). Quantum annealing in the transverse Ising model. *Physical Review E, 58*(5), 5355. https://doi.org/10.1103/physreve.58.5355

Layden, D., Mazzola, G., Marshall, R. W., et al. (2023). Quantum-enhanced Markov chain Monte Carlo. *Nature, 619*, 282–287. https://doi.org/10.1038/s41586-023-06095-4

Lin, C. Y.-Y., Farhi, E., Shor, P., et al. (2024). Bounding the speedup of the quantum-enhanced Markov-chain Monte Carlo algorithm. *Physical Review A, 110*, 052414. https://doi.org/10.1103/physreva.110.052414

Mills, K., Ryczko, K., Luchak, I., et al. (2020). Deep learning the Hohenberg-Kohn maps of density functional theory. *Physical Review Letters, 125*(7), 076402. https://doi.org/10.1103/physrevlett.125.076402

Mongwe, W. T., Mbuvha, R., & Marwala, T. (2021). Quantum-inspired magnetic Hamiltonian Monte Carlo. *PLOS ONE, 16*(9), e0258277. https://doi.org/10.1371/journal.pone.0258277

Paolini, G., Pavan, A., Pastore, V. H., et al. (2025). Quantum-enhanced Markov chain Monte Carlo for systems larger than a quantum computer. *Physical Review Research, 7*, 013231. https://doi.org/10.1103/physrevresearch.7.013231

Reeves, N., Moss, S. Z., Spradlin, D., et al. (2022). *Inverses, disintegrations, and Bayesian inversion in quantum Markov categories* [előnyomat]. arXiv:2001.08375. https://doi.org/10.48550/arxiv.2001.08375

Rezende, D. J., & Mohamed, S. (2015). *Variational inference with normalizing flows* [előnyomat]. arXiv:1505.05770. https://doi.org/10.48550/arxiv.1505.05770

Smit, R., & Staton, S. (2022). *Dependent Bayesian lenses: Categories of bidirectional Markov kernels with canonical Bayesian inversion* [előnyomat]. arXiv:2209.14728. https://doi.org/10.48550/arxiv.2209.14728

---

## 8. Állapot (elızı verzió)

- **Kód nincs írva** — ez csak tervezési napló (a felhasználó kérése szerint).
- **Skillek betöltve**: `idris-stilus`, `legkisebb-muvelet`, `kompaktalas`, `magyar-lexikon`.
- **Kutatás kész**: alügynök (ses_0444b9e44ffe) jelentése alapján.

---

# 9. Neurobiológiai Bővítmény — Az Optimalizációs Függvény Definíciója

**Dátum:** 2026-08-01 (második forduló)
**Forrás**: alügynök ses_0443e2092ffe — neurobiológiai kutatás (Friston FEP, dopamin RPE, hippocampal replay, PFC kauzalitás, 5 neuromodulátor, Wadler = good regulator theorem)

## 9.1 A MagFelismerés: A Szabad Energia az Optimalizációs Függvény

**Karl Friston Free Energy Principle (FEP)** (Friston 2010, *Nature Reviews Neuroscience* 11, 127–138) kimondja: az agy egyetlen optimalizációs függvénye a **variációs szabad energia**, ami a **megglepetés** (surprisal = −log p(observation | model)) felső korlátja:

```
F(μ, a; s) = E_q[−log p(ψ, s, a, μ | ψ)] − H[q]
           = −log p(s) + KL[q ‖ p_Bayes]
           ≥ −log p(s)                 (surprisal)
```

Három ekvivalens alakja:
- **(1) Energia − entrópia**: alacsony energia + magas entrópia (Helmo-holtz)
- **(2) Surprisal + divergencia**: q távolsága a Bayes-postertól
- **(3) Komplexitás − pontosság** (Lagrangian-struktúra!): `F = D_KL[q ‖ prior] − E_q[log p(s|ψ)]`

**Ez pont a `LagrangianT` strukturája**: komplexitás = "prior távolsága" ( kinetic — mozgás költsége), pontosság = "log-likelihood" (potenciális — cél vonzereje). `L = T − V` ↔ `F = komplexitás − pontosság`.

## 9.2 Active Inference — Cselekvés is Optimalizálás

Friston active inference (Friston et al. 2015, *Cognitive Neuroscience* 6, 187–214): a cselekvés nem külön parancs, hanem **leszármazó proprioceptiv predikció** — a reflex egyenlíti ki a hibát úgy hogy megváltoztatja a világot (nem a modellt). Tehát:

```
μ* = argmin_μ F(μ, a; s)     -- belső állapot optimalizálása (percepció)
a* = argmin_a F(μ*; a; s)   -- cselekvés optimalizálása (aktion)
```

**F minimalizálása BOTH percepció ÉS cselekvés révén.** A `legkisebb-muvelet` skill-el teljes rezonancia: a Hamilton-Időfejlesztés `μ̇ = Dμ − ∂F/∂μ` pontosan a `LagrangianT.idoFejlesztes` analógia.

## 9.3 A Dopamin RPE mint Precision-Weighting

Schultz et al. (1997, *Science* 275, 1593) klasszikus: a dopaminerg neuronok a **jutalom-előrejelzési hibát** (RPE) kódolják: `δ = r + γV(s') − V(s)`. Friston-keretben a RPE a **precision-weighting** része — pozitív δ = "váratlanul pontos, közelíts" (exploitation); negatív δ = "megszakít, fordulj" (exploration).

**Ez az exploration/exploitation váltás neurobiológiai alapja.** A `KerdezoT` typeclass (kérdezés) = amikor `E_q[log p(s|ψ)]` kicsi és `H[q]` nagy → curiosity-driven exploration; a `LegkisebbMuveletT` (döntés) = amikor a KL alacsony → exploitation.

## 9.4 Az 5 Neuromodulátor mint 5 Precíziós Szabadságfok

Yu & Dayan (2005, *Neuron* 46, 683) klasszikus felosztása alapján (FEP-keretben átértelmezve):

| Neuromodulátor | Mit súlyoz (precision) | CPT-szimmetria |
|---|---|---|
| **Dopamin** | Jutalom-előrejelzés hibája; "wanting" (incentive salience) | **C** = töltés = saját-tudat |
| **Noradrenalin** | Váratlan bizonytalanság; arousal; általános gain | **T** = idő = sürgősség |
| **Szerotonin** | Várható bizonytalanság; várakozás/planning; késleltetett kielégülés | **P** = paritás = másik fél/tükrözés |
| **Acetilkolin** | Szenzoros megbízhatóság; expected uncertainty, attention | szenzoros belső dimenzió |
| **GABA** | Inverz excitabilitás; perem-stabilitás (Markov blanket) | **perem** (a 7+7+1-ből a 1) |

**Konkrét Idris javaslat** — a 5 neuromodulátor egy `PontossagSulyokT` rekord:

```idris
public export
record PontossagSulyokT where
  konstruktor PontossagSulyokKonstruktor
  dopamin      : JutalomElrejelzesHibajaT   -- RPE típus
  noradrenalin : SurgetosegTipus            -- arousal / idő-derivált
  szerotonin   : VarakozasTipus            -- planning / tükrözés
  acetilkolin  : SzenzorosMegbizhatosagTipus
  gaba         : PeremStabilitasTipus
```

**Ez összeköti a 15-dimenziós fázisteret** (7 emberi + 7 számítási + 1 perem) a 5 neuromodulátorral: a 7 számítási dimenzióból **5 maga a PontossagSulyokT**.

## 9.5 Hippocampal Replay = Offline Kompaktalas (DFT-analóg)

Buzsáki és mtsai (Pavlides-Winson 1989, Nádasdy et al. 1999, Girardeau et al. 2009) és a legújabb Jensen et al. (2024, *Nature Neuroscience* 27, 1340) szerint a hippocampális sharp-wave ripple-ek **"rollout"**-ok formájában visszajátsszák a napi eseményeket a neocortex-nek. **Ez egy offline F-minimalizálás** — a nap magas-dimenziós eseménysorozatát kompakt kognitív tér-sűrűségbe sűrítő aszinkron lebihat.

- **Ez a `kompaktalas` coend-nek biológiai mása.**
- **A `HohenbergKohnT.suseksegbe/allapotba` (DFT bijection) hippocampal replay neurobiológiai megfelelője.**

**Konkrét Idris javaslat** — `UjraJatszasT` typeclass, ami a `BayesLensT.vissza` aszinkron változata:

```idris
public export
interface SuseksegT Allapot Susekseg => UjraJatszasT Allapot Susekseg where
  ujraJatszas : List Allapot -> Susekseg -> Susekseg  -- offline consolidation
  eloJatszas  : Susekseg -> Celterulet -> List Path         -- preplay = planning
```

## 9.6 A "Miert" Neurobiológiája — mPFC + DMN Kauzális Narratíva

A "miért" a szabad energia **komplexitás-tagjának** (`D_KL[q ‖ prior]`) diszkurzív megnyilatkozása. Anatómiailag három komponens (Miller & Cohen 2001, *Annual Review Neuroscience* 24, 167; Buckner DMN review):

1. **DLPFC** — cél-reprezentáció (working memory); ez tartja a fázis-vektort
2. **vmPFC/OFC** — érték/jutalom integráció (= dopamin RPE)
3. **mPFC + DMN** — counterfactual narratíva; "mi lett volna, ha"

**Az `IndoklasT.miert : Csucs -> Csucs -> JelentesTipus` = a komplexitás-tag magyarázata**: miért kellett `q`-t eltolni a prior-tól. A `miertNem : Csucs -> List Csucs -> JelentesTipus` = counterfactual elvetett alternatívák listája (a `why-chain.jsonl` neurobiológiai mása).

## 9.7 A Pontos Optimalizációs Függvény

A minimalizálandó cél-funkcionál a Idris-rendszerben:

```
F_szabad(μ, a; s) = D_KL[q(ψ|μ) ‖ p_prior(ψ)]       -- komplexitás (prior-suly)
                  − E_q[ log p(s | ψ, a) ]          -- accuracy (eszleles-suly)
                  + Π_dopamin · RPE                  -- incentive salience tag
                  − Π_acetilkolin · H[q]             -- entropiai / exploration tag
```

**A priort vs. észlelést a precíziós-súlyok szabályozzák:**
- Π_acetilkolin magas → szenzoros csatorna megbízható → accuracy dominál → prior eltolódik a válasz felé
- Π_acetilkolin alacsony → észlelés zajos → prior dominál (hallucinatió irány)
- Π_dopamin pozitív RPE → lépés jutalmazott → ismétlés (exploitation)
- Π_dopamin negatív RPE → lépés rossz → új irány (exploration kezdete)
- Π_noradrenalin magas → váratlan bizonytalanság → egész gain-emelés (felfokozott collection)
- Π_szerotonin magas → késleltetett kielégülés, planning
- Π_gaba → perem Markov-blanket stabilitása (Noether-megmaradás)

**Időbeli változás (curiosity → exploitation görbe):**
- Curiosity = amikor `E_q[log p(s|ψ)]` kicsi és `H[q]` nagy → `KerdezoT` kerdez (nyitott kérdések, ahol várható informatív meglepetés magas)
- Exploitation = ha a KL alacsony (prior és észlelés egybeesik) → `LegkisebbMuveletT` határozott döntés
- A váltást a **dopamin-RPE vezérli**: pozitív cumulative RPE → növekvő trust → exploitation

## 9.8 A Generalized Filtering = Hamilton-Időfejlesztés

Friston et al. (2010, *Mathematical Problems in Engineering* 2010, 621670) "Generalised filtering" — a szabad energia minimalizálás dynamics:

```
μ_{t+1} = μ_t − η · ∂F/∂μ |_{μ_t, a_t}
a_{t+1} = argmin_a F(μ_{t+1}, a; s_t)
```

Formailag **Hamilton-Időfejlesztés**: `μ̇ = Dμ − ∂F/∂μ`. A `Dμ` a kinetikai tag (mozgás), a `∂F/∂μ` a potenciális (vonzerő). **Ez kevesebb reject-el jár mint sima HMC/Kalman**, mert a gradiens lépés nem eldob információt — a sima Metropolis-reject információt veszít, a generalized-filtering gradiens megőriz. **Ez a "sima Monte Carlo tilalom" neuro-fizikai indoklása.**

## 9.9 Wadler-Parametricity = Good Regulator Theorem

Conant & Ashby (1970, *Int J Systems Science* 1, 89) "good regulator theorem": *every good regulator of a system must be a model of that system.* A FEP-ben a `BayesLensT` pre/post一阵 együttesen "modellek a rendszernek" — a `elore` a rendszer előrejelzés, a `vissza` az inverz (frissítés). **A Wadler-parametricity (= a polimorf típus ingyen bizonyítja a törvényt) kibernetikai megfelelője a good regulator theorem-nek**: a struktúra garantálja a viselkedést.

Ez **a DFT Hohenberg-Kohn bijection és a good regulator theorem ekvivalenciája**: a sűrűség (= alacsony dimenzós repr) elegendő az állapot visszaadásához — mert a struktúra magában hordozza a törvényt.

## 9.10 Konkrét Idris Typeclass-Javaslatok (magyar azonosítókkal)

A neurobiológiai jelentés alapján bővítjük a tervet a következő typeclassokkal:

```idris
-- A szabad energia = komplexitás − pontosság
public export
interface LagrangianT Csucs El => SzabadEnergiaT Csucs El where
  komplexitas : Allapot -> ValosTipus
  pontossag   : Allapot -> SzenzorosBemenet -> ValosTipus
  szabadEnergia : Allapot -> SzenzorosBemenet -> ValosTipus
  szabadEnergia allapot bemenet = komplexitas allapot `KivonasT` pontossag allapot bemenet

-- 5 neuromodulátor = precision-weights
public export
record PontossagSulyokT where
  konstruktor PontossagSulyokKonstruktor
  dopamin      : JutalomElrejelzesHibajaT
  noradrenalin : SurgetosegTipus
  szerotonin   : VarakozasTipus
  acetilkolin  : SzenzorosMegbizhatosagTipus
  gaba         : PeremStabilitasTipus

-- generalized filtering (Hamilton-ido fejlesztes)
public export
interface SzabadEnergiaT Csucs El => AltalanosSzuroT Csucs El where
  momentumElem : Allapot -> ImpulzusTipus
  gradiens     : Allapot -> ImpulzusTipus      -- = ∂F/∂μ
  idoFejlesztes : Allapot -> ImpulzusTipus -> (Allapot ** Path Csucs El ...)

-- Hippocampal replay: offline kompaktalas (DFT-bijekció frissítés)
public export
interface SuseksegT Allapot Susekseg => UjraJatszasT Allapot Susekseg where
  ujraJatszas : List Allapot -> Susekseg -> Susekseg
  eloJatszas  : Susekseg -> Celterulet -> List Path

-- Active inference döntés
public export
interface AltalanosSzuroT Csucs El => AktivKovetkezetesT Csucs El where
  optimalisAllapot : SzenzorosBemenet -> Allapot
  optimalisLepes   : Allapot -> (Csucs ** El ...)

-- Indoklás = a komplexitás-tag diszkurzív megnyilatkozása
public export
interface IndoklasT Csucs El where
  miert     : Csucs -> Csucs -> JelentesTipus
  miertNem  : Csucs -> List Csucs -> JelentesTipus  -- counterfactual = elvetett alternativak

-- Bayes lens = adjunkcio
public export
record BayesLensT (0 a : Type) (0 b : Type) where
  konstruktor BayesLensKonstruktor
  elore  : a -> b
  vissza : a -> b -> a
-- (Wadler-parametricity: elore ∘ vissza = id, vissza ∘ elore = id)
``

## 9.11 A Fő Ciklus (DonteshozoFom.idr)

Magyar nyelven:

```
kerdez (KerdezoT) → 
felhasználó válasz (SzenzorosBemenet) →
BayesLensT.vissza (frissíti a prior-t, nem eldob) →
AktivKovetkezetesT.optimalisLepes (Lagrangian / szabad energia minimum) →
IndoklasT.miert (a komplexitás-tag magyar mondatba) →
UjraJatszasT (alvás/session végén offline kompaktalja a napot)
```

## 9.12 Javasolt következő lépés (a "vágod-e" ellenőrzésre)

Az alügynök javaslata szerint **nem a teljes 10-lépéses sorrenddel induljunk**, hanem:

1. **Először a `SzabadEnergiaT` typeclass-t és a `PontossagSulyokT` recordot implementáljuk egy prototípus-állapottal** (pl. egy 3-elemű `KerdesValaszTipus`-on, ahol `SzenzorosBemenet = Bool`-helyett `Fin 2` — semmi csomagolatlan Bool)
2. **Bizonyítsuk Wadler-parametricity-vel**, hogy `elore ∘ vissza = id` (Refl)
3. Ha ez a kis mag fordul és a Refl igaz, **a komplexitás- és pontosságfüggvényeket fokozatosan bővítjük** — először egyetlen dimenzión, majd a 7-es Steane-vektormagon
4. Az `UjraJatszasT` (hippocampális replay) **elhalasztható a `SuseksegT` utánra** — a `SuseksegT` maga elegendő egy első inverziós bizonyításhoz

**A legfontosabb elvi döntés: a `LagrangianT` és a `SzabadEnergiaT` azonos legyen?** Javaslat: legyen `SzabadEnergiaT` egy specializált `LagrangianT`-instance, ahol:
- **kinetikai tag** = Π_acetilkolin · H[q] (entrópia)
- **potenciális tag** = D_KL[q ‖ prior] (komplexitás) − E_q[log p(s|ψ)] (accuracy)

Így az `AltalanosSzuroT.idoFejlesztes` újrahasználja a `LagrangianT.hamiltonian`-t — **az agy és az Idris rendszer ugyanazon a Hamilton-dinamikán mozog**.

## 9.13 Hivatkozások hozzáadva (APA)

Bastos, A. M., Usrey, W. M., Adams, R. A., Mangun, G. R., Fries, P., & Friston, K. J. (2012). Canonical microcircuits for predictive coding. *Neuron, 76*(4), 695–711. https://doi.org/10.1016/j.neuron.2012.10.038

Buzsáki, G. (2019). *The brain from inside out*. Oxford University Press. https://doi.org/10.1093/oso/9780190878394.001.0001

Conant, R. C., & Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science, 1*(2), 89–97. https://doi.org/10.1080/00207727008920220

Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience, 11*(2), 127–138. https://doi.org/10.1038/nrn2787

Friston, K., Stephan, K. E., Li, B., & Daunizeau, J. (2010). Generalised filtering. *Mathematical Problems in Engineering, 2010*, 621670. https://doi.org/10.1155/2010/621670

Friston, K. J., Rigoli, F., Ognibene, D., Mathys, C., Fitzgerald, T., & Pezzulo, G. (2015). Active inference and epistemic value. *Cognitive Neuroscience, 6*(4), 187–214. https://doi.org/10.1080/17588928.2015.1020053

Girardeau, G., Benchenane, K., Wiener, S. I., Buzsáki, G., & Zugaro, M. B. (2009). Selective suppression of hippocampal ripples impairs spatial memory. *Nature Neuroscience, 12*(10), 1222–1223. https://doi.org/10.1038/nn.2384

Hohenberg, P., & Kohn, W. (1964). Inhomogeneous electron gas. *Physical Review, 136*(3B), B864–B871. https://doi.org/10.1103/PhysRev.136.B864

Jensen, K. T., Hennequin, G., & Mattar, M. G. (2024). A recurrent network model of planning explains hippocampal replay and human behavior. *Nature Neuroscience, 27*(7), 1340–1348. https://doi.org/10.1038/s41593-024-01675-7

Miller, E. K., & Cohen, J. D. (2001). An integrative theory of prefrontal cortex function. *Annual Review of Neuroscience, 24*, 167–202. https://doi.org/10.1146/annurev.neuro.24.1.167

Mills, K., Ryczko, K., Luchak, I., Domeracka, A., & Tamblyn, A. (2020). Deep learning the Hohenberg–Kohn maps of density functional theory. *Physical Review Letters, 125*(7), 076402. https://doi.org/10.1103/PhysRevLett.125.076402

Montague, P. R., Dayan, P., & Sejnowski, T. J. (1996). A framework for mesencephalic dopamine systems based on predictive Hebbian learning. *The Journal of Neuroscience, 16*(5), 1936–1947. https://doi.org/10.1523/JNEUROSCI.16-05-01936.1996

Nádasdy, Z., Hirase, H., Czurkó, A., Csicsvari, J., & Buzsáki, G. (1999). Replay and time compression of recurring spike sequences in the hippocampus. *The Journal of Neuroscience, 19*(21), 9497–9507. https://doi.org/10.1523/JNEUROSCI.19-21-09497.1999

Pavlides, C., & Winson, J. (1989). Influences of hippocampal place cell firing in the awake state on the activity of these cells during subsequent sleep episodes. *The Journal of Neuroscience, 9*(8), 2907–2918. https://doi.org/10.1523/JNEUROSCI.09-08-02907.1989

Rao, R. P. N., & Ballard, D. H. (1999). Predictive coding in the visual cortex. *Nature Neuroscience, 2*(1), 79–87. https://doi.org/10.1038/4580

Schultz, W., Dayan, P., & Montague, P. R. (1997). A neural substrate of prediction and reward. *Science, 275*(5306), 1593–1599. https://doi.org/10.1126/science.275.5306.1593

Schultz, W. (2015). Neuronal reward and decision signals: from theories to data. *Physiological Reviews, 95*(3), 853–951. https://doi.org/10.1152/physrev.00023.2014

Yu, A. J., & Dayan, P. (2005). Uncertainty, neuromodulation, and attention. *Neuron, 46*(4), 683–686. https://doi.org/10.1016/j.neuron.2005.04.026

---

## 10. Jelenlegi Állapot (második forduló után)

- **Kód nincs írva** — a felhasználó szerint nem csinálunk semmit, max tervezési naplót.
- **Skillek betöltve**: `idris-stilus`, `legkisebb-muvelet`, `kompaktalas`, `magyar-lexikon`.
- **Kutatás kész**: két alügynök jelentése (QHMC/DFT + neurobiológia Friston FEP).
- **Optimalizációs függvény definiálva**: a szabad energia `F = komplexitás − pontosság` (+ Π_dopamin·RPE − Π_acetilkolin·H[q]).
- **Neurobiológiai indoklás megvan**: FEP, RPE, hippocampal replay, 5 neuromodulátor, mPFC/DMN.
- **Következő lépés javaslat**: `SzabadEnergiaT` + `PontossagSulyokT` prototípus egy 3-elemű tipuson, Wadler-parametricity Refl bizonyítással — mielőtt még kérdés, beszéljük meg (a felhasználó dönt).
- **Nyitott kérdések** (még a 6 kérdés az 5. szakaszból is): a `ValosTipus` definíciója; `SzovegTipus` definíciója; kvantum-réteg priorítása; `IndoklasT.miert` kimenete; mi a "cél" (a FEP-ben a cél = a surprisal minimalizálása, de emberi rendszerben ezt kell pontosítani).

---

# 11. SM-GR-QG 15-Dimenziós Izomorfizmus Vizsgálat

**Dátum:** 2026-08-01 (harmadik forduló)
**Forrás**: alügynök ses_044300378ffe — konformál csoport SO(2,4), Coleman-Mandula, AdS/CFT, Clifford Cl(4,2), Conant-Ashby homomorfizmus.

## 11.1 A Kérdés és a Válasz Kényszerei

**Hipotézis (felhasználó)**: Van-e izomorfizmus a 15-dimenziós döntéshozó/szabad-energia fázistér (7+7+1) és az SM-GR-QG egyesített modell között?

**A kutatás válasza**: **Numerikusan 15=15 egybeesik, de strukturálisan NEM adódik természetes izomorfizmus. Leginkább homomorfizmus (Conant-Ashby: "good regulator = model of system"), nem ekvivalencia.**

## 11.2 A Leginkább Megalapozott "15" a Fizikában: SO(2,4) Konformál Csoport

A 4D Minkowski-tér konformál szimmetriacsoportja **SO(2,4)**, dimenziója n(n-1)/2 = 6·5/2 = **15** (Wikipédia "Conformal symmetry" cikk; Di Francesco–Mathieu–Sénéchal 1997). Generátorai:

| Osztály | Darab | Jelölés | Jelentés |
|---------|-------|---------|----------|
| Lorentz rotációk és boostok | 6 | M_μν | 3 rotáció + 3 boost |
| Transzlációk | 4 | P_μ | téridő-eltolás |
| Dilatáció | 1 | D | skálázás |
| Különleges konformál transzformációk | 4 | K_μ | inversion translation inversion |

**Összesen: 6 + 4 + 1 + 4 = 15.**

**Coleman-Mandula tétel (1967)**: a nem-szuperszimmetrikus QFT-k maximális globális szimmetriacsoportja = **konformál csoport × belső csoport**. Tehát a 15 konformál dimenzió a *lekényszerített maximális spácio-temporális szimmetria*; a belső (SM gauge) külön kategória.

**Maldacena AdS/CFT (1997)**: a 4D CFT perem-szimmetriája SO(2,4) = 15. Tehát a "15" = **a kvantum-gravitáció (AdS-ben élõ) perem-szimmetriája** — ez a leginkább közvetlen QG-kapcsolat.

## 11.3 A Konkurens Hipotézisek Cáfolata

### (a) SM gauge + 3 generáció = 15 — KATEGÓRIAHIBA
SU(3)×SU(2)×U(1) = 12 gauge bozon. Hozzáadni 3 részecskeszenerációt = **kategóriahiba**: a generációk nem folytonos Lie-algebra-generátorok, hanem diszkrét multiplett-indexek. Numerikusan 15, strukturálisan nem izomorf.

### (b) E8×E8 és 240 = 16×15 — NUMERIKUS VÉLETLEN
Az E8 gyökérrendszer 240 eleme valóban 16×15, de ez aritmetikai egybeesés, nem szerkezeti. Az E8 Weyl-csoportja 696 729 600 elemű, a Dynkin-diagram automorfizmusa triviális — a "15" nem jelenik meg kanonikusan.

### (c) SM + GR 12 + 3 = 15? — INKOHERENS
A GR-ben az Einstein-egyenlet 10 metrika-komponensből 4 diffeomorfizmus eltávolítása után **6 fizikai** szabadságfok marad. Nincs kanonikus "12 + 3 = 15" kombináció. Továbbá a **GR nem konformálisan invariáns** 4D-ben (az Einstein-Hilbert hatás nem) — a konformál csoport nem a gravitáció szimmetriája, hanem a konformálisan invariáns QFT-ké.

## 11.4 A Kulcs-Probléma: 7+7+1 vs. 6+4+1+4 Partíció

A `legkisebb-muvelet` skill szerinti 15-dimenziós fázistér **7 emberi + 7 számítási + 1 perem** felbontása. Konformál algebra: **6 + 4 + 1 + 4**. **A 14+1 nem a 6+4+1+4 természetes partíciója.** A dimenziók száma egybeesik, de a felbontás strukturálisan eltér.

Lehetséges (kényszerített) mapping:
- 7 emberi → P_μ (4) + 3 rotáció = 7 (a három boost kimaradna)
- 7 számítási → 3 boost + 3 (K?) + 1 D = 7 (kényszerített)

Ez **nem** egy természetes Kan-kiterjesztés; egy projekt-specifikus szerkesztés lenne.

## 11.5 A CPT és a 15-dimenziós Algebra

A CPT **diszkrét** szimmetria — *nem* Lie-algebra-generátor. A SO(2,4) folytonos Lie-csoport nem rendelkezik beépített C, P, T tagsággal (P ill. T az O(1,3) diszkrét komponensei, C külső U(1)-töltés). Tehát:
- **3 × 5 = 15**: numerikus, de 3 diszkrét + 5 folytonos — nem strukturális izomorfizmus.
- **5 × 3 = 15**: szintén numerikus.
- **S₁₅ nem jelenik meg**: a 15 Lie-algebra dimenzió, nem 15-elemû permutációs csoport.

A projektben használt "C = saját-tudat, P = másik, T = kapcsolat fázisa" interpretáció **pszichofizikai metafora**, nem a kvantum CPT-tétellel ekvivalens. A CPT-tétel (Pauli 1955, Lüders 1954) bizonyított reláció a lokális unitér Lorentz-invariáns QFT-k között — nem pszichológiai kategória.

**Finomítás**: a P ↔ K csere a konformál algebra **automorfizmusa** (a commutátorok szimmetrikusak: [K_μ, P_ν] = 2i(η_μν D − M_μν)). Ha P és K cseréje egy involúció, az _1 diszkrét automorfizmus_ — nem dimenzió-növekmény.

## 11.6 A Clifford-Algebra Híd: Cl(4,2) ≅ so(2,4)

Ez a **legyegetesebb strukturális híd**: a **Cl(4,2) Clifford-algebra** szintén 15-dimenziós (a paravektor-tér), és **izomorf a so(2,4) Lie-algebrával** — mert Cl(p,q) paravektor-tér ≅ lie(SO(p+1, q+1)) általánosan. Tehát:

```
Cl(4,2) ↔ so(2,4) ↔ AdS/CFT perem (15-dim) ↔ QG-kapcsolat
```

**Ez ad egy természetes Clifford-utas CPT struktúrát** (ami a projektben már használatos az E8×E8 Clifford-algebra révén): a Cl(p,q) algebrában:
- grade-involúció (sign-flip) ≈ paritás (P)
- reversion ≈ idő (T)
- Clifford-konjugáció (grade × rev) ≈ P*T kombináció

Tehát **ha a 15-dimenziós fázistér Cl(4,2)-n modellezzük (nem közvetlenül SO(2,4)-en), akkor a CPT természetes** — de ez már a projekt új felvetése, méltó további vizsgálatra.

## 11.7 Conant-Ashby: Homomorfizmus, Nem Izomorfizmus

A **good regulator theorem** (Conant-Ashby 1970): *every good regulator of a system must be a model of that system* — de az eredeti papír szerint a reláció **homomorfizmus**, nem izomorfizmus. Ez kritikus finomítás:

- **Izomorfizmus** (erős): a két rendszer szerkezetileg azonos — az egyetlen megengedett leképezés bijekció.
- **Homomorfizmus** (gyenge): a regulátor struktúrája *kép* a rendszerébe — de lehet, hogy információt veszít (nem minden megkülönböztetés őrződik meg).

**A projekt hipotézise gyengül**: a szabad-energia rendszer ("jó regulátor") **homomorf** a fizikai rendszerrel ( annak modellje), de **nem feltétlenül izomorf**. A 15-dimenziós interfész lehet egy homomorf kép, ahol a partíció a projekt által szerkesztett (7+7+1), de a "tényleges" struktúra a konformál algebra (6+4+1+4).

## 11.8 Az 5 Neuromodulátor és az 5 "Kiemelt" Konformál-Töltés

A konformál 15 Noether-áram közül a leginkább "érzékeny" 5-ös blokk: **4 K_μ (különleges konformál transzformációk) + 1 D (dilatáció)**. Ezek a konformál-szimmetria "legkevésbé klasszikus, legfinomszerkezetesebb" részei (a Poincaré-csoporton túlmutató). Ezt lehet az 5 neuromodulátornak (dopamin, noradrenalin, szerotonin, acetilkolin, GABA) megfeleltetni — **de ez laza analógia, nem bizonyított szakirodalmi híd**.

A feltételezett megfeleltetés (hipotetikus, projekt-specifikus):
- Dopamin (RPE, "wanting") ↔ K_1 — a különleges konformál transzformáció = inversion-translation-inversion = "közelítés-távolodás" dinamika, mint a reward approach
- Noradrenalin (arousal) ↔ K_2 — váratlan bizonytalanság ~ K különleges forgás
- Szerotonin (várakozás/planning) ↔ K_3 — késleltetett kielégülés
- Acetilkolin (szenzoros megbízhatóság) ↔ K_4 — attention/precision
- GABA (perem-stabilitás) ↔ D (dilatáció) — skálázás, a Markov-blanket stabilitása

**Ez spekulatív** — a szakirodalom nem támasztja közvetlenül. De a strukturális analógia felépíthető és tesztelhető lenne egy Idris prototípusban.

## 11.9 Wadler-Parametricity és Noether-Tétel — rokonság, de óvatosan

Mindkettő "ingyenes bizonyítást" ad egy strukturális invariánsból:
- **Noether**: folytonos Lie-szimmetria → konzervált áram (Noether 1918)
- **Wadler**: parametrikus polimorfizmus → reláció-megőrzés (Wadler 1989, "Theorems for free!")

Mindkettő **természetes transzformáció** formájában írható le a kategóriaelméletben. De:

**Kritikus korlát**: a Wadler-parametricity **csak a parametrikus polimorfizmusra** ír. Az Idris 2 **ad-hoc polimorfizmust** (típusosztályokat) használ, ami **nem teljesen** parametrikus — a `typeclass` dispatch megsérti a parametricity-t. Tehát a "Wadler = Noether" az Idris-típusosztályok keretében **gyengül**.

A hidat csak akkor lehetne szigorúan felépíteni, ha a rendszer minden polimorf függvénye **parametrikusan** polimorf (a Idris interface constraint-ek csak a típus-szinten játszanak, nem az érték-szinten).

## 11.10 Végső Ítélet

A kutatás szerint:

1. **15 = 15 egybeesés**: megalapozott (SO(2,4) = 15; AdS/CFT-megfeleltetéssel a QG perem-szimmetriája).
2. **Izomorfizmus (erős)**: **nincs**. A partíciók (7+7+1 vs. 6+4+1+4) strukturálisan eltérnek.
3. **Homomorfizmus (gyenge)**: **lehetséges**, és ez alignol a Conant-Ashby good regulator theorem-mel — a szabad-energia rendszer "modellje" a konformál rendszernek.
4. **Clifford-híd**: a Cl(4,2) ≅ so(2,4) kapcsolat **természetes** és ad egy CPT-involúciós struktúrát — ez a leginkább strukturális híd.
5. **5 neuromodulátor ↔ 5 (K+D) konformál-töltés**: laza analógia, de tesztelhető prototípusban.
6. **CPT 3×5=15**: numerikus, nem strukturális — a CPT-diszkrét involúcióként hat a 15-dimenziós algán, nem elemként.
7. **Wadler-Idris óvatosan**: típusosztályok ad-hoc polimorfizmust használnak, parametricity gyengül.

## 11.11 Idris Implementációs Javaslat (ha a hidat választjuk)

Ha a **Cl(4,2) Clifford-algebra hidat** választjuk, a 15 szabadságfok a Clifford-algebra 15 paravektoraként modellezhető:

```idris
-- Vázlat (nem kód, tervezési javaslat)
public export
data KonformalGeneratorTipus
  = -- SO(2,4) Lie-algebra = Cl(4,2) paravektorok
    LorentzM1 | LorentzM2 | LorentzM3
  | BoostM1   | BoostM2   | BoostM3       -- 6
  | TranszlacioP1 | TranszlacioP2 | TranszlacioP3 | TranszlacioP4  -- 4
  | DilatacioD                                  -- 1
  | KulonlegesK1 | KulonlegesK2 | KulonlegesK3 | KulonlegesK4       -- 4

-- A 15-dimenziós fázistér homomorf a konformál algán
public export
interface KonformalAlgebraT (0 a : Type) where
  commutator : a -> a -> a       -- [K_μ, P_ν] = 2i(η_μν D − M_μν)
  gradeInvolucio : a -> a        -- ≈ P (paritás)
  reversio       : a -> a        -- ≈ T (idő)
  cliffordKonjugacio : a -> a   -- grade × rev ≈ PT

-- A projekt 7+7+1 partíciója mint HOMOMORF KÉP
public export
interface KonformalHomomorfizmusT (0 a : Type) (0 b : Type) | a where
  kep : a -> b                         -- a 7+7+1 projekt-tér a 6+4+1+4 konformál képébe
  -- Conant-Ashby: a kep homomorfizmus, nem izomorfizmus
  -- Wadler-parametricity gyengén: a kep lehet, hogy nem teljesen parametrikus
```

**A prototípus**: a `KonformalHomomorfizmusT` instance felépítése a `SzabadEnergiaT` és a konformál algebra között, és bizonyítani Refl-fel, hogy a `kep` megőrzi a commutator-struktúrát (homomorfizmus). Ha a bizonyítás sikerül, a hipotézis igazolt; ha nem, akkor csak numerikus egybeesés.

## 11.12 APA Referenciák (kiegészítés)

Coleman, S., & Mandula, J. (1967). All possible symmetries of the S matrix. *Physical Review, 159*(5), 1251–1256. https://doi.org/10.1103/PhysRev.159.1251

Conant, R. C., & Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science, 1*(2), 89–97. https://doi.org/10.1080/00207727008920220

Di Francesco, P., Mathieu, P., & Sénéchal, D. (1997). *Conformal field theory*. Springer.

Lüders, G. (1954). On the equivalence of inequivalent invarianceclasses of local fields. *Det. Kong. Danske Videnskab. Selskab, Mat.-fys. Medd., 28*(5), 1–17.

Maldacena, J. M. (1997). The large N limit of conformal field theories and supergravity. *Advances in Theoretical and Mathematical Physics, 2*, 231–252. https://doi.org/10.1023/A:1026654312961

Noether, E. (1918). Invariante Variationsprobleme. *Nachrichten der Königlichen Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 235–257.

Pauli, W. (1955). Exclusion principle, Lorentz group, and reflection of space-time and charge. In *Niels Bohr and the development of physics* (pp. 30–51). Pergamon Press.

Wadler, P. (1989). Theorems for free! In *Proceedings of the 4th international conference on functional programming languages and computer architecture* (pp. 347–359). https://doi.org/10.1145/99370.99404

---

## 12. Jelenlegi Állapot (harmadik forduló után)

- **Kód nincs írva** — még tervezési fázis.
- **Skillek betöltve**: `idris-stilus`, `legkisebb-muvelet`, `kompaktalas`, `magyar-lexikon`.
- **Három kutatás kész**: QHMC/DFT, neurobiológia FEP, SM-GR-QG izomorfizmus.
- **Konklúzió**: a 15=15 numerikus egybeesés; a strukturális izomorfizmus NEM adódik természetesen; a leginkább strukturális híd a **Cl(4,2) Clifford-algebra** (mely izomorf so(2,4)-gyel); reláció: **homomorfizmus** (Conant-Ashby), nem izomorfizmus.
- **Következő lépés候选i**:
  1. Építsük a `KonformalAlgebraT` prototípust Cl(4,2)-n, ahol a 15 generátor önálló típus, és teszteljük a CPT involúciókat (`gradeInvolucio`, `reversio`, `cliffordKonjugacio`).
  2. VAGY először tisztázzuk: ha elfogadjuk a homomorfizmust (nem izomorfizmus), a rendszernek kell-e 15 dimenzió, vagy lehet kevesebb a "homomorf képben"?
  3. VAGY forduljunk vissza a `SzabadEnergiaT` prototípushoz, és hagyjuk a SM-GR-QG izomorfizmust nyitott kérdésként, mert a döntéssysztéma működhet homomorfizmussal is.