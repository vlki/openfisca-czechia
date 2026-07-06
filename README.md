# OpenFisca-Czechia

## [EN] Introduction

OpenFisca is a versatile simulation and microsimulation free software. This repository contains the OpenFisca model of the Czech tax and benefit system. Therefore, the working language here is Czech. You can however check the [general OpenFisca documentation](https://openfisca.org/doc/) in English!

## [CS] Introduction

OpenFisca je svobodný software pro simulace a mikrosimulace. Tento repozitář obsahuje OpenFisca model českého daňového a dávkového systému. Dále najdete instrukce k použití modelu, doporučuji ale nejdřív projít [obecnou dokumentaci k OpenFisca](https://openfisca.org/doc/).

## Co model obsahuje

Model aktuálně obsahuje:

* výpočet DSSP (dávky státní sociální pomoci) podle legislativy platné k červenci 2026
* výpočet daně z příjmu fyzických osob

Soubory modelu najdete ve složce `openfisca_czechia`.

* Parametry použité v modelu jsou v podsložce `parameters`
* Vstupy a výpočty jsou v podsložce `variables`
* Testy pro výpočty najdete v podsložce `tests`

## Licence

Kód je dostupný pod [licencí AGPLv3](LICENSE)
