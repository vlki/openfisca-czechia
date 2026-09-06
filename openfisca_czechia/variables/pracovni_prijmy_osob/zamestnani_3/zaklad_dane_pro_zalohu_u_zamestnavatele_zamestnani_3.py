from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.uhrn_prijmu_u_zamestnavatele_pro_zalohu import (
    uhrn_prijmu_u_zamestnavatele_pro_zalohu,
)


class zaklad_dane_pro_zalohu_u_zamestnavatele_zamestnani_3(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Základ daně pro zálohu u zaměstnavatele třetího zaměstnání"
    documentation = """
    Úhrn příjmů u téhož zaměstnavatele, které u něj nejsou samostatným základem
    daně pro srážkovou daň. Nenulový je jen u zaměstnání, které svého
    zaměstnavatele reprezentuje.
    """

    def formula(osoba, period, parameters):
        je_prvni_u_daneho_zamestnavatele = osoba(
            "je_zamestnani_3_prvni_u_daneho_zamestnavatele", period
        )
        uhrn_prijmu = uhrn_prijmu_u_zamestnavatele_pro_zalohu(osoba, period, 3)

        return where(je_prvni_u_daneho_zamestnavatele, uhrn_prijmu, 0.0)
