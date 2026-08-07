from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class ma_prednostni_exekuce(Variable):
    value_type = bool
    default_value = False
    entity = Osoba
    definition_period = MONTH
    label = "Má osoba přednostní exekuce?"
