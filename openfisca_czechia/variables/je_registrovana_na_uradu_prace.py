from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class je_registrovana_na_uradu_prace(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba registrována na Úřadu práce"
    definition_period = MONTH
    default_value = False
