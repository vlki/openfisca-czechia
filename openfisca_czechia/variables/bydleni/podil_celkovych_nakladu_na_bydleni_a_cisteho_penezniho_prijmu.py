from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class podil_celkovych_nakladu_na_bydleni_a_cisteho_penezniho_prijmu(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Podíl celkových nákladů domácnosti na bydlení a čistého peněžního příjmu"

    def formula(domacnost, period, parameters):
        celkove_naklady_na_bydleni = domacnost("celkove_naklady_na_bydleni", period)
        cisty_penezni_prijem_domacnosti = domacnost(
            "cisty_penezni_prijem_domacnosti", period
        )

        return where(
            cisty_penezni_prijem_domacnosti > 0,
            celkove_naklady_na_bydleni / cisty_penezni_prijem_domacnosti,
            0,
        )
