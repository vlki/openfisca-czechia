from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class je_rodic(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba rodičem dítěte v domácnosti"
    definition_period = MONTH
    default_value = False
