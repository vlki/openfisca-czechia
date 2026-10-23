# OpenFisca-Czechia

[![PyPi](https://img.shields.io/pypi/v/openfisca-czechia.svg?style=flat)](https://pypi.python.org/pypi/openfisca-czechia)

## [EN] Introduction

OpenFisca is a versatile simulation and microsimulation free software. This repository contains the OpenFisca model of the Czech tax and benefit system. Therefore, the working language here is Czech. You can however check the [general OpenFisca documentation](https://openfisca.org/doc/) in English.

## [CS] Introduction

OpenFisca je svobodný software pro simulace a mikrosimulace. Tento repozitář obsahuje OpenFisca model českého daňového a dávkového systému. Dále najdete instrukce k použití modelu, doporučujeme ale nejdřív projít [obecnou dokumentaci k OpenFisca](https://openfisca.org/doc/).

## Obsah

* [Co model obsahuje](#co-model-obsahuje)
* [Co zatím model neobsahuje](#co-zatím-model-neobsahuje)
* [Kdo model používá](#kdo-model-používá)
* [Organizace složek](#organizace-složek)
* [Použití jako balíček v Python skriptech](#použití-jako-balíček-v-python-skriptech)
* [Použití pomocí Claude/ChatGPT/dalších AI nástrojů](#použití-pomocí-claudechatgptdalších-ai-nástrojů)
* [Použití přes webové API](#použití-přes-webové-api)
* [Kontakt](#kontakt)
* [Licence](#licence)

## Co model obsahuje

Model aktuálně obsahuje především:

* výpočet DSSP (dávky státní sociální pomoci), bez majetkového testu
* výpočet daně z příjmu fyzických osob ze závislé činnosti
* výpočet odvodů na sociální a zdravotní pojištění osob ze závislé činnosti
* výpočet exekučních a insolvenčních srážek

Vše dle platné legislativy k říjnu 2026.

## Co zatím model neobsahuje

* Majetkový test DSSP
* Odvody z příjmu z podnikání (OSVČ)

## Kdo model využívá

V současnosti je model využíván pro všechny výpočty [Kalkulačky dávek, daní a exekucí Centra SPOT](https://kalkulacka.centrumspot.cz/).

## Organizace složek

Soubory modelu najdete ve složce `openfisca_czechia`.

* Parametry použité v modelu jsou v podsložce `parameters`
* Vstupy a výpočty jsou v podsložce `variables`
* Testy pro výpočty najdete v podsložce `tests`

## Použití jako balíček v Python skriptech

Doporučujeme použít nástroj [uv](https://docs.astral.sh/uv/) pro správu verzí Pythonu a virtuálního prostředí.

Pokud nemáte připravený projekt pomocí uv, pak v nové složce nejdříve spusťte následující příkaz, který i nainstaluje vhodnou verzi Pythonu. Doporučená verze je 3.13, nejnižší podporovaná je 3.9.

```sh
uv init --python 3.13
```

Následně přidejte do projektu balíček `openfisca-czechia`.

```sh
uv add openfisca-czechia
```

A pak použijte balíček například pomocí následujícího kódu ([dokumentace k Python API](https://openfisca.org/doc/simulate/run-simulation.html)):

```python
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_czechia import CountryTaxBenefitSystem

PERIOD = "2026-10"

TEST_CASE = {
    "osoby": {
        "dospely1": {
            "je_rodic": {PERIOD: True},
            "je_rodic_pecujici_o_dite": {PERIOD: True},
            "hruby_prijem_ze_zamestnani_1": {PERIOD: 25000},
            "typ_pracovni_smlouvy_zamestnani_1": {PERIOD: "hpp"},
            "je_podepsane_prohlaseni_k_dani_u_zamestnani_1": {PERIOD: True},
            "uplatnuje_danove_zvyhodneni_na_vyzivovane_deti": {PERIOD: True},
            "pocet_exekuci_osoby": {PERIOD: 1},
            "pocet_vyzivovanych_osob_pro_vypocet_srazky_v_exekuci_nebo_insolvenci": {PERIOD: 1},
        },
        "dite1": {
            "je_nezaopatrene_dite": {PERIOD: True},
            "vek": {PERIOD: 2},
        },
    },
    "domacnosti": {
        "domacnost1": {
            "clenove": ["dospely1", "dite1"],
            "typ_bydleni": {PERIOD: "byt_nebo_rodinny_dum"},
            "vztah_k_nemovitosti": {PERIOD: "najemni_podnajemni"},
            "dssp_okres_bydliste": {PERIOD: "praha"},
            "naklady_na_najemne": {PERIOD: 12000},
            "dalsi_poplatky_spojene_s_bydlenim": {PERIOD: 2000},
            "naklady_na_energie": {PERIOD: 5000},
        }
    },
}


def main():
    tax_benefit_system = CountryTaxBenefitSystem()

    simulation_builder = SimulationBuilder()
    simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

    cisty_pracovni_prijem_osob = simulation.calculate("cisty_pracovni_prijem_osoby", PERIOD)
    dssp = simulation.calculate("dssp", PERIOD)
    slozka_na_bydleni = simulation.get_array("dssp_slozka_na_bydleni", PERIOD)
    slozka_na_zivobyti = simulation.get_array("dssp_slozka_na_zivobyti", PERIOD)
    bonus_na_dite = simulation.get_array("dssp_bonus_na_dite", PERIOD)
    pracovni_bonus = simulation.get_array("dssp_pracovni_bonus", PERIOD)
    srazka_v_exekuci_nebo_insolvenci = simulation.calculate("srazka_v_exekuci_nebo_insolvenci", PERIOD)
    cisty_penezni_prijem_domacnosti_po_srazkach = simulation.calculate("cisty_penezni_prijem_domacnosti_po_srazkach", PERIOD)
    rezidualni_prijem_domacnosti = simulation.calculate("rezidualni_prijem_domacnosti", PERIOD)

    print(f"Cisty pracovni prijem osob: {cisty_pracovni_prijem_osob}")
    print(f"DSSP: {dssp}")
    print(f"- slozka na bydleni: {slozka_na_bydleni}")
    print(f"- slozka na zivobyti: {slozka_na_zivobyti}")
    print(f"- bonus na dite: {bonus_na_dite}")
    print(f"- pracovni bonus: {pracovni_bonus}")
    print(f"Srazka v exekuci nebo insolvenci: {srazka_v_exekuci_nebo_insolvenci}")
    print(f"Cisty penezni prijem domacnosti po srazkach: {cisty_penezni_prijem_domacnosti_po_srazkach}")
    print(f"Rezidualni prijem domacnosti: {rezidualni_prijem_domacnosti}")


if __name__ == "__main__":
    main()

```

Pokud je kód v souboru `main.py`, pak ho spustíte následujícím způsobem:

```sh
uv run main.py
```

Výsledek by měl v tomto případě být:

```
Cisty pracovni prijem osob: [22187.     0.]
DSSP: [13324.]
- slozka na bydleni: [10576.]
- slozka na zivobyti: [0.]
- bonus na dite: [1000.]
- pracovni bonus: [1747.6001]
Srazka v exekuci nebo insolvenci: [1491.    0.]
Cisty penezni prijem domacnosti po srazkach: [34020.]
Rezidualni prijem domacnosti: [15020.]
```

## Použití pomocí Claude/ChatGPT/dalších AI nástrojů

Nástroje jako Claude nebo ChatGPT (či další AI nástroje) umí počítat situace domácností pomocí OpenFisca, pokud se jim předají instrukce, jak OpenFiscu pro Česko použít. Je to užitečné především pro uživatele, kteří si nejsou jistí při práci s jazykem Python, protože Claude nebo ChatGPT pak fungují jako prostředník, který umí požadavky uživatele přeložit na vstupy do OpenFisca modelu a výstupy zpět předat.

Pro použití si nejdříve stáhněte soubor [SKILL.md](/SKILL.md) a nainstalujte si ho jako skill ve svém Claude/ChatGPT. Instrukce, jak takový skill nainstalovat si dohledejte v dokumentaci nástroje, nebo se přímo Claude/ChatGPT zeptejte.

Jakmile máte skill nainstalovaný, pak stačí v promptu zmínit, že chcete použít OpenFisca a Claude/ChatGPT by měl sáhnout pro skill.

Příklad promptu:
```
Vypočti mi pomocí OpenFiscy výši exekuční srážky a výši DSSP u domácnosti 2 seniorů (oba věk 70), co jeden má starobní důchod 6000 Kč a druhý starobní důchod 8000 Kč.
```

## Použití přes webové API

Balíček jde spustit jako webový server například pomocí [uv](https://docs.astral.sh/uv/) následujícím způsobem:

```sh
uv run --python 3.13 --with openfisca-core --with openfisca-czechia openfisca serve
```

To spustí webový server na lokálním portu 5000, tj. http://localhost:5000.

Pak jde spustit simulaci před webové API ([dokumentace k webovému API](https://openfisca.org/doc/openfisca-web-api/index.html)) například pomocí Node.js tak, že následující vložíte do `script.js`:

```js
const period = "2026-10";

const input = {
  osoby: {
    dospely1: {
      je_rodic: { [period]: true },
      je_rodic_pecujici_o_dite: { [period]: true },
      hruby_prijem_ze_zamestnani_1: { [period]: 25000 },
      typ_pracovni_smlouvy_zamestnani_1: { [period]: "hpp" },
      je_podepsane_prohlaseni_k_dani_u_zamestnani_1: { [period]: true },
      uplatnuje_danove_zvyhodneni_na_vyzivovane_deti: { [period]: true },
      pocet_exekuci_osoby: { [period]: 1 },
      pocet_vyzivovanych_osob_pro_vypocet_srazky_v_exekuci_nebo_insolvenci: {
        [period]: 1,
      },

      // Proměnné, které pošleme s null se dopočítají a vrátí v odpovědi
      cisty_pracovni_prijem_osoby: { [period]: null },
      srazka_v_exekuci_nebo_insolvenci: { [period]: null },
    },
    dite1: {
      je_nezaopatrene_dite: { [period]: true },
      vek: { [period]: 2 },
    },
  },
  domacnosti: {
    domacnost1: {
      clenove: ["dospely1", "dite1"],
      typ_bydleni: { [period]: "byt_nebo_rodinny_dum" },
      vztah_k_nemovitosti: { [period]: "najemni_podnajemni" },
      dssp_okres_bydliste: { [period]: "praha" },
      naklady_na_najemne: { [period]: 12000 },
      dalsi_poplatky_spojene_s_bydlenim: { [period]: 2000 },
      naklady_na_energie: { [period]: 5000 },

      // Proměnné, které pošleme s null se dopočítají a vrátí v odpovědi
      dssp: { [period]: null },
      dssp_slozka_na_bydleni: { [period]: null },
      dssp_slozka_na_zivobyti: { [period]: null },
      dssp_bonus_na_dite: { [period]: null },
      dssp_pracovni_bonus: { [period]: null },
      cisty_penezni_prijem_domacnosti_po_srazkach: { [period]: null },
      rezidualni_prijem_domacnosti: { [period]: null },
    },
  },
};

fetch("http://localhost:5001/calculate", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(input),
})
  .then((response) => response.json())
  .then((output) => {
    const dospely1 = output.osoby.dospely1;
    const domacnost1 = output.domacnosti.domacnost1;

    console.log({
      cisty_pracovni_prijem_osoby: dospely1.cisty_pracovni_prijem_osoby,
      srazka_v_exekuci_nebo_insolvenci:
        dospely1.srazka_v_exekuci_nebo_insolvenci,
      dssp: domacnost1.dssp,
      slozka_na_bydleni: domacnost1.dssp_slozka_na_bydleni,
      slozka_na_zivobyti: domacnost1.dssp_slozka_na_zivobyti,
      bonus_na_dite: domacnost1.dssp_bonus_na_dite,
      pracovni_bonus: domacnost1.dssp_pracovni_bonus,
      cisty_penezni_prijem_domacnosti_po_srazkach:
        domacnost1.cisty_penezni_prijem_domacnosti_po_srazkach,
      rezidualni_prijem_domacnosti: domacnost1.rezidualni_prijem_domacnosti,
    });
  });

```

A skript následně pomocí Node.js spustíte:

```sh
node script.js
```

Výsledek by měl v tomto případě být:

```
{
  cisty_pracovni_prijem_osoby: { '2026-10': 22187 },
  srazka_v_exekuci_nebo_insolvenci: { '2026-10': 1491 },
  dssp: { '2026-10': 13324 },
  slozka_na_bydleni: { '2026-10': 10576 },
  slozka_na_zivobyti: { '2026-10': 0 },
  bonus_na_dite: { '2026-10': 1000 },
  pracovni_bonus: { '2026-10': 1747.6001 },
  cisty_penezni_prijem_domacnosti_po_srazkach: { '2026-10': 34020 },
  rezidualni_prijem_domacnosti: { '2026-10': 15020 }
}
```

## Kontakt

Správcem modelu v tomto repozitáři je Jan Vlček. V případě dotazů pište na [jan.vlcek@vlki.cz](mailto:jan.vlcek@vlki.cz)

## Licence

Kód je dostupný pod [licencí AGPLv3](LICENSE)
