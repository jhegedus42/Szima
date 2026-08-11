# opencode

Ezt a munkát szeretett cicámnak, Szimának dedikálom.

Dedicated to Szima.

Idris 2 alapú kategórikus algebrai alapozás projekt: kategóriaelmélet, E8×E8 Clifford algebra, és Steane [[7,1,3]] kvantumhibajavítás formális modelljei.

Ez a tárhely célja a matematikai struktúrák formális megfogalmazása és ellenőrzése Idris 2 nyelven. A projekt hangsúlyozza a szigorú típusosságot, algebrai adattípusok használatát, valamint a Steane kód és az E8×E8 szerkezetek alkalmazását a logikai modellezésben.

Főbb részek

- Kategóriaelmélet alapok és konstrukciók
- E8×E8 algebrai modulok és Clifford műveletek
- Steane [[7,1,3]] hibajavító kód reprezentációk
- Típusos logika és Render/Show megjelenítési osztályok

Telepítési követelmények

- Idris 2 (ajánlott verzió: 0.8.0)
- macOS (arm64) vagy kompatibilis fejlesztői környezet
- Homebrew csomagkezelő (opcionális)

Gyors telepítés macOS rendszeren

1. Telepítsd az Idris 2 eszközt Homebrew segítségével:

   brew install idris2

2. Ellenőrizd az Idris 2 telepítést:

   idris2 --version

Fejlesztés

- Minden maglogikai típus és reláció Idris 2-ben legyen definiálva.
- Kerüld a String típus használatát a mag típusokban; használj algebrai adattípusokat és Render/Show típusosztályokat a megjelenítéshez.
- Minden azonosító és dokumentáció magyar nyelvű legyen a projekt belső szabályzata szerint.

Contribúció

Ha szeretnél hozzájárulni:

1. Forkold a tárhelyet.
2. Hozz létre egy új ágat a változtatásokhoz.
3. Küldj pull requestet részletes leírással.

Licenc

A projekt jelenleg licenc alatt áll: lásd a LICENSE fájlt a gyökérkönyvtárban.

Kapcsolat

Fenntartó: jhegedus42

---

English

# opencode

Dedicated to Szima.

Idris 2-based categorical algebra foundations project: category theory, E8×E8 Clifford algebra, and formal models of the Steane [[7,1,3]] quantum error-correcting code.

This repository aims to formally express and verify mathematical structures in Idris 2. The project emphasizes strong typing, the use of algebraic data types, and the application of the Steane code and E8×E8 structures in logical modeling.

Main components

- Foundations and constructions of category theory
- E8×E8 algebraic modules and Clifford operations
- Representations of the Steane [[7,1,3]] error-correcting code
- Typed logic and Render/Show-like display typeclasses

Requirements

- Idris 2 (recommended version: 0.8.0)
- macOS (arm64) or a compatible development environment
- Homebrew package manager (optional)

Quick start (macOS)

1. Install Idris 2 via Homebrew:

   brew install idris2

2. Verify the installation:

   idris2 --version

Development guidelines

- Define all core logical types and relations in Idris 2.
- Avoid using String for core types; prefer algebraic data types and typed Render/Show classes for presentation.
- Internal identifiers and documentation should be in Hungarian as per project conventions.

Contributing

If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Open a pull request with a detailed description.

License

This project is licensed; see the LICENSE file in the repository root for details.

Contact

Maintainer: jhegedus42
