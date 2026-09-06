from openfisca_core.model_api import select

from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.typ_pracovni_smlouvy import (
    TypPracovniSmlouvy,
)


def povinnost_odvodu_socialniho_pojisteni(osoba, period, parameters, index):
    """Zda ze zaměstnání se zadaným indexem vzniká povinnost odvodů sociálního pojištění.

    Povinnost je navázaná na účast na nemocenském pojištění. Podle § 7a zákona
    o nemocenském pojištění jsou zaměstnanci na dohodu o provedení práce účastni
    pojištění, jestliže jejich započitatelný příjem dosáhl rozhodné částky, přičemž
    se sčítají příjmy ze všech takových dohod u téhož zaměstnavatele. Podle § 7
    odst. 4 se obdobně sčítají příjmy ze zaměstnání malého rozsahu u téhož
    zaměstnavatele.

    Zjednodušení modelu: z pracovního poměru se odvádí vždy, bez ohledu na výši
    příjmu, a do úhrnu pro dohody o pracovní činnosti se nezapočítává. Zaměstnáním
    malého rozsahu by byl jen pracovní poměr pod rozhodným příjmem, což v praxi
    nenastává.
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
    ).socialni_pojisteni.hranice_u_dpp_pro_povinnost_odvodu
    hranice_dpc = parameters(
        period
    ).socialni_pojisteni.hranice_u_dpc_pro_povinnost_odvodu

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
