from openfisca_core.model_api import where

from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.je_stejny_zamestnavatel import (
    je_stejny_zamestnavatel,
)


def uhrn_prijmu_u_zamestnavatele_pro_zalohu(osoba, period, index):
    """Úhrn příjmů u téhož zaměstnavatele, ze kterého se počítá záloha na daň.

    Zálohu počítá plátce daně z úhrnu všech příjmů, které u něj poplatníkovi
    plynou a které nejsou samostatným základem daně pro srážkovou daň. Na rozdíl
    od limitů pro srážkovou daň se tady dohody a pracovní poměr sčítají dohromady.
    """
    uhrn = 0.0
    for jiny_index in INDEXY_ZAMESTNANI:
        podleha_srazkove_dani = osoba(
            f"podleha_prijem_ze_zamestnani_{jiny_index}_srazkove_dani", period
        )
        je_zapocitatelny = (
            je_stejny_zamestnavatel(osoba, period, index, jiny_index)
            & ~podleha_srazkove_dani
        )

        uhrn = uhrn + where(
            je_zapocitatelny,
            osoba(f"hruby_prijem_ze_zamestnani_{jiny_index}", period),
            0,
        )

    return uhrn
