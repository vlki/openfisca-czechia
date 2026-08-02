from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class StupenInvalidity(Enum):
    __order__ = "bez_invalidity stupen_1 stupen_2 stupen_3"
    bez_invalidity = "Bez invalidity"
    stupen_1 = "1. stupeň invalidity"
    stupen_2 = "2. stupeň invalidity"
    stupen_3 = "3. stupeň invalidity"


class stupen_invalidity(Variable):
    value_type = Enum
    possible_values = StupenInvalidity
    default_value = StupenInvalidity.bez_invalidity
    entity = Osoba
    definition_period = MONTH
    label = "Stupeň invalidity osoby"
