from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class podpora_bydleni_ma_narok(Variable):
    value_type = bool
    entity = Domacnost
    definition_period = MONTH
    label = "Má domácnost nárok na podporu podle zákona o podpoře bydlení"

    def formula(domacnost, period, parameters):
        prijem = domacnost("podpora_bydleni_prijem_domacnosti", period)
        hranice_prijmu = domacnost("podpora_bydleni_hranice_prijmu", period)

        return prijem <= hranice_prijmu
