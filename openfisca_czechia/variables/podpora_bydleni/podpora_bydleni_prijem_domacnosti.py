from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class podpora_bydleni_prijem_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = (
        "Příjmy domácnosti bez DSSP a srážek v exekuci/insolvenci pro podporu bydlení"
    )

    def formula(domacnost, period, parameters):
        # Čistý peněžní příjem srážky v exekuci/insolvenci ještě neodečítá, stačí
        # z něj vyjmout DSSP
        cisty_penezni_prijem_domacnosti = domacnost(
            "cisty_penezni_prijem_domacnosti", period
        )
        dssp = domacnost("dssp", period)

        return cisty_penezni_prijem_domacnosti - dssp
