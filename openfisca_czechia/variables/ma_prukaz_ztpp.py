from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class ma_prukaz_ztpp(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda má osoba průkaz ZTP/P"
    definition_period = MONTH
    default_value = False
