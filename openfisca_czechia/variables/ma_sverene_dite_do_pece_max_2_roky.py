from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class ma_sverene_dite_do_pece_max_2_roky(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda má osoba svěřené dítě do péče nejdéle po dobu 2 let"
    definition_period = MONTH
    default_value = False
