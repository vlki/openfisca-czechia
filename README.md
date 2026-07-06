# OpenFisca-Czechia

[![PyPi](https://img.shields.io/pypi/v/openfisca-czechia.svg?style=flat)](https://pypi.python.org/pypi/openfisca-czechia)

## [EN] Introduction

OpenFisca is a versatile simulation and microsimulation free software. This repository contains the OpenFisca model of the Czech tax and benefit system. Therefore, the working language here is Czech. You can however check the [general OpenFisca documentation](https://openfisca.org/doc/) in English.

## [CS] Introduction

OpenFisca je svobodný software pro simulace a mikrosimulace. Tento repozitář obsahuje OpenFisca model českého daňového a dávkového systému. Dále najdete instrukce k použití modelu, doporučujeme ale nejdřív projít [obecnou dokumentaci k OpenFisca](https://openfisca.org/doc/).

## Co model obsahuje

Model aktuálně obsahuje:

* výpočet DSSP (dávky státní sociální pomoci) podle legislativy platné k červenci 2026
* výpočet daně z příjmu fyzických osob

Soubory modelu najdete ve složce `openfisca_czechia`.

* Parametry použité v modelu jsou v podsložce `parameters`
* Vstupy a výpočty jsou v podsložce `variables`
* Testy pro výpočty najdete v podsložce `tests`

## Použití jako balíčku v Python skriptech

Doporučujeme použít nástroj [uv](https://docs.astral.sh/uv/) pro správu verzí Pythonu a virtuálního prostředí.

Pokud nemáte připravený projekt pomocí uv, pak v nové složce nejdříve spusťte následující příkaz, který i nainstaluje vhodnou verzi Pythonu. Doporučená verze je 3.13, nejnižší podporovaná je 3.9.

```sh
uv init --python 3.13
```

Následně přidejte do projektu balíček `openfisca-czechia`.

```sh
uv add openfisca-czechia
```

A pak použijte balíček například pomocí následujícího kódu:

```python
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_czechia import CountryTaxBenefitSystem

TEST_CASE = {
    "osoby": {
        "dospely1": {
            "cisty_prijem_osoby": {"2026-01": 8000},
            "dssp_je_osoba_pracovne_aktivni": {"2026-01": True},
            "dssp_je_osoba_zranitelna": {"2026-01": True},
        },
        "dite1": {
            "vek": {"2026-01": 2},
            "je_nezaopatrene_dite": {"2026-01": True},
            "dssp_je_osoba_zranitelna": {"2026-01": True},
        },
    },
    "domacnosti": {
        "domacnost1": {
            "clenove": ["dospely1", "dite1"],
            "typ_bydleni": {"2026-01": "byt_nebo_rodinny_dum"},
            "vztah_k_nemovitosti": {"2026-01": "najemni_podnajemni"},
            "dssp_velikost_obce_bydliste": {"2026-01": "praha_a_brno"},
            "naklady_na_najemne": {"2026-01": 12000},
            "dalsi_poplatky_spojene_s_bydlenim": {"2026-01": 2000},
            "naklady_na_energie": {"2026-01": 5000},
        }
    },
}


def main():
    tax_benefit_system = CountryTaxBenefitSystem()

    simulation_builder = SimulationBuilder()
    simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

    vyse_dssp = simulation.calculate("dssp", "2026-01")

    vyse_dssp_slozky_na_bydleni = simulation.get_array(
        "dssp_slozka_na_bydleni", "2026-01"
    )
    vyse_dssp_slozky_na_zivobyti = simulation.get_array(
        "dssp_slozka_na_zivobyti", "2026-01"
    )
    vyse_dssp_bonusu_na_dite = simulation.get_array("dssp_bonus_na_dite", "2026-01")
    vyse_dssp_pracovniho_bonusu = simulation.get_array("dssp_pracovni_bonus", "2026-01")

    print(f"DSSP: {vyse_dssp}")
    print(f"- slozka na bydleni: {vyse_dssp_slozky_na_bydleni}")
    print(f"- slozka na zivobyti: {vyse_dssp_slozky_na_zivobyti}")
    print(f"- bonus na dite: {vyse_dssp_bonusu_na_dite}")
    print(f"- pracovni bonus: {vyse_dssp_pracovniho_bonusu}")


if __name__ == "__main__":
    main()
```

Pokud je kód v souboru `main.py`, pak ho spustíte následujícím způsobem:

```sh
uv run main.py
```


## Licence

Kód je dostupný pod [licencí AGPLv3](LICENSE)
