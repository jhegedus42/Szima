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

## 8. Állapot

- **Kód nincs írva** — ez csak tervezési napló (a felhasználó kérése szerint).
- **Skillek betöltve**: `idris-stilus`, `legkisebb-muvelet`, `kompaktalas`, `magyar-lexikon`.
- **Kutatás kész**: alügynök (ses_0444b9e44ffe) jelentése alapján.
- **Következő lépés**: a felhasználó válaszol a 6 kérdésre (5. szakasz), azután kezdem a Lépés 1-et (`Alap/GrafT.idr`).