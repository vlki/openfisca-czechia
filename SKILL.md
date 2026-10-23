---
name: openfisca-czechia
description: Skill pro vyhodnocování daňové, dávkové a exekuční situace domácností pomocí modelu legislativy OpenFisca pro Česko. Model OpenFisca zachycuje jak aktuální legislativu, tak historickou, lze ale též modelovat alternativní nastavení systému podle požadavků uživatele.
---

# OpenFisca pro Česko

## Výpočet pro domácnost

Hlavní pravidlo: výpočty dělej jen pomocí OpenFisca, snaž se nevytvářet si vzorečky sám někde vedle.

### Postup:

1. Stáhni si lokálně model OpenFisca pro Česko z repozitáře https://github.com/vlki/openfisca-czechia
2. Pak na základě požadavku uživatele prozkoumej model a zjisti, co za vstupní proměnné je potreba zadat, aby šlo vypočítat to, co uživatel chce
3. Pak vyhodnoť, jestli uživatele zajímá současná legislativa nebo historická; pokud nespecifikoval, tak předpokládej současnou
4. Pak z požadavku uživatele vyhodnoť, jak vypadá vstup pro model (kolik je osob domácnosti a potřebné vstupní proměnné k nim a případně vstupní proměnné pro domácnost jako celek), vypiš uživateli, jak ten vstup vypadá (tohle rozděl na část, kterou uživatel explicitně chtěl a na část, co jsi sám odhadl/předpokládáš) a co jsou jiné vstupní proměnné, které může zadat, protože ovlivní výsledný výpočet. Dej mu tento vstup k potvrzení než budeš pokračovat dál. Pokud uživatel nezadal žádné vstupní proměnné, tak ho vyzvi k zadání a vypiš mu, co všechno může zadat, protože to má na výsledný výpočet vliv.
5. Po potvrzení uživatelem vstup vlož do Python skriptu, který provede výpočet pomocí OpenFisca modelu, plus přidej všechny relevantní výstupní proměnné, které chce uživatel spočítat; příklad skriptu pro výpočet dávky státní sociální pomoci (DSSP):

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

6. Nakonec vezmi výsledky ze skriptu a uživateli je zobraz přehledně v tabulce. Zároveň nad tabulkou uveď kompletní vstupní proměnné, které byly předány včetně těch, které do výpočtů vstupovaly implicitně s výchozími hodnotami. Pokud uživatel žádá i mezivýpočty, pak si najdi, které všechny meziproměnné bylo třeba v OpenFisca spočítat a zobraz je uživateli za hlavní tabulkou též.

## Vizualizace výpočtů

1. Při dotazu na ukázání, jak se počítá některá z proměnných modelu OpenFisca zase nejdřív začni tím, že si stáhně lokálně model OpenFisca pro Česko z repozitáře https://github.com/vlki/openfisca-czechia
2. Následně identifikuj v modelu proměnnou nebo více proměnných, které chce uživatel ukázat, jak se počítají
3. Tím, že je z formule každé proměnné jasně vidět, které další proměnné a parametry pro svůj výpočet potřebují, tak si takhle zbuduj celý strom proměnných a parametrů, které vedou k výpočtu cílové proměnné
4. Uživateli následně strom vizualizuj nejlépe pomocí grafu -- ukážeš výstupní proměnnou jako kostičku a všechny její vstupní proměnné a parametry jako další kostičky spojené linkou a takhle dál až to bude celý graf; jak přesně graf vizualizuješ uprav podle toho, kolik proměnných strom výpočtu má; barevně odliš proměnné od výpočtů a uveď v legendě, jak jsou ukázány výpočty a jak parametry
