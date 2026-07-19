from openfisca_core.model_api import max_
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dpfo_z_hlavniho_zamestnani(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daň z příjmu fyzických osob z hlavního zaměstnání"

    def formula(person, period, parameters):
        dpfo_pred_slevami = person(
            "dpfo_z_hlavniho_zamestnani_pred_uplatnenim_slev", period
        )

        sleva_na_poplatnika = parameters(period).dpfo.sleva_na_poplatnika

        dpfo = max_(dpfo_pred_slevami - sleva_na_poplatnika, 0)

        return dpfo
