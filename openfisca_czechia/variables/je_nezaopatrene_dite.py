from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class je_nezaopatrene_dite(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba nezaopatřené dítě"
    definition_period = MONTH
    default_value = False
