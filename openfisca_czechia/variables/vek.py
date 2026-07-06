from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class vek(Variable):
    value_type = int
    entity = Osoba
    label = "Věk osoby"
    definition_period = MONTH
    default_value = 0
