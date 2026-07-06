from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class naklady_na_energie(Variable):
    value_type = float
    entity = Domacnost
    label = "Náklady domácnosti na energie"
    definition_period = MONTH
    default_value = 0
