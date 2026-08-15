from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class je_rodic_pecujici_o_dite(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba rodičem pečujícím o dítě"
    definition_period = MONTH
    default_value = False
