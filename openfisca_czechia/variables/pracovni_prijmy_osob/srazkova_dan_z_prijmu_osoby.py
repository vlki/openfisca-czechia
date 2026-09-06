from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class srazkova_dan_z_prijmu_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Celková srážková daň z příjmu osoby ze všech zaměstnání"
    documentation = """
    Součet srážkové daně přes všechna zaměstnání. Které konkrétní zaměstnání
    srážkové dani podléhá, říkají proměnné
    podleha_prijem_ze_zamestnani_i_srazkove_dani.
    """

    def formula(osoba, period, parameters):
        srazkova_dan = 0.0
        for index in INDEXY_ZAMESTNANI:
            srazkova_dan = srazkova_dan + osoba(
                f"srazkova_dan_ze_zamestnani_{index}", period
            )

        return srazkova_dan
