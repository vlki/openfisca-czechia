from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class odvod_socialniho_pojisteni_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Celkový odvod sociálního pojištění zaměstnance ze všech zaměstnání"

    def formula(osoba, period, parameters):
        odvod = 0.0
        for index in INDEXY_ZAMESTNANI:
            odvod = odvod + osoba(
                f"odvod_socialniho_pojisteni_zamestnance_ze_zamestnani_{index}", period
            )

        return odvod
