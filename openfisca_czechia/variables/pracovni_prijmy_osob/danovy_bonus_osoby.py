from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class danovy_bonus_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daňový bonus uplatněný u osoby"

    def formula(person, period, parameters):
        dpfo_z_hlavniho_zamestnani = person("dpfo_z_hlavniho_zamestnani", period)

        return where(dpfo_z_hlavniho_zamestnani < 0, dpfo_z_hlavniho_zamestnani * -1, 0)
