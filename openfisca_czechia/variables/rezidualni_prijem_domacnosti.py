from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class rezidualni_prijem_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Čistý peněžní příjem domácnosti"

    def formula(domacnost, period, parameters):
        cisty_penezni_prijem_domacnosti = domacnost(
            "cisty_penezni_prijem_domacnosti", period
        )
        celkove_naklady_na_bydleni = domacnost("celkove_naklady_na_bydleni", period)

        return cisty_penezni_prijem_domacnosti - celkove_naklady_na_bydleni
