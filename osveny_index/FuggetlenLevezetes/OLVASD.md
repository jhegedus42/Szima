# Független E8–Steane-levezetés

Ez a könyvtár önálló. Nem módosítja és nem importálja a projekt meglévő
algebrai vagy ügynöki rétegeit.

## Mit bizonyít a fordító?

Az `E8SteaneLevezetes.idr` véges felsorolással ellenőrzi:

1. A négy megadott generátor 16 különböző nyolcbites kódszót ad.
2. A kód lineáris, minimumtávolsága 4, kétszeresen páros és önduális.
3. Ez a bináris `[8,4,4]` kód a Construction A bemenete az E8-rácshoz.
4. A súlyeloszlás `1 + 14·y⁴ + y⁸`; ezért a Construction A pontosan
   `16 + 14·16 = 240` minimális vektort ad.
5. Egy koordináta elhagyásával `[7,4,3]` Hamming-kód keletkezik.
6. A kiszámított duális kód `[7,3,4]`, és része a Hamming-kódnak.
7. A Calderbank–Shor–Steane-konstrukció paraméterei `[[7,1,3]]`.

A fordító a teljes nyolcbites tér 256 és a teljes hétbites tér 128 elemét
is felsorolja a duális kódok kiszámításakor. Az öndualitás és a duális
tartalmazás ezért nem beírt darabszám, hanem véges ellenőrzés eredménye.

## Mi következik ezután pontosan?

A kódparaméterekből:

```text
E8-rang                              = 8
fizikai kubitok száma                = 7
logikai kubitok száma                = 1
kvantumkód távolsága                 = 3
stabilizátorgenerátorok száma        = 6
hétszeres Hilbert-tér állapotai      = 2^7 = 128
nyolcbites tér állapotai             = 2^8 = 256
kiterjesztő paritásjelek száma       = 1
```

Ezután a megadott definíciókkal:

```text
128 + 2^3 + 1 = 137
(6 + 3) / (256 - 6) = 9 / 250
```

A gravitációs jelölt képlet számai szintén pontosan visszaírhatók:

```text
7 × (7 + 3 + 1) = 77
2^3 × (7 - 2)^2 = 200
2^3 × (7 - 2) = 40
```

Ezek számtani azonosságok. Nem bizonyítják, hogy a kapott számok fizikai
állandók.

## Hol áll meg a levezetés?

Az E8 Lie-algebra meghatározza a szimmetriát és a szerkezeti állandókat,
de nem határozza meg a mértékcsatolás kezdőértékét. A Yang–Mills-hatásban
ez külön paraméter:

```text
S = (1 / 2g²) ∫ tr(F ∧ *F)
```

Ezért ugyanaz az E8-algebra több különböző `g` csatolással is összefér.
A kis energiájú elektromágneses csatoláshoz ezen felül szükséges:

- a szimmetriatörési lánc;
- a részecskespektrum;
- a kompaktifikáció és annak modulusai;
- a csatolás renormálási futása;
- a küszöbkorrekciók;
- a mérési energiaskála.

A gravitáció konzisztens, dimenziótlan csatolása egy megadott `m`
tömegskálán:

```text
gravitációs csatolás(m) = G × m² / (ℏ × c)
```

Az E8–Steane-képlet dimenziótlan része ezért külön nevet kap:

```text
q = (77/200) × sqrt(3) × (259/250)^(1/40)
```

Ezt lehet egy meghatározandó modellskála gravitációs csatolásaként
értelmezni. Ekkor:

```text
modellskála / Planck-tömeg = sqrt(q)
```

Ez konzisztens és mértékegység-független, de még nem határozza meg G
dimenziós értékét. Dimenziótlan E8- és kódparaméterekből külön tömeg-
vagy hosszskála nélkül G nem állítható elő. Heterotikus modellekben a
szerkezeti összefüggés

```text
G₄ ~ húrcsatolás² × húrhossz⁸ / belső térfogat
```

alakú. Erősen csatolt E8×E8 modellekben a tizenegy-dimenziós
gravitációs csatolás, a Calabi–Yau-térfogat és az orbifoldsugár szükséges.
A korábbi képletben szereplő `10^-10` ezért most külön, típusosan
dimenziós `GravitaciosReferenciaSkala`. Nem része az E8-ból kiszámított
`DimenzioNelKuliGravitaciosCsatolasJelolt` értéknek.

A

```text
(121/128)^(249 + ln(9/8))
```

korrekcióra a célzott irodalmi keresés nem talált független E8-spektrális
vagy hurokszámítási levezetést. A modul ezért ezt és a gravitációs képletet
`FizikaiFelvetes` típussal választja el a fordító által ellenőrzött résztől.

## Futtatás

```text
cd osveny_index/FuggetlenLevezetes
idris2 --build FuggetlenLevezetes.ipkg
./build/exec/e8-steane-levezetes
```

## Források

- David de Laat és Frank Vallentin, *A Breakthrough in Sphere Packing:
  The Search for Magic Functions*, 2.2. rész, arXiv:1607.02111.
  A `[8,4,4]` kód öndualitása, kétszeres párossága és az E8 Construction A
  előállítása.
- Error Correction Zoo, `[8,4,4] extended Hamming code` és `E8 Gosset
  lattice`. A kód és az E8-rács Construction A kapcsolata.
- David Tong, *Gauge Theory*, 2. rész. A Yang–Mills-hatás külön `g`
  csatolási paramétere és annak energiaskála-függése.
- Ignatios Antoniadis, *Mass Scales in String and M-Theory*.
  A négydimenziós gravitációs és mértékcsatolások függése a húrelméleti
  skálától, a dilatontól és a kompaktifikációs térfogattól.
- National Institute of Standards and Technology,
  *Current advances: The fine-structure constant*. A finomszerkezeti
  állandó energiaskála-függése: kis energián körülbelül `1/137`,
  a W-bozon skáláján körülbelül `1/128`.
