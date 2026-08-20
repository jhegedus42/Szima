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

## A paritásbuborék pontos tartalma

A `ParitasBuborek.idr` az előző láncban rejlő további szerkezetet
ellenőrzi.

Legyen `C8` a kiterjesztett Hamming-kód, `C7` az első koordináta
elhagyásával kapott Hamming-kód. A törölt koordináta minden kódszónál
egyenlő a megmaradt hét koordináta paritásával. A `C7` páros súlyú
részkódja pontosan `C7` duálisa. Ezért a paritás konkrét hányadosleképezés:

```text
0 → C7-duális → C7 → kételemű test → 0
```

A mag nyolcelemű, a páratlan mellékosztály is nyolcelemű. A törölt bit
tehát nem egyszerűen elveszik: a kilyukasztás után a
`C7 / C7-duális` hányados egyetlen logikai jeleként jelenik meg.

A Calderbank–Shor–Steane-konstrukció két klasszikus összetevője két
ilyen mellékosztályjelet ad:

```text
(C7 × C7) / (C7-duális × C7-duális)
    ≅ kételemű test × kételemű test.
```

A modul közvetlenül felsorolja:

- a normalizátor 256 fázis nélküli Pauli-mintáját;
- a stabilizátor 64 mintáját;
- a négy, egyenként 64 elemű logikai mellékosztályt;
- a két logikai alapoperátor nemnulla szimplektikus párosítását;
- a nemtriviális logikai Pauli-operátorok hármas minimumsúlyát.

Ez a négyelemű, nemelfajuló szimplektikus hányados pontosan egy logikai
kubit fázis nélküli Pauli-tere. A `paritásbuborék` elnevezés ennek a
könyvtárnak a neve a kilyukasztással létrejövő egydimenziós klasszikus
öndualitási hiányra. Nem bevett fizikai szakkifejezés.

Shubham P. Jain és Victor V. Albert 2024-es általános konstrukciója
ugyanezt a műveletet használja: kétszeresen páros önduális klasszikus kód
egy koordinátájának kilyukasztásából egy logikai kubitot kódoló,
gyengén önduális kvantumkódot készít. A jelen Idris-modul a nyolc- és
héthosszú esetet teljes véges felsorolással, a paritáshányadost is
láthatóvá téve ellenőrzi.

## A 240 gyök tizenöt rostja

A modul a Construction A minimális vektorait kombinatorikus
gyökleírókkal is felsorolja:

```text
8 tengely × 2 előjel                         = 16 koordinátagyök
14 súlynégyes kódszó × 16 előjelminta       = 224 kódszógyök
összesen                                    = 240 gyök
```

A koordinátagyökök címkéje a nullakódszó; a többi gyök címkéje a hozzá
tartozó súlynégyes kódszó. Így `1 + 14 = 15` rost keletkezik, és minden
rostban pontosan 16 gyök van. A csupa-egy kódszóval való eltolás a
rostcímkéket a `[8,4,4]` kód 15 nemnulla szavára viszi. A négydimenziós
bináris információs tér 15 nemnulla pontja ezért bijektíven címkézi a
rostokat.

Ugyanez a 15 nemnulla négydimenziós bináris pont a `[[15,1,3]]`
kvantum Reed–Muller-kód szokásos fizikaikubit-indexhalmaza. Ez pontos
közös véges indexhalmaz, de önmagában nem bizonyít kódekvivalenciát,
dinamikai azonosságot vagy közvetlen fizikai leképezést. A rostfelbontás
a választott Construction A koordinátakerettől függ; nem az E8
gyökrendszer keretfüggetlen felbontása.

## Mit nem jelent itt az E9 és a buborék?

Az affin E9 Kac–Moody-algebra nem „négy E8 és még egy bit”. Az E8
centrálisan kiterjesztett hurokalgebrája egy derivációval:

```text
E8 ⊗ összes egész Laurent-fok
  + központi generátor
  + fokszám-deriváció.
```

Ez végtelen dimenziós algebra. Egy megállási jel, Hamming-távolság vagy
harmincharmadik bit csak külön, véges modell lehet; E9-ként való
azonosításához hiányzik a hurokfok, a központi kettős kokiciklus, a
deriváció és a Lie-zárójel.

A húrelméleti „semmi buboréka” szintén más fogalom: olyan
vákuumbomlási geometria, amelyben a kompakt belső tér összehúzódik, és
egy világtérvégi perem keletkezik. A jelen paritásbuborék véges
kódelméleti hányados. A két fogalom között ez a modul nem állít
fizikai azonosságot.

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
A modul ezért nem állít elő dimenziós G-jelöltet, és nem hasonlít ilyet
mérési értékhez. Kimenete kizárólag a mértékegység-független
`DimenzioNelKuliGravitaciosCsatolasJelolt` és a hozzá tartozó
Planck-tömegarány.

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
- Shubham P. Jain és Victor V. Albert, *Transversal Clifford and
  T-gate codes of short length and high distance*, arXiv:2408.12752.
  Önduális klasszikus kód kilyukasztása, a duális kód mint stabilizátor,
  valamint a csupa-egy logikai Pauli-operátorok.
- Anatoly Dymarsky és Alfred Shapere, *Quantum stabilizer codes,
  lattices, and conformal field theories*, arXiv:2009.01244.
  A `[8,4,4]` súlyfelsorolója, Construction A, az E8 thétafüggvénye és
  a 240 gyök.
- Error Correction Zoo, `[[15,1,3]] quantum Reed–Muller code`.
  A fizikai kubitok indexelése a 15 nemnulla négydimenziós bináris
  ponttal.
- Guillaume Bossard és szerzőtársai, *Generalized diffeomorphisms for
  E9*, Physical Review D 96, 106022 (2017).
  Az affin E9 mint centrálisan kiterjesztett E8-hurokalgebra
  derivációval.
- Ben Friedrich, Arthur Hebecker és Johannes Walcher, *Cobordism and
  Bubbles of Anything in the String Landscape*, Journal of High Energy
  Physics 2024, 127.
  A semmi buborékának és a világtérvégi peremnek a húrelméleti jelentése.
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
