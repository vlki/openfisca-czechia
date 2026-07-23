from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class ciste_pracovni_prijmy_osob_v_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Čisté pracovní příjmy všech osob v domácnosti"

    def formula(domacnost, period, parameters):
        return domacnost.sum(domacnost.members("cisty_pracovni_prijem_osoby", period))
