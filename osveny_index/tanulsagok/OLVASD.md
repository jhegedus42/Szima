# Tanulságok — a 2026-08-17-es közös felfedezések futtatható archívuma

Ezek a fájlok a /tmp-ből lettek ide mentve (a /tmp újraindításnál törlődik).
Mindegyik egy-egy **élő kísérlet**, amelyből az AGENTS.md „Tanulság" szekciója
született. Újrafuttathatók: `idris2 -c <fájl>` (a /tmp-ből másolt séma miatt
egyesek nem fordulnak le — ÉPP EZ A TANULSÁG BENNÜK).

## A kisbetűs-név csapda felderítése (AGENTS.md: Idris 2 csapda)

| Fájl | Mi | Eredmény |
|---|---|---|
| `PróbaÉkezet.idr` | működnek-e az ékezetes azonosítók? | IGEN (a fájlnevet is egyezni kell) |
| `proba_ekezet.idr` | ugyanez kisbetűs fájlnévvel | modulnév-egyezés hiba (tanulság) |
| `ProbaLegkisebb.idr` | `bizKetto : kettoLeg = 2` | ELBUKIK — a csapda minimalisztikusan |
| `ProbaNevvel.idr` | nagybetűs `KettoLegNev` vs `the Nat` | nagybetűs ÁTMEGY, a `the`-s nem |
| `ProbaKicsi2/3.idr`, `ProbaVegso.idr` | a csapda izolálása lépésről lépésre | a `Delay`/unifikáció működése látszik |
| `Mutatvany.idr` / `MutatvanyJo.idr` | a csapda és a megoldás, egymás mellett | rossz: Mismatch; jó: exit 0 |

## A Refl-tanulság felderítése (AGENTS.md: Tanulság: mit bizonyít a Refl)

| Fájl | Mi | Eredmény |
|---|---|---|
| `Cafolat.idr` | SZÁNDÉKOSAN hamis Refl (8 = 9) | ELUTASÍTVA — a kernel számol, nem hisz |
| `TartalomProba.idr` | köröző vs strukturált definíció, egyszerre | mindkettő "átmegy" — a köröző üres |
| `TartalomProba2/3.idr` | a shell-lánc-elgépelés nyomai | a "0 hiba" műtermék esete (l. AGENTS.md 6. pont) |
| `TisztaA/B.idr` | a tiszta újrafuttatás: köröző és strukturált elgépelve | MINDKETTŐ elutasítva — helyreállt a rend |
| `KetUt.idr` | **A HÍD**: két független recept (16+224 vs 112+128) ugyanarra a 240-re | Refl ✓ |
| `KetUtTorott/Torott2.idr` | a híd bármelyik oldalát átírva | a bizonyítás MAGÁTÓL eltörik |
| `BizonyitasEszkozok.idr` | Refl + cong + trans (és a rewrite irány-csapdája) | eszköztár, 0 hibával |
| `MiertJo.idr` | a típusok összekeverése (KerdoszoT ≠ Esetrag) | fordítási időben elutasítva |

## Egyéb

| Fájl | Mi |
|---|---|
| `test_kerdoszo.idr`, `DebugFonetika.idr` | korábbi sessionök hibakereső maradványai (megtartva, semmit nem törlünk) |
