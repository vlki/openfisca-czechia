from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.je_stejny_zamestnavatel import (
    je_stejny_zamestnavatel,
)


def je_prvni_zamestnani_u_daneho_zamestnavatele(osoba, period, index):
    """Zda dané zaměstnání reprezentuje skupinu zaměstnání u téhož zaměstnavatele.

    Zálohu na daň počítá zaměstnavatel jednou z úhrnu příjmů. Aby se při více
    zaměstnáních u téhož zaměstnavatele nezapočítala vícekrát, přiřazuje se
    zaměstnání s nejnižším indexem.
    """
    je_prvni = osoba(f"hruby_prijem_ze_zamestnani_{index}", period) > 0

    for drivejsi_index in range(1, index):
        je_prvni = je_prvni & ~(
            je_stejny_zamestnavatel(osoba, period, index, drivejsi_index)
            & (osoba(f"hruby_prijem_ze_zamestnani_{drivejsi_index}", period) > 0)
        )

    return je_prvni
