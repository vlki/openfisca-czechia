from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class je_v_insolvenci(Variable):
    value_type = bool
    default_value = False
    entity = Osoba
    definition_period = MONTH
    label = "Zda je osoba v insolvenci"
