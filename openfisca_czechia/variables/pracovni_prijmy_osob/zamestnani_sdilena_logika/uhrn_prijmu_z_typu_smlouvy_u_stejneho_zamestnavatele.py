from openfisca_core.model_api import where

from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.je_stejny_zamestnavatel import (
    je_stejny_zamestnavatel,
)


def uhrn_prijmu_z_typu_smlouvy_u_stejneho_zamestnavatele(
    osoba, period, index, typ_smlouvy
):
    """Úhrn příjmů ze zaměstnání daného typu smlouvy u téhož zaměstnavatele.

    Zákon o nemocenském pojištění i § 6 odst. 4 zákona o daních z příjmů testují
    své limity na úhrnu u téhož plátce, ne na jednotlivé smlouvě.

    Výsledek nezávisí na typu smlouvy zaměstnání se zadaným indexem, jen na jeho
    zaměstnavateli. Dvě zaměstnání u téhož zaměstnavatele proto mají tento úhrn
    shodný.
    """
    uhrn = 0.0
    for jiny_index in INDEXY_ZAMESTNANI:
        je_zapocitatelny = je_stejny_zamestnavatel(osoba, period, index, jiny_index) & (
            osoba(f"typ_pracovni_smlouvy_zamestnani_{jiny_index}", period)
            == typ_smlouvy
        )

        uhrn = uhrn + where(
            je_zapocitatelny,
            osoba(f"hruby_prijem_ze_zamestnani_{jiny_index}", period),
            0,
        )

    return uhrn
