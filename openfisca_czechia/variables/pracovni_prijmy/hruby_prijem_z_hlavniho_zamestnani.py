from openfisca_core.holders import set_input_divide_by_period
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class hruby_prijem_z_hlavniho_zamestnani(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    default_value = 0.0
    set_input = set_input_divide_by_period
    label = "Hrubý příjem z hlavního zaměstnání"
