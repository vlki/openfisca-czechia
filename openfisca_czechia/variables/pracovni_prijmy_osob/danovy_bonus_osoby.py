from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class danovy_bonus_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daňový bonus uplatněný u osoby"

    def formula(osoba, period, parameters):
        zaloha_na_dan_z_prijmu = osoba("zaloha_na_dan_z_prijmu_osoby", period)

        return where(zaloha_na_dan_z_prijmu < 0, zaloha_na_dan_z_prijmu * -1, 0)
