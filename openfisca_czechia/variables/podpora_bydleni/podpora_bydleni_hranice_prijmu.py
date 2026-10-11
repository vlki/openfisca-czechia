from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class podpora_bydleni_hranice_prijmu(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Hranice příjmů domácnosti pro nárok na podporu bydlení"

    def formula(domacnost, period, parameters):
        zivotni_minimum_domacnosti = domacnost("zivotni_minimum_domacnosti", period)
        nasobek = parameters(
            period
        ).podpora_bydleni.nasobek_zivotniho_minima_pro_hranici_prijmu

        return nasobek * zivotni_minimum_domacnosti
