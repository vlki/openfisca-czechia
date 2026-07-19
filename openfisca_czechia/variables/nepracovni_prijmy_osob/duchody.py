from openfisca_core.holders import set_input_divide_by_period
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class duchody(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    set_input = set_input_divide_by_period
    default_value = 0.0
    label = "Důchody (starobní, invalidní nebo vdovecký)"
