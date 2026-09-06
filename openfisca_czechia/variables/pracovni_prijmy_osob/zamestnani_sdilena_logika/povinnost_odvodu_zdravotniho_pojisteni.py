from openfisca_core.model_api import select

from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.typ_pracovni_smlouvy import (
    TypPracovniSmlouvy,
)


def povinnost_odvodu_zdravotniho_pojisteni(osoba, period, parameters, index):
    """Zda ze zaměstnání se zadaným indexem vzniká povinnost odvodů zdravotního pojištění.

    Zaměstnancem pro účely veřejného zdravotního pojištění je podle § 5 písm. a)
    zákona č. 48/1997 Sb. osoba s příjmem ze závislé činnosti. Výjimkou jsou mimo
    jiné osoby činné na základě dohody o provedení práce, jejichž úhrn příjmů
    z těchto dohod u jednoho zaměstnavatele za kalendářní měsíc nedosáhl rozhodné
    částky, a obdobně osoby na dohodu o pracovní činnosti pod rozhodným příjmem.

    Hranice jsou číselně shodné s hranicemi pro účast na nemocenském pojištění, ale
    model je má jako samostatné parametry, protože plynou z jiného předpisu a mohou
    se rozejít.

    Zjednodušení modelu: z pracovního poměru se odvádí vždy, bez ohledu na výši
    příjmu, a do úhrnu pro dohody o pracovní činnosti se nezapočítává.
    """
    typ_pracovni_smlouvy = osoba(f"typ_pracovni_smlouvy_zamestnani_{index}", period)
    hruby_prijem = osoba(f"hruby_prijem_ze_zamestnani_{index}", period)

    uhrn_prijmu_z_dpp = osoba(
        f"uhrn_prijmu_z_dpp_u_stejneho_zamestnavatele_zamestnani_{index}", period
    )
    uhrn_prijmu_z_dpc = osoba(
        f"uhrn_prijmu_z_dpc_u_stejneho_zamestnavatele_zamestnani_{index}", period
    )

    hranice_dpp = parameters(
        period
    ).zdravotni_pojisteni.hranice_u_dpp_pro_povinnost_odvodu
    hranice_dpc = parameters(
        period
    ).zdravotni_pojisteni.hranice_u_dpc_pro_povinnost_odvodu

    return select(
        [
            hruby_prijem <= 0,
            typ_pracovni_smlouvy == TypPracovniSmlouvy.hpp,
            typ_pracovni_smlouvy == TypPracovniSmlouvy.dpp,
            typ_pracovni_smlouvy == TypPracovniSmlouvy.dpc,
        ],
        [
            False,
            True,
            uhrn_prijmu_z_dpp >= hranice_dpp,
            uhrn_prijmu_z_dpc >= hranice_dpc,
        ],
    )
