from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class pocet_exekuci_osoby(Variable):
    value_type = int
    default_value = 0
    entity = Osoba
    definition_period = MONTH
    label = "Kolik exekucí je proti osobě vedeno"
