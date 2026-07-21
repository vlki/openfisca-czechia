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
        danove_zvyhodneni_na_vyzivovane_deti = person(
            "danove_zvyhodneni_na_vyzivovane_deti_u_hlavniho_zamestnani", period
        )

        sleva_na_poplatnika = parameters(period).dpfo.sleva_na_poplatnika

        dpfo = max_(dpfo_pred_slevami - sleva_na_poplatnika, 0)

        # Daňové zvýhodnění může být vyšší než daň a pak se stává daňovým bonusem
        return dpfo - danove_zvyhodneni_na_vyzivovane_deti
