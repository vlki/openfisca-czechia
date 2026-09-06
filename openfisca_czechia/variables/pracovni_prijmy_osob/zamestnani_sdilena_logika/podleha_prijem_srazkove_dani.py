from openfisca_core.model_api import select

from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.typ_pracovni_smlouvy import (
    TypPracovniSmlouvy,
)


def podleha_prijem_srazkove_dani(osoba, period, parameters, index):
    """Zda příjem ze zaměstnání se zadaným indexem podléhá srážkové dani.

    Podle § 6 odst. 4 zákona o daních z příjmů je příjem samostatným základem daně
    pro daň vybíranou srážkou, pokud zaměstnanec u tohoto plátce neučinil prohlášení
    k dani a zároveň úhrnná výše příjmů u téhož plátce za kalendářní měsíc nedosáhne
    částky rozhodné pro účast na nemocenském pojištění.

    Pro DPP a pro ostatní příjmy (HPP a DPČ) platí dvě samostatné hranice, které se
    nesčítají a nelze je navzájem kompenzovat. Zdroj:
    https://financnisprava.gov.cz/cs/dane/dane/dan-z-prijmu/informace-stanoviska-a-sdeleni/2017/sdeleni-pro-platce-dane-ze-zavisle-cinnosti-a-tvurce-mzdovych-programu-k-6-odst-4-zakona-o-danich-z-prijmu

    Aktuálně v kódu ignorujeme počítání hranice u HPP, protože nepředpokládáme, že
    HPP s tak malým příjmem a bez podepsaného prohlášení může nastat.
    """
    hruby_prijem = osoba(f"hruby_prijem_ze_zamestnani_{index}", period)
    typ_pracovni_smlouvy = osoba(f"typ_pracovni_smlouvy_zamestnani_{index}", period)
    je_podepsane_prohlaseni = osoba(
        f"je_podepsane_prohlaseni_k_dani_u_zamestnani_{index}", period
    )

    uhrn_prijmu_z_dpp = osoba(
        f"uhrn_prijmu_z_dpp_u_stejneho_zamestnavatele_zamestnani_{index}", period
    )
    uhrn_prijmu_z_dpc = osoba(
        f"uhrn_prijmu_z_dpc_u_stejneho_zamestnavatele_zamestnani_{index}", period
    )

    hranice_u_dpp = parameters(
        period
    ).socialni_pojisteni.hranice_u_dpp_pro_povinnost_odvodu
    hranice_u_dpc = parameters(
        period
    ).socialni_pojisteni.hranice_u_dpc_pro_povinnost_odvodu

    je_uhrn_pod_hranici = select(
        [
            typ_pracovni_smlouvy == TypPracovniSmlouvy.dpp,
            typ_pracovni_smlouvy == TypPracovniSmlouvy.dpc,
        ],
        [
            uhrn_prijmu_z_dpp < hranice_u_dpp,
            uhrn_prijmu_z_dpc < hranice_u_dpc,
        ],
        # u HPP aktuálně nikdy neaplikujeme srážkovou daň
        default=False,
    )

    return (hruby_prijem > 0) & ~je_podepsane_prohlaseni & je_uhrn_pod_hranici
