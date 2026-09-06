from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class hruby_pracovni_prijem_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Hrubý pracovní příjem osoby ze všech zaměstnání"

    def formula(osoba, period, parameters):
        hruby_prijem = 0.0
        for index in INDEXY_ZAMESTNANI:
            hruby_prijem = hruby_prijem + osoba(
                f"hruby_prijem_ze_zamestnani_{index}", period
            )

        return hruby_prijem
