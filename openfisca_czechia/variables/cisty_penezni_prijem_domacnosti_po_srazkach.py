from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class cisty_penezni_prijem_domacnosti_po_srazkach(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Čistý peněžní příjem domácnosti po srážkách"

    def formula(domacnost, period, parameters):
        cisty_penezni_prijem = domacnost("cisty_penezni_prijem_domacnosti", period)

        srazky_dospelych = domacnost.sum(
            domacnost.members("srazka_v_exekuci_nebo_insolvenci", period)
        )

        return cisty_penezni_prijem - srazky_dospelych
